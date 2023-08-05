from __future__ import unicode_literals

import os

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.core.exceptions import ValidationError
from djblets.testing.decorators import add_fixtures

from reviewboard.scmtools.core import HEAD
from reviewboard.scmtools.models import Repository, Tool
from reviewboard.scmtools.signals import (checked_file_exists,
                                          checking_file_exists,
                                          fetched_file, fetching_file)
from reviewboard.testing.testcase import TestCase


class RepositoryTests(TestCase):
    """Unit tests for Repository operations."""

    fixtures = ['test_scmtools']

    def setUp(self):
        super(RepositoryTests, self).setUp()

        self.local_repo_path = os.path.join(os.path.dirname(__file__),
                                            '..', 'testdata', 'git_repo')
        self.repository = Repository.objects.create(
            name='Git test repo',
            path=self.local_repo_path,
            tool=Tool.objects.get(name='Git'))

        self.scmtool_cls = self.repository.get_scmtool().__class__
        self.old_get_file = self.scmtool_cls.get_file
        self.old_file_exists = self.scmtool_cls.file_exists

    def tearDown(self):
        super(RepositoryTests, self).tearDown()

        cache.clear()

        self.scmtool_cls.get_file = self.old_get_file
        self.scmtool_cls.file_exists = self.old_file_exists

    def test_archive(self):
        """Testing Repository.archive"""
        self.repository.archive()
        self.assertTrue(self.repository.name.startswith('ar:Git test repo:'))
        self.assertTrue(self.repository.archived)
        self.assertFalse(self.repository.public)
        self.assertIsNotNone(self.repository.archived_timestamp)

        repository = Repository.objects.get(pk=self.repository.pk)
        self.assertEqual(repository.name, self.repository.name)
        self.assertEqual(repository.archived, self.repository.archived)
        self.assertEqual(repository.public, self.repository.public)
        self.assertEqual(repository.archived_timestamp,
                         self.repository.archived_timestamp)

    def test_archive_no_save(self):
        """Testing Repository.archive with save=False"""
        self.repository.archive(save=False)
        self.assertTrue(self.repository.name.startswith('ar:Git test repo:'))
        self.assertTrue(self.repository.archived)
        self.assertFalse(self.repository.public)
        self.assertIsNotNone(self.repository.archived_timestamp)

        repository = Repository.objects.get(pk=self.repository.pk)
        self.assertNotEqual(repository.name, self.repository.name)
        self.assertNotEqual(repository.archived, self.repository.archived)
        self.assertNotEqual(repository.public, self.repository.public)
        self.assertNotEqual(repository.archived_timestamp,
                            self.repository.archived_timestamp)

    def test_clean_without_conflict(self):
        """Testing Repository.clean without name/path conflicts"""
        with self.assertNumQueries(1):
            self.repository.clean()

    def test_clean_with_name_conflict(self):
        """Testing Repository.clean with name conflict"""
        repository = Repository(name=self.repository.name,
                                path='path/to/repo.git',
                                tool=self.repository.tool)

        with self.assertRaises(ValidationError) as ctx:
            with self.assertNumQueries(1):
                repository.clean()

        self.assertEqual(ctx.exception.message_dict, {
            'name': ['A repository with this name already exists'],
        })

    def test_clean_with_path_conflict(self):
        """Testing Repository.clean with path conflict"""
        repository = Repository(name='New test repo',
                                path=self.repository.path,
                                tool=self.repository.tool)

        with self.assertRaises(ValidationError) as ctx:
            with self.assertNumQueries(1):
                repository.clean()

        self.assertEqual(ctx.exception.message_dict, {
            'path': ['A repository with this path already exists'],
        })

    def test_clean_with_name_and_path_conflict(self):
        """Testing Repository.clean with name and path conflict"""
        repository = Repository(name=self.repository.name,
                                path=self.repository.path,
                                tool=self.repository.tool)

        with self.assertRaises(ValidationError) as ctx:
            with self.assertNumQueries(1):
                repository.clean()

        self.assertEqual(ctx.exception.message_dict, {
            'name': ['A repository with this name already exists'],
            'path': ['A repository with this path already exists'],
        })

    def test_clean_with_path_conflict_with_archived(self):
        """Testing Repository.clean with archived repositories ignored for
        path conflict
        """
        self.repository.archive()

        repository = Repository(name='New test repo',
                                path=self.repository.path,
                                tool=self.repository.tool)

        with self.assertNumQueries(1):
            repository.clean()

    def test_get_file_caching(self):
        """Testing Repository.get_file caches result"""
        def get_file(self, path, revision, **kwargs):
            num_calls['get_file'] += 1
            return b'file data'

        num_calls = {
            'get_file': 0,
        }

        path = 'readme'
        revision = 'e965047'
        request = {}

        self.scmtool_cls.get_file = get_file

        data1 = self.repository.get_file(path, revision, request=request)
        data2 = self.repository.get_file(path, revision, request=request)

        self.assertEqual(data1, 'file data')
        self.assertEqual(data1, data2)
        self.assertEqual(num_calls['get_file'], 1)

    def test_get_file_signals(self):
        """Testing Repository.get_file emits signals"""
        def on_fetching_file(sender, path, revision, request, **kwargs):
            found_signals.append(('fetching_file', path, revision, request))

        def on_fetched_file(sender, path, revision, request, **kwargs):
            found_signals.append(('fetched_file', path, revision, request))

        found_signals = []

        fetching_file.connect(on_fetching_file, sender=self.repository)
        fetched_file.connect(on_fetched_file, sender=self.repository)

        path = 'readme'
        revision = 'e965047'
        request = {}

        self.repository.get_file(path, revision, request=request)

        self.assertEqual(len(found_signals), 2)
        self.assertEqual(found_signals[0],
                         ('fetching_file', path, revision, request))
        self.assertEqual(found_signals[1],
                         ('fetched_file', path, revision, request))

    def test_get_file_exists_caching_when_exists(self):
        """Testing Repository.get_file_exists caches result when exists"""
        def file_exists(self, path, revision, **kwargs):
            num_calls['get_file_exists'] += 1
            return True

        num_calls = {
            'get_file_exists': 0,
        }

        path = 'readme'
        revision = 'e965047'
        request = {}

        self.scmtool_cls.file_exists = file_exists

        exists1 = self.repository.get_file_exists(path, revision,
                                                  request=request)
        exists2 = self.repository.get_file_exists(path, revision,
                                                  request=request)

        self.assertTrue(exists1)
        self.assertTrue(exists2)
        self.assertEqual(num_calls['get_file_exists'], 1)

    def test_get_file_exists_caching_when_not_exists(self):
        """Testing Repository.get_file_exists doesn't cache result when the
        file does not exist
        """
        def file_exists(self, path, revision, **kwargs):
            num_calls['get_file_exists'] += 1
            return False

        num_calls = {
            'get_file_exists': 0,
        }

        path = 'readme'
        revision = '12345'
        request = {}

        self.scmtool_cls.file_exists = file_exists

        exists1 = self.repository.get_file_exists(path, revision,
                                                  request=request)
        exists2 = self.repository.get_file_exists(path, revision,
                                                  request=request)

        self.assertFalse(exists1)
        self.assertFalse(exists2)
        self.assertEqual(num_calls['get_file_exists'], 2)

    def test_get_file_exists_caching_with_fetched_file(self):
        """Testing Repository.get_file_exists uses get_file's cached result"""
        def get_file(self, path, revision, **kwargs):
            num_calls['get_file'] += 1
            return 'file data'

        def file_exists(self, path, revision, **kwargs):
            num_calls['get_file_exists'] += 1
            return True

        num_calls = {
            'get_file_exists': 0,
            'get_file': 0,
        }

        path = 'readme'
        revision = 'e965047'
        request = {}

        self.scmtool_cls.get_file = get_file
        self.scmtool_cls.file_exists = file_exists

        self.repository.get_file(path, revision, request=request)
        exists1 = self.repository.get_file_exists(path, revision,
                                                  request=request)
        exists2 = self.repository.get_file_exists(path, revision,
                                                  request=request)

        self.assertTrue(exists1)
        self.assertTrue(exists2)
        self.assertEqual(num_calls['get_file'], 1)
        self.assertEqual(num_calls['get_file_exists'], 0)

    def test_get_file_exists_signals(self):
        """Testing Repository.get_file_exists emits signals"""
        def on_checking(sender, path, revision, request, **kwargs):
            found_signals.append(('checking_file_exists', path,
                                  revision, request))

        def on_checked(sender, path, revision, request, **kwargs):
            found_signals.append(('checked_file_exists', path,
                                  revision, request))

        found_signals = []

        checking_file_exists.connect(on_checking, sender=self.repository)
        checked_file_exists.connect(on_checked, sender=self.repository)

        path = 'readme'
        revision = 'e965047'
        request = {}

        self.repository.get_file_exists(path, revision, request=request)

        self.assertEqual(len(found_signals), 2)
        self.assertEqual(found_signals[0],
                         ('checking_file_exists', path, revision, request))
        self.assertEqual(found_signals[1],
                         ('checked_file_exists', path, revision, request))

    def test_get_file_signature_warning(self):
        """Test old SCMTool.get_file signature triggers warning"""
        def get_file(self, path, revision):
            return 'file data'

        self.scmtool_cls.get_file = get_file

        path = 'readme'
        revision = 'e965047'
        request = {}

        warn_msg = ('SCMTool.get_file() must take keyword arguments, '
                    'signature for %s is deprecated.' %
                    self.repository.get_scmtool().name)

        with self.assert_warns(message=warn_msg):
            self.repository.get_file(path, revision, request=request)

    def test_file_exists_signature_warning(self):
        """Test old SCMTool.file_exists signature triggers warning"""
        def file_exists(self, path, revision=HEAD):
            return True

        self.scmtool_cls.file_exists = file_exists

        path = 'readme'
        revision = 'e965047'
        request = {}

        warn_msg = ('SCMTool.file_exists() must take keyword arguments, '
                    'signature for %s is deprecated.' %
                    self.repository.get_scmtool().name)

        with self.assert_warns(message=warn_msg):
            self.repository.get_file_exists(path, revision, request=request)

    def test_repository_name_with_255_characters(self):
        """Testing Repository.name with 255 characters"""
        self.repository = Repository.objects.create(
            name='t' * 255,
            path=self.local_repo_path,
            tool=Tool.objects.get(name='Git'))

        self.assertEqual(len(self.repository.name), 255)

    def test_is_accessible_by_with_public(self):
        """Testing Repository.is_accessible_by with public repository"""
        user = self.create_user()
        repository = self.create_repository()

        self.assertTrue(repository.is_accessible_by(user))
        self.assertTrue(repository.is_accessible_by(AnonymousUser()))

    def test_is_accessible_by_with_public_and_hidden(self):
        """Testing Repository.is_accessible_by with public hidden repository"""
        user = self.create_user()
        repository = self.create_repository(visible=False)

        self.assertTrue(repository.is_accessible_by(user))
        self.assertTrue(repository.is_accessible_by(AnonymousUser()))

    def test_is_accessible_by_with_private_and_not_member(self):
        """Testing Repository.is_accessible_by with private repository and
        user not a member
        """
        user = self.create_user()
        repository = self.create_repository(public=False)

        self.assertFalse(repository.is_accessible_by(user))
        self.assertFalse(repository.is_accessible_by(AnonymousUser()))

    def test_is_accessible_by_with_private_and_member(self):
        """Testing Repository.is_accessible_by with private repository and
        user is a member
        """
        user = self.create_user()
        repository = self.create_repository(public=False)
        repository.users.add(user)

        self.assertTrue(repository.is_accessible_by(user))

    def test_is_accessible_by_with_private_and_member_by_group(self):
        """Testing Repository.is_accessible_by with private repository and
        user is a member by group
        """
        user = self.create_user()

        group = self.create_review_group(invite_only=True)
        group.users.add(user)

        repository = self.create_repository(public=False)
        repository.review_groups.add(group)

        self.assertTrue(repository.is_accessible_by(user))

    def test_is_accessible_by_with_private_and_superuser(self):
        """Testing Repository.is_accessible_by with private repository and
        user is a superuser
        """
        user = self.create_user(is_superuser=True)
        repository = self.create_repository(public=False)

        self.assertTrue(repository.is_accessible_by(user))

    def test_is_accessible_by_with_private_hidden_not_member(self):
        """Testing Repository.is_accessible_by with private hidden
        repository and user not a member
        """
        user = self.create_user()
        repository = self.create_repository(public=False,
                                            visible=False)

        self.assertFalse(repository.is_accessible_by(user))

    def test_is_accessible_by_with_private_hidden_and_member(self):
        """Testing Repository.is_accessible_by with private hidden
        repository and user is a member
        """
        user = self.create_user()

        repository = self.create_repository(public=False,
                                            visible=False)
        repository.users.add(user)

        self.assertTrue(repository.is_accessible_by(user))

    def test_is_accessible_by_with_private_hidden_and_member_by_group(self):
        """Testing Repository.is_accessible_by with private hidden
        repository and user is a member
        """
        user = self.create_user()

        group = self.create_review_group(invite_only=True)
        group.users.add(user)

        repository = self.create_repository(public=False,
                                            visible=False)
        repository.review_groups.add(group)

        self.assertTrue(repository.is_accessible_by(user))

    def test_is_accessible_by_with_private_hidden_and_superuser(self):
        """Testing Repository.is_accessible_by with private hidden
        repository and superuser
        """
        user = self.create_user(is_superuser=True)
        repository = self.create_repository(public=False,
                                            visible=False)

        self.assertTrue(repository.is_accessible_by(user))

    @add_fixtures(['test_users', 'test_site'])
    def test_is_accessible_by_with_local_site_accessible(self):
        """Testing Repository.is_accessible_by with Local Site accessible by
        user
        """
        user = self.create_user()

        repository = self.create_repository(with_local_site=True)
        repository.local_site.users.add(user)

        self.assertTrue(repository.is_accessible_by(user))

    @add_fixtures(['test_users', 'test_site'])
    def test_is_accessible_by_with_local_site_not_accessible(self):
        """Testing Repository.is_accessible_by with Local Site not accessible
        by user
        """
        user = self.create_user()
        repository = self.create_repository(with_local_site=True)

        self.assertFalse(repository.is_accessible_by(user))
        self.assertFalse(repository.is_accessible_by(AnonymousUser()))
