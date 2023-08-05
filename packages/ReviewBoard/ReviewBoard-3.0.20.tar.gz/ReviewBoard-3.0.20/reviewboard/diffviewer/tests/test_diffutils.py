from __future__ import unicode_literals

from django.test.client import RequestFactory
from django.utils import six
from django.utils.six.moves import zip_longest
from djblets.siteconfig.models import SiteConfiguration
from djblets.testing.decorators import add_fixtures
from kgb import SpyAgency

from reviewboard.diffviewer.diffutils import (
    get_diff_data_chunks_info,
    get_diff_files,
    get_displayed_diff_line_ranges,
    get_file_chunks_in_range,
    get_last_header_before_line,
    get_last_line_number_in_diff,
    get_line_changed_regions,
    get_matched_interdiff_files,
    get_original_file,
    patch,
    _PATCH_GARBAGE_INPUT,
    _get_last_header_in_chunks_before_line)
from reviewboard.diffviewer.errors import PatchError
from reviewboard.diffviewer.models import FileDiff
from reviewboard.scmtools.core import PRE_CREATION
from reviewboard.testing import TestCase


class GetDiffDataChunksInfoTests(TestCase):
    """Unit tests for get_diff_data_chunks_info."""

    def test_with_basic_diff(self):
        """Testing get_diff_data_chunks_info with a basic one-chunk diff"""
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -10,7 +12,10 @@\n'
                b' #\n'
                b' #\n'
                b' #\n'
                b'-# old line\n'
                b'+# new line\n'
                b'+# new line\n'
                b'+# new line\n'
                b'+# new line\n'
                b' #\n'
                b' #\n'
                b' #\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 9,
                        'chunk_len': 7,
                        'changes_start': 12,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 11,
                        'chunk_len': 10,
                        'changes_start': 14,
                        'changes_len': 4,
                    },
                },
            ])

    def test_with_multiple_chunks(self):
        """Testing get_diff_data_chunks_info with multiple chunks in a diff"""
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -10,7 +12,10 @@\n'
                b' #\n'
                b' #\n'
                b' #\n'
                b'-# old line\n'
                b'+# new line\n'
                b'+# new line\n'
                b'+# new line\n'
                b'+# new line\n'
                b' #\n'
                b' #\n'
                b' #\n'
                b'@@ -23,7 +40,7 @@\n'
                b' #\n'
                b' #\n'
                b' #\n'
                b'-# old line\n'
                b'+# new line\n'
                b' #\n'
                b' #\n'
                b' #\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 9,
                        'chunk_len': 7,
                        'changes_start': 12,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 11,
                        'chunk_len': 10,
                        'changes_start': 14,
                        'changes_len': 4,
                    },
                },
                {
                    'orig': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 22,
                        'chunk_len': 7,
                        'changes_start': 25,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 39,
                        'chunk_len': 7,
                        'changes_start': 42,
                        'changes_len': 1,
                    },
                },
            ])

    def test_with_multiple_chunks_no_context(self):
        """Testing get_diff_data_chunks_info with multiple chunks and no
        context
        """
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -13,1 +15,4 @@\n'
                b'-# old line\n'
                b'+# new line\n'
                b'+# new line\n'
                b'+# new line\n'
                b'+# new line\n'
                b'@@ -26,1 +43,1 @@\n'
                b'-# old line\n'
                b'+# new line\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 0,
                        'chunk_start': 12,
                        'chunk_len': 1,
                        'changes_start': 12,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 0,
                        'chunk_start': 14,
                        'chunk_len': 4,
                        'changes_start': 14,
                        'changes_len': 4,
                    },
                },
                {
                    'orig': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 0,
                        'chunk_start': 25,
                        'chunk_len': 1,
                        'changes_start': 25,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 0,
                        'chunk_start': 42,
                        'chunk_len': 1,
                        'changes_start': 42,
                        'changes_len': 1,
                    },
                },
            ])

    def test_with_all_inserts(self):
        """Testing get_diff_data_chunks_info with all inserts"""
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -10,6 +12,10 @@\n'
                b' #\n'
                b' #\n'
                b' #\n'
                b'+# new line\n'
                b'+# new line\n'
                b'+# new line\n'
                b'+# new line\n'
                b' #\n'
                b' #\n'
                b' #\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 6,
                        'post_lines_of_context': 0,
                        'chunk_start': 9,
                        'chunk_len': 6,
                        'changes_start': 9,
                        'changes_len': 0,
                    },
                    'modified': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 11,
                        'chunk_len': 10,
                        'changes_start': 14,
                        'changes_len': 4,
                    },
                },
            ])

    def test_with_all_deletes(self):
        """Testing get_diff_data_chunks_info with all deletes"""
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -10,10 +12,6 @@\n'
                b' #\n'
                b' #\n'
                b' #\n'
                b'-# old line\n'
                b'-# old line\n'
                b'-# old line\n'
                b'-# old line\n'
                b' #\n'
                b' #\n'
                b' #\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 9,
                        'chunk_len': 10,
                        'changes_start': 12,
                        'changes_len': 4,
                    },
                    'modified': {
                        'pre_lines_of_context': 6,
                        'post_lines_of_context': 0,
                        'chunk_start': 11,
                        'chunk_len': 6,
                        'changes_start': 11,
                        'changes_len': 0,
                    },
                },
            ])

    def test_with_complex_chunk(self):
        """Testing get_diff_data_chunks_info with complex chunk containing
        inserts, deletes, and equals
        """
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -10,9 +12,12 @@\n'
                b' #\n'
                b' #\n'
                b' #\n'
                b'+# new line\n'
                b' #\n'
                b'-# old line\n'
                b'+# new line\n'
                b'+# new line\n'
                b' #\n'
                b'+# new line\n'
                b' #\n'
                b' #\n'
                b' #\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 4,
                        'post_lines_of_context': 4,
                        'chunk_start': 9,
                        'chunk_len': 9,
                        'changes_start': 13,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 11,
                        'chunk_len': 12,
                        'changes_start': 14,
                        'changes_len': 6,
                    },
                },
            ])

    def test_with_change_on_first_line(self):
        """Testing get_diff_data_chunks_info with change on first line"""
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -1,4 +1,5 @@\n'
                b'-# old line\n'
                b'+# new line\n'
                b'+# new line\n'
                b' #\n'
                b' #\n'
                b' #\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 3,
                        'chunk_start': 0,
                        'chunk_len': 4,
                        'changes_start': 0,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 3,
                        'chunk_start': 0,
                        'chunk_len': 5,
                        'changes_start': 0,
                        'changes_len': 2,
                    },
                },
            ])

    def test_with_change_on_second_line(self):
        """Testing get_diff_data_chunks_info with change on second line"""
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -1,5 +1,6 @@\n'
                b' #\n'
                b'-# old line\n'
                b'+# new line\n'
                b'+# new line\n'
                b' #\n'
                b' #\n'
                b' #\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 1,
                        'post_lines_of_context': 3,
                        'chunk_start': 0,
                        'chunk_len': 5,
                        'changes_start': 1,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 1,
                        'post_lines_of_context': 3,
                        'chunk_start': 0,
                        'chunk_len': 6,
                        'changes_start': 1,
                        'changes_len': 2,
                    },
                },
            ])

    def test_with_change_on_third_line(self):
        """Testing get_diff_data_chunks_info with change on third line"""
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -1,6 +1,7 @@\n'
                b' #\n'
                b' #\n'
                b'-# old line\n'
                b'+# new line\n'
                b'+# new line\n'
                b' #\n'
                b' #\n'
                b' #\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 2,
                        'post_lines_of_context': 3,
                        'chunk_start': 0,
                        'chunk_len': 6,
                        'changes_start': 2,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 2,
                        'post_lines_of_context': 3,
                        'chunk_start': 0,
                        'chunk_len': 7,
                        'changes_start': 2,
                        'changes_len': 2,
                    },
                },
            ])

    def test_with_single_line_replace(self):
        """Testing get_diff_data_chunks_info with single-line diff with
        replaced line
        """
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -1,1 +1,1 @@\n'
                b'-# old line\n'
                b'+# new line\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 0,
                        'chunk_start': 0,
                        'chunk_len': 1,
                        'changes_start': 0,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 0,
                        'chunk_start': 0,
                        'chunk_len': 1,
                        'changes_start': 0,
                        'changes_len': 1,
                    },
                },
            ])

    def test_with_insert_before_only_line(self):
        """Testing get_diff_data_chunks_info with insert before only line
        in diff
        """
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -1,1 +1,2 @@\n'
                b'+# new line\n'
                b' #\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 1,
                        'post_lines_of_context': 0,
                        'chunk_start': 0,
                        'chunk_len': 1,
                        'changes_start': 0,
                        'changes_len': 0,
                    },
                    'modified': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 1,
                        'chunk_start': 0,
                        'chunk_len': 2,
                        'changes_start': 0,
                        'changes_len': 1,
                    },
                },
            ])

    def test_with_no_lengths(self):
        """Testing get_diff_data_chunks_info with no lengths specified"""
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -1 +1 @@\n'
                b'-# old line\n'
                b'+# new line\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 0,
                        'chunk_start': 0,
                        'chunk_len': 1,
                        'changes_start': 0,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 0,
                        'post_lines_of_context': 0,
                        'chunk_start': 0,
                        'chunk_len': 1,
                        'changes_start': 0,
                        'changes_len': 1,
                    },
                },
            ])

    def test_with_header_context(self):
        """Testing get_diff_data_chunks_info with class/functino context
        shown in the header
        """
        self.assertEqual(
            get_diff_data_chunks_info(
                b'@@ -10,7 +12,10 @@ def foo(self):\n'
                b' #\n'
                b' #\n'
                b' #\n'
                b'-# old line\n'
                b'+# new line\n'
                b'+# new line\n'
                b'+# new line\n'
                b'+# new line\n'
                b' #\n'
                b' #\n'
                b' #\n'),
            [
                {
                    'orig': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 9,
                        'chunk_len': 7,
                        'changes_start': 12,
                        'changes_len': 1,
                    },
                    'modified': {
                        'pre_lines_of_context': 3,
                        'post_lines_of_context': 3,
                        'chunk_start': 11,
                        'chunk_len': 10,
                        'changes_start': 14,
                        'changes_len': 4,
                    },
                },
            ])


class GetDiffFilesTests(SpyAgency, TestCase):
    """Unit tests for get_diff_files."""

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_interdiff_when_renaming_twice(self):
        """Testing get_diff_files with interdiff when renaming twice"""
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        one_to_two = (b'diff --git a/foo.txt b/foo.txt\n'
                      b'deleted file mode 100644\n'
                      b'index 092beec..0000000\n'
                      b'--- a/foo.txt\n'
                      b'+++ /dev/null\n'
                      b'@@ -1,2 +0,0 @@\n'
                      b'-This is foo!\n'
                      b'-=]\n'
                      b'diff --git a/foo2.txt b/foo2.txt\n'
                      b'new file mode 100644\n'
                      b'index 0000000..092beec\n'
                      b'--- /dev/null\n'
                      b'+++ b/foo2.txt\n'
                      b'@@ -0,0 +1,2 @@\n'
                      b'+This is foo!\n'
                      b'+=]\n')
        one_to_three = (b'diff --git a/foo.txt b/foo.txt\n'
                        b'deleted file mode 100644\n'
                        b'index 092beec..0000000\n'
                        b'--- a/foo.txt\n'
                        b'+++ /dev/null\n'
                        b'@@ -1,2 +0,0 @@\n'
                        b'-This is foo!\n'
                        b'-=]\n'
                        b'diff --git a/foo3.txt b/foo3.txt\n'
                        b'new file mode 100644\n'
                        b'index 0000000..092beec\n'
                        b'--- /dev/null\n'
                        b'+++ b/foo3.txt\n'
                        b'@@ -0,0 +1,2 @@\n'
                        b'+This is foo!\n'
                        b'+=]\n')

        diffset = self.create_diffset(review_request=review_request)
        self.create_filediff(diffset=diffset, source_file='foo.txt',
                             dest_file='foo2.txt', status=FileDiff.MODIFIED,
                             diff=one_to_two)

        interdiffset = self.create_diffset(review_request=review_request)
        self.create_filediff(diffset=interdiffset, source_file='foo.txt',
                             dest_file='foo3.txt', status=FileDiff.MODIFIED,
                             diff=one_to_three)

        diff_files = get_diff_files(diffset=diffset, interdiffset=interdiffset)
        two_to_three = diff_files[0]

        self.assertEqual(two_to_three['depot_filename'], 'foo2.txt')
        self.assertEqual(two_to_three['dest_filename'], 'foo3.txt')

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_get_diff_files_with_interdiff_and_files_same_source(self):
        """Testing get_diff_files with interdiff and multiple files using the
        same source_file
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        # This one should be reverted, as it has no counterpart in the
        # interdiff.
        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            dest_detail='124',
            diff='diff1')

        # This one should match up with interfilediff1.
        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo2.txt',
            dest_detail='124',
            status=FileDiff.COPIED,
            diff='diff2')

        # This one should be reverted, as it has no counterpart in the
        # interdiff.
        filediff3 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo3.txt',
            dest_detail='124',
            status=FileDiff.COPIED,
            diff='diff3')

        # This one should match up with interfilediff3 and interfilediff4.
        filediff4 = self.create_filediff(
            diffset=diffset,
            source_file='foo4.txt',
            source_revision=123,
            dest_file='foo4.txt',
            dest_detail='124',
            diff='diff4')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        # This one should match up with filediff2.
        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo2.txt',
            dest_detail='124',
            status=FileDiff.COPIED,
            diff='interdiff1')

        # This one should show up as a new file.
        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=PRE_CREATION,
            dest_file='foo.txt',
            dest_detail='125',
            diff='interdiff2')

        # This one should match up with filediff4.
        interfilediff3 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo4.txt',
            source_revision=123,
            dest_file='foo5.txt',
            dest_detail='124',
            diff='interdiff2')

        # This one should match up with filediff4 as well.
        interfilediff4 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo4.txt',
            source_revision=123,
            dest_file='foo6.txt',
            dest_detail='124',
            diff='interdiff3')

        diff_files = get_diff_files(diffset=diffset,
                                    interdiffset=interdiffset)
        self.assertEqual(len(diff_files), 6)

        diff_file = diff_files[0]
        self.assertEqual(diff_file['depot_filename'], 'foo.txt')
        self.assertEqual(diff_file['dest_filename'], 'foo.txt')
        self.assertEqual(diff_file['filediff'], filediff1)
        self.assertEqual(diff_file['interfilediff'], None)
        self.assertEqual(diff_file['revision'], 'Diff Revision 1')
        self.assertEqual(diff_file['dest_revision'],
                         'Diff Revision 2 - File Reverted')
        self.assertFalse(diff_file['is_new_file'])
        self.assertTrue(diff_file['force_interdiff'])

        diff_file = diff_files[1]
        self.assertEqual(diff_file['depot_filename'], 'foo.txt')
        self.assertEqual(diff_file['dest_filename'], 'foo.txt')
        self.assertEqual(diff_file['filediff'], interfilediff2)
        self.assertEqual(diff_file['interfilediff'], None)
        self.assertEqual(diff_file['revision'], 'Diff Revision 1')
        self.assertEqual(diff_file['dest_revision'], 'New File')
        self.assertTrue(diff_file['is_new_file'])
        self.assertFalse(diff_file['force_interdiff'])

        diff_file = diff_files[2]
        self.assertEqual(diff_file['depot_filename'], 'foo2.txt')
        self.assertEqual(diff_file['dest_filename'], 'foo2.txt')
        self.assertEqual(diff_file['filediff'], filediff2)
        self.assertEqual(diff_file['interfilediff'], interfilediff1)
        self.assertEqual(diff_file['revision'], 'Diff Revision 1')
        self.assertEqual(diff_file['dest_revision'], 'Diff Revision 2')
        self.assertFalse(diff_file['is_new_file'])
        self.assertTrue(diff_file['force_interdiff'])

        diff_file = diff_files[3]
        self.assertEqual(diff_file['depot_filename'], 'foo.txt')
        self.assertEqual(diff_file['dest_filename'], 'foo3.txt')
        self.assertEqual(diff_file['filediff'], filediff3)
        self.assertEqual(diff_file['interfilediff'], None)
        self.assertEqual(diff_file['revision'], 'Diff Revision 1')
        self.assertEqual(diff_file['dest_revision'],
                         'Diff Revision 2 - File Reverted')
        self.assertFalse(diff_file['is_new_file'])
        self.assertTrue(diff_file['force_interdiff'])

        diff_file = diff_files[4]
        self.assertEqual(diff_file['depot_filename'], 'foo4.txt')
        self.assertEqual(diff_file['dest_filename'], 'foo5.txt')
        self.assertEqual(diff_file['filediff'], filediff4)
        self.assertEqual(diff_file['interfilediff'], interfilediff3)
        self.assertEqual(diff_file['revision'], 'Diff Revision 1')
        self.assertEqual(diff_file['dest_revision'], 'Diff Revision 2')
        self.assertFalse(diff_file['is_new_file'])
        self.assertTrue(diff_file['force_interdiff'])

        diff_file = diff_files[5]
        self.assertEqual(diff_file['depot_filename'], 'foo4.txt')
        self.assertEqual(diff_file['dest_filename'], 'foo6.txt')
        self.assertEqual(diff_file['filediff'], filediff4)
        self.assertEqual(diff_file['interfilediff'], interfilediff4)
        self.assertEqual(diff_file['revision'], 'Diff Revision 1')
        self.assertEqual(diff_file['dest_revision'], 'Diff Revision 2')
        self.assertFalse(diff_file['is_new_file'])
        self.assertTrue(diff_file['force_interdiff'])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_get_diff_files_with_interdiff_using_filediff_only(self):
        """Testing get_diff_files with interdiff using filediff but no
        interfilediff
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo2.txt',
            status=FileDiff.COPIED,
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            status=FileDiff.COPIED,
            diff='interdiff1')

        self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo2.txt',
            status=FileDiff.COPIED,
            diff='interdiff2')

        diff_files = get_diff_files(diffset=diffset,
                                    interdiffset=interdiffset,
                                    filediff=filediff)
        self.assertEqual(len(diff_files), 1)

        diff_file = diff_files[0]
        self.assertEqual(diff_file['depot_filename'], 'foo.txt')
        self.assertEqual(diff_file['dest_filename'], 'foo.txt')
        self.assertEqual(diff_file['filediff'], filediff)
        self.assertEqual(diff_file['interfilediff'], None)
        self.assertEqual(diff_file['revision'], 'Diff Revision 1')
        self.assertEqual(diff_file['dest_revision'],
                         'Diff Revision 2 - File Reverted')
        self.assertFalse(diff_file['is_new_file'])
        self.assertTrue(diff_file['force_interdiff'])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_get_diff_files_with_interdiff_using_both_filediffs(self):
        """Testing get_diff_files with interdiff using filediff and
        interfilediff
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo2.txt',
            status=FileDiff.COPIED,
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            status=FileDiff.COPIED,
            diff='interdiff1')

        self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo2.txt',
            status=FileDiff.COPIED,
            diff='interdiff2')

        diff_files = get_diff_files(diffset=diffset,
                                    interdiffset=interdiffset,
                                    filediff=filediff,
                                    interfilediff=interfilediff)
        self.assertEqual(len(diff_files), 1)

        diff_file = diff_files[0]
        self.assertEqual(diff_file['depot_filename'], 'foo.txt')
        self.assertEqual(diff_file['dest_filename'], 'foo.txt')
        self.assertEqual(diff_file['filediff'], filediff)
        self.assertEqual(diff_file['interfilediff'], interfilediff)
        self.assertEqual(diff_file['revision'], 'Diff Revision 1')
        self.assertEqual(diff_file['dest_revision'], 'Diff Revision 2')
        self.assertFalse(diff_file['is_new_file'])
        self.assertTrue(diff_file['force_interdiff'])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_get_diff_files_filename_normalization_extra_data(self):
        """Testing that filename normalization from get_diff_files receives
        FileDiff extra_data
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')
        filediff.extra_data['test'] = True

        tool_class = repository.scmtool_class
        self.spy_on(tool_class.normalize_path_for_display,
                    owner=tool_class)

        get_diff_files(diffset=diffset, filediff=filediff)

        self.assertSpyCalledWith(tool_class.normalize_path_for_display,
                                 'foo.txt', extra_data={'test': True})


class GetMatchedInterdiffFilesTests(TestCase):
    """Unit tests for get_matched_interdiff_files."""

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_simple_matches(self):
        """Testing get_matched_interdiff_files with simple source file matches
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            diff='interdiff2')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1, interfilediff2])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, interfilediff2),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_new_added_file_left(self):
        """Testing get_matched_interdiff_files with new added file on left
        side only
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=PRE_CREATION,
            dest_file='foo2.txt',
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, None),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_new_added_file_right(self):
        """Testing get_matched_interdiff_files with new added file on right
        side only
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=PRE_CREATION,
            dest_file='foo2.txt',
            diff='interdiff2')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1],
            interfilediffs=[interfilediff1, interfilediff2])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (None, interfilediff2),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_new_added_file_both(self):
        """Testing get_matched_interdiff_files with new added file on both
        sides
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=PRE_CREATION,
            dest_file='foo2.txt',
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=PRE_CREATION,
            dest_file='foo2.txt',
            diff='interdiff2')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1, interfilediff2])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, interfilediff2),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_new_deleted_file_left(self):
        """Testing get_matched_interdiff_files with new deleted file on left
        side only
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            status=FileDiff.DELETED,
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, None),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_new_deleted_file_right(self):
        """Testing get_matched_interdiff_files with new deleted file on right
        side only
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            status=FileDiff.DELETED,
            diff='interdiff2')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1],
            interfilediffs=[interfilediff1, interfilediff2])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (None, interfilediff2),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_new_deleted_file_both(self):
        """Testing get_matched_interdiff_files with new deleted file on both
        sides
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            status=FileDiff.DELETED,
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            status=FileDiff.DELETED,
            diff='interdiff2')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1, interfilediff2])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, interfilediff2),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_new_modified_file_right(self):
        """Testing get_matched_interdiff_files with new modified file on
        right side
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            diff='interdiff2')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1],
            interfilediffs=[interfilediff1, interfilediff2])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (None, interfilediff2),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_reverted_file(self):
        """Testing get_matched_interdiff_files with reverted file"""
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, None),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_both_renames(self):
        """Testing get_matched_interdiff_files with matching renames on both
        sides
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo2.txt',
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo2.txt',
            diff='interdiff2')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1, interfilediff2])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, interfilediff2),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_new_renames(self):
        """Testing get_matched_interdiff_files with modified on left side,
        modified + renamed on right
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo3.txt',
            diff='interdiff2')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1, interfilediff2])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, interfilediff2),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_multiple_copies(self):
        """Testing get_matched_interdiff_files with multiple copies of file
        from left on right
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo3.txt',
            diff='interdiff2')

        interfilediff3 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo4.txt',
            diff='interdiff3')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1, interfilediff2, interfilediff3])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, interfilediff2),
                (filediff2, interfilediff3),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_added_left_only(self):
        """Testing get_matched_interdiff_files with file added in left only"""
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=PRE_CREATION,
            dest_file='foo.txt',
            dest_detail='124',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            dest_detail='124',
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            dest_detail='124',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=PRE_CREATION,
            dest_file='foo3.txt',
            dest_detail='125',
            diff='interdiff2')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1, interfilediff2])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, None),
                (None, interfilediff2),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_deleted_right_only(self):
        """Testing get_matched_interdiff_files with file deleted in right only
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision='123',
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            status=FileDiff.DELETED,
            diff='diff2')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            status=FileDiff.DELETED,
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo3.txt',
            diff='interdiff2')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2],
            interfilediffs=[interfilediff1, interfilediff2])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, None),
                (None, interfilediff2),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_same_names_multiple_ops(self):
        """Testing get_matched_interdiff_files with same names and multiple
        operation (pathological case)
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)

        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=PRE_CREATION,
            dest_file='foo.txt',
            diff='diff1')

        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            diff='diff2')

        filediff3 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo2.txt',
            diff='diff3')

        filediff4 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            status=FileDiff.DELETED,
            diff='diff1')

        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo3.txt',
            diff='interdiff1')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo2.txt',
            diff='interdiff2')

        interfilediff3 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo3.txt',
            diff='interdiff3')

        interfilediff4 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            status=FileDiff.DELETED,
            diff='interdiff4')

        interfilediff5 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=PRE_CREATION,
            dest_file='foo.txt',
            diff='interdiff5')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2, filediff3, filediff4],
            interfilediffs=[interfilediff1, interfilediff2, interfilediff3,
                            interfilediff4, interfilediff5])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff5),
                (filediff3, interfilediff2),
                (filediff4, interfilediff4),
                (filediff2, interfilediff1),
                (filediff2, interfilediff3),
            ])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_with_new_file_same_name(self):
        """Testing get_matched_interdiff_files with new file on right with
        same name from left
        """
        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)

        diffset = self.create_diffset(review_request=review_request,
                                      revision=1)
        interdiffset = self.create_diffset(review_request=review_request,
                                           revision=2)

        # Modified in revision 1 and in revision 2. Match.
        filediff1 = self.create_filediff(
            diffset=diffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            dest_detail='124',
            diff='diff1')

        interfilediff1 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo.txt',
            source_revision=123,
            dest_file='foo.txt',
            dest_detail='124',
            diff='interdiff1')

        # Modified in revision 1. Re-created in revision 2 with the same
        # revision (implying an edge case where the file was deleted in a
        # parent diff and re-introduced in the main diff, turning into what
        # looks like a modification in the FileDiff).
        filediff2 = self.create_filediff(
            diffset=diffset,
            source_file='foo2.txt',
            source_revision=123,
            dest_file='foo2.txt',
            dest_detail='124',
            diff='diff2')

        interfilediff2 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo2.txt',
            source_revision=PRE_CREATION,
            dest_file='foo2.txt',
            dest_detail='124',
            diff='interdiff2')

        # Modified in revision 1. Re-created in revision 2 with a new revision
        # (implying it was deleted upstream).
        filediff3 = self.create_filediff(
            diffset=diffset,
            source_file='foo3.txt',
            source_revision=123,
            dest_file='foo3.txt',
            dest_detail='124',
            diff='diff3')

        interfilediff3 = self.create_filediff(
            diffset=interdiffset,
            source_file='foo3.txt',
            source_revision=PRE_CREATION,
            dest_file='foo3.txt',
            dest_detail='125',
            diff='interdiff3')

        matched_files = get_matched_interdiff_files(
            tool=repository.get_scmtool(),
            filediffs=[filediff1, filediff2, filediff3],
            interfilediffs=[interfilediff1, interfilediff2, interfilediff3])

        self.assertEqual(
            list(matched_files),
            [
                (filediff1, interfilediff1),
                (filediff2, interfilediff2),
                (filediff3, None),
                (None, interfilediff3),
            ])


class GetLineChangedRegionsTests(TestCase):
    """Unit tests for get_line_changed_regions."""

    def test_get_line_changed_regions(self):
        """Testing get_line_changed_regions"""
        def deep_equal(A, B):
            typea, typeb = type(A), type(B)
            self.assertEqual(typea, typeb)

            if typea is tuple or typea is list:
                for a, b in zip_longest(A, B):
                    deep_equal(a, b)
            else:
                self.assertEqual(A, B)

        deep_equal(get_line_changed_regions(None, None),
                   (None, None))

        old = 'submitter = models.ForeignKey(Person, verbose_name="Submitter")'
        new = 'submitter = models.ForeignKey(User, verbose_name="Submitter")'
        regions = get_line_changed_regions(old, new)
        deep_equal(regions, ([(30, 36)], [(30, 34)]))

        old = '-from reviews.models import ReviewRequest, Person, Group'
        new = '+from .reviews.models import ReviewRequest, Group'
        regions = get_line_changed_regions(old, new)
        deep_equal(regions, ([(0, 1), (6, 6), (43, 51)],
                             [(0, 1), (6, 7), (44, 44)]))

        old = 'abcdefghijklm'
        new = 'nopqrstuvwxyz'
        regions = get_line_changed_regions(old, new)
        deep_equal(regions, (None, None))


class GetDisplayedDiffLineRangesTests(TestCase):
    """Unit tests for get_displayed_diff_line_ranges."""

    def test_with_delete_single_lines(self):
        """Testing get_displayed_diff_line_ranges with delete chunk and single
        virtual line
        """
        chunks = [
            {
                'change': 'delete',
                'lines': [
                    (10, 20, 'deleted line', [], '', '', [], False),
                    # ...
                    (50, 60, 'deleted line', [], '', '', [], False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 20),
            ({
                'display_range': (30, 30),
                'virtual_range': (20, 20),
                'chunk_range': (chunks[0], chunks[0]),
            }, None))

    def test_with_delete_mutiple_lines(self):
        """Testing get_displayed_diff_line_ranges with delete chunk and multiple
        virtual lines
        """
        chunks = [
            {
                'change': 'delete',
                'lines': [
                    (10, 20, 'deleted line', [], '', '', [], False),
                    # ...
                    (50, 60, 'deleted line', [], '', '', [], False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 21),
            ({
                'display_range': (30, 31),
                'virtual_range': (20, 21),
                'chunk_range': (chunks[0], chunks[0]),
            }, None))

    def test_with_replace_single_line(self):
        """Testing get_displayed_diff_line_ranges with replace chunk and single
        virtual line
        """
        chunks = [
            {
                'change': 'replace',
                'lines': [
                    (10, 20, 'foo', [], 30, 'replaced line', [], False),
                    # ...
                    (50, 60, 'foo', [], 70, 'replaced line', [], False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 20),
            ({
                'display_range': (30, 30),
                'virtual_range': (20, 20),
                'chunk_range': (chunks[0], chunks[0]),
            }, {
                'display_range': (40, 40),
                'virtual_range': (20, 20),
                'chunk_range': (chunks[0], chunks[0]),
            }))

    def test_with_replace_multiple_lines(self):
        """Testing get_displayed_diff_line_ranges with replace chunk and
        multiple virtual lines
        """
        chunks = [
            {
                'change': 'replace',
                'lines': [
                    (10, 20, 'foo', [], 30, 'replaced line', [], False),
                    # ...
                    (50, 60, 'foo', [], 70, 'replaced line', [], False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 21),
            ({
                'display_range': (30, 31),
                'virtual_range': (20, 21),
                'chunk_range': (chunks[0], chunks[0]),
            }, {
                'display_range': (40, 41),
                'virtual_range': (20, 21),
                'chunk_range': (chunks[0], chunks[0]),
            }))

    def test_with_insert_single_line(self):
        """Testing get_displayed_diff_line_ranges with insert chunk and single
        virtual line
        """
        chunks = [
            {
                'change': 'insert',
                'lines': [
                    (10, '', '', [], 20, 'inserted line', [], False),
                    # ...
                    (50, '', '', [], 60, 'inserted line', [], False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 20),
            (None, {
                'display_range': (30, 30),
                'virtual_range': (20, 20),
                'chunk_range': (chunks[0], chunks[0]),
            }))

    def test_with_insert_multiple_lines(self):
        """Testing get_displayed_diff_line_ranges with insert chunk and multiple
        virtual lines
        """
        chunks = [
            {
                'change': 'insert',
                'lines': [
                    (10, '', '', [], 20, 'inserted line', [], False),
                    # ...
                    (50, '', '', [], 60, 'inserted line', [], False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 21),
            (None, {
                'display_range': (30, 31),
                'virtual_range': (20, 21),
                'chunk_range': (chunks[0], chunks[0]),
            }))

    def test_with_fake_equal_orig(self):
        """Testing get_displayed_diff_line_ranges with fake equal from
        original side of interdiff
        """
        chunks = [
            {
                'change': 'equal',
                'lines': [
                    (10, '', '', [], 20, 'inserted line', [], False),
                    # ...
                    (50, '', '', [], 60, 'inserted line', [], False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 21),
            (None, {
                'display_range': (30, 31),
                'virtual_range': (20, 21),
                'chunk_range': (chunks[0], chunks[0]),
            }))

    def test_with_fake_equal_patched(self):
        """Testing get_displayed_diff_line_ranges with fake equal from
        patched side of interdiff
        """
        chunks = [
            {
                'change': 'equal',
                'lines': [
                    (10, 20, 'deleted line', [], '', '', [], False),
                    # ...
                    (50, 60, 'deleted line', [], '', '', [], False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 21),
            ({
                'display_range': (30, 31),
                'virtual_range': (20, 21),
                'chunk_range': (chunks[0], chunks[0]),
            }, None))

    def test_with_spanning_insert_delete(self):
        """Testing get_displayed_diff_line_ranges with spanning delete and
        insert
        """
        chunks = [
            {
                'change': 'delete',
                'lines': [
                    (10, 20, 'deleted line', [], '', '', [], False),
                    # ...
                    (50, 60, 'deleted line', [], '', '', [], False),
                ],
            },
            {
                'change': 'insert',
                'lines': [
                    (51, '', '', [], 61, 'inserted line', [], False),
                    # ...
                    (100, '', '', [], 110, 'inserted line', [], False),
                ],
            },
            {
                'change': 'equal',
                'lines': [
                    (101, 61, 'equal line', [], 111, 'equal line', [],
                     False),
                    # ...
                    (200, 160, 'equal line', [], 210, 'equal line', [],
                     False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 69),
            ({
                'display_range': (30, 60),
                'virtual_range': (20, 50),
                'chunk_range': (chunks[0], chunks[0]),
            }, {
                'display_range': (61, 79),
                'virtual_range': (51, 69),
                'chunk_range': (chunks[1], chunks[1]),
            }))

    def test_with_spanning_delete_insert(self):
        """Testing get_displayed_diff_line_ranges with spanning insert and
        delete
        """
        chunks = [
            {
                'change': 'insert',
                'lines': [
                    (10, '', '', [], 20, 'inserted line', [], False),
                    # ...
                    (50, '', '', [], 60, 'inserted line', [], False),
                ],
            },
            {
                'change': 'delete',
                'lines': [
                    (51, 61, 'inserted line', [], '', '', [], False),
                    # ...
                    (100, 110, 'inserted line', [], '', '', [], False),
                ],
            },
            {
                'change': 'equal',
                'lines': [
                    (101, 111, 'equal line', [], 61, 'equal line', [],
                     False),
                    # ...
                    (200, 210, 'equal line', [], 160, 'equal line', [],
                     False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 69),
            ({
                'display_range': (61, 79),
                'virtual_range': (51, 69),
                'chunk_range': (chunks[1], chunks[1]),
            }, {
                'display_range': (30, 60),
                'virtual_range': (20, 50),
                'chunk_range': (chunks[0], chunks[0]),
            }))

    def test_with_spanning_last_chunk(self):
        """Testing get_displayed_diff_line_ranges with spanning chunks through
        last chunk
        """
        chunks = [
            {
                'change': 'delete',
                'lines': [
                    (10, 20, 'deleted line', [], '', '', [], False),
                    # ...
                    (50, 60, 'deleted line', [], '', '', [], False),
                ],
            },
            {
                'change': 'insert',
                'lines': [
                    (51, '', '', [], 61, 'inserted line', [], False),
                    # ...
                    (100, '', '', [], 110, 'inserted line', [], False),
                ],
            },
        ]

        self.assertEqual(
            get_displayed_diff_line_ranges(chunks, 20, 69),
            ({
                'display_range': (30, 60),
                'virtual_range': (20, 50),
                'chunk_range': (chunks[0], chunks[0]),
            }, {
                'display_range': (61, 79),
                'virtual_range': (51, 69),
                'chunk_range': (chunks[1], chunks[1]),
            }))


class DiffExpansionHeaderTests(TestCase):
    """Testing generation of diff expansion headers."""

    def test_find_header_with_filtered_equal(self):
        """Testing finding a header in a file that has filtered equals
        chunks
        """
        # See diffviewer.diffutils.get_file_chunks_in_range for a description
        # of chunks and its elements. We fake the elements of lines here
        # because we only need elements 0, 1, and 4 (of what would be a list).
        chunks = [
            {
                'change': 'equal',
                'meta': {
                    'left_headers': [(1, 'foo')],
                    'right_headers': [],
                },
                'lines': [
                    {
                        0: 1,
                        1: 1,
                        4: '',
                    },
                    {
                        0: 2,
                        1: 2,
                        4: 1,
                    },
                ]
            },
            {
                'change': 'equal',
                'meta': {
                    'left_headers': [],
                    'right_headers': [(2, 'bar')],
                },
                'lines': [
                    {
                        0: 3,
                        1: '',
                        4: 2,
                    },
                    {
                        0: 4,
                        1: 3,
                        4: 3,
                    },
                ]
            }
        ]

        left_header = {
            'line': 1,
            'text': 'foo',
        }
        right_header = {
            'line': 3,
            'text': 'bar',
        }

        self.assertEqual(
            _get_last_header_in_chunks_before_line(chunks, 2),
            {
                'left': left_header,
                'right': None,
            })

        self.assertEqual(
            _get_last_header_in_chunks_before_line(chunks, 4),
            {
                'left': left_header,
                'right': right_header,
            })

    def test_find_header_with_header_oustside_chunk(self):
        """Testing finding a header in a file where the header in a chunk does
        not belong to the chunk it is in
        """
        chunks = [
            {
                'change': 'equal',
                'meta': {
                    'left_headers': [
                        (1, 'foo'),
                        (100, 'bar'),
                    ],
                },
                'lines': [
                    {
                        0: 1,
                        1: 1,
                        4: 1,
                    },
                    {
                        0: 2,
                        1: 2,
                        4: 1,
                    },
                ]
            }
        ]

        self.assertEqual(
            _get_last_header_in_chunks_before_line(chunks, 2),
            {
                'left': {
                    'line': 1,
                    'text': 'foo',
                },
                'right': None,
            })

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_headers_use_correct_line_insert(self):
        """Testing header generation for chunks with insert chunks above"""
        line_number = 27  # This is a header line below the chunk of inserts

        diff = (b"diff --git a/tests.py b/tests.py\n"
                b"index a4fc53e..f2414cc 100644\n"
                b"--- a/tests.py\n"
                b"+++ b/tests.py\n"
                b"@@ -20,6 +20,9 @@ from reviewboard.site.urlresolvers import "
                b"local_site_reverse\n"
                b" from reviewboard.site.models import LocalSite\n"
                b" from reviewboard.webapi.errors import INVALID_REPOSITORY\n"
                b"\n"
                b"+class Foo(object):\n"
                b"+    def bar(self):\n"
                b"+        pass\n"
                b"\n"
                b" class BaseWebAPITestCase(TestCase, EmailTestHelper);\n"
                b"     fixtures = ['test_users', 'test_reviewrequests', 'test_"
                b"scmtools',\n")

        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)

        filediff = self.create_filediff(
            diffset=diffset, source_file='tests.py', dest_file='tests.py',
            source_revision='a4fc53e08863f5341effb5204b77504c120166ae',
            diff=diff)

        context = {'user': review_request.submitter}

        siteconfig_settings = {
            'diffviewer_syntax_highlighting': False,
        }

        with self.siteconfig_settings(siteconfig_settings,
                                      reload_settings=False):
            header = get_last_header_before_line(context=context,
                                                 filediff=filediff,
                                                 interfilediff=None,
                                                 target_line=line_number)
            chunks = get_file_chunks_in_range(
                context=context,
                filediff=filediff,
                interfilediff=None,
                first_line=1,
                num_lines=get_last_line_number_in_diff(
                    context=context,
                    filediff=filediff,
                    interfilediff=None))

        lines = []

        for chunk in chunks:
            lines.extend(chunk['lines'])

        # The header we find should be before our line number (which has a
        # header itself).
        self.assertTrue(header['right']['line'] < line_number)

        # The line numbers start at 1 and not 0.
        self.assertEqual(header['right']['text'],
                         lines[header['right']['line'] - 1][5])

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_header_correct_line_delete(self):
        """Testing header generation for chunks with delete chunks above"""
        line_number = 53  # This is a header line below the chunk of deletes

        diff = (b"diff --git a/tests.py b/tests.py\n"
                b"index a4fc53e..ba7d34b 100644\n"
                b"--- a/tests.py\n"
                b"+++ b/tests.py\n"
                b"@@ -47,9 +47,6 @@ class BaseWebAPITestCase(TestCase, "
                b"EmailTestHelper);\n"
                b"\n"
                b"         yourself.base_url = 'http;//testserver'\n"
                b"\n"
                b"-    def tearDown(yourself);\n"
                b"-        yourself.client.logout()\n"
                b"-\n"
                b"     def api_func_wrapper(yourself, api_func, path, query, "
                b"expected_status,\n"
                b"                          follow_redirects, expected_"
                b"redirects);\n"
                b"         response = api_func(path, query, follow=follow_"
                b"redirects)\n")

        repository = self.create_repository(tool_name='Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)

        filediff = self.create_filediff(
            diffset=diffset, source_file='tests.py', dest_file='tests.py',
            source_revision='a4fc53e08863f5341effb5204b77504c120166ae',
            diff=diff)

        context = {'user': review_request.submitter}

        siteconfig_settings = {
            'diffviewer_syntax_highlighting': False,
        }

        with self.siteconfig_settings(siteconfig_settings,
                                      reload_settings=False):
            header = get_last_header_before_line(context=context,
                                                 filediff=filediff,
                                                 interfilediff=None,
                                                 target_line=line_number)
            chunks = get_file_chunks_in_range(
                context=context,
                filediff=filediff,
                interfilediff=None,
                first_line=1,
                num_lines=get_last_line_number_in_diff(
                    context=context,
                    filediff=filediff,
                    interfilediff=None))

        lines = []

        for chunk in chunks:
            lines.extend(chunk['lines'])

        # The header we find should be before our line number (which has a
        # header itself).
        self.assertTrue(header['left']['line'] < line_number)

        # The line numbers start at 1 and not 0.
        self.assertEqual(header['left']['text'],
                         lines[header['left']['line'] - 1][2])


class PatchTests(TestCase):
    """Unit tests for patch."""

    def test_patch(self):
        """Testing patch"""
        old = (b'int\n'
               b'main()\n'
               b'{\n'
               b'\tprintf("foo\\n");\n'
               b'}\n')

        new = (b'#include <stdio.h>\n'
               b'\n'
               b'int\n'
               b'main()\n'
               b'{\n'
               b'\tprintf("foo bar\\n");\n'
               b'\treturn 0;\n'
               b'}\n')

        diff = (b'--- foo.c\t2007-01-24 02:11:31.000000000 -0800\n'
                b'+++ foo.c\t2007-01-24 02:14:42.000000000 -0800\n'
                b'@@ -1,5 +1,8 @@\n'
                b'+#include <stdio.h>\n'
                b'+\n'
                b' int\n'
                b' main()\n'
                b' {\n'
                b'-\tprintf("foo\\n");\n'
                b'+\tprintf("foo bar\\n");\n'
                b'+\treturn 0;\n'
                b' }\n')

        patched = patch(diff, old, 'foo.c')
        self.assertEqual(patched, new)

        diff = (b'--- README\t2007-01-24 02:10:28.000000000 -0800\n'
                b'+++ README\t2007-01-24 02:11:01.000000000 -0800\n'
                b'@@ -1,9 +1,10 @@\n'
                b' Test data for a README file.\n'
                b' \n'
                b' There\'s a line here.\n'
                b'-\n'
                b' A line there.\n'
                b' \n'
                b' And here.\n')

        with self.assertRaises(Exception):
            patch(diff, old, 'foo.c')

    def test_empty_patch(self):
        """Testing patch with an empty diff"""
        old = 'This is a test'
        diff = ''
        patched = patch(diff, old, 'test.c')
        self.assertEqual(patched, old)

    def test_patch_crlf_file_crlf_diff(self):
        """Testing patch with a CRLF file and a CRLF diff"""
        old = (b'Test data for a README file.\r\n'
               b'\r\n'
               b'There\'s a line here.\r\n'
               b'\r\n'
               b'A line there.\r\n'
               b'\r\n'
               b'And here.\r\n')

        new = (b'Test data for a README file.\n'
               b'\n'
               b'There\'s a line here.\n'
               b'A line there.\n'
               b'\n'
               b'And here.\n')

        diff = (b'--- README\t2007-07-02 23:33:27.000000000 -0700\n'
                b'+++ README\t2007-07-02 23:32:59.000000000 -0700\n'
                b'@@ -1,7 +1,6 @@\n'
                b' Test data for a README file.\r\n'
                b' \r\n'
                b' There\'s a line here.\r\n'
                b'-\r\n'
                b' A line there.\r\n'
                b' \r\n'
                b' And here.\r\n')

        patched = patch(diff, old, new)
        self.assertEqual(patched, new)

    def test_patch_cr_file_crlf_diff(self):
        """Testing patch with a CR file and a CRLF diff"""
        old = (b'Test data for a README file.\n'
               b'\n'
               b'There\'s a line here.\n'
               b'\n'
               b'A line there.\n'
               b'\n'
               b'And here.\n')

        new = (b'Test data for a README file.\n'
               b'\n'
               b'There\'s a line here.\n'
               b'A line there.\n'
               b'\n'
               b'And here.\n')

        diff = (b'--- README\t2007-07-02 23:33:27.000000000 -0700\n'
                b'+++ README\t2007-07-02 23:32:59.000000000 -0700\n'
                b'@@ -1,7 +1,6 @@\n'
                b' Test data for a README file.\r\n'
                b' \r\n'
                b' There\'s a line here.\r\n'
                b'-\r\n'
                b' A line there.\r\n'
                b' \r\n'
                b' And here.\r\n')

        patched = patch(diff, old, new)
        self.assertEqual(patched, new)

    def test_patch_crlf_file_cr_diff(self):
        """Testing patch with a CRLF file and a CR diff"""
        old = (b'Test data for a README file.\r\n'
               b'\r\n'
               b'There\'s a line here.\r\n'
               b'\r\n'
               b'A line there.\r\n'
               b'\r\n'
               b'And here.\r\n')

        new = (b'Test data for a README file.\n'
               b'\n'
               b'There\'s a line here.\n'
               b'A line there.\n'
               b'\n'
               b'And here.\n')

        diff = (b'--- README\t2007-07-02 23:33:27.000000000 -0700\n'
                b'+++ README\t2007-07-02 23:32:59.000000000 -0700\n'
                b'@@ -1,7 +1,6 @@\n'
                b' Test data for a README file.\n'
                b' \n'
                b' There\'s a line here.\n'
                b'-\n'
                b' A line there.\n'
                b' \n'
                b' And here.\n')

        patched = patch(diff, old, new)
        self.assertEqual(patched, new)

    def test_patch_file_with_fake_no_newline(self):
        """Testing patch with a file indicating no newline
        with a trailing \\r
        """
        old = (
            b'Test data for a README file.\n'
            b'\n'
            b'There\'s a line here.\n'
            b'\n'
            b'A line there.\n'
            b'\n'
            b'And a new line here!\n'
            b'\n'
            b'We must have several lines to reproduce this problem.\n'
            b'\n'
            b'So that there\'s enough hidden context.\n'
            b'\n'
            b'And dividers so we can reproduce the bug.\n'
            b'\n'
            b'Which will a --- line at the end of one file due to the '
            b'lack of newline,\n'
            b'causing a parse error.\n'
            b'\n'
            b'And here.\n'
            b'Yes, this is a good README file. Like most README files, '
            b'this doesn\'t tell youanything you really didn\'t already '
            b'know.\r')

        new = (
            b'Test data for a README file.\n'
            b'\n'
            b'There\'s a line here.\n'
            b'Here\'s a change!\n'
            b'\n'
            b'A line there.\n'
            b'\n'
            b'And a new line here!\n'
            b'\n'
            b'We must have several lines to reproduce this problem.\n'
            b'\n'
            b'So that there\'s enough hidden context.\n'
            b'\n'
            b'And dividers so we can reproduce the bug.\n'
            b'\n'
            b'Which will a --- line at the end of one file due to the '
            b'lack of newline,\n'
            b'causing a parse error.\n'
            b'\n'
            b'And here.\n'
            b'Yes, this is a good README file. Like most README files, '
            b'this doesn\'t tell youanything you really didn\'t '
            b'already know.\n')

        diff = (
            b'--- README\t2008-02-25 03:40:42.000000000 -0800\n'
            b'+++ README\t2008-02-25 03:40:55.000000000 -0800\n'
            b'@@ -1,6 +1,7 @@\n'
            b' Test data for a README file.\n'
            b' \n'
            b' There\'s a line here.\n'
            b'+Here\'s a change!\n'
            b' \n'
            b' A line there.\n'
            b' \n'
            b'@@ -16,4 +17,4 @@\n'
            b' causing a parse error.\n'
            b' \n'
            b' And here.\n'
            b'-Yes, this is a good README file. Like most README files, this '
            b'doesn\'t tell youanything you really didn\'t already know.\n'
            b'\\ No newline at end of file\n'
            b'+Yes, this is a good README file. Like most README files, this '
            b'doesn\'t tell youanything you really didn\'t already know.\n')

        patched = patch(diff, old, 'README')
        self.assertEqual(patched, new)


class GetOriginalFileTests(SpyAgency, TestCase):
    """Unit tests for get_original_file."""

    fixtures = ['test_scmtools']

    def test_created_in_parent(self):
        """Test get_original_file with a file created in the parent diff"""
        parent_diff = (
            b'diff --git a/test b/test\n'
            b'new file mode 100644\n'
            b'index 0000000..61ee8b5\n'
            b'--- /dev/null\n'
            b'+++ b/test\n'
            b'@@ -0,0 +1 @@\n'
            b'+abc123\n'
        )

        diff = (
            b'diff --git a/test b/test\n'
            b'index 61ee8b5..b9af648 100644\n'
            b'--- a/test\n'
            b'+++ b/test\n'
            b'@@ -1 +1 @@\n'
            b'-abc123\n'
            b'+def456\n'
        )

        repository = self.create_repository(tool_name='Git')
        diffset = self.create_diffset(repository=repository)
        filediff = FileDiff.objects.create(
            diffset=diffset,
            source_file='test',
            source_revision='61ee8b5',
            dest_file='test',
            dest_detail='b9af648',
            extra_data={
                'parent_source_filename': 'test',
                'parent_source_revision': six.text_type(PRE_CREATION),
            })
        filediff.parent_diff = parent_diff
        filediff.diff = diff
        filediff.save()

        request = self.create_http_request('/')

        self.assertEqual(get_original_file(filediff=filediff,
                                           request=request,
                                           encoding_list=['ascii']),
                         b'abc123\n')

    def test_empty_parent_diff_old_patch(self):
        """Testing get_original_file with an empty parent diff with a patch
        tool that does not accept empty diffs
        """
        parent_diff = (
            b'diff --git a/empty b/empty\n'
            b'new file mode 100644\n'
            b'index 0000000..e69de29\n'
        )

        diff = (
            b'diff --git a/empty b/empty\n'
            b'index e69de29..0e4b0c7 100644\n'
            b'--- a/empty\n'
            b'+++ a/empty\n'
            b'@@ -0,0 +1 @@\n'
            b'+abc123\n'
        )

        repository = self.create_repository(tool_name='Git')
        diffset = self.create_diffset(repository=repository)
        filediff = FileDiff.objects.create(
            diffset=diffset,
            source_file='empty',
            source_revision=PRE_CREATION,
            dest_file='empty',
            dest_detail='0e4b0c7')
        filediff.parent_diff = parent_diff
        filediff.diff = diff
        filediff.save()

        request_factory = RequestFactory()

        # Older versions of patch will choke on an empty patch with a "garbage
        # input" error, but newer versions will handle it just fine. We stub
        # out patch here to always fail so we can test for the case of an older
        # version of patch without requiring it to be installed.
        def _patch(diff, orig_file, filename, request=None):
            self.assertEqual(diff, parent_diff)
            raise PatchError(
                filename=filename,
                error_output=_PATCH_GARBAGE_INPUT,
                orig_file=orig_file,
                new_file='tmp123-new',
                diff=b'',
                rejects=None)

        self.spy_on(patch, call_fake=_patch)

        # One query for each of the following:
        # - saving the RawFileDiffData in RawFileDiffData.recompute_line_counts
        # - saving the FileDiff in FileDiff.is_parent_diff_empty
        with self.assertNumQueries(2):
            orig = get_original_file(
                filediff=filediff,
                request=request_factory.get('/'),
                encoding_list=['ascii'])

        self.assertEqual(orig, b'')

        # Refresh the object from the database with the parent diff attached
        # and then verify that re-calculating the original file does not cause
        # additional queries.
        filediff = (
            FileDiff.objects
            .filter(pk=filediff.pk)
            .select_related('parent_diff_hash')
            .first()
        )

        with self.assertNumQueries(0):
            orig = get_original_file(
                filediff=filediff,
                request=request_factory.get('/'),
                encoding_list=['ascii'])

    def test_empty_parent_diff_new_patch(self):
        """Testing get_original_file with an empty parent diff with a patch
        tool that does accept empty diffs
        """
        parent_diff = (
            b'diff --git a/empty b/empty\n'
            b'new file mode 100644\n'
            b'index 0000000..e69de29\n'
        )

        diff = (
            b'diff --git a/empty b/empty\n'
            b'index e69de29..0e4b0c7 100644\n'
            b'--- a/empty\n'
            b'+++ a/empty\n'
            b'@@ -0,0 +1 @@\n'
            b'+abc123\n'
        )

        repository = self.create_repository(tool_name='Git')
        diffset = self.create_diffset(repository=repository)
        filediff = FileDiff.objects.create(
            diffset=diffset,
            source_file='empty',
            source_revision=PRE_CREATION,
            dest_file='empty',
            dest_detail='0e4b0c7')
        filediff.parent_diff = parent_diff
        filediff.diff = diff
        filediff.save()

        request_factory = RequestFactory()

        # Newer versions of patch will allow empty patches. We stub out patch
        # here to always fail so we can test for the case of a newer version
        # of patch without requiring it to be installed.
        def _patch(diff, orig_file, filename, request=None):
            # This is the only call to patch() that should be made.
            self.assertEqual(diff, parent_diff)
            return orig_file

        self.spy_on(patch, call_fake=_patch)

        with self.assertNumQueries(0):
            orig = get_original_file(
                filediff=filediff,
                request=request_factory.get('/'),
                encoding_list=['ascii'])

        self.assertEqual(orig, b'')

        # Refresh the object from the database with the parent diff attached
        # and then verify that re-calculating the original file does not cause
        # additional queries.
        filediff = (
            FileDiff.objects
            .select_related('parent_diff_hash')
            .get(pk=filediff.pk)
        )

        with self.assertNumQueries(0):
            orig = get_original_file(
                filediff=filediff,
                request=request_factory.get('/'),
                encoding_list=['ascii'])

    def test_parent_diff_with_rename_and_modern_fields(self):
        """Testing get_original_file with a file renamed in parent diff
        with modern parent_source_* keys in extra_data
        """
        parent_diff = (
            b'diff --git a/old-name b/new-name\n'
            b'rename from old-name\n'
            b'rename to new-name\n'
            b'index b7a8c9f..e69de29 100644\n'
            b'--- a/old-name\n'
            b'+++ a/new-name\n'
            b'@@ -1,1 +1,1 @@\n'
            b'-orig file\n'
            b'+abc123\n'
        )

        diff = (
            b'diff --git a/new-name b/new-name\n'
            b'index e69de29..0e4b0c7 100644\n'
            b'--- a/new-name\n'
            b'+++ a/new-name\n'
            b'@@ -1,1 +1,1 @@\n'
            b'+abc123\n'
            b'+def456\n'
        )

        repository = self.create_repository(tool_name='Git')
        diffset = self.create_diffset(repository=repository)
        filediff = FileDiff.objects.create(
            diffset=diffset,
            source_file='new-name',
            source_revision='e69de29',
            dest_file='new-name',
            dest_detail='0e4b0c7',
            extra_data={
                'parent_source_filename': 'old-file',
                'parent_source_revision': 'b7a8c9f',
            })
        filediff.parent_diff = parent_diff
        filediff.diff = diff
        filediff.save()

        request_factory = RequestFactory()

        def _get_file(_self, path, revision, *args, **kwargs):
            self.assertEqual(path, 'old-file')
            self.assertEqual(revision, 'b7a8c9f')

            return b'orig file\n'

        self.spy_on(repository.get_file, call_fake=_get_file)

        with self.assertNumQueries(0):
            orig = get_original_file(filediff=filediff,
                                     request=request_factory.get('/'),
                                     encoding_list=['ascii'])

        self.assertEqual(orig, b'abc123\n')

        # Refresh the object from the database with the parent diff attached
        # and then verify that re-calculating the original file does not cause
        # additional queries.
        filediff = (
            diffset.files
            .select_related('parent_diff_hash')
            .get(pk=filediff.pk)
        )

        with self.assertNumQueries(0):
            orig = get_original_file(filediff=filediff,
                                     request=request_factory.get('/'),
                                     encoding_list=['ascii'])
