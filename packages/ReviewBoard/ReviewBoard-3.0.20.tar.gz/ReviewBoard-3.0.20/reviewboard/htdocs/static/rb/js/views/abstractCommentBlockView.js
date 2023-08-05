'use strict';

RB.AbstractCommentBlockView = Backbone.View.extend({
    events: {
        'click': '_onClicked'
    },

    tooltipSides: 'lrbt',

    /**
     * Dispose the comment block.
     *
     * This will remove the view and the tooltip.
     */
    dispose: function dispose() {
        this.trigger('removing');
        this.remove();
        this._$tooltip.remove();
    },


    /**
     * Render the comment block.
     *
     * Along with the block, a floating tooltip will be created that
     * displays summaries of the comments.
     *
     * Returns:
     *     RB.AbstractCommentBlockView:
     *     This object, for chaining.
     */
    render: function render() {
        this._$tooltip = $.tooltip(this.$el, { side: this.tooltipSides }).addClass('comments');

        this.renderContent();

        this.model.on('change:draftComment', this._onDraftCommentChanged, this);
        this._onDraftCommentChanged();

        this._updateTooltip();

        return this;
    },


    /**
     * Hide the tooltip from the page.
     *
     * This will force the tooltip to hide, preventing it from interfering
     * with operations such as moving a comment block.
     *
     * It will automatically show again the next time there is a mouse enter
     * event.
     */
    hideTooltip: function hideTooltip() {
        this._$tooltip.hide();
    },


    /**
     * Position the comment dlg to the right side of comment block.
     *
     * This can be overridden to change where the comment dialog will
     * be displayed.
     *
     * Args:
     *     commntDlg (RB.CommentDialogView):
     *          The view for the comment dialog.
     */
    positionCommentDlg: function positionCommentDlg(commentDlg) {
        commentDlg.positionBeside(this.$el, {
            side: 'r',
            fitOnScreen: true
        });
    },


    /**
     * Position the notification bubble around the comment block.
     *
     * This can be overridden to change where the bubble will be displayed.
     * By default, it is centered over the block.
     *
     * Args:
     *     $bubble (jQuery):
     *         The selector for the notification bubble.
     */
    positionNotifyBubble: function positionNotifyBubble($bubble) {
        $bubble.move(Math.round((this.$el.width() - $bubble.width()) / 2), Math.round((this.$el.height() - $bubble.height()) / 2));
    },


    /**
     * Notify the user of some update.
     *
     * This notification appears in the comment area.
     *
     * Args:
     *     text (string):
     *         The text to show in the notification.
     *
     *     cb (function, optional):
     *         A callback function to call once the notification has been
     *         removed.
     *
     *     context (object):
     *         Context to bind when calling the ``cb`` callback function.
     */
    notify: function notify(text, cb, context) {
        var $bubble = $('<div class="bubble">').css('opacity', 0).appendTo(this.$el).text(text);

        this.positionNotifyBubble($bubble);

        $bubble.animate({
            top: '-=10px',
            opacity: 0.8
        }, 350, 'swing').delay(1200).animate({
            top: '+=10px',
            opacity: 0
        }, 350, 'swing', function () {
            $bubble.remove();

            if (_.isFunction(cb)) {
                cb.call(context);
            }
        });
    },


    /**
     * Update the tooltip contents.
     *
     * The contents will show the summary of each comment, including
     * the draft comment, if any.
     */
    _updateTooltip: function _updateTooltip() {
        var $list = $('<ul/>');
        var draftComment = this.model.get('draftComment');
        var tooltipTemplate = _.template('<li>\n <div class="reviewer">\n  <%- user %>:\n </div>\n <pre class="rich-text"><%= html %></pre>\n</li>');

        if (draftComment) {
            $(tooltipTemplate({
                user: RB.UserSession.instance.get('fullName'),
                html: draftComment.get('html')
            })).addClass('draft').appendTo($list);
        }

        this.model.get('serializedComments').forEach(function (comment) {
            $(tooltipTemplate({
                user: comment.user.name,
                html: comment.html
            })).appendTo($list);
        });

        this._$tooltip.empty().append($list);
    },


    /**
     * Handle changes to the model's draftComment property.
     *
     * If there's a new draft comment, we'll begin listening for updates
     * on it in order to update the tooltip or display notification bubbles.
     *
     * The comment block's style will reflect whether or not we have a
     * draft comment.
     *
     * If the draft comment is deleted, and there are no other comments,
     * the view will be removed.
     */
    _onDraftCommentChanged: function _onDraftCommentChanged() {
        var _this = this;

        var comment = this.model.get('draftComment');

        if (!comment) {
            this.$el.removeClass('draft');
            return;
        }

        comment.on('change:text', this._updateTooltip, this);

        comment.on('destroy', function () {
            _this.notify(gettext('Comment Deleted'), function () {
                // Discard the comment block if empty.
                if (_this.model.isEmpty()) {
                    _this.$el.fadeOut(350, function () {
                        return _this.dispose();
                    });
                } else {
                    _this.$el.removeClass('draft');
                    _this._updateTooltip();
                }
            });
        });

        comment.on('saved', function (options) {
            _this._updateTooltip();

            if (!options.boundsUpdated) {
                _this.notify(gettext('Comment Saved'));
            }

            RB.DraftReviewBannerView.instance.show();
        });

        this.$el.addClass('draft');
    },


    /**
     * Handle the comment block being clicked.
     *
     * Emits the 'clicked' signal so that parent views can process it.
     */
    _onClicked: function _onClicked() {
        this.trigger('clicked');
    }
});

//# sourceMappingURL=abstractCommentBlockView.js.map