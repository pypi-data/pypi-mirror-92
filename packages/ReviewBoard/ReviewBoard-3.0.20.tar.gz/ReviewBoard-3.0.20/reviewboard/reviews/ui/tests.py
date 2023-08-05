from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import RequestFactory
from djblets.util.templatetags.djblets_images import crop_image
from kgb import SpyAgency

from reviewboard.reviews.templatetags.reviewtags import has_usable_review_ui
from reviewboard.admin.server import build_server_url
from reviewboard.reviews.ui.base import (FileAttachmentReviewUI,
                                         register_ui,
                                         unregister_ui)
from reviewboard.reviews.ui.image import ImageReviewUI
from reviewboard.testing import TestCase


class InitReviewUI(FileAttachmentReviewUI):
    supported_mimetypes = ['image/jpg']

    def __init__(self, review_request, obj):
        raise Exception


class SandboxReviewUI(FileAttachmentReviewUI):
    supported_mimetypes = ['image/png']

    def is_enabled_for(self, user=None, review_request=None,
                       file_attachment=None, **kwargs):
        raise Exception

    def get_comment_thumbnail(self, comment):
        raise Exception

    def get_comment_link_url(self, comment):
        raise Exception

    def get_comment_link_text(self, comment):
        raise Exception

    def get_extra_context(self, request):
        raise Exception

    def get_js_view_data(self):
        raise Exception


class ConflictFreeReviewUI(FileAttachmentReviewUI):
    supported_mimetypes = ['image/gif']

    def serialize_comment(self, comment):
        raise Exception

    def get_js_model_data(self):
        raise Exception


class SandboxTests(SpyAgency, TestCase):
    """Testing sandboxing extensions."""
    fixtures = ['test_users']

    def setUp(self):
        super(SandboxTests, self).setUp()

        register_ui(InitReviewUI)
        register_ui(SandboxReviewUI)
        register_ui(ConflictFreeReviewUI)

        self.factory = RequestFactory()

        self.user = User.objects.get(username='doc')
        self.review_request = self.create_review_request()

        self.png_file = self.create_file_attachment(self.review_request)
        self.png_file.mimetype = 'image/png'

        self.jpg_file = self.create_file_attachment(self.review_request)
        self.jpg_file.mimetype = 'image/jpg'

        self.gif_file = self.create_file_attachment(self.review_request)
        self.gif_file.mimetype = 'image/gif'

    def tearDown(self):
        super(SandboxTests, self).tearDown()

        unregister_ui(InitReviewUI)
        unregister_ui(SandboxReviewUI)
        unregister_ui(ConflictFreeReviewUI)

    def test_init_review_ui(self):
        """Testing FileAttachmentReviewUI sandboxes __init__"""
        self.spy_on(InitReviewUI.__init__)

        self.jpg_file.review_ui

        self.assertTrue(InitReviewUI.__init__.called)

    def test_is_enabled_for(self):
        """Testing FileAttachmentReviewUI sandboxes is_enabled_for"""
        review_ui = self.png_file.review_ui
        self.spy_on(review_ui.is_enabled_for)

        self.assertFalse(has_usable_review_ui(self.user,
                                              self.review_request,
                                              self.png_file))
        self.assertTrue(review_ui.is_enabled_for.called)

    def test_get_comment_thumbnail(self):
        """Testing FileAttachmentReviewUI sandboxes get_comment_thumbnail"""
        comment = "Comment"

        review = self.create_review(self.review_request, user=self.user)
        file_attachment_comment = review.file_attachment_comments.create(
            file_attachment=self.png_file, text=comment)

        review_ui = file_attachment_comment.review_ui
        self.spy_on(review_ui.get_comment_thumbnail)

        file_attachment_comment.thumbnail

        self.assertTrue(review_ui.get_comment_thumbnail.called)

    def test_get_comment_link_url(self):
        """Testing FileAttachmentReviewUI sandboxes get_comment_link_url"""
        comment = "Comment"

        review = self.create_review(self.review_request, user=self.user)
        file_attachment_comment = review.file_attachment_comments.create(
            file_attachment=self.png_file, text=comment)

        review_ui = file_attachment_comment.review_ui
        self.spy_on(review_ui.get_comment_link_url)

        file_attachment_comment.get_absolute_url()

        self.assertTrue(review_ui.get_comment_link_url.called)

    def test_get_comment_link_text(self):
        """Testing FileAttachmentReviewUI sandboxes get_comment_link_text"""
        comment = "Comment"

        review = self.create_review(self.review_request, user=self.user)
        file_attachment_comment = review.file_attachment_comments.create(
            file_attachment=self.png_file, text=comment)

        review_ui = file_attachment_comment.review_ui
        self.spy_on(review_ui.get_comment_link_text)

        file_attachment_comment.get_link_text()

        self.assertTrue(review_ui.get_comment_link_text.called)

    def test_get_extra_context(self):
        """Testing FileAttachmentReviewUI sandboxes get_extra_context"""
        review_ui = self.png_file.review_ui
        request = self.factory.get('test')
        request.user = self.user

        self.spy_on(review_ui.get_extra_context)

        review_ui.render_to_string(request=request)

        self.assertTrue(review_ui.get_extra_context.called)

    def test_get_js_model_data(self):
        """Testing FileAttachmentReviewUI sandboxes get_js_model_data"""
        review_ui = self.gif_file.review_ui
        request = self.factory.get('test')
        request.user = self.user

        self.spy_on(review_ui.get_js_model_data)

        review_ui.render_to_response(request=request)

        self.assertTrue(review_ui.get_js_model_data.called)

    def test_get_js_view_data(self):
        """Testing FileAttachmentReviewUI sandboxes get_js_view_data"""
        review_ui = self.png_file.review_ui
        request = self.factory.get('test')
        request.user = self.user

        self.spy_on(review_ui.get_js_view_data)

        review_ui.render_to_response(request=request)

        self.assertTrue(review_ui.get_js_view_data.called)

    def test_serialize_comments(self):
        """Testing FileAttachmentReviewUI sandboxes serialize_comments"""
        review_ui = self.gif_file.review_ui

        self.spy_on(review_ui.serialize_comments)

        review_ui.get_comments_json()

        self.assertTrue(review_ui.serialize_comments.called)

    def test_serialize_comment(self):
        """Testing FileAttachmentReviewUI sandboxes serialize_comment"""
        comment = 'comment'

        review_ui = self.gif_file.review_ui
        request = self.factory.get('test')
        request.user = self.user
        review_ui.request = request

        review = self.create_review(self.review_request, user=self.user)
        file_attachment_comment = review.file_attachment_comments.create(
            file_attachment=self.gif_file, text=comment)

        self.spy_on(review_ui.serialize_comment)

        serial_comments = review_ui.serialize_comments(
            comments=[file_attachment_comment])
        self.assertEqual(len(serial_comments), 0)

        self.assertTrue(review_ui.serialize_comment.called)


class ImageReviewUITests(TestCase):
    """Tests for the ImageReviewUI."""

    fixtures = ['test_users']

    def setUp(self):
        self.review_request = self.create_review_request()
        self.attachment = self.create_file_attachment(
            self.review_request)
        self.review = self.create_review(self.review_request)

    def test_get_comment_thumbnail(self):
        """Testing ImageReviewUI.get_comment_thumbnail for an image comment"""
        ui = ImageReviewUI(self.review_request, self.attachment)
        comment = self.create_file_attachment_comment(
            self.review,
            self.attachment,
            extra_fields={
                'x': 0,
                'y': 0,
                'width': 1,
                'height': 1,
            })
        thumbnail = ui.get_comment_thumbnail(comment)

        self.assertEqual(
            thumbnail,
            '<img class="modified-image" src="%s" width="1" height="1"'
            ' alt="%s" />'
            % (build_server_url(crop_image(self.attachment.file, 0, 0, 1, 1)),
               comment.text)
        )

    def test_get_comment_thumbnail_diff(self):
        """Testing ImageReviewUI.get_comment_thumbnail for an image diff
        comment
        """
        diff_attachment = self.create_file_attachment(self.review_request)

        ui = ImageReviewUI(self.review_request, self.attachment)
        ui.set_diff_against(diff_attachment)

        comment = self.create_file_attachment_comment(
            self.review,
            self.attachment,
            diff_attachment,
            extra_fields={
                'x': 0,
                'y': 0,
                'width': 1,
                'height': 1,
            })
        thumbnail = ui.get_comment_thumbnail(comment)

        self.assertEqual(
            thumbnail,
            '<div class="image-review-ui-diff-thumbnail">'
            '<img class="orig-image" src="%s" width="1" height="1" alt="%s" />'
            '<img class="modified-image" src="%s" width="1" height="1"'
            ' alt="%s" />'
            '</div>'
            % (build_server_url(crop_image(diff_attachment.file, 0, 0, 1, 1)),
               comment.text,
               build_server_url(crop_image(self.attachment.file, 0, 0, 1, 1)),
               comment.text)
        )
