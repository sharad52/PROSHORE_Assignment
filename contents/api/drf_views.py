from rest_framework import generics as drf_generics
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from contents.api import utils as gu


class DispatcherAPIView(APIView):
    """
    The base class for ManageViews
    A ManageView is a view which is used to dispatch the requests to the appropriate views
    This is done so that we can use one URL with different methods (GET, PUT, etc)
    """

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'VIEWS_BY_METHOD'):
            raise Exception('VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!')
        if request.method.lower() in self.VIEWS_BY_METHOD:
            method_resolver = request.method.lower()

            # get list if pk is not provided in url
            if method_resolver == 'get':
                if self.kwargs.get('pk', None) is None:
                    method_resolver = 'list'

            return self.VIEWS_BY_METHOD[method_resolver]()(request, *args, **kwargs)

        return Response(status=405)


def DispatcherAPIViewFactory(cls_name, model_name, module_name, methods=None):
    """
    dynamically generates DispatcherAPIView subclass
    :param cls_name: string which should be used as class name
    :param model_name: string model name which is use to generate VIEWS_BY_METHOD
    :param module_name: module namespace for getting class during runtime dynamically
    :param methods: list of method names
    :return: view class
    """
    import sys

    def _get_cls(pre_text):
        return getattr(
            sys.modules[module_name],
            '%s%s' % (pre_text, model_name)
        )

    METHODS_TO_NAMES = {
        'post': 'Save',
        'put': 'Update',
        'get': 'Get',
        'list': 'List',
        'delete': 'Destroy'
    }

    # main method dict that contains all the method available
    if not methods:
        methods = ['post', 'put', 'get', 'list', 'delete']
    VIEWS_BY_METHOD = {x: _get_cls(METHODS_TO_NAMES[x]).as_view for x in methods}

    # dynamically generating class using DispatcherAPIView as base class
    # adding generated VIEWS_BY_METHOD
    cls = type(cls_name, (DispatcherAPIView,), {"VIEWS_BY_METHOD": VIEWS_BY_METHOD})
    return cls


class GlobalAPIView(APIView):

    def __init__(self, **kwargs):
        super(GlobalAPIView, self).__init__(**kwargs)
        self.company = None

    def init_variables(self, request):
        self.company = 'PROSHORE'

    def dispatch(self, request, *args, **kwargs):
        """
         Copied from APIView and added init_variable call
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            self.init_variables(request)  # added line
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class GlobalCreateAPIView(GlobalAPIView, drf_generics.CreateAPIView):
    has_company = True
    model = None
    http_method_names = ['post']

    def get_queryset(self):
        if self.has_company:
            queryset = self.model.objects.filter(company=self.company)
        else:
            queryset = self.model.objects.all()
        return queryset

    def perform_create(self, serializer):
        if self.has_company:
            serializer.save(company=self.company)
        else:
            serializer.save()


class GlobalListCreateAPIView(GlobalAPIView, drf_generics.ListCreateAPIView):
    has_company = True
    model = None

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_serializer(self, *args, **kwargs):
        """
        copied from GenericAPIView and added first line
        """
        kwargs['many'] = True
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        if self.has_company:
            serializer.save(company=self.company)
        else:
            serializer.save()


class GlobalUpdateAPIView(GlobalAPIView, drf_generics.UpdateAPIView):
    has_company = True
    model = None
    http_method_names = ['put']

    def get_queryset(self):
        if self.has_company:
            queryset = self.model.objects.filter(pk=self.kwargs['pk'], company=self.company)
        else:
            queryset = self.model.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def perform_update(self, serializer):
        serializer.save()


class GlobalRetrieveAPIView(GlobalAPIView, drf_generics.RetrieveAPIView):
    has_company = True
    model = None
    http_method_names = ['get']

    def get_queryset(self):
        if self.has_company:
            queryset = self.model.objects.filter(company=self.company)
        else:
            queryset = self.model.objects.all()
        return queryset


class GlobalDestroyAPIView(GlobalAPIView, drf_generics.DestroyAPIView):
    has_company = True
    model = None
    http_method_names = ['delete']

    def validate_delete(self, obj):
        pass

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        self.validate_delete(obj)
        return super(GlobalDestroyAPIView, self).delete(request, *args, **kwargs)

    def get_queryset(self):
        if self.has_company:
            queryset = self.model.objects.filter(company=self.company)
        else:
            queryset = self.model.objects.all()
        return queryset


class GlobalListAPIView(GlobalAPIView, drf_generics.ListAPIView):
    model = None
    ordering = ['id']
    query_key = 'name'
    select_related_lst = []
    prefetch_related_lst = []

    def get_initial_queryset(self):
        """
        overwrite this function to deliver initial queryset
        the results from this queryset is used for further logic
        """
        return self.model.objects.all().select_related(
            *self.select_related_lst
        ).prefetch_related(
            *self.prefetch_related_lst
        )

    def handle_model_field_filter(self, queryset):
        """
        Assumption:
        params with prefix of 'm_' is regarded as model field filter

        :param queryset: model queryset
        :return: filtered queryset based on model filed_name
        """
        params = self.request.query_params
        filter_kwargs = {}
        for k, v in params.items():
            if k[:2] == 'm_':
                v = gu.str_to_bool(v)
                filter_kwargs[k[2:]] = v  # 'm_' part of the param is removed and filter_kwargs is generated
        return queryset.filter(**filter_kwargs)

    def handle_search(self):
        queryset = self.get_initial_queryset()
        queryset = self.handle_model_field_filter(queryset)
        filter_kwargs = {}
        val = self.request.query_params.get('search', None)
        if val:
            filter_kwargs['%s__icontains' % self.query_key] = val
            queryset = queryset.filter(**filter_kwargs).order_by(*self.ordering)
        return queryset

    def get_queryset(self):
        filter_kwargs = {}
        if hasattr(self.model, 'company'):
            filter_kwargs = {'company': self.company}

        id_val = self.request.query_params.get('id', None)
        qstatus = self.request.query_params.get('status', None)

        if id_val:
            filter_kwargs['id'] = id_val

        if qstatus:
            filter_kwargs['status'] = qstatus

        searched_queryset = self.handle_search()
        queryset = searched_queryset.filter(**filter_kwargs).order_by(*self.ordering)
        return queryset


class GlobalApproveAPIView(GlobalAPIView):
    model = None
    http_method_names = ['post']

    def post(self, request, pk):
        from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
        try:
            ins = self.model.objects.get(id=pk, company=self.company)
            ins.backend_approve()
            return Response({'message': '%s was successfully approved' % self.model.__name__}, status=HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response({'message': '%s not found' % self.model.__name__}, status=HTTP_400_BAD_REQUEST)


class GlobalUnapproveAPIView(GlobalAPIView):
    model = None
    http_method_names = ['post']

    def post(self, request, pk):
        from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
        try:
            ins = self.model.objects.get(id=pk, company=self.company)
            ins.backend_unapprove()
            return Response({'message': '%s was successfully Unapproved' % self.model.__name__}, status=HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response({'message': '%s not found' % self.model.__name__}, status=HTTP_400_BAD_REQUEST)


class GlobalDeleteAPIView(GlobalDestroyAPIView):
    http_method_names = ['delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == "Approved":
            msg = 'Delete unsuccessful. %s already approved' % self.model.__name__
            return Response({'message': msg}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        msg = '%s was deleted successfully' % self.model.__name__
        return Response({'message': msg}, status=status.HTTP_200_OK)


class CreateAPIViewCompanyUniqueness(GlobalCreateAPIView):
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if hasattr(request.data, '_mutable'):
            swap = request.data._mutable
            request.data._mutable = True
            request.data['company'] = self.request.user.currently_activated_company.id
            request.data._mutable = swap
        else:
            request.data['company'] = self.request.user.currently_activated_company.id

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateAPIViewCompanyUniqueness(GlobalUpdateAPIView):
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if hasattr(request.data, '_mutable'):
            swap = request.data._mutable
            request.data._mutable = True
            request.data['company'] = self.request.user.currently_activated_company.id
            request.data._mutable = swap
        else:
            request.data['company'] = self.request.user.currently_activated_company.id

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class GlobalDRFPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class GlobalVoucherApproveAPIView(GlobalAPIView, GenericAPIView):
    model = None
    http_method_names = ['post']

    def get_queryset(self):
        queryset = self.model.objects.filter(pk=self.kwargs['pk'], company=self.company)
        return queryset

    def approve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        is_valid = serializer.is_valid(raise_exception=True)
        if is_valid:
            instance.backend_approve()
        return Response(
            {'message': '%s was successfully approved' % self.model.__name__},
            status=HTTP_200_OK
        )

    def post(self, request, pk):
        return self.approve(request, pk)


class GlobalVoucherUnapproveAPIView(GlobalAPIView, GenericAPIView):
    model = None
    http_method_names = ['post']

    def get_queryset(self):
        queryset = self.model.objects.filter(pk=self.kwargs['pk'], company=self.company)
        return queryset

    def unapprove(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        is_valid = serializer.is_valid(raise_exception=True)
        if is_valid:
            instance.backend_unapprove()
        return Response(
            {'message': '%s was successfully unapproved' % self.model.__name__},
            status=HTTP_200_OK
        )

    def post(self, request, pk):
        return self.unapprove(request, pk)
