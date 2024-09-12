from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CarPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'limit'
    # max_page_size = 2

    def get_paginated_response(self, data):
        return Response(
            {
                'count': self.page.paginator.count,
                'page': self.page.number,
                'data': data
            }
        )