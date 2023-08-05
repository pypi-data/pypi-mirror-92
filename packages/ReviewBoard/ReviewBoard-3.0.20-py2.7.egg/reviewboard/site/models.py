#
# models.py -- Models for the "reviewboard.site" app.
#
# Copyright (c) 2010  David Trowbridge
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from djblets.db.fields import JSONField

from reviewboard.site.signals import local_site_user_added


@python_2_unicode_compatible
class LocalSite(models.Model):
    """
    A division within a Review Board installation.

    This allows the creation of independent, isolated divisions within a given
    server. Users can be designated as members of a LocalSite, and optionally
    as admins (which allows them to manipulate the repositories, groups and
    users in the site).

    Pretty much every other model in this module can all be assigned to a
    single LocalSite, at which point only members will be able to see or
    manipulate these objects. Access control is performed at every level, and
    consistency is enforced through a liberal sprinkling of assertions and unit
    tests.
    """
    name = models.SlugField(_('name'), max_length=32, blank=False, unique=True)
    public = models.BooleanField(
        default=False,
        help_text=_('Allow people outside the team to access and post '
                    'review requests and reviews.'))
    users = models.ManyToManyField(User, blank=True,
                                   related_name='local_site')
    admins = models.ManyToManyField(User, blank=True,
                                    related_name='local_site_admins')

    extra_data = JSONField(null=True)

    def is_accessible_by(self, user):
        """Returns whether or not the user has access to this LocalSite.

        This checks that the user is logged in, and that they're listed in the
        'users' field.
        """
        return (self.public or
                (user.is_authenticated() and
                 (user.is_staff or self.users.filter(pk=user.pk).exists())))

    def is_mutable_by(self, user, perm='site.change_localsite'):
        """Returns whether or not a user can modify settings in a LocalSite.

        This checks that the user is either staff with the proper permissions,
        or that they're listed in the 'admins' field.

        By default, this is checking whether the LocalSite itself can be
        modified, but a different permission can be passed to check for
        another object.
        """
        return user.has_perm(perm) or self.admins.filter(pk=user.pk).exists()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'site_localsite'
        verbose_name = _('Local Site')
        verbose_name_plural = _('Local Sites')


@receiver(m2m_changed, sender=LocalSite.users.through)
def _on_local_site_users_changed(sender, instance, model,
                                 action, pk_set, **kwargs):
    """Handle the m2m_changed event for LocalSite and User.

    This function handles both the case where users are added to local sites
    and local sites are added to the set of a user's local sites. In both of
    these cases, the local_site_user_added signal is dispatched.
    """
    if action == 'post_add':
        if isinstance(instance, User):
            users = [instance]
            local_sites = LocalSite.objects.filter(id__in=pk_set)
        else:
            users = User.objects.filter(id__in=pk_set)
            local_sites = [instance]

        for user in users:
            for local_site in local_sites:
                local_site_user_added.send(sender=LocalSite,
                                           user=user,
                                           local_site=local_site)
