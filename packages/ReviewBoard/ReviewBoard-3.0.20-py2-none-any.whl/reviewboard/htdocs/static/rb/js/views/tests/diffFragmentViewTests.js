'use strict';

suite('rb/views/DiffFragmentView', function () {
    var fragmentTemplate = _.template('<table>\n <thead>\n </thead>\n <tbody class="diff-header diff-header-above">\n  <tr>\n   <td>\n    <div>\n     <a href="#" class="diff-expand-btn"\n        data-lines-of-context="20,0"></a>\n    </div>\n   </td>\n  </tr>\n </tbody>\n <tbody class="insert"></tbody>\n <tbody class="insert">\n  <tr>\n   <td>\n    <div class="diff-collapse-btn" data-lines-of-context="0,0"></div>\n   </td>\n  </tr>\n </tbody>\n <tbody class="diff-header diff-header-below">\n  <tr>\n   <td>\n    <div>\n     <a href="#" class="diff-expand-btn"\n        data-lines-of-context="0,20"></a>\n    </div>\n   </td>\n  </tr>\n </tbody>\n</table>');

    var view = void 0;
    var loadDiff = void 0;

    beforeEach(function () {
        loadDiff = jasmine.createSpy('loadDiff');

        view = new RB.DiffFragmentView({
            loadDiff: loadDiff,
            collapsible: true
        });
        view.$el.html(fragmentTemplate());
        $testsScratch.append(view.$el);

        /* Make all the deferred/delayed functions run immediately. */
        spyOn(_, 'defer').and.callFake(function (cb) {
            return cb();
        });
        spyOn(_, 'delay').and.callFake(function (cb) {
            return cb();
        });
    });

    describe('render', function () {
        it('With visible and collapsible === true', function () {
            view.render();

            expect(view.$el.hasClass('allow-transitions')).toBe(true);
            expect(view._$table.hasClass('expanded')).toBe(false);
            expect(view._$table.hasClass('collapsed')).toBe(true);

            /*
             * Ideally we'd check for the proper transform values we're setting
             * (or part of them anyway), but browsers may turn those into
             * "matrix(...)" values. So this is better than nothing.
             */
            expect(view._$thead.css('transform')).not.toBe('none');

            _.each(view._$diffHeaders, function (headerEl) {
                expect($(headerEl).css('transform')).not.toBe('none');
            });
        });

        it('With hidden and collapsible === true', function () {
            view.$el.hide();
            view.render();

            expect(view.$el.hasClass('allow-transitions')).toBe(true);
            expect(view._$table.hasClass('expanded')).toBe(true);
            expect(view._$table.hasClass('collapsed')).toBe(false);

            /*
             * Ideally we'd check for the proper transform values we're setting
             * (or part of them anyway), but browsers may turn those into
             * "matrix(...)" values. So this is better than nothing.
             */
            expect(view._$thead.css('transform')).toBe('none');

            _.each(view._$diffHeaders, function (headerEl) {
                expect($(headerEl).css('transform')).toBe('none');
            });
        });

        it('With collapsible === false', function () {
            view._collapsible = false;
            view.render();

            expect(view.$el.hasClass('allow-transitions')).toBe(false);
            expect(view._$table.hasClass('expanded')).toBe(true);
            expect(view._$table.hasClass('collapsed')).toBe(false);

            /*
             * Ideally we'd check for the proper transform values we're setting
             * (or part of them anyway), but browsers may turn those into
             * "matrix(...)" values. So this is better than nothing.
             */
            expect(view._$thead.css('transform')).toBe('none');

            _.each(view._$diffHeaders, function (headerEl) {
                expect($(headerEl).css('transform')).toBe('none');
            });
        });
    });

    describe('Events', function () {
        it('click expansion button', function () {
            view.render();
            view.$('.diff-expand-btn').eq(0).click();

            expect(loadDiff).toHaveBeenCalled();
            expect(loadDiff.calls.mostRecent().args[0].linesOfContext).toBe('20,0');
        });

        it('click collapse button', function () {
            view.render();
            view.$('.diff-collapse-btn').eq(0).click();

            expect(loadDiff).toHaveBeenCalled();
            expect(loadDiff.calls.mostRecent().args[0].linesOfContext).toBe('0,0');
        });

        describe('mouseenter', function () {
            it('With collapsible === true', function () {
                view.render();

                spyOn(view.$el, 'is').and.callFake(function (sel) {
                    expect(sel).toBe(':hover');

                    return true;
                });
                view.$el.trigger('mouseenter');

                expect(view._$table.hasClass('collapsed')).toBe(false);
                expect(view._$table.hasClass('expanded')).toBe(true);
                expect(view._$thead.css('transform')).toBe('none');

                _.each(view._$diffHeaders, function (headerEl) {
                    expect($(headerEl).css('transform')).toBe('none');
                });
            });

            it('With collapsible === false', function () {
                view._collapsible = false;
                view.render();

                spyOn(view.$el, 'is').and.callFake(function (sel) {
                    expect(sel).toBe(':hover');

                    return true;
                });
                view.$el.trigger('mouseenter');

                expect(view._$table.hasClass('collapsed')).toBe(false);
                expect(view._$table.hasClass('expanded')).toBe(true);
                expect(view._$thead.css('transform')).toBe('none');

                _.each(view._$diffHeaders, function (headerEl) {
                    expect($(headerEl).css('transform')).toBe('none');
                });
            });
        });

        describe('mouseleave', function () {
            it('With collapsible === true', function () {
                var isHovering = true;

                view.render();

                /* First, trigger a mouseenter. */
                spyOn(view.$el, 'is').and.callFake(function (sel) {
                    expect(sel).toBe(':hover');

                    return isHovering;
                });
                view.$el.trigger('mouseenter');

                /* Now the mouse leave. */
                isHovering = false;
                view.$el.trigger('mouseleave');

                expect(view._$table.hasClass('collapsed')).toBe(true);
                expect(view._$table.hasClass('expanded')).toBe(false);
                expect(view._$thead.css('transform')).not.toBe('none');

                _.each(view._$diffHeaders, function (headerEl) {
                    expect($(headerEl).css('transform')).not.toBe('none');
                });
            });

            it('With collapsible === false', function () {
                var isHovering = true;

                view._collapsible = false;
                view.render();

                /* First, trigger a mouseenter. */
                spyOn(view.$el, 'is').and.callFake(function (sel) {
                    expect(sel).toBe(':hover');

                    return isHovering;
                });
                view.$el.trigger('mouseenter');

                /* Now the mouse leave. */
                isHovering = false;
                view.$el.trigger('mouseleave');

                expect(view._$table.hasClass('collapsed')).toBe(false);
                expect(view._$table.hasClass('expanded')).toBe(true);
                expect(view._$thead.css('transform')).toBe('none');

                _.each(view._$diffHeaders, function (headerEl) {
                    expect($(headerEl).css('transform')).toBe('none');
                });
            });
        });
    });
});

//# sourceMappingURL=diffFragmentViewTests.js.map