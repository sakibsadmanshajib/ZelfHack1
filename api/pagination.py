from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'data': data,
            'total_contents': self.page.paginator.count,
            'page_size': self.page_size
        })
