"""
Exposes Django request information from middleware
"""

def get_current_request():
	"""
	This method will be monkey patched by middleware in order to expose the current Django request
	"""
	return None

def get_current_request_hostname():
	"""
	This method will return the hostname that was used in the current Django request
	"""
	hostname = None
	request = get_current_request()
	if request:
		hostname = request.META.get('HTTP_HOST')

	return hostname