# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2016, 2020 CERN.
#
# CERN Analysis Preservation Framework is free software; you can redistribute
# it and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Analysis Preservation Framework is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Analysis Preservation Framework; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

from invenio_access.models import ActionRoles
from invenio_accounts.models import Role

from conftest import add_role_to_user


def test_no_schema_given_fails(app, cli_runner):
    res = cli_runner('fixtures permissions -p read -r test-users@cern.ch --allow')
    assert res.exit_code == 2
    assert "Missing argument 'SCHEMA_NAME'" in res.output


def test_no_role_given_fails(app, cli_runner):
    res = cli_runner('fixtures permissions -p read --allow test-schema')
    assert res.exit_code == 2
    assert "ERROR: Users (-u) or roles (-r) are required arguments" in res.output


def test_no_permissions_given_fails(app, cli_runner):
    res = cli_runner('fixtures permissions -r test-users@cern.ch --allow test-schema')
    assert res.exit_code == 2
    assert "Missing option '--permissions'" in res.output


def test_role_doesnt_exist_exception(app, db, create_schema, cli_runner):

    _schema = create_schema('test-schema')

    db.session.add(_schema)
    db.session.commit()
    schema_id = _schema.id
    res = cli_runner('fixtures permissions -p read -r test-users@cern.ch --allow test-schema')
    assert res.exit_code == 1
    assert 'Role with name test-users@cern.ch not found.' in res.output


def test_action_doesnt_exist_exception(app, db, create_schema, cli_runner):

    _schema = create_schema('test-schema')

    db.session.add(_schema)
    db.session.commit()
    schema_id = _schema.id
    res = cli_runner('fixtures permissions -p write -r test-users@cern.ch --allow test-schema')
    assert res.exit_code == 1
    assert 'Action deposit-schema-write is not registered.' in res.output


def test_action_allow_read_and_update_deposit(app, db, users, create_schema, cli_runner):
    user = users['cms_user']
    add_role_to_user(user, 'test-users@cern.ch')

    _schema = create_schema('test-schema')

    db.session.add(_schema)
    db.session.commit()
    schema_id = _schema.id

    res = cli_runner('fixtures permissions -p read -p update -r test-users@cern.ch --allow test-schema')
    assert res.exit_code == 0
    assert 'Process finished.' in res.output

    action_roles = ActionRoles.query.filter_by(argument=str(schema_id)).all()
    role = Role.query.filter_by(name='test-users@cern.ch').one()

    assert len(action_roles) == 2

    action_roles.sort(key=lambda x: x.action)
    assert action_roles[0].exclude is False
    assert action_roles[0].action == 'deposit-schema-read'
    assert action_roles[0].role_id == role.id

    assert action_roles[1].exclude is False
    assert action_roles[1].action == 'deposit-schema-update'
    assert action_roles[1].role_id == role.id


def test_action_deny_read_deposit(app, db, users, create_schema, cli_runner):
    user = users['cms_user']
    add_role_to_user(user, 'test-users@cern.ch')

    _schema = create_schema('test-schema')

    db.session.add(_schema)
    db.session.commit()
    schema_id = _schema.id

    res = cli_runner('fixtures permissions -p read -r test-users@cern.ch --deny test-schema')
    assert res.exit_code == 0
    assert 'Process finished.' in res.output

    action_roles = ActionRoles.query.filter_by(argument=str(schema_id)).all()
    role = Role.query.filter_by(name='test-users@cern.ch').one()

    assert len(action_roles) == 1
    assert action_roles[0].exclude is True
    assert action_roles[0].action == 'deposit-schema-read'
    assert action_roles[0].role_id == role.id


def test_action_remove_read_deposit(app, db, users, create_schema, cli_runner):
    user = users['cms_user']
    add_role_to_user(user, 'test-users@cern.ch')

    _schema = create_schema('test-schema')

    db.session.add(_schema)
    db.session.commit()
    schema_id = _schema.id

    # give access
    res = cli_runner('fixtures permissions -p read -r test-users@cern.ch --allow test-schema')
    assert res.exit_code == 0
    assert 'Process finished.' in res.output

    # remove access
    res = cli_runner('fixtures permissions -p read -r test-users@cern.ch --remove test-schema')
    assert res.exit_code == 0
    assert 'Process finished.' in res.output

    action_roles = ActionRoles.query.filter_by(argument=str(schema_id)).all()
    assert len(action_roles) == 0


def test_action_allow_read_record(app, db, users, create_schema, cli_runner):
    user = users['cms_user']
    add_role_to_user(user, 'test-users@cern.ch')

    _schema = create_schema('test-schema')

    db.session.add(_schema)
    db.session.commit()
    schema_id = _schema.id

    res = cli_runner('fixtures permissions -p read -r test-users@cern.ch --record --allow test-schema')
    assert res.exit_code == 0
    assert 'Process finished.' in res.output

    action_roles = ActionRoles.query.filter_by(argument=str(schema_id)).all()

    assert len(action_roles) == 1
    assert action_roles[0].exclude is False
    assert action_roles[0].action == 'record-schema-read'


def test_action_allow_read_schema(app, db, users, create_schema, cli_runner):
    user = users['cms_user']
    add_role_to_user(user, 'test-users@cern.ch')
    _schema = create_schema('test-schema')
    schema_id = str(_schema.id)

    db.session.add(_schema)
    db.session.commit()

    res = cli_runner('fixtures permissions -p read -r test-users@cern.ch --schema --allow test-schema')
    assert res.exit_code == 0
    assert 'Process finished.' in res.output

    action_roles = ActionRoles.query.filter_by(argument=str(schema_id)).all()

    assert len(action_roles) == 1
    assert action_roles[0].exclude is False
    assert action_roles[0].action == 'schema-object-read'
    assert action_roles[0].argument == schema_id


def test_action_allow_read_schema_fails_if_already_in_db(app, db, users, create_schema, cli_runner):
    user = users['cms_user']
    add_role_to_user(user, 'test-users@cern.ch')
    _schema = create_schema('test-schema', experiment='CMS')

    db.session.add(_schema)
    db.session.commit()

    # 1st time success
    res = cli_runner('fixtures permissions -p read -r test-users@cern.ch --schema --allow test-schema')
    assert res.exit_code == 0
    assert 'Process finished.' in res.output

    # 2nd time fails
    res = cli_runner('fixtures permissions -p read -r test-users@cern.ch --schema --allow test-schema')

    assert res.exit_code == 0
    assert 'Action user/role already exists.' in res.output
