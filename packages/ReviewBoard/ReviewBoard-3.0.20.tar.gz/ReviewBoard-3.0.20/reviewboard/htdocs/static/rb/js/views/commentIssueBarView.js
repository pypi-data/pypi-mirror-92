'use strict';

/**
 * Manages a comment's issue status bar.
 *
 * The buttons on the bar will update the comment's issue status on the server
 * when clicked. The bar will update to reflect the issue status of any
 * comments tracked by the issue summary table.
 */
RB.CommentIssueBarView = Backbone.View.extend({
    events: {
        'click .reopen': '_onReopenClicked',
        'click .resolve': '_onFixedClicked',
        'click .drop': '_onDropClicked',
        'click .verify-dropped': '_onVerifyDroppedClicked',
        'click .verify-resolved': '_onVerifyFixedClicked'
    },

    statusInfo: {
        open: {
            visibleButtons: ['.drop', '.resolve'],
            text: gettext('An issue was opened.')
        },
        resolved: {
            visibleButtons: ['.reopen'],
            text: gettext('The issue has been resolved.')
        },
        dropped: {
            visibleButtons: ['.reopen'],
            text: gettext('The issue has been dropped.')
        },
        'verifying-dropped': {
            visibleButtons: ['.reopen'],
            text: gettext('Waiting for verification before dropping...')
        },
        'verifying-resolved': {
            visibleButtons: ['.reopen'],
            text: gettext('Waiting for verification before resolving...')
        }
    },

    template: _.template('<div class="issue-state">\n <div class="issue-container">\n  <span class="rb-icon"></span>\n  <span class="issue-details">\n   <span class="issue-message"></span>\n   <% if (interactive) { %>\n    <span class="issue-actions">\n     <input type="button" class="issue-button resolve"\n            value="<%- fixedLabel %>">\n     <input type="button" class="issue-button drop"\n            value="<%- dropLabel %>">\n     <input type="button" class="issue-button reopen"\n            value="<%- reopenLabel %>">\n     <input type="button" class="issue-button verify-resolved"\n            value="<%- verifyFixedLabel %>">\n     <input type="button" class="issue-button verify-dropped"\n            value="<%- verifyDroppedLabel %>">\n    </span>\n   <% } %>\n  </span>\n </div>\n</div>'),

    /**
     * Initialize the view.
     */
    initialize: function initialize() {
        var page = RB.PageManager.getPage();

        this._manager = this.options.commentIssueManager || page.model.commentIssueManager;
        this._issueStatus = this.options.issueStatus;
        this._$buttons = null;
        this._$state = null;
        this._$icon = null;
        this._$message = null;
    },


    /**
     * Render the issue status bar.
     *
     * Returns:
     *     RB.CommentIssueBarView:
     *     This object, for chaining.
     */
    render: function render() {
        if (this.$el.children().length === 0) {
            this.$el.append(this.template({
                interactive: this.options.interactive,
                fixedLabel: gettext('Fixed'),
                dropLabel: gettext('Drop'),
                reopenLabel: gettext('Re-open'),
                verifyDroppedLabel: gettext('Verify Dropped'),
                verifyFixedLabel: gettext('Verify Fixed')
            }));
        }

        this._$buttons = this.$('.issue-button');
        this._$state = this.$('.issue-state');
        this._$icon = this.$('.rb-icon');
        this._$message = this.$('.issue-message');

        this._manager.on('issueStatusUpdated', this._onIssueStatusUpdated, this);
        this._showStatus(this._issueStatus);

        return this;
    },


    /**
     * Set the issue status of the comment on the server.
     *
     * Args:
     *     issueStatus (string):
     *         The new issue status (one of ``open``, ``resolved``, or
     *         ``dropped``).
     */
    _setStatus: function _setStatus(issueStatus) {
        this._$buttons.prop('disabled', true);
        this._manager.setCommentState(this.options.reviewID, this.options.commentID, this.options.commentType, issueStatus);
    },


    /**
     * Show the current issue status of the comment.
     *
     * This will affect the button visibility and the text of the bar.
     *
     * Args:
     *     issueStatus (string):
     *         The issue status to show (one of ``open``, ``resolved``, or
     *         ``dropped``).
     */
    _showStatus: function _showStatus(issueStatus) {
        var statusInfo = this.statusInfo[issueStatus];
        var prevStatus = this._issueStatus;

        this._issueStatus = issueStatus;

        this._$state.removeClass(prevStatus).addClass(issueStatus);

        var iconClass = void 0;

        if (issueStatus === RB.BaseComment.STATE_VERIFYING_DROPPED || issueStatus === RB.BaseComment.STATE_VERIFYING_RESOLVED) {
            iconClass = 'rb-icon rb-icon-issue-verifying';
        } else {
            iconClass = 'rb-icon rb-icon-issue-' + issueStatus;
        }

        this._$icon.attr('class', iconClass);
        this._$buttons.hide();
        this._$message.text(statusInfo.text);

        if (this.options.interactive) {
            var visibleButtons = statusInfo.visibleButtons;

            if (this.options.canVerify) {
                if (issueStatus === RB.BaseComment.STATE_VERIFYING_DROPPED) {
                    visibleButtons.push('.verify-dropped');
                } else if (issueStatus === RB.BaseComment.STATE_VERIFYING_RESOLVED) {
                    visibleButtons.push('.verify-resolved');
                }
            }

            this._$buttons.filter(visibleButtons.join(',')).show();
            this._$buttons.prop('disabled', false);
        }

        this.trigger('statusChanged', prevStatus, issueStatus);
    },


    /**
     * Handler for when "Re-open" is clicked.
     *
     * Reopens the issue.
     */
    _onReopenClicked: function _onReopenClicked() {
        this._setStatus(RB.BaseComment.STATE_OPEN);
    },


    /**
     * Handler for when "Fixed" is clicked.
     *
     * Marks the issue as fixed.
     */
    _onFixedClicked: function _onFixedClicked() {
        var _this = this;

        var comment = this._manager.getComment(this.options.reviewID, this.options.commentID, this.options.commentType);

        comment.ready({
            ready: function ready() {
                if (comment.requiresVerification() && comment.getAuthorUsername() !== RB.UserSession.instance.get('username')) {
                    _this._setStatus(RB.BaseComment.STATE_VERIFYING_RESOLVED);
                } else {
                    _this._setStatus(RB.BaseComment.STATE_RESOLVED);
                }
            }
        });
    },


    /**
     * Handler for when "Drop" is clicked.
     *
     * Marks the issue as dropped.
     */
    _onDropClicked: function _onDropClicked() {
        var _this2 = this;

        var comment = this._manager.getComment(this.options.reviewID, this.options.commentID, this.options.commentType);

        comment.ready({
            ready: function ready() {
                if (comment.requiresVerification() && comment.getAuthorUsername() !== RB.UserSession.instance.get('username')) {
                    _this2._setStatus(RB.BaseComment.STATE_VERIFYING_DROPPED);
                } else {
                    _this2._setStatus(RB.BaseComment.STATE_DROPPED);
                }
            }
        });
    },


    /**
     * Handler for when "Verify Fixed" is clicked.
     */
    _onVerifyFixedClicked: function _onVerifyFixedClicked() {
        this._setStatus(RB.BaseComment.STATE_RESOLVED);
    },


    /**
     * Handler for when "Verify Dropped" is clicked.
     */
    _onVerifyDroppedClicked: function _onVerifyDroppedClicked() {
        this._setStatus(RB.BaseComment.STATE_DROPPED);
    },


    /**
     * Handler for when the issue status for the comment changes.
     *
     * Updates the dispaly to reflect the issue's current status.
     *
     * Args:
     *     comment (RB.BaseComment):
     *         The comment model which was updated.
     */
    _onIssueStatusUpdated: function _onIssueStatusUpdated(comment) {
        if (comment.id === this.options.commentID) {
            this._showStatus(comment.get('issueStatus'));
        }
    }
});

//# sourceMappingURL=commentIssueBarView.js.map