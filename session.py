import requests
from requests import session
from .settings import current_environment
from .settings import ecm3_client_details
from .settings import sandbox_client_details
from .exceptions import InvalidEnvironmentError
from .exceptions import UnsupportedHTTPMethodError
from json import JSONDecodeError


class Session:
    def __init__(self):
        """
        Creates a new instance of the EazySDK session
        """
        self.client_settings = None
        self.environment = current_environment['env'].lower()
        # https://[[environment]].eazycollect.co.uk/
        acceptable_environments = {
            'ecm3',
            'sandbox',
        }
        if self.environment not in acceptable_environments:
            raise InvalidEnvironmentError(
                '%s is not a valid environment. The acceptable inputs'
                ' are \n'
                '- sandbox - a server for testing API calls\n'
                '- live - the production ECM3 environment' % self.environment
            )
        elif self.environment == 'ecm3':
            self.client_settings = ecm3_client_details
        else:
            self.client_settings = sandbox_client_details
        # Get the client code for the configured environment
        self.client_code = self.client_settings['client_code']
        # The base URL for all requests sent to the API
        self.base_url = 'https://%s.eazycollect.co.uk/api/v3/client/%s/' \
                        % (self.environment, self.client_code)
        self.headers = {
            'apiKey': self.client_settings['api_key'],
            'Content-Length': '0',
        }
        self.params = None
        self.endpoint = None
        self.method = None

        self.session = session()

    def request(self, method, endpoint, params=None, headers=None):
        """
        Create a request to ECM3
        :Args:
        - method - The method of the HTTP call. EazySDK exposes the
                   DELETE, GET, PATCH and POST HTTP methods
        - endpoint - The desired environment for making API calls.
                        By default, the environment is set to 'sandbox'.
        """
        self.headers = headers
        self.headers = Session().headers
        self.endpoint = self.base_url + endpoint
        self.method = method
        if params is not None:
            self.params = params
        else:
            self.params = None
        if method not in(['GET', 'POST', 'PATCH', 'DELETE']):
            raise UnsupportedHTTPMethodError(
                '%s is not a supported HTTP method when communicating '
                'with ECM3. Valid methods are GET, POST, PATCH and'
                'DELETE' % method
            )
        request_call = getattr(requests, self.method.lower())
        response = request_call(
            self.endpoint,
            params=self.params,
            headers=self.headers,
        )
        try:
            if response.text:
                return response.text
            else:
                response_json = {}
        except JSONDecodeError:
            response_json = {}
        return response_json

    def get(self):
        """
        Perform a GET request to a given endpoint in ECM3
        """
        return self.request('GET', self.endpoint, self.params)

    def post(self):
        """
        Perform a POST request to a given endpoint in ECM3
        """
        return self.request('POST', self.endpoint, self.params)

    def patch(self):
        """
        Perform a PATCH request to a given endpoint in ECM3
        """
        return self.request('PATCH', self.endpoint, self.params)

    def delete(self):
        """
        Perform a DELETE request to a given endpoint in ECM3
        """
        return self.request('DELETE', self.endpoint, self.params)
