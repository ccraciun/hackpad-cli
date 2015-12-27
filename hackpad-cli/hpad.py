"""
Hackpad API command line client.

Usage:
    hpad.py [options] pad list
    hpad.py [options] pad create [--format=<format>] [--] <file>
    hpad.py [options] pad <pad_id> revisions
    hpad.py [options] pad <pad_id> put [--format=<format>] <file>
    hpad.py [options] pad <pad_id> get [--revision=<revision>] [--format=<format>]

Options:
    -u URL, --url=URL           Hackpad url [default: https://hackpad.com/]
    -k KEY, --key=KEY           User key
    -s SECRET, --secret=SECRET  User secret
    -c FILE, --config=FILE      Auth file containing url, user key and secret
    --revision=<revision>       Pad revision id [default: latest]
    --format=<format>           Pad format (html|md|native|txt) [default: md]
"""
import json
import pprint

from docopt import docopt
from requests_oauthlib import OAuth1Session


API_PATH = 'api/1.0/'

CONTENT_TYPE_HEADER = 'Content-Type'
CONTENT_TYPE_MAP = {
        'txt': 'text/plain',
        'html': 'text/html',
        'md': 'text/x-web-markdown',
        }

def main():
    arguments = docopt(__doc__, version='hpad.py 0.1')
    if arguments['--config']:
        arguments.update(json.load(open(arguments['--config'])))
    pprint.pprint(arguments)

    api_endpoint = arguments['--url'] + API_PATH

    oauth_session = OAuth1Session(arguments['--key'], client_secret=arguments['--secret'])

    if arguments['pad']:
        if arguments['list']:
            print(api_endpoint + 'pads/all')
            print(oauth_session.get(api_endpoint + 'pads/all').json())
        if arguments['create']:
            req_url = api_endpoint + 'pad/create'
            if arguments['<file>'] == '-':
                f = sys.stdin
            else:
                f = open(arguments['<file>'])
            req_headers = {CONTENT_TYPE_HEADER: CONTENT_TYPE_MAP[arguments['--format']]}
            print(req_url)
            print(req_headers)
            #pprint.pprint(oauth_session.put(req_url, f, headers=req_headers))
        if arguments['get']:
            req_url = api_endpoint + 'pad/' + arguments['<pad_id>'] + '/content/'
            if arguments['--revision']:
                req_url += arguments['--revision']
            if arguments['--format']:
                req_url += '.' + arguments['--format']
            print(req_url)
            print(oauth_session.get(req_url).content)
        if arguments['put']:
            req_url = api_endpoint + 'pad/' + arguments['<pad_id>'] + '/content'
            # TODO: Pull file setup out of here, merge with create above.
            if arguments['<file>'] == '-':
                f = sys.stdin
            else:
                f = open(arguments['<file>'])
            req_headers = {CONTENT_TYPE_HEADER: CONTENT_TYPE_MAP[arguments['--format']]}
            print(req_url)
            print(req_headers)
            #pprint.pprint(oauth_session.put(req_url, f, headers=req_headers))
        if arguments['revisions']:
            req_url = api_endpoint + 'pad/' + arguments['<pad_id>'] + '/revisions'
            print(req_url)
            pprint.pprint(oauth_session.get(req_url).json())


if __name__ == '__main__':
    main()
