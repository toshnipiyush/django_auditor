from threading import current_thread

from django.utils.deprecation import MiddlewareMixin

_requests = {}

'''
   This file uses threading along with MiddlewareMixin  which stores the reference to the request user at 
   initialization of the model instance and still allows you to overwrite the value before saving. It captures the 
   current request and user in thread local storage. This threading technique enables apps to access the current request
   and user without requiring the request object to be passed directly.
'''


def current_request():
    """
    :return the request which is present in _request property:
    """
    return _requests.get(current_thread().ident, None)


class RequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        :param request created by the current thread:
        """
        _requests[current_thread().ident] = request

    def process_response(self, request, response):
        """
        :param request:
        :param response:
        :return response of current thread based on request after flushing request:
        """
        # when response is ready, request should be flushed
        _requests.pop(current_thread().ident, None)
        return response

    def process_exception(self, request, exception):
        """
        :param request:
        :param exception:
        """
        # if an exception has happened, request should be flushed too
        _requests.pop(current_thread().ident, None)