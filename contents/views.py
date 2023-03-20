from django.shortcuts import render
from django.views import View as DFView
from contents.df_views import GlobalDFView
from contents.models import Content
from contents.serializers import ContentSerializer
from contents.mixins import GlobalPaginatorMixin


class ContentView(GlobalDFView):
    model = Content
    template = 'content.html'
    serializer = ContentSerializer


class ContentListView(DFView, GlobalPaginatorMixin):
    model = Content

    def get_queryset(self):
        qset = self.model.objects.all()
        return qset
    
    def process_form(self, request):
        """
        update self.kwargs_dict as required
        :param request: returns a list after processing the query form
        :return: full list of matched items
        """
        full_list = None
        if request.GET and 'query' in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                pass
        if full_list is None:
            full_list = self.get_queryset()

        return full_list
    
    def get_list(self, request):
        return self.process_form(request)
    
    def get(self, request):
        lst_content = self.get_paginated_list(request)
        context = {
            'lst_content': lst_content
        }
        return render(request, 'content_list.html', context)
    

def error_404_view(request, exception):
    return render('request', '404.html')