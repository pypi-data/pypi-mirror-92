'use strict';

suite('rb/ui/managers/NotificationManagerModel', function () {
    var instance = RB.NotificationManager.instance;
    var origNotification = void 0;

    var Notification = function Notification(title, options) {
        this.title = title;
        this.options = options;
        this.close = function () {};
    };
    Notification.requestPermission = function () {
        Notification.permission = 'granted';
    };

    beforeEach(function () {
        origNotification = RB.NotificationManager.Notification;
        RB.NotificationManager.Notification = Notification;

        RB.UserSession.instance.set('enableDesktopNotifications', true);

        instance.setup();

        expect(Notification.permission).toBe('granted');
    });

    afterEach(function () {
        RB.NotificationManager.Notification = origNotification;
    });

    describe('Notification Manager', function () {
        it('Calls external API', function () {
            instance.notify({
                title: 'Test',
                body: 'This is a test'
            });

            var notification = instance._notification;
            expect(notification).not.toBe(null);
            expect(notification.title).toBe('Test');
            expect(notification.options.body).toBe('This is a test');
        });

        it('Should notify', function () {
            instance._canNotify = true;
            spyOn(instance, '_haveNotificationPermissions').and.returnValue(true);

            expect(instance.shouldNotify()).toBe(true);
        });

        it('Should not notify due to user permissions', function () {
            instance._canNotify = false;
            spyOn(instance, '_haveNotificationPermissions').and.returnValue(true);

            expect(instance.shouldNotify()).toBe(false);
        });

        it('Should not notify due to browser permissions', function () {
            instance._canNotify = true;
            spyOn(instance, '_haveNotificationPermissions').and.returnValue(false);

            expect(instance.shouldNotify()).toBe(false);
        });
    });
});

//# sourceMappingURL=notificationManagerTests.js.map