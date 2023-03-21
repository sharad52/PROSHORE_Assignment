from django.shortcuts import render
from django.views import View as DFView
from contents.df_views import GlobalDFView
from contents.models import Content
from contents.serializers import ContentSerializer
from contents.mixins import GlobalPaginatorMixin
from contents.forms import ContentForm
from django.db.models import Q


class ContentView(GlobalDFView):
    model = Content
    template = 'content.html'
    serializer = ContentSerializer


class ContentListView(DFView, GlobalPaginatorMixin):
    model = Content
    form_class = ContentForm

    def get_queryset(self):
        qset = self.model.objects.all()
        return qset
    
    def get_form(self):
        frm = self.form_class()
        if self.request.GET and 'go' in self.request.GET:
            frm = self.form_class(self.request.GET)
        return frm
    
    def process_form(self, request):
        """
        update self.kwargs_dict as required
        :param request: returns a list after processing the query form
        :return: full list of matched items
        """

        full_list = None
        if request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                title = form.cleaned_data.get('title', None)
                author = form.cleaned_data.get('author_name', None)
                
                if title or author:
                    full_list = Content.objects.filter(
                        Q(title__icontains=title) |
                        Q(author_name__icontains=author)

                    )
        if full_list is None:
            full_list = self.get_queryset()

        return full_list
    
    def get_list(self, request):
        return self.process_form(request)
    
    def get(self, request):
        lst_content = self.get_paginated_list(request)
        search_form = self.get_form()
        context = {
            'lst_content': lst_content,
            'frm': search_form
        }
        return render(request, 'content_list.html', context)
    

def error_404_view(request, exception):
    return render('request', '404.html')