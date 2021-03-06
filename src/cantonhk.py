__author__ = 'kuro'

import argparse
import codecs
import json
import re
import os
import django
from django.conf import settings as django_settings
from django.template import Template, Context
from models import CantonKey

SUPPORTED_FORMAT = ['ibus', 'cin', 'json']


def deploy(options):

    if not hasattr(options, 'format'):
        exit('Format not defined')
    elif not hasattr(options, 'input_path'):
        exit('IM table not found.')

    if options.format == 'ibus':
        deploy_ibus(options.input_path)


def deploy_ibus(input_path):
    from subprocess import call
    pass


def read(options):
    if hasattr(options, 'input_file'):
        read_donar_table(options.input_file)
    else:
        exit('Missing input file.')


def read_donar_table(input_file):
    print("input file = %s" % input_file)

    keymap = []

    with codecs.open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if re.search(r'^#', line):
                continue

            try:
                key, choices_string = line.split('\t')
                choices_string = re.sub(r'\n', r'', choices_string)
                choices = choices_string.split(',')
                keymap.append(CantonKey(key, choices))
            except Exception:
                pass    # Ignore unexpected lines.

    return keymap


def write(options):
    if not hasattr(options, 'format'):
        exit("Output format not defined.")
    elif options.format not in SUPPORTED_FORMAT:
        exit("Format %s is'nt supported yet." % options.format)
    elif not hasattr(options, 'input_file'):
        exit("Missing input file")
    elif not hasattr(options, 'output_path'):
        exit("Missing output path")
    else:
        directory = os.path.dirname(options.output_path)
        # Create the output directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        print("Genearting %s table" % options.format)
        generate_table(options.format,
                       input_path=options.input_file,
                       output_path=options.output_path)
        print("Table saved to path `%s`" % options.output_path)


def generate_table(im_format, input_path, output_path):
    keymap = read_donar_table(input_path)

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                # ... some options here ...
            },
        },
    ]

    django_settings.configure(TEMPLATES=TEMPLATES)
    django.setup()

    if im_format == 'cin':
        t = Template(codecs.open(os.path.join(os.getcwd(), '../res/templates/mac_openvanilla.cin'), 'r', encoding='utf-8').read())
        f = open(output_path, 'w', encoding='utf-8')
        f.write(t.render(Context({'keys': keymap})))
        f.close()
    elif im_format == 'ibus':
        t = Template(codecs.open(os.path.join(os.getcwd(), '../res/templates/ibus.txt'), 'r', encoding='utf-8').read())
        f = open(output_path, 'w', encoding='utf-8')
        f.write(t.render(Context({'keys': keymap})))
        f.close()
    elif im_format == 'json':
        full_json = []
        for key_obj in keymap:
            key_json = key_obj.to_json()
            full_json.append(key_json)
            print("key = %s\njson = %s" % (key_obj.choices, key_json))
        f = open(output_path, 'w', encoding='utf-8')
        f.write(json.dumps(full_json, ensure_ascii=False))
        # f.write(json.dumps(full_json, ensure_ascii=False, indent=4))  uncomment this for pretty printing.
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    read_parser = subparsers.add_parser('read', help='read help')
    read_parser.add_argument(dest='input_file', help='File to read in.')
    read_parser.set_defaults(func=read)

    write_parser = subparsers.add_parser('write', help='write help')
    write_parser.add_argument("-i", "--input", dest='input_file', help='File to read in.')
    write_parser.add_argument("-f", "--format", dest="format", choices=['cin', 'ibus', 'json'],
                              help="The output format for target IM daemon.")
    write_parser.add_argument("-o", "--output", dest='output_path',
                              help='Output path for generated table')
    write_parser.set_defaults(func=write)

    options = parser.parse_args()
    options.func(options)