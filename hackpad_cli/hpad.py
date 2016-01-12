"""
Hackpad API command line client.

Usage:
    hpad.py [options] pad list
    hpad.py [options] pad search <query> [--start=<start>] [--limit=<limit>]
    hpad.py [options] pad create [--format=<format>] [--] <file>
    hpad.py [options] pad <pad_id> revisions
    hpad.py [options] pad <pad_id> put [--format=<format>] <file>
    hpad.py [options] pad <pad_id> get [--revision=<revision>] [--format=<format>]
    hpad.py [options] pad <pad_id> revert --revision=<revision>
    hpad.py [options] pad <pad_id> get-options
    hpad.py [options] pad <pad_id> set-option <setting> <value>
    hpad.py [options] pad <pad_id> revoke-access <user>

Options:
    -u URL, --url=URL           Hackpad url
    -k KEY, --key=KEY           User key
    -s SECRET, --secret=SECRET  User secret
    -c FILE, --config=FILE      Auth file containing url, user key and secret [default: ~/.hackpad.cred.json]
    --revision=<revision>       Pad revision id [default: latest]
    --format=<format>           Pad format (html|md|native|txt) [default: md]
    --start=<start>             Offset in search results to start at
    --limit=<limit>             Number of search results to return
    -D --debug                  Print debugging info.
"""
from hackpad_cli.hackpad import HackpadSession


def main():
    import json
    import pprint

    from os.path import expanduser
    from docopt import docopt
    arguments = docopt(__doc__, version='hpad.py 0.1')

    session_config = {}
    if arguments['--config']:
        config_path = expanduser(arguments['--config'])
        config = json.load(open(config_path))
        if arguments['--url']:
            session_config = config[arguments['--url']]
        else:
            session_config = next(filter(lambda x: x.get('default'), config.values()))

    if arguments['--key']:
        session_config['key'] = arguments['--key']
    if arguments['--secret']:
        session_config['secret'] = arguments['--secret']
    if arguments['--url']:
        session_config['url'] = arguments['--url']

    hackpad_session = HackpadSession(session_config['key'], session_config['secret'],
                                     url=session_config['url'], debug=arguments['--debug'])

    if arguments['pad'] and (arguments['create'] or arguments['put']):
        if arguments['<file>'] == '-':
            stream = sys.stdin
        else:
            stream = open(arguments['<file>'])

    if arguments['pad']:
        if arguments['list']:
            resp = hackpad_session.pad_list()
            pprint.pprint(resp.json())

        if arguments['search']:
            resp = hackpad_session.pad_search(arguments['<query>'], start=arguments['--start'],
                                              limit=arguments['--limit'])
            pprint.pprint(resp.json())

        if arguments['create']:
            resp = hackpad_session.pad_create(stream.read(), data_format=arguments['--format'])
            pprint.pprint(resp.json())

        if arguments['get']:
            resp = hackpad_session.pad_get(arguments['<pad_id>'], revision=arguments['--revision'],
                                           data_format=arguments['--format'])
            pprint.pprint(resp.content)

        if arguments['put']:
            resp = hackpad_session.pad_put(arguments['<pad_id>'], stream.read(),
                                           data_format=arguments['--format'])
            pprint.pprint(resp.json())

        if arguments['revert']:
            resp = hackpad_session.pad_revert(arguments['<pad_id>'], arguments['--revision'])
            pprint.pprint(resp.json())

        if arguments['revisions']:
            resp = hackpad_session.pad_revisions(arguments['<pad_id>'])
            pprint.pprint(resp.json())

        if arguments['get-options']:
            resp = hackpad_session.pad_get_options(arguments['<pad_id>'])
            pprint.pprint(resp.json())

        if arguments['set-option']:
            resp = hackpad_session.pad_set_option(arguments['<pad_id>'], arguments['<setting>'],
                                                  arguments['<value>'])
            pprint.pprint(resp.json())

        if arguments['revoke-access']:
            resp = hackpad_session.pad_revoke_access(arguments['<pad_id>'], arguments['<user>'])
            pprint.pprint(resp.json())


if __name__ == '__main__':
    main()
