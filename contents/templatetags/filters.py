from .utils_tags import register
import simplejson
from django.core import serializers
from django.db.models import QuerySet, Model
from django.utils.safestring import mark_safe
import decimal


def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return ''.join(str(o) for o in [obj])
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


@register.filter
def jsonify(obj):
    '''
    usages examples {{init_data|jsonify}}
    '''
    if isinstance(obj, QuerySet):
        return serializers.serialize('json', obj)
    if isinstance(obj, Model):
        model_dict = obj.__dict__
        del model_dict['_state']
        return mark_safe(simplejson.dumps(model_dict))
    return mark_safe(simplejson.dumps(obj, default=handler))

