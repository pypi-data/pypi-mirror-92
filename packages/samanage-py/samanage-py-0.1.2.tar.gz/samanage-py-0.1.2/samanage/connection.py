import logging
import json
import requests
import time

from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, RequestException, ProxyError
from requests.exceptions import SSLError, Timeout, ConnectionError
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

RETRIES_STATUS_LIST = (
    429,  # Status code for too many requests
    500, 502, 503, 504  # Server Errors
)

RETRIES_BACKOFF_FACTOR = 0.5


class Connection:
    """ Handles all connection between the app and the server """

    _allowed_methods = ['get', 'post', 'put', 'delete']

    def __init__(self, token, *args, retries=3, requests_delay=200, timeout=None, raise_http_errors=True, **kwargs):

        if isinstance(token, int):
            raise ValueError('Provide valid token credential')

        self._previous_request_at = None
        self.requests_delay = requests_delay or 0
        self.raise_http_errors = raise_http_errors
        self.session = None
        self.timeout = timeout
        self.token = token
        self.retries = retries
        self.headers = kwargs.get('headers', None)
            
    def get_session(self):
        session = requests.Session()

        if self.retries:
            retry = Retry(total=self.retries, read=self.retries,
                          connect=self.retries,
                          backoff_factor=RETRIES_BACKOFF_FACTOR,
                          status_forcelist=RETRIES_STATUS_LIST)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
        return session

    def _check_delay(self):
        """ Checks if a delay is needed between requests and sleeps if True """
        if self._previous_request_at:
            dif = round(time.time() - self._previous_request_at,
                        2) * 1000  # difference in miliseconds
            if dif < self.requests_delay:
                sleep_for = (self.requests_delay - dif)
                logger.info('Sleeping for {} miliseconds'.format(sleep_for))
                time.sleep(sleep_for / 1000)  # sleep needs seconds
        self._previous_request_at = time.time()

    def _internal_request(self, request_obj, url, method, **kwargs):
        method = method.lower()

        if method not in self._allowed_methods:
            raise ValueError('Method must be one of the allowed methods')

        if self.timeout is not None:
            kwargs['timeout'] = self.timeout

        if self.headers is not None:
            kwargs['headers'] = self.headers

        request_done = False

        while not request_done:
            self._check_delay()
            try:
                logger.info(f"Requesting ({method.upper()} URL: {url}")
                # logger.info(f"Requesting parameters: {kwargs}")
                response = request_obj.request(method, url, **kwargs)
                response.raise_for_status()
                logger.info(
                    f"Received response ({response.status_code}) from URL {response.url}")
                request_done = True
                return response
            except (ConnectionError, ProxyError, SSLError, Timeout) as e:
                logger.debug(f'Connection Error calling: {url}')
                raise e
            except HTTPError as e:
                try:
                    error = response.json()
                    error_message = error.get('error', {})
                except ValueError:
                    error_message = ''

                status_code = int(e.response.status_code / 100)
                if status_code == 4:
                      # Client Error
                    # Logged as error. Could be a library error or Api changes
                    logger.error('Client Error: {} | Error Message: {}'.format(str(e), error_message))
                else:
                    # Server Error
                    logger.debug('Server Error: {}'.format(str(e)))
                if self.raise_http_errors:
                    if error_message:
                        raise HTTPError('{} | Error Message: {}'.format(e.args[0], error_message), response=response) from None
                    else:
                        raise e
                else:
                    return e.response
            except RequestException as e:
                logger.debug(f"Request Exception: {str(e)}")


    def request(self, url, method, **kwargs):
        if self.session is None:
            self.session = self.get_session()
        return self._internal_request(self.session, url, method, **kwargs)

    def get(self, url, params=None, **kwargs):
        return self.request(url, 'get', params=params, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.request(url, 'post', data=data, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request(url, 'put', data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, 'delete', **kwargs)

    def __del__(self):
        if self.session:
            self.session.close()

