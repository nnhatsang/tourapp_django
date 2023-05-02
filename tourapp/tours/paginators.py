from rest_framework import pagination


class AttractionPaginator(pagination.PageNumberPagination):
    page_size = 4
    page_query_param = 'page'


class TourPaginator(pagination.PageNumberPagination):
    page_size = 4
    page_query_param = 'page'


class CommentPaginator(pagination.PageNumberPagination):
    page_size = 20
    page_query_param = 'page'


class RatePaginator(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class CommentBlogPaginator(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class BlogPaginator(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
