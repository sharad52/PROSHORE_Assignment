from django.shortcuts import render
from django.views import View as DFView
from contents.df_views import GlobalDFView
from contents.models import Content
from contents.serializers import ContentSerializer


class ContentView(GlobalDFView):
    model = Content
    template = 'content.html'
    serializer = ContentSerializer


class ContentListView(DFView):
    
    def get(self, request):
        list_content = Content.objects.all()
        context = {
            'list_content': list_content
        }
        return render(request, 'content_list.html', context)
    

def error_404_view(request, exception):
    return render('request', '404.html')