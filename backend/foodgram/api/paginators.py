from rest_framework.pagination import PageNumberPagination

class PageLimitPagination(PageNumberPagination):
    """
    Standard paginator with the definition of the `page_size_query_param` attribute
    for displaying the requested number of pages.

    Attributes:
    - page_size_query_param (str): The query parameter to determine the number of items per page.
                                  Defaults to "limit".
    """
    page_size_query_param = "limit"
