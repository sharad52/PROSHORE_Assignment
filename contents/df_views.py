from django.shortcuts import render, get_object_or_404
from django.views import View as DFView


class GlobalDFView(DFView):
    http_method_names = ['get']
    model = None
    serializer = None
    template = None

    def init_variables(self, request):
        self.company = 'PROSHORE'

    def get_update_dict(self, pk):
        update_dict = dict()
        obj = get_object_or_404(self.model, id=pk)
        update_dict['init_data'] = self.serializer(obj).data
        update_dict['UpdateId'] = pk
        return update_dict

    def get_create_dict(self):
        create_dict = dict()
        create_dict['init_data'] = dict()
        create_dict['UpdateId'] = None
        return create_dict

    def get_context_dict(self, pk):
        if pk is None:
            context_dict = self.get_create_dict()
            context_dict['scenario'] = 'Create'
        else:
            context_dict = self.get_update_dict(pk)
            context_dict['scenario'] = 'Update'
        return context_dict

    def get(self, request, pk=None):
        context_dict = self.get_context_dict(pk)
        return render(request, self.template, context_dict)