from bson.objectid import ObjectId

from django import template

from ..utils import get_mongodb

register = template.Library()


def get_author(id_):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(id_)})
    return author['fullname']


def get_author_by_id(id_):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(id_)})
    return author['fullname'] if author else "Anonymous"


register.filter('author', get_author)
register.filter('author_by_id', get_author_by_id)
