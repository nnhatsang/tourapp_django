from rest_framework import pagination


class AttractionPaginator(pagination.PageNumberPagination):
    page_size = 5
    page_query_param = 'page'


class TourPaginator(pagination.PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
