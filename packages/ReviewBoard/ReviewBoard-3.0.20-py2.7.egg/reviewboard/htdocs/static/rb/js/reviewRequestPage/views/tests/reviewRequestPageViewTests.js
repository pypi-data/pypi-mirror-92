'use strict';

suite('rb/reviewRequestPage/views/ReviewRequestPageView', function () {
    var template = '<div id="review-banner"></div>\n<a id="collapse-all"></a>\n<a id="expand-all"></a>\n<div>\n <div class="review review-request-page-entry" id="review123">\n  <div class="review-request-page-entry-contents">\n   <div class="body">\n    <pre class="body_top">Body Top</pre>\n    <div class="comment-section" data-context-type="body_top">\n    </div>\n    <div class="comment-section" data-context-id="123"\n         data-context-type="diff_comments">\n    </div>\n    <pre class="body_bottom">Body Bottom</pre>\n    <div class="comment-section" data-context-type="body_bottom">\n    </div>\n   </div>\n </div>\n <div class="review review-request-page-entry" id="review124">\n  <div class="review-request-page-entry-contents">\n   <div class="body">\n    <pre class="body_top">Body Top</pre>\n    <div class="comment-section" data-context-type="body_top">\n    </div>\n    <pre class="body_bottom">Body Bottom</pre>\n    <div class="comment-section" data-context-type="body_bottom">\n    </div>\n   </div>\n  </div>\n </div>\n</div>';

    var page = void 0;
    var pageView = void 0;
    var entry1 = void 0;
    var entry2 = void 0;

    beforeEach(function () {
        var $el = $('<div/>').html(template).appendTo($testsScratch);

        RB.DnDUploader.instance = null;

        page = new RB.ReviewRequestPage.ReviewRequestPage({
            checkForUpdates: false,
            reviewRequestData: {},
            editorData: {
                fileAttachments: [],
                mutableByUser: true,
                showSendEmail: false
            }
        }, {
            parse: true
        });

        pageView = new RB.ReviewRequestPage.ReviewRequestPageView({
            el: $el,
            model: page
        });

        // Stub this out.
        spyOn(RB.ReviewRequestPage.IssueSummaryTableView.prototype, 'render');

        var reviewRequest = page.get('reviewRequest');

        pageView.addEntryView(new RB.ReviewRequestPage.ReviewEntryView({
            model: new RB.ReviewRequestPage.ReviewEntry({
                review: reviewRequest.createReview(123, {
                    shipIt: true,
                    public: true,
                    bodyTop: 'Body Top',
                    bodyBottom: 'Body Bottom'
                }),
                reviewRequestEditor: pageView.reviewRequestEditor
            }),
            el: $el.find('#review123')
        }));

        pageView.addEntryView(new RB.ReviewRequestPage.ReviewEntryView({
            model: new RB.ReviewRequestPage.ReviewEntry({
                review: reviewRequest.createReview(124, {
                    shipIt: false,
                    public: true,
                    bodyTop: 'Body Top',
                    bodyBottom: 'Body Bottom'
                }),
                reviewRequestEditor: pageView.reviewRequestEditor
            }),
            el: $el.find('#review124')
        }));

        pageView.render();

        expect(pageView._entryViews.length).toBe(2);
        entry1 = pageView._entryViews[0];
        entry2 = pageView._entryViews[1];
    });

    afterEach(function () {
        RB.DnDUploader.instance = null;
    });

    describe('Actions', function () {
        it('Collapse all', function () {
            var $el1 = entry1.$el.find('.review-request-page-entry-contents');
            var $el2 = entry2.$el.find('.review-request-page-entry-contents');

            expect($el1.hasClass('collapsed')).toBe(false);
            expect($el2.hasClass('collapsed')).toBe(false);

            pageView.$('#collapse-all').click();

            expect($el1.hasClass('collapsed')).toBe(true);
            expect($el2.hasClass('collapsed')).toBe(true);
        });

        it('Expand all', function () {
            var $el1 = entry1.$el.find('.review-request-page-entry-contents');
            var $el2 = entry2.$el.find('.review-request-page-entry-contents');

            $el1.addClass('collapsed');
            $el2.addClass('collapsed');

            pageView.$('#expand-all').click();

            expect($el1.hasClass('collapsed')).toBe(false);
            expect($el2.hasClass('collapsed')).toBe(false);
        });
    });

    describe('Methods', function () {
        describe('openCommentEditor', function () {
            beforeEach(function () {
                spyOn(RB.ReviewRequestPage.ReviewReplyEditorView.prototype, 'openCommentEditor');
                spyOn(entry1, 'getReviewReplyEditorView').and.callThrough();
                spyOn(entry2, 'getReviewReplyEditorView').and.callThrough();
            });

            it('With body_top', function () {
                pageView.openCommentEditor('body_top');

                expect(entry1.getReviewReplyEditorView).toHaveBeenCalled();
                expect(RB.ReviewRequestPage.ReviewReplyEditorView.prototype.openCommentEditor).toHaveBeenCalled();

                /* We should have matched the first one. */
                expect(entry2.getReviewReplyEditorView).not.toHaveBeenCalled();
            });

            it('With body_bottom', function () {
                pageView.openCommentEditor('body_bottom');

                expect(entry1.getReviewReplyEditorView).toHaveBeenCalled();
                expect(RB.ReviewRequestPage.ReviewReplyEditorView.prototype.openCommentEditor).toHaveBeenCalled();

                /* We should have matched the first one. */
                expect(entry2.getReviewReplyEditorView).not.toHaveBeenCalled();
            });

            it('With comments', function () {
                pageView.openCommentEditor('diff_comments', 123);

                expect(entry1.getReviewReplyEditorView).toHaveBeenCalled();
                expect(RB.ReviewRequestPage.ReviewReplyEditorView.prototype.openCommentEditor).toHaveBeenCalled();

                /* We should have matched the first one. */
                expect(entry2.getReviewReplyEditorView).not.toHaveBeenCalled();
            });
        });
    });
});

//# sourceMappingURL=reviewRequestPageViewTests.js.map