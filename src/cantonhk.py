__author__ = 'kuro'

import argparse


def read(input_file):
    print "input file = %s" % input_file


def write(format):
    print "format = %s" % format


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    #parser.add_argument(dest="action", choices=['read', 'write'], help="Action applied to file.")
    #parser.add_argument("-f", "--format", dest="format", choices=['mac', 'gcin', 'ibus'],
    #                    help="The output format for target IM daemon.")


    #create the parser for the 'download' command
    read_parser = subparsers.add_parser('read', help='read help')
    read_parser.add_argument(dest='input_file', help='File to read in.')

    write_parser = subparsers.add_parser('write', help='write help')
    write_parser.add_argument("-f", "--format", dest="format", choices=['mac', 'gcin', 'ibus'],
                              help="The output format for target IM daemon.")

    options = parser.parse_args()

    if hasattr(options, 'input_file'):
        read(options.input_file)
    elif hasattr(options, 'format'):
        write(options.format)
    else:
        exit("I don't know what the fuck you're trying to do here.")