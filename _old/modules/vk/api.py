__author__ = "Alexander Gorokhov"
__email__ = "sashgorokhov@gmail.com"

__enable_requests__ = True
try:
    import requests
except ImportError:
    __enable_requests__ = False


class VKError(Exception):
    def __init__(self, error):
        super().__init__(error)
        self.vkerror = error
        self.error_code = int(error['error_code'])
        self.error_msg = str(error['error_msg'])
        self.request_params = error['request_params']


class VKApi:
    def __init__(self, access_token=None):
        self.access_token = access_token
        self.api_version = '5.21'
        self._lock = threading.Lock()

    def _compile_params(self, params_dict):
        params = list()
        for key in params_dict:
            if len(str(params_dict[key])) != 0:
                if isinstance(params_dict[key], list):
                    params.append((key, ','.join(map(str, params_dict[key]))))
                else:
                    params.append((key, str(params_dict[key])))
        if self.access_token:
            params.append(("access_token", str(self.access_token)))
        params.append(('v', str(self.api_version)))
        return params

    def call(self, method, **params_dict):
        params = self._compile_params(params_dict)

        url = 'https://api.vk.com/method/{0}?{1}'.format(method, urllib.parse.urlencode(params))
        with self._lock:
            response = urllib.request.urlopen(url).read()
        response = json.loads(response.decode())

        if 'error' in response:
            raise VKError(response['error'])
        return response['response']

    def download(self, link, filename=None, reportHook=None):
        if filename:
            urllib.request.urlretrieve(link, filename, reportHook)
        else:
            return urllib.request.urlretrieve(link, reporthook=reportHook)[0]

    def upload(self, link, filename, res_type):
        if __enable_requests__:
            response = requests.post(link, files={res_type: open(filename, 'rb')}).json()
            return response
        else:
            raise RuntimeError('api.upload(): Requests are disabled(import error)')


def test_connection(access_token):
    api = VKApi(access_token)
    try:
        api.call("users.get")
    except VKError:
        return False
    return True