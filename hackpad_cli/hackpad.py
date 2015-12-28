from requests_oauthlib import OAuth1Session


API_PATH = 'api/1.0'

CONTENT_TYPE_HEADER = 'Content-Type'
CONTENT_TYPE_MAP = {
        'txt': 'text/plain',
        'html': 'text/html',
        'md': 'text/x-web-markdown',
        }


class HackpadSession(object):
    def __init__(self, key, secret, url='https://hackpad.com'):
        self.url = url.strip('/')
        self.oauth_session = OAuth1Session(key, secret)
        self.api_endpoint = url + API_PATH

    def get(self, url, *args, **kwargs):
        print('GET', url, args, kwargs)
        return self.oauth_session.get(url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        print('POST', url, args, kwargs)
        return self.oauth_session.post(url, *args, **kwargs)

    def pad_list(self):
        req_url = "%s/pads/all" % self.api_endpoint
        return self.get(req_url)

    def pad_create(self, data, data_format='md'):
        req_url = "%s/pad/create" % self.api_endpoint
        req_headers = {CONTENT_TYPE_HEADER: CONTENT_TYPE_MAP[data_format]}
        return self.post(req_url, data, headers=req_headers)

    def pad_get(self, pad_id, data_format='md', revision='latest'):
        req_url = "%s/pad/%s/content/%s.%s" % (self.api_endpoint,
                                               pad_id, revision,
                                               data_format)
        return self.get(req_url)

    def pad_put(self, pad_id, data, data_format='md'):
        req_url = "%s/pad/%s/content" % (self.api_endpoint, pad_id)
        req_headers = {CONTENT_TYPE_HEADER: CONTENT_TYPE_MAP[data_format]}
        return self.post(req_url, data, headers=req_headers)

    def pad_revert(self, pad_id, revision):
        req_url = "%s/pad/%s/revert-to/%s" % (self.api_endpoint, pad_id, revision)
        return self.post(req_url)

    def pad_revisions(self, pad_id):
        req_url = "%s/pad/%s/revisions" % (self.api_endpoint, pad_id)
        return self.get(req_url)

    def pad_get_options(self, pad_id):
        req_url = "%s/pad/%s/options" % (self.api_endpoint, pad_id)
        return self.get(req_url)

    def pad_set_option(self, pad_id, setting, value):
        req_url = "%s/pad/%s/options" % (self.api_endpoint, pad_id)
        req_params = {setting: value}
        return self.post(req_url, params=req_params)
