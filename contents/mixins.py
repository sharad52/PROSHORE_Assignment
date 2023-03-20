from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class GlobalPaginator(object):
    DEFAULT_PAGE_CAPACITY = 6

    def __init__(self, page_capacity=None):
        self.page_capacity = page_capacity or self.DEFAULT_PAGE_CAPACITY

    def get_list(self, all_lst, page):
        paginator = Paginator(all_lst, self.page_capacity)
        try:
            page_lst = paginator.page(page)
        except PageNotAnInteger:
            page_lst = paginator.page(1)
        except EmptyPage:
            page_lst = paginator.page(paginator.num_pages)

        return page_lst


class GlobalPaginatorMixin(object):
    def get_list(self, request):
        return []

    def get_paginated_list(self, request, full_list=None):
        full_list = full_list or self.get_list(request=request)
        page_capacity = request.GET.get('page_capacity')
        if page_capacity == 'all':
            page_capacity = len(full_list)
        page = request.GET.get('page')
        global_paginator = GlobalPaginator(page_capacity) if page_capacity else GlobalPaginator()
        paginated_list = global_paginator.get_list(full_list, page)
        return paginated_list