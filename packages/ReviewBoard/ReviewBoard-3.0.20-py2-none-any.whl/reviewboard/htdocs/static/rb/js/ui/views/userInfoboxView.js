'use strict';

/**
 * An infobox for displaying information on users.
 */
RB.UserInfoboxView = RB.BaseInfoboxView.extend({
    infoboxID: 'user-infobox',

    /**
     * Render the infobox.
     */
    render: function render() {
        RB.BaseInfoboxView.prototype.render.call(this);

        var $localTime = this.$('.localtime').children('time');

        if ($localTime.length > 0) {
            var timezone = $localTime.data('timezone');
            var now = moment.tz(timezone);

            $localTime.text(now.format('LT'));
        }

        this.$('.timesince').timesince();

        return this;
    }
});

$.fn.user_infobox = RB.InfoboxManagerView.createJQueryFn(RB.UserInfoboxView);

//# sourceMappingURL=userInfoboxView.js.map