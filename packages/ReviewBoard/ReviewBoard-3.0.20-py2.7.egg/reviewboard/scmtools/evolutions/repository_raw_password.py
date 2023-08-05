from __future__ import unicode_literals

from django_evolution.mutations import RenameField


MUTATIONS = [
    RenameField('Repository', 'password', 'encrypted_password',
                db_column='password'),
]
