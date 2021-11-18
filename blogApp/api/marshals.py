from flask_restful import fields
from blogApp.models import Authors


class PrevLink(fields.Raw):
    """class for creating previous page link"""
    def format(self, value):
        if value['prev_num'] >= 1:
            return value['base_link']+str(value['prev_num'])
        else:
            return ''


class NextLink(fields.Raw):
    """class for creating next page link"""
    def format(self, value):
        if value['next_num'] <= value['total']:
            return value['base_link']+str(value['next_num'])
        else:
            return ''


blog_fields = {
    '_links': {
        'self': {
            'href': fields.Url('.blog', absolute=True, scheme='https')
        }
    },
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    '_created': fields.DateTime(dt_format='rfc822'),
    'tags': fields.List(fields.Nested({
        '_links': {
            'self': {
                'href': fields.Url('.tag', absolute=True, scheme='https')
            }
        },
        'name': fields.String
    }))
}


blogs_list_fields = {
    '_links': {
        'self': {
            'href': fields.String(attribute='self')
        },
        'first': {
            'href': fields.String(attribute='first')
        },
        'prev': {
            'href': PrevLink(attribute='prev'),
        },
        'next': {
            'href': NextLink(attribute='next'),
        },
        'last': {
            'href': fields.String(attribute='last'),
        }
    },
    'count': fields.Integer,
    'total': fields.Integer,
    'blogs': fields.List(
        fields.Nested({
            '_links': {
                'self': {
                    'href': fields.Url('.blog', absolute=True, scheme='https')
                }
            },
            'id': fields.Integer,
            'title': fields.String,
            'author': fields.Nested({
                '_links': {
                    'self': {
                        'href': fields.Url('.author', absolute=True, scheme='https')
                    }
                },
                'name': fields.String(attribute='name')
            }),
            'tags': fields.List(fields.Nested({
                '_links': {
                    'self': {
                        'href': fields.Url('.tag', absolute=True, scheme='https')
                    }
                },
                'name': fields.String
            }))
        }),
    )
}

author_fields = {
    '_links': {
        'self': {
            'href': fields.Url('.author', absolute=True, scheme='https')
        }
    },
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
    'about':fields.String
}
