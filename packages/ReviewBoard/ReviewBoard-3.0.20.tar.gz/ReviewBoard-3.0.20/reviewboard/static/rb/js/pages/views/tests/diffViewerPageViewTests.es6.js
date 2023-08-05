suite('rb/pages/views/DiffViewerPageView', function() {
    const tableTemplate = _.template(dedent`
        <div class="diff-container">
         <table class="sidebyside">
          <thead>
           <tr class="filename-row">
            <th colspan="4">
             <a name="<%- fileID %>" class="file-anchor"></a>
            </th>
           </tr>
          </thead>
          <% _.each(chunks, function(chunk) { %>
           <tbody class="<%- chunk.type %>">
            <% _.each(chunk.lines, function(line, i) { %>
             <tr line="<%- line.vNumber %>">
              <th>
               <% if (i === 0 && chunk.type !== "equal") { %>
                <a name="<%- chunk.id %>" class="chunk-anchor"></a>
               <% } %>
               <%- line.leftNumber || "" %>
              </th>
              <td class="l"></td>
              <th><%- line.rightNumber || "" %></th>
              <td class="r"></td>
             </tr>
            <% }); %>
           </tbody>
          <% }); %>
         </table>
        </div>
    `);

    const pageTemplate = dedent`
        <div>
         <div id="review-banner"></div>
         <div id="diffs"></div>
        </div>
    `;

    let page;
    let pageView;
    let $diffs;

    beforeEach(function() {
        /*
         * Disable the router so that the page doesn't change the URL on the
         * page while tests run.
         */
        spyOn(Backbone.history, 'start');

        page = new RB.DiffViewerPage({
            checkForUpdates: false,
            pagination: {
                current_page: 1,
            },
            reviewRequestData: {
                id: 123,
                loaded: true,
                state: RB.ReviewRequest.PENDING,
            },
            revision: {
                revision: 1,
                interdiff_revision: null,
                is_interdiff: false,
            },
            editorData: {
                mutableByUser: true,
                statusMutableByUser: true,
            },
        }, {
            parse: true,
        });

        pageView = new RB.DiffViewerPageView({
            el: $(pageTemplate).appendTo($testsScratch),
            model: page,
        });

        $diffs = pageView.$el.children('#diffs');

        /* Don't communicate with the server for page updates. */
        spyOn(page.get('reviewRequest'), 'ready').and.callFake(
            (options, context) => options.ready.call(context));
    });

    afterEach(function() {
        RB.DnDUploader.instance = null;
    });

    describe('Anchors', function() {
        it('Tracks all types', function() {
            $diffs.html(tableTemplate({
                fileID: 'file1',
                chunks: [
                    {
                        id: '1.1',
                        lines: [
                            {
                                type: 'insert',
                                vNumber: 100,
                                leftNumber: 100,
                                rightNumber: 101,
                            },
                        ],
                    },
                    {
                        id: '1.2',
                        lines: [
                            {
                                type: 'equal',
                                vNumber: 101,
                                leftNumber: 101,
                                rightNumber: 101,
                            },
                        ],
                    },
                    {
                        id: '1.3',
                        lines: [
                            {
                                type: 'delete',
                                vNumber: 102,
                                leftNumber: 102,
                                rightNumber: 101,
                            },
                        ],
                    },
                ],
            }));

            pageView.render();
            pageView._updateAnchors(pageView.$el.find('table').eq(0));

            expect(pageView._$anchors.length).toBe(4);
            expect(pageView._$anchors[0].name).toBe('file1');
            expect(pageView._$anchors[1].name).toBe('1.1');
            expect(pageView._$anchors[2].name).toBe('1.2');
            expect(pageView._$anchors[3].name).toBe('1.3');
            expect(pageView._selectedAnchorIndex).toBe(0);
        });

        describe('Navigation', function() {
            beforeEach(function() {
                $diffs.html([
                    tableTemplate({
                        fileID: 'file1',
                        chunks: [
                            {
                                id: '1.1',
                                lines: [
                                    {
                                        type: 'insert',
                                        vNumber: 100,
                                        leftNumber: 100,
                                        rightNumber: 101,
                                    },
                                ],
                            },
                            {
                                id: '1.2',
                                lines: [
                                    {
                                        type: 'equal',
                                        vNumber: 101,
                                        leftNumber: 101,
                                        rightNumber: 101,
                                    },
                                ],
                            },
                        ],
                    }),
                    tableTemplate({
                        fileID: 'file2',
                        chunks: [],
                    }),
                    tableTemplate({
                        fileID: 'file3',
                        chunks: [
                            {
                                id: '2.1',
                                lines: [
                                    {
                                        type: 'insert',
                                        vNumber: 100,
                                        leftNumber: 100,
                                        rightNumber: 101,
                                    }
                                ]
                            },
                            {
                                id: '2.2',
                                lines: [
                                    {
                                        type: 'equal',
                                        vNumber: 101,
                                        leftNumber: 101,
                                        rightNumber: 101,
                                    },
                                ],
                            },
                        ],
                    }),
                ]);

                pageView.render();

                pageView.$el.find('table').each(function() {
                    pageView._updateAnchors($(this));
                });
            });

            describe('Previous file', function() {
                it('From file', function() {
                    pageView.selectAnchorByName('file2');
                    expect(pageView._selectedAnchorIndex).toBe(3);

                    pageView._selectPreviousFile();

                    expect(pageView._selectedAnchorIndex).toBe(0);
                });

                it('From chunk', function() {
                    pageView.selectAnchorByName('2.2');
                    expect(pageView._selectedAnchorIndex).toBe(6);

                    pageView._selectPreviousFile();

                    expect(pageView._selectedAnchorIndex).toBe(4);
                });

                it('On first file', function() {
                    pageView.selectAnchorByName('file1');
                    expect(pageView._selectedAnchorIndex).toBe(0);

                    pageView._selectPreviousFile();

                    expect(pageView._selectedAnchorIndex).toBe(0);
                });
            });

            describe('Next file', function() {
                it('From file', function() {
                    pageView.selectAnchorByName('file1');
                    expect(pageView._selectedAnchorIndex).toBe(0);

                    pageView._selectNextFile();

                    expect(pageView._selectedAnchorIndex).toBe(3);
                });

                it('From chunk', function() {
                    pageView.selectAnchorByName('1.1');
                    expect(pageView._selectedAnchorIndex).toBe(1);

                    pageView._selectNextFile();

                    expect(pageView._selectedAnchorIndex).toBe(3);
                });

                it('On last file', function() {
                    pageView.selectAnchorByName('file3');
                    expect(pageView._selectedAnchorIndex).toBe(4);

                    pageView._selectNextFile();

                    expect(pageView._selectedAnchorIndex).toBe(4);
                });
            });

            describe('Previous anchor', function() {
                it('From file to file', function() {
                    pageView.selectAnchorByName('file3');
                    expect(pageView._selectedAnchorIndex).toBe(4);

                    pageView._selectPreviousDiff();

                    expect(pageView._selectedAnchorIndex).toBe(3);
                });

                it('From file to chunk', function() {
                    pageView.selectAnchorByName('file2');
                    expect(pageView._selectedAnchorIndex).toBe(3);

                    pageView._selectPreviousDiff();

                    expect(pageView._selectedAnchorIndex).toBe(2);
                });

                it('From chunk to file', function() {
                    pageView.selectAnchorByName('2.1');
                    expect(pageView._selectedAnchorIndex).toBe(5);

                    pageView._selectPreviousDiff();

                    expect(pageView._selectedAnchorIndex).toBe(4);
                });

                it('From chunk to chunk', function() {
                    pageView.selectAnchorByName('2.2');
                    expect(pageView._selectedAnchorIndex).toBe(6);

                    pageView._selectPreviousDiff();

                    expect(pageView._selectedAnchorIndex).toBe(5);
                });

                it('On first file', function() {
                    pageView.selectAnchorByName('file1');
                    expect(pageView._selectedAnchorIndex).toBe(0);

                    pageView._selectPreviousDiff();

                    expect(pageView._selectedAnchorIndex).toBe(0);
                });
            });

            describe('Next anchor', function() {
                it('From file to file', function() {
                    pageView.selectAnchorByName('file2');
                    expect(pageView._selectedAnchorIndex).toBe(3);

                    pageView._selectNextDiff();

                    expect(pageView._selectedAnchorIndex).toBe(4);
                });

                it('From file to chunk', function() {
                    pageView.selectAnchorByName('file1');
                    expect(pageView._selectedAnchorIndex).toBe(0);

                    pageView._selectNextDiff();

                    expect(pageView._selectedAnchorIndex).toBe(1);
                });

                it('From chunk to file', function() {
                    pageView.selectAnchorByName('1.2');
                    expect(pageView._selectedAnchorIndex).toBe(2);

                    pageView._selectNextDiff();

                    expect(pageView._selectedAnchorIndex).toBe(3);
                });

                it('From chunk to chunk', function() {
                    pageView.selectAnchorByName('2.1');
                    expect(pageView._selectedAnchorIndex).toBe(5);

                    pageView._selectNextDiff();

                    expect(pageView._selectedAnchorIndex).toBe(6);
                });

                it('On last chunk', function() {
                    pageView.selectAnchorByName('2.2');
                    expect(pageView._selectedAnchorIndex).toBe(6);

                    pageView._selectNextDiff();

                    expect(pageView._selectedAnchorIndex).toBe(6);
                });
            });
        });
    });

    describe('Key bindings', function() {
        function triggerKeyPress(c) {
            const evt = $.Event('keypress');
            evt.which = c.charCodeAt(0);

            pageView.$el.trigger(evt);
        }

        function testKeys(description, funcName, keyList) {
            describe(description, function() {
                keyList.forEach(key => {
                    let label;
                    let c;

                    if (key.length === 2) {
                        label = key[0];
                        c = key[1];
                    } else {
                        label = "'" + key + "'";
                        c = key;
                    }

                    it(label, function() {
                        pageView.render();
                        spyOn(pageView, funcName);
                        triggerKeyPress(c);
                        expect(pageView[funcName]).toHaveBeenCalled();
                    });
                });
            });
        }

        testKeys('Previous file',
                 '_selectPreviousFile',
                 ['a', 'A', 'K', 'P', '<', 'm']);
        testKeys('Next file',
                 '_selectNextFile',
                 ['f', 'F', 'J', 'N', '>']);
        testKeys('Previous anchor',
                 '_selectPreviousDiff',
                 ['s', 'S', 'k', 'p', ',']);
        testKeys('Next anchor',
                 '_selectNextDiff',
                 ['d', 'D', 'j', 'n', '.']);
        testKeys('Previous comment',
                 '_selectPreviousComment',
                 ['[', 'x']);
        testKeys('Next comment',
                 '_selectNextComment',
                 [']', 'c']);
        testKeys('Recenter selected',
                 '_recenterSelected',
                 [['Enter', '\x0d']]);
        testKeys('Create comment',
                 '_createComment',
                 ['r', 'R']);
    });

    describe('Reviewable Management', function() {
        beforeEach(function() {
            spyOn(pageView, 'queueLoadDiff');

            pageView.render();
        });

        it('File added', function() {
            expect($diffs.find('.diff-container').length).toBe(0);
            expect(pageView.queueLoadDiff.calls.count()).toBe(0);

            page.files.reset([
                new RB.DiffFile({
                    id: 100,
                    filediff: {
                        id: 200,
                        revision: 1,
                    },
                }),
            ]);

            expect($diffs.find('.diff-container').length).toBe(1);
            expect(pageView.queueLoadDiff.calls.count()).toBe(1);
        });

        it('Files reset', function() {
            expect($diffs.find('.diff-container').length).toBe(0);
            expect(pageView.queueLoadDiff.calls.count()).toBe(0);

            /* Add an initial batch of files. */
            page.files.reset([
                new RB.DiffFile({
                    id: 100,
                    filediff: {
                        id: 200,
                        revision: 1,
                    },
                }),
            ]);

            expect($diffs.find('.diff-container').length).toBe(1);
            expect(pageView.queueLoadDiff.calls.count()).toBe(1);

            /* Now do another. */
            page.files.reset([
                new RB.DiffFile({
                    id: 101,
                    filediff: {
                        id: 201,
                        revision: 2,
                    },
                }),
            ]);

            const $containers = $diffs.find('.diff-container');
            expect($containers.length).toBe(1);
            expect($containers.find('.sidebyside')[0].id)
                .toBe('file_container_101');
            expect(pageView.queueLoadDiff.calls.count()).toBe(2);
        });
    });

    describe('Page view/URL state', function() {
        let router;

        beforeEach(function() {
            router = pageView.router;

            spyOn(page, 'loadDiffRevision');

            /*
             * Bypass all the actual history logic and get to the actual
             * router handler.
             */
            spyOn(router, 'navigate').and.callFake((url, options) => {
                if (!options || options.trigger !== false) {
                    Backbone.history.loadUrl(url);
                }
            });
        });

        describe('Initial URL', function() {
            it('Initial default load', function() {
                pageView._setInitialURL('', 'index_header');

                expect(router.navigate).toHaveBeenCalledWith(
                    '1/#index_header',
                    {
                        replace: true,
                        trigger: false,
                    });
                expect(page.loadDiffRevision).not.toHaveBeenCalled();
            });

            it('Initial load of first page explicit', function() {
                pageView._setInitialURL('?page=1', 'index_header');

                expect(router.navigate).toHaveBeenCalledWith(
                    '1/?page=1#index_header',
                    {
                        replace: true,
                        trigger: false,
                    });
                expect(page.loadDiffRevision).not.toHaveBeenCalled();
            });

            it('Initial load of page > 1', function() {
                pageView._setInitialURL('?page=2', 'index_header');

                expect(router.navigate).toHaveBeenCalledWith(
                    '1/?page=2#index_header',
                    {
                        replace: true,
                        trigger: false,
                    });
                expect(page.loadDiffRevision).not.toHaveBeenCalled();
            });

            it('Initial load of interdiff', function() {
                page.revision.set('revision', 2);
                page.revision.set('interdiffRevision', 3);
                pageView._setInitialURL('?page=2', 'index_header');

                expect(router.navigate).toHaveBeenCalledWith(
                    '2-3/?page=2#index_header',
                    {
                        replace: true,
                        trigger: false,
                    });
                expect(page.loadDiffRevision).not.toHaveBeenCalled();
            });

            it('Initial load with filename patterns', function() {
                pageView._setInitialURL('?filenames=*.js,src/*',
                                        'index_header');

                expect(router.navigate).toHaveBeenCalledWith(
                    '1/?filenames=*.js,src/*#index_header',
                    {
                        replace: true,
                        trigger: false,
                    });
                expect(page.loadDiffRevision).not.toHaveBeenCalled();
            });
        });

        describe('_navigate', function() {
            beforeEach(function() {
                page.set('filenamePatterns', '*.js,src/*');
            });

            it('With page == 1', function() {
                pageView._navigate({
                    page: 1,
                });

                expect(router.navigate).toHaveBeenCalledWith(
                    '1/?filenames=*.js%2Csrc%2F*',
                    {
                        trigger: true,
                    });
                expect(page.loadDiffRevision).toHaveBeenCalledWith({
                    page: 1,
                    revision: 1,
                    interdiffRevision: null,
                    filenamePatterns: '*.js,src/*',
                });
            });

            it('With page > 1', function() {
                pageView._navigate({
                    page: 2,
                });

                expect(router.navigate).toHaveBeenCalledWith(
                    '1/?page=2&filenames=*.js%2Csrc%2F*',
                    {
                        trigger: true,
                    });
                expect(page.loadDiffRevision).toHaveBeenCalledWith({
                    page: 2,
                    revision: 1,
                    interdiffRevision: null,
                    filenamePatterns: '*.js,src/*',
                });
            });

            it('New revision on page > 1', function() {
                page.pagination.set('currentPage', 2);
                pageView._onRevisionSelected([0, 2]);

                expect(router.navigate).toHaveBeenCalledWith(
                    '2/?filenames=*.js%2Csrc%2F*',
                    {
                        trigger: true,
                    });
                expect(page.loadDiffRevision).toHaveBeenCalledWith({
                    page: 1,
                    revision: 2,
                    interdiffRevision: null,
                    filenamePatterns: '*.js,src/*',
                });
            });

            it('Same revision on page > 1', function() {
                page.pagination.set('currentPage', 2);

                pageView._navigate({
                    revision: 1,
                });

                expect(router.navigate).toHaveBeenCalledWith(
                    '1/?page=2&filenames=*.js%2Csrc%2F*',
                    {
                        trigger: true,
                    });
                expect(page.loadDiffRevision).toHaveBeenCalledWith({
                    page: 2,
                    revision: 1,
                    interdiffRevision: null,
                    filenamePatterns: '*.js,src/*',
                });
            });

            it('With updateURLOnly', function() {
                page.pagination.set('currentPage', 2);

                pageView._navigate({
                    revision: 2,
                    interdiffRevision: 3,
                    updateURLOnly: true,
                });

                expect(router.navigate).toHaveBeenCalledWith(
                    '2-3/?filenames=*.js%2Csrc%2F*',
                    {
                        replace: true,
                        trigger: false,
                    });
                expect(page.loadDiffRevision).not.toHaveBeenCalled();
            });

            it('With anchor', function() {
                pageView._navigate({
                    anchor: 'test',
                });

                expect(router.navigate).toHaveBeenCalledWith(
                    '1/?filenames=*.js%2Csrc%2F*#test',
                    {
                        trigger: true,
                    });
                expect(page.loadDiffRevision).toHaveBeenCalledWith({
                    page: 1,
                    revision: 1,
                    interdiffRevision: null,
                    filenamePatterns: '*.js,src/*',
                });
            });
        });

        describe('Revision selector', function() {
            describe('New diff revision selected', function() {
                it('From single revision', function() {
                    pageView._onRevisionSelected([0, 2]);

                    expect(router.navigate).toHaveBeenCalledWith(
                        '2/',
                        {
                            trigger: true,
                        });
                    expect(page.loadDiffRevision).toHaveBeenCalledWith({
                        page: 1,
                        revision: 2,
                        interdiffRevision: null,
                        filenamePatterns: null,
                    });
                });

                it('From interdiff revision', function() {
                    page.revision.set('interdiffRevision', 2);

                    pageView._onRevisionSelected([0, 2]);

                    expect(router.navigate).toHaveBeenCalledWith(
                        '2/',
                        {
                            trigger: true,
                        });
                    expect(page.loadDiffRevision).toHaveBeenCalledWith({
                        page: 1,
                        revision: 2,
                        interdiffRevision: null,
                        filenamePatterns: null,
                    });
                });
            });

            it('New interdiff revision selected', function() {
                pageView._onRevisionSelected([2, 5]);

                expect(router.navigate).toHaveBeenCalledWith(
                    '2-5/',
                    {
                        trigger: true,
                    });
                expect(page.loadDiffRevision).toHaveBeenCalledWith({
                    page: 1,
                    revision: 2,
                    interdiffRevision: 5,
                    filenamePatterns: null,
                });
            });
        });

        describe('Page selector', function() {
            it('With page == 1', function() {
                pageView._onPageSelected(true, 1);

                expect(router.navigate).toHaveBeenCalledWith(
                    '1/',
                    {
                        trigger: true,
                    });
                expect(page.loadDiffRevision).toHaveBeenCalledWith({
                    page: 1,
                    revision: 1,
                    interdiffRevision: null,
                    filenamePatterns: null,
                });
            });

            it('With page > 1', function() {
                pageView._onPageSelected(true, 2);

                expect(router.navigate).toHaveBeenCalledWith(
                    '1/?page=2',
                    {
                        trigger: true,
                    });
                expect(page.loadDiffRevision).toHaveBeenCalledWith({
                    page: 2,
                    revision: 1,
                    interdiffRevision: null,
                    filenamePatterns: null,
                });
            });
        });

        it('Anchor selection', function() {
            const $anchor = $('<a name="test"/>');

            pageView.render();
            pageView.selectAnchor($anchor);

            expect(router.navigate).toHaveBeenCalledWith(
                '1/#test',
                {
                    replace: true,
                    trigger: false,
                });
            expect(page.loadDiffRevision).not.toHaveBeenCalled();
        });
    });
});
