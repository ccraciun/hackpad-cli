"""
Hackpad API command line client.

Usage:
    hpad.py [options] pad list
    hpad.py [options] pad create [--format=<format>] [--] <file>
    hpad.py [options] pad <pad_id> revisions
    hpad.py [options] pad <pad_id> put [--format=<format>] <file>
    hpad.py [options] pad <pad_id> get [--revision=<revision>] [--format=<format>]
    hpad.py [options] pad <pad_id> revert --revision=<revision>
    hpad.py [options] pad <pad_id> get_options
    hpad.py [options] pad <pad_id> set_option <setting> <value>

Options:
    -u URL, --url=URL           Hackpad url [default: https://hackpad.com/]
    -k KEY, --key=KEY           User key
    -s SECRET, --secret=SECRET  User secret
    -c FILE, --config=FILE      Auth file containing url, user key and secret
    --revision=<revision>       Pad revision id [default: latest]
    --format=<format>           Pad format (html|md|native|txt) [default: md]
"""
from hackpad_cli.hackpad import HackpadSession


def main():
    import json
    import pprint

    from docopt import docopt
    arguments = docopt(__doc__, version='hpad.py 0.1')
    if arguments['--config']:
        arguments.update(json.load(open(arguments['--config'])))

    hackpad_session = HackpadSession(arguments['--key'], arguments['--secret'],
                                     url=arguments['--url'])

    if arguments['pad'] and (arguments['create'] or arguments['put']):
        if arguments['<file>'] == '-':
            stream = sys.stdin
        else:
            stream = open(arguments['<file>'])

    if arguments['pad']:
        if arguments['list']:
            resp = hackpad_session.pad_list()
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

        if arguments['get_options']:
            resp = hackpad_session.pad_get_options(arguments['<pad_id>'])
            pprint.pprint(resp.json())

        if arguments['set_option']:
            resp = hackpad_session.pad_set_option(arguments['<pad_id>'], arguments['<setting>'],
                                                  arguments['<value>'])
            pprint.pprint(resp.json())


if __name__ == '__main__':
    main()
