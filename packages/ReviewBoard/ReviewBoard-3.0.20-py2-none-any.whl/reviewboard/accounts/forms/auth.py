from __future__ import unicode_literals

import re
import sre_constants

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import \
    AuthenticationForm as DjangoAuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from djblets.auth.ratelimit import is_ratelimited
from djblets.siteconfig.forms import SiteSettingsForm

from reviewboard.admin.checks import get_can_enable_dns, get_can_enable_ldap


class ActiveDirectorySettingsForm(SiteSettingsForm):
    """A form for configuring the Active Directory authentication backend."""

    auth_ad_domain_name = forms.CharField(
        label=_("Domain name"),
        help_text=_("Enter the domain name to use, (ie. example.com). This "
                    "will be used to query for LDAP servers and to bind to "
                    "the domain."),
        required=True,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ad_use_tls = forms.BooleanField(
        label=_("Use TLS for authentication"),
        required=False)

    auth_ad_find_dc_from_dns = forms.BooleanField(
        label=_("Find DC from DNS"),
        help_text=_("Query DNS to find which domain controller to use"),
        required=False)

    auth_ad_domain_controller = forms.CharField(
        label=_("Domain controller"),
        help_text=_("If not using DNS to find the DC, specify the domain "
                    "controller(s) here "
                    "(eg. ctrl1.example.com ctrl2.example.com:389)"),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ad_ou_name = forms.CharField(
        label=_("OU name"),
        help_text=_("Optionally restrict users to specified OU."),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ad_group_name = forms.CharField(
        label=_("Group name"),
        help_text=_("Optionally restrict users to specified group."),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ad_search_root = forms.CharField(
        label=_("Custom search root"),
        help_text=_("Optionally specify a custom search root, overriding "
                    "the built-in computed search root. If set, \"OU name\" "
                    "is ignored."),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ad_recursion_depth = forms.IntegerField(
        label=_("Recursion Depth"),
        help_text=_('Depth to recurse when checking group membership. '
                    '0 to turn off, -1 for unlimited.'),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    def load(self):
        """Load the data for the form."""
        can_enable_dns, reason = get_can_enable_dns()

        if not can_enable_dns:
            self.disabled_fields['auth_ad_find_dc_from_dns'] = reason

        can_enable_ldap, reason = get_can_enable_ldap()

        if not can_enable_ldap:
            self.disabled_fields['auth_ad_use_tls'] = True
            self.disabled_fields['auth_ad_group_name'] = True
            self.disabled_fields['auth_ad_recursion_depth'] = True
            self.disabled_fields['auth_ad_ou_name'] = True
            self.disabled_fields['auth_ad_search_root'] = True
            self.disabled_fields['auth_ad_find_dc_from_dns'] = True
            self.disabled_fields['auth_ad_domain_controller'] = True

            self.disabled_reasons['auth_ad_domain_name'] = reason

        super(ActiveDirectorySettingsForm, self).load()

    class Meta:
        title = _('Active Directory Authentication Settings')
        fieldsets = (
            (None, {
                'fields': ('auth_ad_domain_name',
                           'auth_ad_use_tls',
                           'auth_ad_find_dc_from_dns',
                           'auth_ad_domain_controller'),
            }),
            (_('Access Control Settings'), {
                'fields': ('auth_ad_ou_name',
                           'auth_ad_group_name'),
            }),
            (_('Advanced Settings'), {
                'fields': ('auth_ad_search_root',
                           'auth_ad_recursion_depth'),
            }),
        )


class StandardAuthSettingsForm(SiteSettingsForm):
    """A form for configuring the builtin authentication backend."""

    auth_enable_registration = forms.BooleanField(
        label=_("Enable registration"),
        help_text=_("Allow users to register new accounts."),
        required=False)

    auth_registration_show_captcha = forms.BooleanField(
        label=_('Show a captcha for registration'),
        required=False)

    recaptcha_public_key = forms.CharField(
        label=_('reCAPTCHA Public Key'),
        required=False,
        widget=forms.TextInput(attrs={'size': '60'}))

    recaptcha_private_key = forms.CharField(
        label=_('reCAPTCHA Private Key'),
        required=False,
        widget=forms.TextInput(attrs={'size': '60'}))

    def __init__(self, *args, **kwargs):
        super(StandardAuthSettingsForm, self).__init__(*args, **kwargs)

        # This is done at initialization time instead of in the field
        # definition because the format operation causes the lazy translation
        # to be evaluated, which has to happen after the i18n infrastructure
        # has been started.
        self.fields['auth_registration_show_captcha'].help_text = mark_safe(
            _('Displays a captcha using <a href="%(recaptcha_url)s">'
              'reCAPTCHA</a> on the registration page. To enable this, you '
              'will need to go <a href="%(register_url)s">here</A> to '
              'register an account and type in your new keys below.')
            % {
                'recaptcha_url': 'http://www.google.com/recaptcha',
                'register_url': 'https://www.google.com/recaptcha/admin'
                                '#createsite',
            })

    def clean_recaptcha_public_key(self):
        """Validate that the reCAPTCHA public key is specified if needed."""
        key = self.cleaned_data['recaptcha_public_key'].strip()

        if self.cleaned_data['auth_registration_show_captcha'] and not key:
            raise ValidationError(_('This field is required.'))

        return key

    def clean_recaptcha_private_key(self):
        """Validate that the reCAPTCHA private key is specified if needed."""
        key = self.cleaned_data['recaptcha_private_key'].strip()

        if self.cleaned_data['auth_registration_show_captcha'] and not key:
            raise ValidationError(_('This field is required.'))

        return key

    class Meta:
        title = _('Registration Settings')
        fieldsets = (
            (None, {
                'fields': ('auth_enable_registration',),
            }),
            (_('reCAPTCHA Settings'), {
                'fields': ('auth_registration_show_captcha',
                           'recaptcha_public_key',
                           'recaptcha_private_key'),
            }),
        )


class HTTPBasicSettingsForm(SiteSettingsForm):
    """A form for configuring the HTTP Digest authentication backend."""

    auth_digest_file_location = forms.CharField(
        label=_(".htpasswd File location"),
        help_text=_("Location of the .htpasswd file which "
                    "stores the usernames and passwords in digest format"),
        widget=forms.TextInput(attrs={'size': '60'}))

    auth_digest_realm = forms.CharField(
        label=_("HTTP Digest Realm"),
        help_text=_("Realm used for HTTP Digest authentication"),
        widget=forms.TextInput(attrs={'size': '40'}))

    class Meta:
        title = _('HTTP Digest Authentication Settings')


class LDAPSettingsForm(SiteSettingsForm):
    """A form for configuring the LDAP authentication backend."""

    # TODO: Invent a URIField and use it.
    auth_ldap_uri = forms.CharField(
        label=_("LDAP Server"),
        help_text=_("The LDAP server to authenticate with. "
                    "For example: ldap://localhost:389"),
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ldap_base_dn = forms.CharField(
        label=_("LDAP Base DN"),
        help_text=_("The LDAP Base DN for performing LDAP searches.  For "
                    "example: ou=users,dc=example,dc=com"),
        required=True,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ldap_uid = forms.CharField(
        label=_("Username Attribute"),
        help_text=_("The attribute in the LDAP server that stores a user's "
                    "login name."),
        required=True)

    auth_ldap_given_name_attribute = forms.CharField(
        label=_("Given Name Attribute"),
        initial="givenName",
        help_text=_("The attribute in the LDAP server that stores the user's "
                    "given name."),
        required=False)

    auth_ldap_surname_attribute = forms.CharField(
        label=_("Surname Attribute"),
        initial="sn",
        help_text=_("The attribute in the LDAP server that stores the user's "
                    "surname."),
        required=False)

    auth_ldap_full_name_attribute = forms.CharField(
        label=_("Full Name Attribute"),
        help_text=_("The attribute in the LDAP server that stores the user's "
                    "full name.  This takes precedence over the "
                    '"Given Name Attribute" and "Surname Attribute."'),
        required=False)

    auth_ldap_email_domain = forms.CharField(
        label=_("E-Mail Domain"),
        help_text=_("The domain name appended to the username to construct "
                    "the user's e-mail address. This takes precedence over "
                    '"E-Mail LDAP Attribute."'),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ldap_email_attribute = forms.CharField(
        label=_("E-Mail LDAP Attribute"),
        help_text=_("The attribute in the LDAP server that stores the user's "
                    "e-mail address. For example: mail"),
        required=False)

    auth_ldap_tls = forms.BooleanField(
        label=_("Use TLS for authentication"),
        required=False)

    auth_ldap_uid_mask = forms.CharField(
        label=_("Custom LDAP User Search Filter"),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ldap_anon_bind_uid = forms.CharField(
        label=_("Review Board LDAP Bind Account"),
        help_text=_("The full distinguished name of a user account with "
                    "sufficient access to perform lookups of users and "
                    "groups in the LDAP server. If the LDAP server permits "
                    "such lookups via anonymous bind, you may leave this "
                    "field blank."),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ldap_anon_bind_passwd = forms.CharField(
        label=_("Review Board LDAP Bind Password"),
        widget=forms.PasswordInput(attrs={'size': '30'}, render_value=True),
        help_text=_("The password for the Review Board LDAP Bind Account."),
        required=False)

    def __init__(self, *args, **kwargs):
        super(LDAPSettingsForm, self).__init__(*args, **kwargs)

        # This is done at initialization time instead of in the field
        # definition because the format operation causes the lazy translation
        # to be evaluated, which has to happen after the i18n infrastructure
        # has been started.
        self.fields['auth_ldap_uid_mask'].help_text = mark_safe(
            _('A custom LDAP search filter, corresponding to RFC 2254. If '
              'left unset, this option is equivalent to <tt>('
              'usernameattribute=%(varname)s)</tt>. Use <tt>'
              '"%(varname)s"</tt> wherever the username would normally go. '
              'Specify this value only if the default cannot locate all '
              'users.')
            % {
                'varname': '%s',
            })

    def load(self):
        """Load the data for the form."""
        can_enable_ldap, reason = get_can_enable_ldap()

        if not can_enable_ldap:
            self.disabled_fields['auth_ldap_uri'] = True
            self.disabled_fields['auth_ldap_given_name_attribute'] = True
            self.disabled_fields['auth_ldap_surname_attribute'] = True
            self.disabled_fields['auth_ldap_full_name_attribute'] = True
            self.disabled_fields['auth_ldap_email_domain'] = True
            self.disabled_fields['auth_ldap_email_attribute'] = True
            self.disabled_fields['auth_ldap_tls'] = True
            self.disabled_fields['auth_ldap_base_dn'] = True
            self.disabled_fields['auth_ldap_uid'] = True
            self.disabled_fields['auth_ldap_uid_mask'] = True
            self.disabled_fields['auth_ldap_anon_bind_uid'] = True
            self.disabled_fields['auth_ldap_anon_bind_password'] = True

            self.disabled_reasons['auth_ldap_uri'] = reason

        super(LDAPSettingsForm, self).load()

    class Meta:
        title = _('LDAP Authentication Settings')
        fieldsets = (
            (None, {
                'fields': ('auth_ldap_uri',
                           'auth_ldap_tls',
                           'auth_ldap_anon_bind_uid',
                           'auth_ldap_anon_bind_passwd',
                           'auth_ldap_base_dn'),
            }),
            (_('User Lookups'), {
                'fields': ('auth_ldap_uid',
                           'auth_ldap_given_name_attribute',
                           'auth_ldap_surname_attribute',
                           'auth_ldap_full_name_attribute',
                           'auth_ldap_email_attribute',
                           'auth_ldap_email_domain',
                           'auth_ldap_uid_mask'),
            }),
        )


class LegacyAuthModuleSettingsForm(SiteSettingsForm):
    """A form for configuring old-style custom authentication backends.

    Newer authentication backends are registered via the extensions framework,
    but there used to be a method by which users just put in a list of python
    module paths. This form allows that configuration to be edited.
    """

    custom_backends = forms.CharField(
        label=_("Backends"),
        help_text=_('A comma-separated list of old-style custom auth '
                    'backends. These are represented as Python module paths.'),
        widget=forms.TextInput(attrs={'size': '40'}))

    def load(self):
        """Load the data for the form."""
        self.fields['custom_backends'].initial = \
            ', '.join(self.siteconfig.get('auth_custom_backends'))

        super(LegacyAuthModuleSettingsForm, self).load()

    def save(self):
        """Save the form."""
        self.siteconfig.set(
            'auth_custom_backends',
            re.split(r',\s*', self.cleaned_data['custom_backends']))

        super(LegacyAuthModuleSettingsForm, self).save()

    class Meta:
        title = _('Legacy Authentication Module Settings')
        save_blacklist = ('custom_backends',)


class NISSettingsForm(SiteSettingsForm):
    """A form for configuring the NIS authentication backend."""

    auth_nis_email_domain = forms.CharField(
        label=_("E-Mail Domain"),
        widget=forms.TextInput(attrs={'size': '40'}))

    class Meta:
        title = _('NIS Authentication Settings')


class X509SettingsForm(SiteSettingsForm):
    """A form for configuring the X509 certificate authentication backend."""

    auth_x509_username_field = forms.ChoiceField(
        label=_("Username Field"),
        choices=(
            # Note: These names correspond to environment variables set by
            #       mod_ssl.
            ("SSL_CLIENT_S_DN", _("DN (Distinguished Name)")),
            ("SSL_CLIENT_S_DN_CN", _("CN (Common Name)")),
            ("SSL_CLIENT_S_DN_Email", _("E-mail address")),
            # Allow the user to use a custom environment variable
            ("CUSTOM", _("Custom Field")),
        ),
        help_text=_("The X.509 certificate field from which the Review Board "
                    "username will be extracted."),
        required=True)

    auth_x509_custom_username_field = forms.CharField(
        label=_("Custom Username Field"),
        help_text=_("The custom X.509 certificate field from which the "
                    "Review Board username will be extracted. "
                    "(only used if Username Field is \"Custom Field\""),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_x509_username_regex = forms.CharField(
        label=_("Username Regex"),
        help_text=_("Optional regex used to convert the selected X.509 "
                    "certificate field to a usable Review Board username. For "
                    "example, if using the e-mail field to retrieve the "
                    "username, use this regex to get the username from an "
                    "e-mail address: '(\s+)@yoursite.com'. There must be only "
                    "one group in the regex."),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_x509_autocreate_users = forms.BooleanField(
        label=_("Automatically create new user accounts."),
        help_text=_("Enabling this option will cause new user accounts to be "
                    "automatically created when a new user with an X.509 "
                    "certificate accesses Review Board."),
        required=False)

    def clean_auth_x509_username_regex(self):
        """Validate that the specified regular expression is valid."""
        regex = self.cleaned_data['auth_x509_username_regex']

        try:
            re.compile(regex)
        except sre_constants.error as e:
            raise ValidationError(e)

        return regex

    class Meta:
        title = _('X.509 Client Certificate Authentication Settings')


class AuthenticationForm(DjangoAuthenticationForm):
    """Form used for user logins.

    This extends Django's built-in AuthenticationForm implementation to allow
    users to specify their e-mail address in place of their username. In
    addition, it also tracks the number of failed login attempts for a given
    time frame, and informs the user whether the maximum number of attempts
    have been exceeded.
    """

    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    def clean_username(self):
        """Validate the 'username' field.

        In case the given text is not a user found on the system, attempt a
        look-up using it as an e-mail address and change the user-entered text
        so that login can succeed.
        """
        username = self.cleaned_data.get('username')

        if not User.objects.filter(username=username).exists():
            try:
                username = User.objects.get(email=username).username
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                pass

        return username

    def clean(self):
        """Validate the authentication form.

        In case authentication has failed for the given user, Djblets's rate
        limiting feature will increment the number of failed login attempts
        until the maximum number of attempts have been reached. The user
        will have to wait until the rate limit time period is over before
        trying again.

        Returns:
            dict:
            The cleaned data for all fields in the form.

        Raises:
            django.core.exceptions.ValidationError:
                The data in the form was not valid.
        """
        request = self.request

        # Check if the number of failed login attempts were already exceeded
        # before authenticating.
        if is_ratelimited(request, increment=False):
            raise forms.ValidationError(
                _('Maximum number of login attempts exceeded.'))

        try:
            self.cleaned_data = super(AuthenticationForm, self).clean()
        except ValidationError:
            # If authentication for a given user has failed (i.e.
            # self.user_cache is None), increment the number of
            # failed login attempts.
            is_ratelimited(request, increment=True)
            raise

        return self.cleaned_data
