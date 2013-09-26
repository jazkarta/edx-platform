"""
This middleware will inspect the incoming request and allow for mapping of a hostname
to a particular modulestore class
"""
import threading
import xmodule.util.request

_current_request_thread_local = threading.local()
_current_request_thread_local.current_thread = None

# IMPORTANT:
# Monkey patch the function to return what the current request thread is
# We use monkey-patching in order to avoid inverted dependencies since
# lib/xmodule is not supposed to have import dependencies up in Django
# layers
xmodule.util.request.get_current_request = lambda: _current_request_thread_local.current_thread

class CurrentRequestStorage(object):
    """
    Exposes Django middleware to put the current request on a thread local, so that various levels of the
    code stack can reference what the current request is
    """

    def process_request(self, request):
        """
        Middleware HTTP request entry point for beginning of request
        """
        global _current_request_thread_local

        _current_request_thread_local.current_thread = request

        return None

    def process_response(self, request, response):
        """
        Middleware HTTP request entry point for end of request
        """
        _current_request_thread_local.current_thread = None
        return response
