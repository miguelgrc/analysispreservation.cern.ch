# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2018 CERN.
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
# or submit itself to any jurisdiction.
"""Unit tests for schemas views."""
import json

from six import PY3
from pytest import mark

from cap.modules.schemas.models import Schema

########################
# api/jsonschemas/  [GET]
# api/jsonschemas/{id}/{version}  [GET]
########################


def test_get_schemas_when_user_not_logged_in_returns_401(client, users):
    resp = client.get('/jsonschemas/')

    assert resp.status_code == 401


def test_get_when_user_outside_of_experiment_returns_403(
        client, db, users, auth_headers_for_user):

    other_user = users['lhcb_user']
    schema = Schema(
        name='cms-schema',
        version='1.2.3',
        fullname='CMS Schema 1.2.3',
        experiment='CMS',
        deposit_schema={'title': 'deposit_schema'},
        deposit_options={'title': 'deposit_options'},
        record_schema={'title': 'record_schema'},
        record_options={'title': 'record_options'},
        record_mapping={
            'mappings': {
                'doc': {
                    'properties': {
                        'title': {
                            'type': 'text'
                        }
                    }
                }
            }
        },
        deposit_mapping={
            'mappings':
                {
                    'doc': {
                        'properties': {
                            'keyword': {
                                'type': 'keyword'
                            }
                        }
                    }
                }
        },
        is_indexed=True,
    )

    db.session.add(schema)
    db.session.add(Schema(name='cms-schema', version='1.1.0'))
    db.session.add(Schema(name='lhcb-schema'))
    db.session.commit()

    resp = client.get(
        '/jsonschemas/cms-schema/1.2.3',
        headers=auth_headers_for_user(other_user))

    assert resp.status_code == 403


def test_get(client, db, users, auth_headers_for_user):
    cms_user = users['cms_user']
    schema = Schema(
        name='cms-schema',
        version='1.2.3',
        fullname='CMS Schema 1.2.3',
        experiment='CMS',
        deposit_schema={'title': 'deposit_schema'},
        deposit_options={'title': 'deposit_options'},
        record_schema={'title': 'record_schema'},
        record_options={'title': 'record_options'},
        record_mapping={
            'mappings': {
                'doc': {
                    'properties': {
                        'title': {
                            'type': 'text'
                        }
                    }
                }
            }
        },
        deposit_mapping={
            'mappings':
                {
                    'doc': {
                        'properties': {
                            'keyword': {
                                'type': 'keyword'
                            }
                        }
                    }
                }
        },
        is_indexed=True,
    )

    db.session.add(schema)
    db.session.add(Schema(name='cms-schema', version='1.1.0'))
    db.session.add(Schema(name='lhcb-schema'))
    db.session.commit()

    resp = client.get('/jsonschemas/', headers=auth_headers_for_user(cms_user))

    assert resp.status_code == 200
    assert resp.json == [
        {
            'name': 'cms-schema',
            'version': '1.2.3',
            'fullname': 'CMS Schema 1.2.3',
            'is_indexed': True,
            'use_deposit_as_record': False,
            'deposit_schema': {
                'title': 'deposit_schema'
            },
            'deposit_options': {
                'title': 'deposit_options'
            },
            'record_schema': {
                'title': 'record_schema'
            },
            'record_options': {
                'title': 'record_options'
            },
            'record_mapping':
                {
                    'mappings':
                        {
                            'doc': {
                                'properties': {
                                    'title': {
                                        'type': 'text'
                                    }
                                }
                            }
                        }
                },
            'deposit_mapping':
                {
                    'mappings':
                        {
                            'doc':
                                {
                                    'properties':
                                        {
                                            'keyword': {
                                                'type': 'keyword'
                                            }
                                        }
                                }
                        }
                },
            'links':
                {
                    'self':
                        u'http://analysispreservation.cern.ch/api/jsonschemas/cms-schema/1.2.3',
                    'deposit':
                        'http://analysispreservation.cern.ch/api/schemas/deposits/records/cms-schema-v1.2.3.json',
                    'record':
                        u'http://analysispreservation.cern.ch/api/schemas/records/cms-schema-v1.2.3.json',
                    #            'versions': u'http://analysispreservation.cern.ch/api/jsonschemas/cms-schema/versions'
                },
        }
    ]

    resp = client.get(
        '/jsonschemas/cms-schema/1.2.3',
        headers=auth_headers_for_user(cms_user))

    assert resp.status_code == 200
    assert resp.json == {
        'name': 'cms-schema',
        'version': '1.2.3',
        'fullname': 'CMS Schema 1.2.3',
        'is_indexed': True,
        'use_deposit_as_record': False,
        'deposit_schema': {
            'title': 'deposit_schema'
        },
        'deposit_options': {
            'title': 'deposit_options'
        },
        'record_schema': {
            'title': 'record_schema'
        },
        'record_options': {
            'title': 'record_options'
        },
        'record_mapping':
            {
                'mappings': {
                    'doc': {
                        'properties': {
                            'title': {
                                'type': 'text'
                            }
                        }
                    }
                }
            },
        'deposit_mapping':
            {
                'mappings':
                    {
                        'doc': {
                            'properties': {
                                'keyword': {
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
            },
        'links':
            {
                'self':
                    u'http://analysispreservation.cern.ch/api/jsonschemas/cms-schema/1.2.3',
                'deposit':
                    'http://analysispreservation.cern.ch/api/schemas/deposits/records/cms-schema-v1.2.3.json',
                'record':
                    u'http://analysispreservation.cern.ch/api/schemas/records/cms-schema-v1.2.3.json',
                #            'versions': u'http://analysispreservation.cern.ch/api/jsonschemas/cms-schema/versions'
            },
    }

    resp = client.get(
        '/jsonschemas/cms-schema', headers=auth_headers_for_user(cms_user))

    assert resp.status_code == 200
    assert resp.json == {
        'name': 'cms-schema',
        'version': '1.2.3',
        'fullname': 'CMS Schema 1.2.3',
        'is_indexed': True,
        'use_deposit_as_record': False,
        'deposit_schema': {
            'title': 'deposit_schema'
        },
        'deposit_options': {
            'title': 'deposit_options'
        },
        'record_schema': {
            'title': 'record_schema'
        },
        'record_options': {
            'title': 'record_options'
        },
        'record_mapping':
            {
                'mappings': {
                    'doc': {
                        'properties': {
                            'title': {
                                'type': 'text'
                            }
                        }
                    }
                }
            },
        'deposit_mapping':
            {
                'mappings':
                    {
                        'doc': {
                            'properties': {
                                'keyword': {
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
            },
        'links':
            {
                'self':
                    u'http://analysispreservation.cern.ch/api/jsonschemas/cms-schema/1.2.3',
                'deposit':
                    'http://analysispreservation.cern.ch/api/schemas/deposits/records/cms-schema-v1.2.3.json',
                'record':
                    u'http://analysispreservation.cern.ch/api/schemas/records/cms-schema-v1.2.3.json',
                #            'versions': u'http://analysispreservation.cern.ch/api/jsonschemas/cms-schema/versions'
            },
    }


def test_get_resolved_schemas(
        client, db, users, create_schema, auth_headers_for_superuser):
    create_schema(
        'nested-schema',
        experiment='CMS',
        deposit_schema={
            'type': 'object',
            'properties': {
                'title': {
                    'type': 'string'
                }
            }
        },
    )
    create_schema(
        'test-analysis',
        experiment='CMS',
        deposit_schema={
            'type': 'object',
            'properties':
                {
                    'nested':
                        {
                            '$ref':
                                'http://analysispreservation.cern.ch/api/schemas/deposits/records/nested-schema-v1.0.0.json'
                        }
                },
        },
        record_schema={
            'title': 'record_schema',
            'type': 'object',
            'properties':
                {
                    'nested':
                        {
                            '$ref':
                                'http://analysispreservation.cern.ch/api/schemas/deposits/records/nested-schema-v1.0.0.json'
                        }
                },
        },
        use_deposit_as_record=False,
    )

    resp = client.get(
        '/jsonschemas/test-analysis/1.0.0?resolve=True',
        headers=auth_headers_for_superuser,
    )

    assert resp.status_code == 200
    assert resp.json == {
        'name': 'test-analysis',
        'fullname': None,
        'version': '1.0.0',
        'is_indexed': True,
        'use_deposit_as_record': False,
        'deposit_schema':
            {
                'type': 'object',
                'properties':
                    {
                        'nested':
                            {
                                'type': 'object',
                                'properties': {
                                    'title': {
                                        'type': 'string'
                                    }
                                },
                            }
                    },
            },
        'record_schema':
            {
                'title': 'record_schema',
                'type': 'object',
                'properties':
                    {
                        'nested':
                            {
                                'type': 'object',
                                'properties': {
                                    'title': {
                                        'type': 'string'
                                    }
                                },
                            }
                    },
            },
        'deposit_mapping': {},
        'deposit_options': {},
        'record_mapping': {},
        'record_options': {},
        'links':
            {
                'self':
                    'http://analysispreservation.cern.ch/api/jsonschemas/test-analysis/1.0.0',
                'deposit':
                    'http://analysispreservation.cern.ch/api/schemas/deposits/records/test-analysis-v1.0.0.json',
                'record':
                    'http://analysispreservation.cern.ch/api/schemas/records/test-analysis-v1.0.0.json',
            },
    }


def test_get_all_version_of_schema(
        client, db, users, auth_headers_for_user):
    cms_user = users['cms_user']
    db.session.add(Schema(name='schema1', version='1.2.3', experiment='CMS'))
    db.session.add(Schema(name='schema1', version='1.2.5', experiment='CMS'))
    db.session.commit()

    resp = client.get(
        '/jsonschemas/schema1/versions/', headers=auth_headers_for_user(cms_user))

    assert resp.status_code == 200
    assert resp.json ==  {
        "latest": {
            "links": {
            "deposit": "http://analysispreservation.cern.ch/api/schemas/deposits/records/schema1-v1.2.5.json",
            "record": "http://analysispreservation.cern.ch/api/schemas/records/schema1-v1.2.5.json",
            "self": "http://analysispreservation.cern.ch/api/jsonschemas/schema1/1.2.5"
            },
            "version": "1.2.5"
        },
        "versions": [
            {
            "links": {
                "deposit": "http://analysispreservation.cern.ch/api/schemas/deposits/records/schema1-v1.2.5.json",
                "record": "http://analysispreservation.cern.ch/api/schemas/records/schema1-v1.2.5.json",
                "self": "http://analysispreservation.cern.ch/api/jsonschemas/schema1/1.2.5"
            },
            "version": "1.2.5"
            },
            {
            "links": {
                "deposit": "http://analysispreservation.cern.ch/api/schemas/deposits/records/schema1-v1.2.3.json",
                "record": "http://analysispreservation.cern.ch/api/schemas/records/schema1-v1.2.3.json",
                "self": "http://analysispreservation.cern.ch/api/jsonschemas/schema1/1.2.3"
            },
            "version": "1.2.3"
            }
        ]
    }

    resp = client.get(
        '/jsonschemas/wrong_schema/versions/', headers=auth_headers_for_user(cms_user))

    assert resp.status_code == 404


def test_get_only_latest_version_of_schemas(
        client, db, users, auth_headers_for_user):
    cms_user = users['cms_user']
    latest_schema = Schema(name='schema1', version='1.2.3', experiment='CMS')
    latest_schema2 = Schema(name='schema2', version='3.0.0', experiment='CMS')
    db.session.add(latest_schema)
    db.session.add(latest_schema2)
    db.session.add(Schema(name='schema1', experiment='CMS', version='1.1.0'))
    db.session.add(Schema(name='schema2', experiment='CMS'))
    db.session.add(Schema(name='schema3', experiment='LHCb'))
    db.session.commit()

    resp = client.get(
        '/jsonschemas?latest=True', headers=auth_headers_for_user(cms_user))

    assert resp.status_code == 200
    assert resp.json == [
        {
            'name': 'schema1',
            'version': '1.2.3',
            'deposit_options': {},
            'record_schema': {},
            'fullname': None,
            'use_deposit_as_record': False,
            'is_indexed': False,
            'record_options': {},
            'deposit_mapping': {},
            'deposit_schema': {},
            'record_mapping': {},
            'links':
                {
                    'record':
                        'http://analysispreservation.cern.ch/api/schemas/records/schema1-v1.2.3.json',
                    'self':
                        'http://analysispreservation.cern.ch/api/jsonschemas/schema1/1.2.3',
                    'deposit':
                        'http://analysispreservation.cern.ch/api/schemas/deposits/records/schema1-v1.2.3.json',
                },
        },
        {
            'links':
                {
                    'record':
                        'http://analysispreservation.cern.ch/api/schemas/records/schema2-v3.0.0.json',
                    'self':
                        'http://analysispreservation.cern.ch/api/jsonschemas/schema2/3.0.0',
                    'deposit':
                        'http://analysispreservation.cern.ch/api/schemas/deposits/records/schema2-v3.0.0.json',
                },
            'deposit_options': {},
            'record_schema': {},
            'fullname': None,
            'use_deposit_as_record': False,
            'version': '3.0.0',
            'is_indexed': False,
            'record_options': {},
            'deposit_mapping': {},
            'deposit_schema': {},
            'record_mapping': {},
            'name': 'schema2',
        },
    ]


def test_get_resolved_schemas_with_invalid_ref_should_404(
        client, db, users, create_schema, auth_headers_for_superuser):
    create_schema(
        'test-analysis',
        experiment='CMS',
        deposit_schema={
            'type': 'object',
            'properties':
                {
                    'nested':
                        {
                            '$ref':
                                'http://analysispreservation.cern.ch/api/schemas/deposits/records/nested-schema-v1.0.0.json'
                        }
                },
        },
        record_schema={
            'title': 'record_schema',
            'type': 'object',
            'properties':
                {
                    'nested':
                        {
                            '$ref':
                                'http://analysispreservation.cern.ch/api/schemas/deposits/records/nested-schema-v1.0.0.json'
                        }
                },
        },
        use_deposit_as_record=False,
    )

    resp = client.get(
        '/jsonschemas/test-analysis/1.0.0?resolve=True',
        headers=auth_headers_for_superuser,
    )

    assert resp.status_code == 404


########################
# api/jsonschemas/  [POST]
########################


def test_post_schema_when_user_not_logged_in_returns_401(
        client, users, json_headers):
    resp = client.post('/jsonschemas/', headers=json_headers)

    assert resp.status_code == 401


def test_post_by_no_suepruser(client, db, users, auth_headers_for_user, json_headers):
    owner = users['cms_user']
    schema = json.dumps(
        dict(
            name='cms-schema',
            version='1.2.3',
            fullname='CMS Schema 1.2.3',
            deposit_schema={'title': 'deposit_schema'},
            deposit_options={'title': 'deposit_options'},
            record_schema={'title': 'record_schema'},
            record_options={'title': 'record_options'},
            record_mapping={
                'mappings': {
                    'doc': {
                        'properties': {
                            'title': {
                                'type': 'text'
                            }
                        }
                    }
                }
            },
            deposit_mapping={
                'mappings':
                    {
                        'doc': {
                            'properties': {
                                'keyword': {
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
            },
            is_indexed=True,
        ))

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 403


def test_post(client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(
            name='cms-schema',
            version='1.2.3',
            fullname='CMS Schema 1.2.3',
            deposit_schema={'title': 'deposit_schema'},
            deposit_options={'title': 'deposit_options'},
            record_schema={'title': 'record_schema'},
            record_options={'title': 'record_options'},
            record_mapping={
                'mappings': {
                    'doc': {
                        'properties': {
                            'title': {
                                'type': 'text'
                            }
                        }
                    }
                }
            },
            deposit_mapping={
                'mappings':
                    {
                        'doc': {
                            'properties': {
                                'keyword': {
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
            },
            is_indexed=True,
        ))

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200
    assert resp.json == {
        'name': 'cms-schema',
        'config': {},
        'experiment': None,
        'version': '1.2.3',
        'fullname': 'CMS Schema 1.2.3',
        'is_indexed': True,
        'use_deposit_as_record': False,
        'deposit_schema': {
            'title': 'deposit_schema'
        },
        'deposit_options': {
            'title': 'deposit_options'
        },
        'record_schema': {
            'title': 'record_schema'
        },
        'record_options': {
            'title': 'record_options'
        },
        'record_mapping':
            {
                'mappings': {
                    'doc': {
                        'properties': {
                            'title': {
                                'type': 'text'
                            }
                        }
                    }
                }
            },
        'deposit_mapping':
            {
                'mappings':
                    {
                        'doc': {
                            'properties': {
                                'keyword': {
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
            },
        'links':
            {
                'self':
                    u'http://analysispreservation.cern.ch/api/jsonschemas/cms-schema/1.2.3',
                'deposit':
                    'http://analysispreservation.cern.ch/api/schemas/deposits/records/cms-schema-v1.2.3.json',
                'record':
                    u'http://analysispreservation.cern.ch/api/schemas/records/cms-schema-v1.2.3.json',
                #            'versions': u'http://analysispreservation.cern.ch/api/jsonschemas/cms-schema/versions'
            },
    }


def test_post_when_validation_errors_returns_400(
        client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(
            version='.1.2.3',
            fullname='CMS Schema 1.2.3',
            deposit_schema={
                'properties': [],
                'dependencies': []
            },
            deposit_options={'title': 'deposit_options'},
            is_indexed=True,
        ))

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400

    error_msg = (
        "[] is not of type 'object'" if PY3 else "[] is not of type u'object'"
    )

    assert resp.json['message'] == {
        'deposit_schema':
            [{
                'dependencies': [error_msg],
                'properties': [error_msg]
            }],
        'name': ['Missing data for required field.'],
        'version': ['String does not match expected pattern.'],
    }


def test_post_when_validation_errors_returns_400_2(
        client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(
            version='1.2.3',
            name="cms-s",
            fullname='CMS Schema 1.2.3',
            deposit_schema={
                'properties': {},
            },
            config={"bananes": "dfs"},
            deposit_options={'title': 'deposit_options'},
            is_indexed=True,
        ))

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400

    assert resp.json['message'] ==  'Schema configuration validation error'

def test_post_when_validation_errors_returns_400_3(
        client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(
            version='1.2.3',
            name="cms-s",
            fullname='CMS Schema 1.2.3',
            deposit_schema={
                'properties': {},
            },
            config={"repositories": {
                "boom": {},
                "baaam": ""
            }},
            deposit_options={'title': 'deposit_options'},
            is_indexed=True,
        ))

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400

    assert resp.json['message'] ==  'Schema configuration validation error'
    assert len(resp.json['errors']) == 8
    assert {'field': ['repositories', 'baaam'], 'message': "'' is not of type 'object'"} in resp.json['errors']


def test_post_with_valid_config_validation_github(client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(
            name='cms-schema',
            version='1.2.3',
            fullname='CMS Schema 1.2.3',
            config={
                "repositories": {
                    "github": {
                        "display_name": "Test Analysis Repo",
                        "display_description": "Main Description",
                        "host": "github.com",
                        "authentication": {
                            "type": "cap"
                        },
                        "repo_name": {
                            "template": "test"
                        },
                        "org_name": "test_org",
                        "repo_description": {
                            "template": "this is a test repo"
                        },
                        "private": False,
                        "license": "MIT"
                    }
                }
            },
            deposit_schema={'title': 'deposit_schema'},
            deposit_options={'title': 'deposit_options'},
            record_schema={'title': 'record_schema'},
            record_options={'title': 'record_options'},
            record_mapping={
                'mappings': {
                    'doc': {
                        'properties': {
                            'title': {
                                'type': 'text'
                            }
                        }
                    }
                }
            },
            deposit_mapping={
                'mappings':
                    {
                        'doc': {
                            'properties': {
                                'keyword': {
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
            },
            is_indexed=True,
        ))
    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )
    assert resp.status_code == 200


def test_post_with_valid_config_validation_gitlab(client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(
            name='cms-schema',
            version='1.2.3',
            fullname='CMS Schema 1.2.3',
            config={
                "repositories": {
                    "gitlab": {
                        "display_name": "Test Analysis Repo",
                        "display_description": "Main Description",
                        "host": "gitlab.cern.ch",
                        "org_id": "12345",
                        "authentication": {
                            "type": "cap"
                        },
                        "repo_name": {
                            "template": "test"
                        },
                        "org_name": "test_org",
                        "repo_description": {
                            "template": "this is a test repo"
                        },
                        "private": False,
                        "license": "MIT"
                    }
                }
            },
            deposit_schema={'title': 'deposit_schema'},
            deposit_options={'title': 'deposit_options'},
            record_schema={'title': 'record_schema'},
            record_options={'title': 'record_options'},
            record_mapping={
                'mappings': {
                    'doc': {
                        'properties': {
                            'title': {
                                'type': 'text'
                            }
                        }
                    }
                }
            },
            deposit_mapping={
                'mappings':
                    {
                        'doc': {
                            'properties': {
                                'keyword': {
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
            },
            is_indexed=True,
        ))
    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )
    assert resp.status_code == 200


def test_post_with_invalid_config_validation_gitlab(client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(
            name='cms-schema',
            version='1.2.3',
            fullname='CMS Schema 1.2.3',
            config={
                "repositories": {
                    "gitlab": {
                        "display_name": "Test Analysis Repo",
                        "display_description": "Main Description",
                        "host": "gitlab.cern.ch",
                        "authentication": {
                            "type": "cap"
                        },
                        "repo_name": {
                            "template": "test"
                        },
                        "org_name": "test_org",
                        "repo_description": {
                            "template": "this is a test repo"
                        },
                        "private": False,
                        "license": "MIT"
                    }
                }
            },
            deposit_schema={'title': 'deposit_schema'},
            deposit_options={'title': 'deposit_options'},
            record_schema={'title': 'record_schema'},
            record_options={'title': 'record_options'},
            record_mapping={
                'mappings': {
                    'doc': {
                        'properties': {
                            'title': {
                                'type': 'text'
                            }
                        }
                    }
                }
            },
            deposit_mapping={
                'mappings':
                    {
                        'doc': {
                            'properties': {
                                'keyword': {
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
            },
            is_indexed=True,
        ))
    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400
    assert resp.json['message'] == 'Schema configuration validation error'


#####################################
# api/jsonschemas/{id}/{version}  [PUT]
#####################################


def test_put_schema_when_user_not_logged_in_returns_401(
        client, schema, users, json_headers):
    resp = client.put(
        '/jsonschemas/{}/{}'.format(schema.name, schema.version),
        headers=json_headers)

    assert resp.status_code == 401


def test_put_when_no_superuser(client, db, auth_headers_for_user, users, json_headers):
    owner = users['superuser']
    cms_user = users['cms_user']
    schema = json.dumps(
        dict(name='cms-schema', version='1.2.3', fullname='Old fullname'))
    new_schema = dict(
        name='new-schema',
        version='1.0.0',
        fullname='New fullname',
        deposit_schema={'title': 'deposit_schema'},
        deposit_options={'title': 'deposit_options'},
        record_schema={'title': 'record_schema'},
        record_options={'title': 'record_options'},
        record_mapping={'doc': {
            'properties': {
                'title': {
                    'type': 'text'
                }
            }
        }},
        deposit_mapping={
            'doc': {
                'properties': {
                    'keyword': {
                        'type': 'keyword'
                    }
                }
            }
        },
        is_indexed=True,
        use_deposit_as_record=True,
    )

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200

    resp = client.put(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(new_schema),
        headers=json_headers + auth_headers_for_user(cms_user),
    )

    assert resp.status_code == 403


def test_put(client, db, auth_headers_for_user, users, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(name='cms-schema', version='1.2.3', fullname='Old fullname'))
    new_schema = dict(
        name='new-schema',
        version='1.0.0',
        fullname='New fullname',
        deposit_schema={'title': 'deposit_schema'},
        deposit_options={'title': 'deposit_options'},
        record_schema={'title': 'record_schema'},
        record_options={'title': 'record_options'},
        record_mapping={'doc': {
            'properties': {
                'title': {
                    'type': 'text'
                }
            }
        }},
        deposit_mapping={
            'doc': {
                'properties': {
                    'keyword': {
                        'type': 'keyword'
                    }
                }
            }
        },
        is_indexed=True,
        use_deposit_as_record=True,
    )

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200

    resp = client.put(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(new_schema),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200
    assert resp.json == {
        'name': 'cms-schema',
        'config': {},
        'experiment': None,
        'version': '1.2.3',
        'fullname': 'New fullname',
        'is_indexed': False,
        'use_deposit_as_record': True,
        'deposit_schema': {},
        'deposit_options': {
            'title': 'deposit_options'
        },
        'record_schema': {},
        'record_options':
            {  # same as deposit_options because use_deposit_as_record == True
                'title': 'deposit_options'
            },
        'record_mapping':
            {  # same as deposit_mapping because use_deposit_as_record == True
                'doc': {
                    'properties': {
                        'keyword': {
                            'type': 'keyword'
                        }
                    }
                }
            },
        'deposit_mapping': {
            'doc': {
                'properties': {
                    'keyword': {
                        'type': 'keyword'
                    }
                }
            }
        },
        'links': {
            'self':
                u'http://analysispreservation.cern.ch/api/jsonschemas/cms-schema/1.2.3',
            'deposit':
                'http://analysispreservation.cern.ch/api/schemas/deposits/records/cms-schema-v1.2.3.json',
            'record':
                u'http://analysispreservation.cern.ch/api/schemas/records/cms-schema-v1.2.3.json',
            #            'versions': u'http://analysispreservation.cern.ch/api/jsonschemas/cms-schema/versions'
        },
    }


def test_put_when_validation_errors_returns_400(
        client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    db.session.add(
        Schema(
            **{
                'name': 'cms-schema',
                'experiment': 'CMS',
                'fullname': 'Old Schema',
            }))
    db.session.commit()

    resp = client.put(
        '/jsonschemas/cms-schema/1.0.0',
        data='{}',
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400
    assert resp.json['message'] == {'_schema': ['Empty data']}


@mark.skip('skipping till we allow put to non-superusers')
def test_put_when_not_an_schema_owner_returns_403(
        client, db, auth_headers_for_user, users, json_headers):
    owner = users['cms_user']
    another_user = users['cms_user2']
    schema = json.dumps(dict(name='cms-schema', version='1.2.3'))

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200

    resp = client.put(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps({}),
        headers=json_headers + auth_headers_for_user(another_user),
    )

    assert resp.status_code == 403


def test_put_schema_with_valid_config(client, db, auth_headers_for_user, users, json_headers):
    owner = users['superuser']
    schema = dict(
        name='new-schema',
        version='1.0.0',
        deposit_schema={'title': 'deposit_schema'},
        config={'reviewable': True},
        is_indexed=True,
        use_deposit_as_record=True,
    )

    resp = client.post(
        '/jsonschemas/',
        data=json.dumps(schema),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200


def test_put_schema_with_invalid_config(client, db, auth_headers_for_user, users, json_headers):
    owner = users['superuser']
    schema = dict(
        name='new-schema',
        version='1.0.0',
        deposit_schema={'title': 'deposit_schema'},
        config={
            'reviewable': 123,
            'notifications': { 'wrong_key': {}},
            'wrong_property': { 'title': "test"}
        },  # INVALID, SHOULD FAIL
        is_indexed=True,
        use_deposit_as_record=True,
    )

    resp = client.post(
        '/jsonschemas/',
        data=json.dumps(schema),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400
    errors = resp.json['errors']
    assert len(errors) == 3
    errors = sorted(errors, key=lambda x: x['field'])
    assert errors[0]['field'] == []
    assert errors[1]['field'] == ['notifications']
    assert errors[2] == {
        'field': ['reviewable'],
        'message': "123 is not of type 'boolean'"
    }



def test_put_schema_with_invalid_notificaiton_config(client, db, auth_headers_for_user, users, json_headers):
    owner = users['superuser']
    schema = dict(
        name='new-schema',
        version='1.0.0',
        deposit_schema={'title': 'deposit_schema'},
        config={
            'reviewable': 123,
            'notifications': {
                'actions': {
                    'publish': {},
                    'publishhh': {}
                }
            },
        },  # INVALID, SHOULD FAIL
        is_indexed=True,
        use_deposit_as_record=True,
    )

    resp = client.post(
        '/jsonschemas/',
        data=json.dumps(schema),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400
    errors = resp.json['errors']
    assert len(errors) == 3
    assert errors[0]['field'] == ['notifications', 'actions', ]
    assert errors[1]['field'] == ['notifications', 'actions', 'publish']
    assert errors[2] == {
        'field': ['reviewable'],
        'message': "123 is not of type 'boolean'"
    }

# #####################################
# # api/jsonschemas/{id}/{version}  [DELETE]
# #####################################


def test_delete_schema_when_user_not_logged_in_returns_401(
        client, schema, users, json_headers):
    resp = client.delete(
        '/jsonschemas/{}/{}'.format(schema.name, schema.version),
        headers=json_headers)

    assert resp.status_code == 401

@mark.skip('skipping till we allow delete to non-superusers')
def test_delete_when_not_an_schema_owner_returns_403(
        client, db, auth_headers_for_user, users, json_headers):
    owner = users['cms_user']
    another_user = users['cms_user2']
    schema = json.dumps(dict(name='cms-schema', version='1.2.3'))

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200

    resp = client.delete(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps({}),
        headers=json_headers + auth_headers_for_user(another_user),
    )

    assert resp.status_code == 403


def test_delete_when_no_superuser(client, db, auth_headers_for_user, users, json_headers):
    owner = users['superuser']
    cms_user = users['cms_user']
    schema = json.dumps(dict(name='cms-schema', version='1.2.3'))

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200

    resp = client.delete(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps({}),
        headers=json_headers + auth_headers_for_user(cms_user),
    )

    assert resp.status_code == 403


def test_delete(client, db, auth_headers_for_user, users, json_headers):
    owner = users['superuser']
    schema = json.dumps(dict(name='cms-schema', version='1.2.3'))

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200

    resp = client.delete(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps({}),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 204

    resp = client.get(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps({}),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 404


########################
# api/jsonschemas/{id}/{version}  [PATCH]
########################


def test_patch_schema_when_user_not_logged_in_returns_401(
        client, schema, users, json_headers):
    resp = client.patch(
        '/jsonschemas/{}/{}'.format(schema.name, schema.version),
        headers=json_headers)

    assert resp.status_code == 401


def test_patch_when_no_superuser(client, db, auth_headers_for_user, users, json_headers):
    owner = users['superuser']
    cms_user = users['cms_user']
    schema = json.dumps(
        dict(name='cms-schema', version='1.2.3', fullname='Old fullname'))
    patch_schema = [{ "op": "add", "path": "/config/reviewable", "value": True }]

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200

    resp = client.patch(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(patch_schema),
        headers=json_headers + auth_headers_for_user(cms_user),
    )

    assert resp.status_code == 403


def test_patch(client, db, auth_headers_for_user, users, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(name='cms-schema', version='1.2.3', fullname='Old fullname'))
    patch_schema = [{ "op": "add", "path": "/config/reviewable", "value": True }]

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200
    assert resp.json['config'] == {}

    resp = client.patch(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(patch_schema),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200
    assert resp.json['config'] == {"reviewable": True}


def test_patch_with_non_editable_field(client, db, auth_headers_for_user, users, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(name='cms-schema', version='1.2.3', fullname='Old fullname'))
    patch_schema = [{ "op": "add", "path": "/name", "value": "cms-patch-schema" }]

    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200
    assert resp.json['config'] == {}

    resp = client.patch(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(patch_schema),
        headers=json_headers + auth_headers_for_user(owner),
    )
    assert resp.status_code == 400

    patch_schema = [{"op": "add", "path": "name/", "value": "patch-cms-schema" }]
    resp = client.patch(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(patch_schema),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400


def test_patch_when_invalid_data_returns_400(
        client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(name='cms-schema', version='1.2.3', fullname='Old fullname'))
    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200
    assert resp.json['config'] == {}

    resp = client.patch(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(''),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400
    assert resp.json['message'] == 'Invalid/No patch data provided.'


def test_patch_when_invalid_data_not_array_returns_400(
        client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(name='cms-schema', version='1.2.3', fullname='Old fullname'))
    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200
    assert resp.json['config'] == {}

    resp = client.patch(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps({"wrong": "data"}),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400
    assert resp.json['message'] == 'Invalid/No patch data provided.'

    resp = client.patch(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(["123", "boom"]),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400
    assert resp.json['message'] == 'Invalid/No patch data provided.'


def test_patch_when_invalid_operation(
        client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(name='cms-schema', version='1.2.3', fullname='Old fullname'))
    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200
    assert resp.json['config'] == {}

    patch_schema = [{ "op": "copy", "path": "/config/reviewable", "value": True }]
    resp = client.patch(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(patch_schema),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400
    assert resp.json['message'] == 'Invalid/No patch data provided.'

    patch_schema = [
        { "op": "copy", "path": "/config/reviewable", "value": True },
        { "op": "add", "path": "/config/reviewable", "value": True }
    ]
    resp = client.patch(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(patch_schema),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200
    assert resp.json['config'] == {"reviewable": True}


def test_patch_when_operation_undefined_returns_400(
        client, db, users, auth_headers_for_user, json_headers):
    owner = users['superuser']
    schema = json.dumps(
        dict(name='cms-schema', version='1.2.3', fullname='Old fullname'))
    resp = client.post(
        '/jsonschemas/',
        data=schema,
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 200
    assert resp.json['config'] == {}

    patch_schema = [{"path": "/config/reviewable", "value": True }]
    resp = client.patch(
        '/jsonschemas/cms-schema/1.2.3',
        data=json.dumps(patch_schema),
        headers=json_headers + auth_headers_for_user(owner),
    )

    assert resp.status_code == 400
    assert 'Invalid/No patch data provided.' in resp.json['message']
