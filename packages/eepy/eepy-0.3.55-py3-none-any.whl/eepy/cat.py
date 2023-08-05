#!/usr/bin/env python3
#
# Copyright (c) 2019-2021 by Hyoung Bok Min, All rights reserved.
#
#  File       : cat.py
#  Written on : Jan. 20, 2021
#  Author     : Hyoung Bok Min (min.skku@gmail.com)
#  Version    : 1.4
#  Modification History :
#    v1.4 : Jan. 20, 2021
#      (1) Function ``iterable(obj)`` is added.
#      (2) The following 2 assertions are added for stricter checking of
#          preconditions for function ``cat()``.
#          - assert iterable(filenames)
#          - assert all(isinstance(fname, str) for fname in filenames)
#    v1.3 : Dec. 06, 2019
#      (1) Create __version__ to record version number of this program.
#      (2) Add '-V' option to show __version__.
#    v1.2 : Nov. 12, 2019
#      (1) Move codes under 'if __name__ == '__main__'' to function _main().
#      (2) Add 'pycat' command to usage_cat().
#    v1.1 : Jun. 23, 2019
#      (1) Fix bugs:
#          (a) old: if remove_cr and line[-1] == '\r':
#              new: if remove_cr and line and line[-1] == '\r':
#          (b) old: if line[-1] == '\r':
#              new: if line and line[-1] == '\r':
#    v1.0 : Feb. 10, 2019
#      (1) 1st released.
#
"""Module for Unix ``cat`` command.

This cat module is very much similar to Unix ``cat`` command, i.e.,
display a UTF-8 encoded file to standard output. But, the features of
this ``cat`` implementaion may be less than those of the Unix cat.

You can run this program as a Python module, i.e.,
    python3 -m eepy.cat
or
    python -m eepy.cat
"""

import os
import sys
if __package__ is None or __package__ == '':
    # relative import produces ModuleNotFoundError, ImportError.
    # use '' in sys.path to import.
    from test import option_exists
else:
    from .test import option_exists

#
# Options
#
number_outputs = False    # -n : number output lines
number_nonblank = False   # -b : number nonempty output lines, overrides -n
file_encoding = 'utf-8'   # -f : text encoding of file
keep_encoding = False     # -k : keep encoding; use the same encoding as input
remove_cr = False         # -r : remove CR at the end of each line if exists
show_Ends = False         # -E : show end of line with $
show_ends = False         # -e : show end of line with $ before cr
show_tabs = False         # -T : show tab characters by using '^I'
show_nonprinting = False  # -v : use ^ and M- notation, except for LFD and TAB
use_stdin = False         # -  : use stdin as input file

# command name of this program
pycatcmd = 'pycat'

# version
__version__ = '1.4';


def cat(filenames):
    """
    Unix cat command, although this is very basic.

    :param filenames: either a file name or a list of file names
    :type filenames:  either ``str`` or ``list of str's``

    :returns: number of files for which printing has failed
    """
    assert filenames or use_stdin, "Need at least one file or '-'."
    if not filenames and use_stdin:
        filenames = ['-']
    if isinstance(filenames, str):
        filenames = [filenames]
    assert iterable(filenames), 'The argument shall be an iterable.'
    assert all(isinstance(fname, str) for fname in filenames), \
        'All elements of the argument shall be strings.'

    if not show_nonprinting and keep_encoding:
        stdout = None    # We use sys.stdout.buffer.write() for this case.
    else:
        # We need this guy to print only '\n' without '\r' at Windows.
        # https://stackoverflow.com/questions/34960955/
        # print-lf-with-python-3-to-windows-stdout/34997357#34997357
        stdout = open(sys.__stdout__.fileno(), mode=sys.__stdout__.mode,
                      buffering=1, encoding=sys.__stdout__.encoding,
                      errors=sys.__stdout__.errors, newline='\n',
                      closefd=False)

    numfiles = len(filenames)
    failcount = 0
    lineno = 0
    for thefile in filenames:
        if thefile == '-':
            # Use stdin as input file.
            if show_nonprinting:
                f = sys.stdin.buffer
            else:
                f = sys.stdin
        else:
            # Open an input file.
            try:
                if show_nonprinting:
                    f = open(thefile, 'rb')
                else:
                    f = open(thefile, 'r', encoding=file_encoding, newline='')
            except IOError:
                failcount += 1
                msg = '{}: No such file exists.'.format(thefile)
                print(msg, file=sys.stderr)
                continue

        # Print contents of the file in binary mode (-v option).
        if show_nonprinting:
            buf_size = 4096
            buf_size1 = buf_size - 1
            last_cr = False
            last_lf = False
            new_buf = b''
            buf = f.read(buf_size)
            if number_outputs and buf:
                lineno += 1
                print('{:6d}\t'.format(lineno), end='', file=stdout)
            if number_nonblank and buf and buf[0] != 10:
                lineno += 1
                print('{:6d}\t'.format(lineno), end='', file=stdout)
            while buf:
                for index, char in enumerate(buf):
                    if (remove_cr or show_ends) and last_cr and char != 10:
                        print('^'+chr(64+char), end='', file=stdout)
                    if char == 9:       # tab
                        if show_tabs:
                            print('^I', end='', file=stdout)
                        else:
                            print(chr(char), end='', file=stdout)
                    elif char == 10:    # newline
                        if show_ends:
                            if last_cr and not remove_cr:
                                print('$\r\n', end='', file=stdout)
                            else:
                                print('$\n', end='', file=stdout)
                        elif show_Ends:
                            print('$\n', end='', file=stdout)
                        else:
                            print(chr(char), end='', file=stdout)
                        if number_outputs:
                            if index < buf_size1:
                                next_line_exists = True
                            else:
                                new_buf = f.read(buf_size)
                                if new_buf:
                                    next_line_exists = True
                            if next_line_exists:
                                lineno += 1
                                print('{:6d}\t'.format(lineno), end='',
                                      file=stdout)
                        elif number_nonblank:
                            if index < buf_size1:
                                if buf[index+1] != 10:
                                    next_line_exists = True
                                else:
                                    next_line_exists = False
                            else:
                                new_buf = f.read(buf_size)
                                if new_buf and new_buf[0] != 10:
                                    next_line_exists = True
                                else:
                                    next_line_exists = False
                            if next_line_exists:
                                lineno += 1
                                print('{:6d}\t'.format(lineno), end='',
                                      file=stdout)
                    elif char == 13:    # carriage_return
                        if not remove_cr and not show_ends:
                            print('^'+chr(64+char), end='', file=stdout)
                    elif char < 32:
                        print('^'+chr(64+char), end='', file=stdout)
                    elif char < 127:
                        print(chr(char), end='', file=stdout)
                    elif char < 128:
                        print('^?', end='', file=stdout)
                    elif char < 160:
                        print('M-^'+chr(64+char-128), end='', file=stdout)
                    elif char < 255:
                        print('M-'+chr(char-128), end='', file=stdout)
                    else:
                        print('M-^?', end='', file=stdout)
                    last_cr = (char == 13)
                    last_lf = (char == 10)
                if new_buf:
                    buf = new_buf
                else:
                    buf = f.read(buf_size)
                new_buf = b''
            if thefile != '-':
                f.close()
            continue

        # Print contents of the file in text mode.
        try:
            for line in f:
                line = line.rstrip('\n')
                if remove_cr and line and line[-1] == '\r':
                    line = line[:-1]
                if show_tabs and line:
                    line = line.replace('\t', '^I')
                if number_nonblank:
                    if line:
                        lineno += 1
                        msg = '{:6d}\t'.format(lineno)
                        if stdout is not None:
                            print(msg, end='', file=stdout)
                        else:
                            sys.stdout.buffer.write(msg.encode(file_encoding))
                elif number_outputs:
                    lineno += 1
                    msg = '{:6d}\t'.format(lineno)
                    if stdout is not None:
                        print(msg, end='', file=stdout)
                    else:
                        sys.stdout.buffer.write(msg.encode(file_encoding))
                if show_ends:
                    if line and line[-1] == '\r':
                        line = line[:-1] + '$' + '\r'
                    else:
                        line = line + '$'
                elif show_Ends:
                    line = line + '$'
                if stdout is not None:
                    print(line, file=stdout)
                else:
                    line = line + '\n'
                    sys.stdout.buffer.write(line.encode(file_encoding))
        except UnicodeDecodeError:
            failcount += 1
            msg = '{}: File is not {} encoded. Use either -f or -v option.'
            name = 'stdin' if thefile == '-' else thefile
            print(msg.format(name, file_encoding), file=sys.stderr)
            if numfiles == 1:
                usage_cat(True, file=sys.stderr)
        finally:
            if thefile != '-':
                f.close()

    if stdout is not None:
        stdout.close()
    return failcount


def iterable(obj):
    """Helper function to check if given object is iterable.

    This method checks if given object ``obj`` is iterable or not.
    FYI, you may use isinstance(obj, Iterable) defined at collections.abc.

    :param obj: We check if this ``obj`` is iterable or not.
    :type obj: any

    :returns: True if ``obj`` is iterable, False otherwise.
    :rtype: bool
    """
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def usage_cat(blank=False, file=None, version=False):
    """Print how to use this module.

    :param blank: Print one blank line if True, do nothing otherwise.
    :type blank:  bool

    :param file: Output to which usage information is printed.
                 If None, sys.stdout is used.
    :type file:  file object which can be fed to 'file' of print() 

    :param version: Show version if True, show usage if false.
    :type version:  bool

    :returns: None
    """
    outfile = sys.stdout if file is None else file
    pyfile = os.path.basename(__file__)
    base = os.path.splitext(pyfile)[0]
    if version:
        msg = '{} (eepy.{}) version {}'.format(pycatcmd, base, __version__)
        print(msg, file=outfile)
        return
    if os.name == 'nt':
        thepy = 'python'
    else:
        thepy = 'python3'
    msg = '\n' if blank else ''
    msg += 'usage: {} -m eepy.{} [options] file1 [file2 [file3 ...]]'
    print(msg.format(thepy, base), file=outfile)
    print('       or', file=outfile)
    msg = '       {} [options] file1 [file2 [file3 ...]]'
    print(msg.format(pycatcmd), file=outfile)
    msg = (
        '\n'
        'options:\n'
        '  -n            number all output lines\n'
        '  -b            number nonempty output lines, overrides -n\n'
        '  -f encoding   text encoding of file  [default: {}]\n'
        '  -k            use the same encoding as input file for output\n'
        '  -r            remove CR character at each line '
        'if exists [default: {}]\n'
        '  -E            display $ at end of every line\n'
        '  -e            same as -E, but before cr if cr-lf, overrides -E\n'
        '  -T            display TAB characters as ^I\n'
        '  -v            use ^ and M- notation, except for LFD and TAB\n'
        '  -V            display version of this program\n'
        '  -h            display this help and exit\n'
        '\n'
        'arguments:\n'
        '  file1 [file2 [file3 ...]]  file(s) to be printed to stdout.\n'
        '                If file1 is \'-\', stdin is used as input file.\n'
        '\n'
        'Path: {}')
    print(msg.format(file_encoding, remove_cr, sys.argv[0]), file=outfile)


def _main():
    # Options as global variables
    global number_outputs, number_nonblank
    global file_encoding, keep_encoding, remove_cr
    global show_Ends, show_ends, show_tabs, show_nonprinting
    global use_stdin

    # Process option arguments.
    args = sys.argv[1:]
    if len(sys.argv) > 1:
        # check options which cannot be combined.
        soleopts = 'f'
        if option_exists(args, '-', nocomb=soleopts):
            plural = 's' if len(soleopts) > 1 else ''
            msg = '[ERROR] \'-{}\' option{} shall not be combined.'
            print(msg.format(soleopts, plural), file=sys.stderr)
            usage_cat(True, file=sys.stderr)
            sys.exit(1)
        # -h: help.
        if option_exists(args, '-h'):
            usage_cat()
            sys.exit(0)
        # -V: version.
        if option_exists(args, '-V'):
            usage_cat(version=True)
            sys.exit(0)
        # -n: number output lines.
        if option_exists(args, '-n', remove=True):
            number_outputs = False if number_outputs else True
        # -b: number nonempty output lines.
        if option_exists(args, '-b', remove=True):
            number_nonblank = False if number_nonblank else True
        # -k: keep encoding.
        if option_exists(args, '-k', remove=True):
            keep_encoding = False if keep_encoding else True
        # -r: remove CR at the end of every line if exists.
        if option_exists(args, '-r', remove=True):
            remove_cr = False if remove_cr else True
        # -E: display $ at the end of every line.
        if option_exists(args, '-E', remove=True):
            show_Ends = False if show_Ends else True
        # -e: display $ at the end of every line before cr.
        if option_exists(args, '-e', remove=True):
            show_ends = False if show_ends else True
        # -T: display tab characters by using '^I'.
        if option_exists(args, '-T', remove=True):
            show_tabs = False if show_tabs else True
        # -v: use ^ and M- notation, except for LFD and TAB.
        if option_exists(args, '-v', remove=True):
            show_nonprinting = False if show_nonprinting else True
        # -f: text encoding
        next_opt = []
        if option_exists(args, '-f', remove=True, more=True, found=next_opt):
            if len(next_opt) < 1:
                msg = '[ERROR] \'-f\' option needs name of encoding.'
                print(msg, file=sys.stderr)
                usage_cat(True, file=sys.stderr)
                sys.exit(1)
            elif len(next_opt) > 1:
                msg = '[ERROR] Please use \'-f\' option only once.'
                print(msg, file=sys.stderr)
                usage_cat(True, file=sys.stderr)
                sys.exit(1)
            else:
                file_encoding = next_opt[0]
        # if more "-" option exists, it's error unless it is '-'.
        more_opts = []
        if option_exists(args, '-', found=more_opts):
            if '-' in more_opts:
                use_stdin = True
                more_opts.remove('-')
                args.remove('-')
            if more_opts:
                msg = '[ERROR] Unsupported option(s): {}'.format(more_opts)
                print(msg, file=sys.stderr)
                usage_cat(True, file=sys.stderr)
                sys.exit(1)

    # Need at least 1 file as an argument.
    if use_stdin:
        if args:
            msg = '[ERROR] File names cannot be specified with '-'.'
            print(msg, file=sys.stderr)
            usage_cat(True, file=sys.stderr)
            sys.exit(2)
    elif len(args) < 1:
        msg = '[ERROR] Need at least 1 file name, or use \'-\' for stdin.'
        print(msg, file=sys.stderr)
        usage_cat(True, file=sys.stderr)
        sys.exit(3)

    # Do it.
    cat(args)

if __name__ == '__main__':
    _main()

# -- cat.py
