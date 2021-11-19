from math import ceil
from flask_restful import fields


class SelfLink(fields.Raw):
    """class for creating link for current page"""

    def format(self, value):
        return value['base_link']+'?limit='+str(value['per_page'])+'&offset='+str(value['current_page'])


class FirstLink(fields.Raw):
    """class for creating link for first page"""

    def format(self, value):
        return value['base_link']+'?limit='+str(value['per_page'])+'&offset=1'


class LastLink(fields.Raw):
    """class for creating link for last page"""

    def format(self, value):
        last_page_number = ceil(int(value['total'])/int(value['per_page']))
        return value['base_link']+'?limit='+str(value['per_page'])+'&offset='+str(last_page_number)


class PrevLinkNew(fields.Raw):
    """class for creating previous page link"""

    def format(self, value):
        if int(value['current_page']) <= 1:
            return ''
        else:
            prev_page = int(value['current_page'])-1
            return value['base_link']+'?limit='+str(value['per_page'])+'&offset='+str(prev_page)


class NextLinkNew(fields.Raw):
    """class for creating next page link"""

    def format(self, value):
        last_page_number = ceil(int(value['total'])/int(value['per_page']))
        if int(value['current_page']) >= last_page_number:
            return ''
        else:
            next_page = int(value['current_page'])+1
            return value['base_link']+'?limit='+str(value['per_page'])+'&offset='+str(next_page)


# output format for navigation links
_links = {
    'self': {
        'href': SelfLink(attribute='links')
    },
    'first': {
        'href': FirstLink(attribute='links')
    },
    'last': {
        'href': LastLink(attribute='links')
    },
    'prev': {
        'href': PrevLinkNew(attribute='links')
    },
    'next': {
        'href': NextLinkNew(attribute='links')
    }
}

# output format for induvidual blogs
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

# output format for listing blogs
blogs_list_fields = {
    '_links': _links,
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

# output format for induvidual authors
author_fields = {
    '_links': {
        'self': {
            'href': fields.Url('.author', absolute=True, scheme='https')
        }
    },
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'about': fields.String
}

# output format for list of authors
authors_list_fields = {
    '_links': _links,
    'count': fields.Integer(attribute='links.per_page'),
    'total': fields.Integer(attribute='links.total'),
    'authors': fields.List(fields.Nested({
        '_links': {
            'self': {
                'href': fields.Url('.author', absolute=True, scheme='https')
            }
        },
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String
    }))
}

# output format for induvidual tags
tag_feilds = {
    '_links': {
        'self': {
            'href': fields.Url('.tag', absolute=True, scheme='https')
        }
    },
    'id': fields.Integer(attribute='tag.id'),
    'name': fields.String(attribute='tag.name'),
    '_embedded': blogs_list_fields
}
