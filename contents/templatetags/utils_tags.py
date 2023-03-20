from django import template


register = template.Library()


@register.simple_tag
def create_list(*args):
    return args


@register.simple_tag
def query_transform(request, **kwargs):
    # replaces param value if it is already available
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated.__setitem__(k, v)
    return updated.urlencode()