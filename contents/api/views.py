from contents.api import drf_views
from contents.models import Content
from contents.serializers import ContentSerializer
from rest_framework import generics


class ContentAPIBase(object):
    has_company = False
    model = Content
    serializer_class = ContentSerializer
    

class SaveContent(ContentAPIBase, drf_views.GlobalCreateAPIView):
    pass


class UpdateContent(ContentAPIBase, drf_views.GlobalUpdateAPIView):
    pass


class GetContent(ContentAPIBase, drf_views.GlobalRetrieveAPIView):
    pass


class DestroyContent(ContentAPIBase, drf_views.GlobalDestroyAPIView):
    pass


class ListContent(ContentAPIBase, drf_views.GlobalListAPIView):
    pass


ContentDispatcherAPIView = drf_views.DispatcherAPIViewFactory(
    'ContentDispatcherAPIView', Content.__name__, __name__
)