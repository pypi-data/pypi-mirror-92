'use strict';

(function () {

    var optionTemplate = _.template('<div>\n<% if (useAvatars && avatarHTML) { %>\n <%= avatarHTML %>\n<% } %>\n<% if (fullname) { %>\n <span class="title"><%- fullname %></span>\n <span class="description">(<%- username %>)</span>\n<% } else { %>\n <span class="title"><%- username %></span>\n<% } %>\n</div>');

    /**
     * A widget to select related users using search and autocomplete.
     */
    RB.RelatedUserSelectorView = RB.RelatedObjectSelectorView.extend({
        searchPlaceholderText: gettext('Search for users...'),

        /**
         * Initialize the view.
         *
         * Args:
         *     options (object):
         *         Options for the view.
         *
         * Option Args:
         *     localSitePrefix (string):
         *         The URL prefix for the local site, if any.
         *
         *     multivalued (boolean):
         *         Whether or not the widget should allow selecting multuple
         *         values.
         *
         *     useAvatars (boolean):
         *         Whether to show avatars. Off by default.
         */
        initialize: function initialize(options) {
            RB.RelatedObjectSelectorView.prototype.initialize.call(this, _.defaults({
                selectizeOptions: {
                    searchField: ['fullname', 'username'],
                    sortField: [{ field: 'fullname' }, { field: 'username' }],
                    valueField: 'username'
                }
            }, options));

            this._localSitePrefix = options.localSitePrefix || '';
            this._useAvatars = !!options.useAvatars;
        },


        /**
         * Render an option in the drop-down menu.
         *
         * Args:
         *     item (object):
         *         The item to render.
         *
         * Returns:
         *     string:
         *     HTML to insert into the drop-down menu.
         */
        renderOption: function renderOption(item) {
            return optionTemplate(_.extend({ useAvatars: this._useAvatars }, item));
        },


        /**
         * Load options from the server.
         *
         * Args:
         *     query (string):
         *         The string typed in by the user.
         *
         *     callback (function):
         *         A callback to be called once data has been loaded. This should
         *         be passed an array of objects, each representing an option in
         *         the drop-down.
         */
        loadOptions: function loadOptions(query, callback) {
            var params = {
                fullname: 1,
                'only-fields': 'avatar_html,fullname,id,username',
                'only-links': '',
                'render-avatars-at': '20'
            };

            if (query.length !== 0) {
                params.q = query;
            }

            $.ajax({
                type: 'GET',
                url: '' + SITE_ROOT + this._localSitePrefix + 'api/users/',
                data: params,
                success: function success(results) {
                    callback(results.users.map(function (u) {
                        return {
                            avatarHTML: u.avatar_html[20],
                            fullname: u.fullname,
                            id: u.id,
                            username: u.username
                        };
                    }));
                },
                error: function error() {
                    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
                        args[_key] = arguments[_key];
                    }

                    console.log('User query failed', args);
                    callback();
                }
            });
        }
    });
})();

//# sourceMappingURL=relatedUserSelectorView.js.map