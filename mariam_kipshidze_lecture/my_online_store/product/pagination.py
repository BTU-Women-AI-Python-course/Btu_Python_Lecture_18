from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class SmallPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2  # Default number of results per request
    max_limit = 100  # Maximum limit for results


class ProductCursorPagination(CursorPagination):
    page_size = 2 # Default number of results per page
    ordering = 'id'
