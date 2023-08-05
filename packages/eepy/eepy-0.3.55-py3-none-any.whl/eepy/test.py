#
#  Copyright (c) 2019 by Hyoung Bok Min, All rights reserved.
#
#  File       : test.py
#  Written on : Feb. 10, 2019
#  Author     : Hyoung Bok Min (min.skku@gmail.com)
#
"""The helper functions for unit testing of homeworks"""

import sys
import io

# Exit code when einput() exits by user's request (enter 'e').
EINPUT_EXIT_CODE = 100


class Capturing(list):
    """Context manager to capture stdout of function call(s).

    This class comes from a good answer of a question at stackoverflow.
    https://stackoverflow.com/questions/16571150/
    how-to-capture-stdout-output-from-a-python-function-call
    """

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def einput(prompt_msg=''):
    """The same as built-in function input(), but with 1 more feature, i.e.,
    'e' is a special character in this function.

    :param prompt_msg: message to be printed on screen.
    :type prompt_msg:  str

    :return: user's keyboard input.
    :rtype:  str

    :note: If user enters one single character 'e', call sys.exit() with
           exit code defined at EINPUT_EXIT_CODE.
    """
    retval = input(prompt_msg)
    if retval == 'e':
        msg = ('[eepy] Program is terminated by user\'s request '
               f'with exit code {EINPUT_EXIT_CODE}.')
        print(msg)
        sys.exit(EINPUT_EXIT_CODE)
    return retval


def get_exc_info(severity='', doing='', tb=False, tbfile=sys.stdout):
    """Get execution information when an Exception has been detected,
    and print the execution information.

    This function shall be called at ``except`` block.
    When this is called, exception type, line number, and filename
    which causes the exception are collected and build an error message.

    :param severity: Severity level, (e.g), '[ERROR]'
    :type severity:  str

    :param doing: Summary of try block, i.e., what were you doing?
                  (e.g), 'importing file'
    :type doing:  str

    :param tb: Print traceback if this is True, 'top', 'bot', or 'both'.
               Number of hyphens may be specified by adding a dot and
               the number.
    :type tb:  bool or str

    :param tbfile: The file to which the execution information is printed.
    :type tbfile:  file object

    :return: the error message which contains the execution information.
    :rtype:  str
    """
    assert type(severity) == str, '[eepy.get_exe_info] severity type'
    assert type(doing) == str, '[eepy.get_exe_info] doing type'

    if tb:
        hline = 20
        if isinstance(tb, str):
            tb_print_method = tb.split('.')
            if len(tb_print_method) > 1:
                tb, hline, *_ = tb_print_method
                hline = int(hline)
            elif len(tb_print_method) == 1:
                tb = tb_print_method[0]
            else:
                tb = True
        import traceback
        if tb == 'top' or tb == 'both':
            print('-'*hline, file=tbfile)
        traceback.print_exc(file=tbfile)
        if tb == 'bot' or tb == 'both':
            print('-'*hline, file=tbfile)

    import os
    # import sys : imported on top of this module
    exc_type, exc_obj, exc_tb = sys.exc_info()    # exc_type == e.__class__
    exc_fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    exc_lineno = exc_tb.tb_lineno

    if severity:
        severity += ' '
    if doing:
        doing = 'while ' + doing + ' '

    msg = (severity + exc_type.__name__ + ' Exception has been detected ' +
           doing + 'at line ' + str(exc_lineno) +
           ' of file "' + exc_fname + '".')
    return msg


def get_tuplelist(filename):
    """Measure reference cpu time for lab for dict."""
    from collections import Counter
    from operator import itemgetter

    fobj = open(filename, 'rb')
    contents = fobj.read()
    fobj.close()
    filesize = len(contents)
    try:
        str_contents = contents.decode('utf-8')
    except UnicodeDecodeError:
        str_contents = contents.decode('cp949')
    counter = Counter(str_contents)
    tlist = counter.most_common()
    tlist.sort(key=lambda x: ord(x[0]))
    tlist.sort(key=itemgetter(1))
    return filesize, tlist


def get_word(string, index):
    """Given a ``string``, returns ``index``-th word in the ``string``.

    :param string: This function returns a word in this ``string``.
    :type string:  str

    :param index:  This function returns ``index``-th word of the ``string``.
                   ``index`` begins with 0.
                   If index is 0, this function returns the 1st word.
                   If index is 1, this function returns the 2nd word.
    :type index:   int

    :return: ``index``-th word of the ``string``.
             If ``index``-th word does not exist, returns an empty string ''.
    :rtype:  str

    :precondition: index >= 0
    """
    assert type(string) == str, "string shall be of type str."
    assert type(index) == int, "index shall be of type int."
    assert index >= 0, "index shall be non-negative integer."

    num_words = number_of_words(string)
    if index >= num_words:
        return ''

    return string.strip().split()[index]


def number_of_words(string):
    """Given a ``string``, returns number of words in the ``string``.

    :param string: This function returns number of words in this ``string``.
    :type string:  str

    :return: number of words in the ``string``.
    :rtype:  int
    """
    assert type(string) == str, "string shall be of type str."

    return len(string.strip().split())


def option_exists(args, opt, remove=False, more=False, found=None, nocomb=''):
    """Check whether ``opt`` exists in ``args`` or not.

    This function is a helper function to parse command line arguments.

    :param args: a list of command line arguments to a script.
    :type args:  list of strings

    :param opt:  an option which I want to search from ``args``.
    :type opt:   str
    :precondition: ``opt`` shall be either '-' or '-' followed by one
                   single character.

    :param remove: Remove the ``opt`` from ``args`` if True,
                   do nothing if False.
    :type remove:  bool

    :param more: Take next option and transfer it to caller via ``found``
                 if True, do nothing if False.
    :type more:  bool
    :example: For example, if '-page 20' is given, 20 is transferred to
              caller via ``found``.

    :param found: If given, required items are returned to this list.
                  See the above example for ``more``.
    :type found:  empty list or None

    :param nocomb: This is a string of option characters.
                   If given, check whether the options in ``nocomb`` are
                   combined in command-line arguments ``args``.
                   If any of the option in ``nocomb`` is combined in ``args``,
                   this function returns True.
                   In other words, options which cannot be combined are
                   listed at ``nocomb`` to check whether they are not
                   combined in command-line arguments actually.
                   If ``nocomb`` is given, only this feature is processed, and
                   function returns either True or False immediately.
    :type nocomb:  str
    :example: Assume that ``nocomb`` is 'ion', and -i option is given by user
              as -kie ('i' is combined with the other options), this function
              returns True. The same is true for -o and -n option in this
              example if ``nocomb`` is 'ion'.

    :return: True if the ``opt`` exists in ``args``, False otherwise,
             when ``nocomb`` is empty.
    :rtype:  bool
    """
    def in_args(thearg, opt):
        """Check whether option ``opt`` is in ``thearg``.

        This is a function inside the function ``option_exists()``.
        If ``thearg`` is the same ``opt``, it's simple.
        if ``thearg`` is a combined option (e.g. -np as a combination of
        -n and -p), ``opt`` (-p) is in ``thearg``.

        :return: True if ``opt`` is in ``thearg``.
        :rtype:  bool

        :note: This is a function inside the function ``option_exists()``.
        """
        assert len(opt) < 3, 'length of opt shall be 2 or less.'
        if thearg == opt:
            return True
        if len(opt) < 2:
            return False
        if len(thearg) < 3:
            return False
        if thearg[0] != opt[0]:   # thearg is not an option
            return False
        if opt[1] in thearg:      # ``thearg`` is a combined option argument
            return True
        return False

    def remove_opt(args, index, opt):
        """Given a list of arguments ``args`` and an ``index`` of the list,
        Remove option (``opt``) from args[index].

        If args[index] == opt, args[index] = None. Otherwise, remove the
        option characcter is removed from the combined option.

        (example) If args[index] is '-np' and opt is '-n', remove 'n'
                  which is opt[1] from '-np', which results in '-p'.
                  args[index] becomes '-p'.

        :note: args[index] is modified.
        :returns: None

        :note: This is a function inside the function ``option_exists()``.
        """
        assert len(opt) < 3, 'length of opt shall be 2 or less.'
        if len(opt) < 2:
            return
        if args[index] == opt:
            args[index] = None
            return
        args[index] = args[index].replace(opt[1], '')

    # This is beginning of function ``option_exists()``.
    # Check preconditions.
    assert 0 < len(opt) < 3 and opt[0] == '-', \
        'opt shall be either \'-\' or \'-\' followed by one single character.'

    # If ``nocomb`` is given, it has highest priority, and check this only.
    if nocomb:
        # returns True if options in ``nocomb`` is combined at the
        # command line arguments.
        for thearg in args:
            if thearg.startswith('-') and len(thearg) > 2:
                # ``thearg`` is a combined options.
                for ch in thearg:
                    if ch in nocomb:
                        return True
        return False

    # Check whether opt exists in args.
    # If exists, collect items at ``found`` if ``found`` is given, and
    # mark it in ``args``` as None if ``remove`` is True.
    exists = False
    for index, thearg in enumerate(args):
        if thearg is None:   # removed
            continue
        elif in_args(thearg, opt) or (opt == '-' and thearg.startswith(opt)):
            exists = True
            if found is not None:
                if more:    # collect arg next to ``opt`` to ``found``
                    if (index+1) < len(args):
                        found.append(args[index+1])
                else:       # collect this arg to ``found```
                    found.append(thearg)
            if remove:
                if len(args[index]) < 3:    # NOT combined option
                    args[index] = None      # mark current arg as removed
                else:
                    remove_opt(args, index, opt)
                if more and ((index+1) < len(args)):
                    args[index+1] = None    # mark next arg as removed

    # Remove None from the list.
    if exists and remove:
        temp = [x for x in args if x is not None]
        args.clear()         # Remove all items in ``args``.
        args.extend(temp)    # Add all items in ``temp``.
    return exists


def unixtime(hour=None, minute=0, second=0, month=None, day=None, year=None):
    """Given time by ``hour``, ``minute``, ``second`` etc., compute seconds
    since unix epoch (00:00:00 on Jan. 1, 1970).

    If time is not given, compute current time of today since unix epoch.
    If date is not given, compute given time of today since unix epoch.
    If both date and time are given: compute given time/date since unix epoch.

    :return: number of seconds since unix epoch
    :rtype:  float
    """
    import time
    from datetime import datetime

    if hour is None:
        dt = datetime.now()
    elif month is None or day is None or year is None:
        dnow = datetime.now()
        dt = datetime(dnow.year, dnow.month, dnow.day, hour, minute, second)
    else:
        dt = datetime(year, month, day, hour, minute, second)
    unixtime = time.mktime(dt.timetuple())
    return unixtime


def unix_wc(filename):
    """Given a file name, compute number of lines, words, bytes, and characters.
    This is the same as the simple feature of unix 'wc' command.

    :param filename: name of the file from which the numbers are counted.
    :type filename:  str

    :return: tuple of number of lines, words, bytes, characters
    :rtype:  tuple of 4 int's

    :note: We use utf-8/cp949 encoding to count number of characters.
    """
    # filesize = os.path.getsize(filename)
    fobj = open(filename, 'rb')
    contents = fobj.read()
    fobj.close()
    filesize = len(contents)
    try:
        nchars = len(contents.decode('utf-8'))
    except UnicodeDecodeError:
        nchars = len(contents.decode('cp949'))
    nwords = len(contents.split())
    nlines = contents.count(b'\n')
    return nlines, nwords, filesize, nchars


def test_equal(errcount, expected, result, tb=False):
    """Compare ``expected`` and ``result``.

    We do the followings for test.
    (1) Compate the return ``result`` and ``expected`` values.
        If they are the same, return True.
    (2) If the return ``result`` and ``expected`` are different,
        give an error message and return False.

    :param errcount: a list of number of errors and number of test cases.
                     These two values shall be initialized by caller, and
                     are accumulated everytime this function is called.
                     errcount[0] : number of detected errors: increased by 1
                                   only when this function return False.
                     errcount[1] : number of test cases: increased by 1
                                   at this function
    :type errcount: list
    Note :If errcount[0] is None, test is disabled (no-test mode).
          errcount[3] is used to control no-test mode of this function,
          and errcount[1:2] is used to control test_function().
          If errcount[3] is None, do nothing and return True.

    :param expected: expected value for each test case
    :type expected:  any

    :param result: result received from call to student's function
    :type params:  any

    :param tb: print traceback if this is True, 'top', or 'bot'.
    :type tb:  bool

    :return: True if the two values match,
             False otherwise.
    :rtype:  bool
    """
    # preconditions
    assert type(errcount) == list
    if errcount[0] is None:   # no-test mode
        if errcount[3] is None:
            return True
    assert len(errcount) == 2
    assert type(errcount[0]) == int
    assert type(errcount[1]) == int

    # 1 more test case is performed.
    errcount[1] += 1

    # values are compared.
    try:
        if type(result) == type(expected) and result == expected:
            return True
    except Exception as e:
        doing = 'comparing expected value={} with result={}'.format(
                repr(expecetd), repr(result))
        print(get_exc_info(' [ERROR:test_equal]', doing, tb))
        if not tb:
            print(e)
        errcount[0] += 1
        return False

    # If return values are different, given error message.
    msg = (' [ERROR:test_equal] Result does not match the expected ' +
           'value: result={}, expected={}')
    print(msg.format(repr(result), repr(expected)))
    errcount[0] += 1
    return False


def test_function(errcount, expected, func, *params, tb=False, printok=False):
    """Run one single test case and compare the result with expected value.

    Assume that the test case returns one single value, and we do the
    followings for test.
    (1) Run student's function with the test case.
    (2) Compare the return result with ``expected`` value
        If they are the same, return True.
    (3) If the return result for the test case is different from
        ``expected``, give an error message and return False.

    :param errcount: a list of number of errors and number of test cases.
                     These two values shall be initialized by caller, and
                     are accumulated everytime this function is called.
                     errcount[0] : number of detected errors: increased by 1
                                   only when this function return False.
                     errcount[1] : number of test cases: increased by 1
                                   at this function
    :type errcount: list
    :note: If errcount[0] is None, test is disabled (no-test mode).
           errcount[1:2] is used to control no-test mode of this function,
           and errcount[3] is used to control test_equal().
           If errcount[1:2] = (None, None), do nothing and return True.
           If errcount[1:2] = (None, True), call function and return True.

    :param expected: expected value for this test case
    :type expected:  any

    :param func: Student's function to be tested this time.
    :type func:  function

    :param params: a tuple of arguments given to the above function
                   ``func``. This is the test case to test the ``func``.
    :type params:  tuple

    :param tb: print traceback if this is True, 'top', or 'bot'.
    :type tb:  bool or str

    :param printok: printing during function call is okay if this is True,
                    printing during function call is not allowed if False.
    :type printok:  bool

    :return: True if expected value matches result of function call,
             False otherwise.
    :rtype: bool
    """
    # preconditions
    assert type(errcount) == list
    if errcount[0] is None:    # no-test mode
        if errcount[1] is None:
            if errcount[2] is None:
                return True
            result = func(*params)
            print(result)
            return result
    assert len(errcount) == 2
    assert type(errcount[0]) == int
    assert type(errcount[1]) == int

    # 1 more test case is performed.
    errcount[1] += 1

    # Student's function is executed.
    try:
        if printok:
            result = func(*params)
        else:
            with Capturing() as output:
                result = func(*params)
            if output:
                doing = 'running {}{}'.format(func.__name__, repr(params))
                print(' [ERROR:test_function]', doing)
                print(' Printing from function is not allowed.')
                print('', '-'*30)
                for line in output:
                    print('', line)
                print('', '-'*30)
                errcount[0] += 1
                return False
    except Exception as e:
        doing = 'running {}{}'.format(func.__name__, repr(params))
        print(get_exc_info(' [ERROR:test_function]', doing, tb))
        if not tb:
            print(e)
        errcount[0] += 1
        return False

    # return values are compared.
    try:
        if type(result) == type(expected) and result == expected:
            return True
    except Exception as e:
        doing = 'comparing expected value with result of {}{}'.format(
                func.__name__, repr(params))
        print(get_exc_info(' [ERROR:test_function]', doing, tb))
        if not tb:
            print(e)
        errcount[0] += 1
        return False

    # If return values are different, given error message.
    msg = (' [ERROR:test_function] Result of {}{} does not match the ' +
           'expected value: result={}, expected={}')
    print(msg.format(func.__name__, repr(params),
                     repr(result), repr(expected)))
    errcount[0] += 1
    return False

# -- end of test.py
