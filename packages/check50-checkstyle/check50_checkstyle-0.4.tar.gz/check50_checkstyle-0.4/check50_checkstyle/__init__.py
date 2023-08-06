# Copyright (C) 2020  Patrick Totzke <patricktotzke@gmail.com>
# This file is released under the GNU GPL, version 3 or a later revision.

import xml.etree.ElementTree as ET

import os
import check50

from check50._api import Failure


##########################
JAVA = "java"
CHECKSTYLE_JAR = "checkstyle-8.39-all.jar"

CHECKSTYLE_JAR_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'lib',
    CHECKSTYLE_JAR)
##########################


class CheckstyleWarning:
    """A single checkstyle error"""

    def __init__(self, **kwargs):
        self.data = kwargs

    def location(self):
        l = None
        if 'filename' in self.data:
            l = self.data['filename']
            if 'line' in self.data:
                prec = "line " + self.data['line']
                if 'column' in self.data:
                    prec += ", char " + self.data['column']
                l += "(" + prec + ")"
        return l

    def __str__(self):
        return "In " + self.location() + ": " + self.data['message']


def run_and_interpret_checkstyle(rationale=None, log_msg=None,
                                 log_individual_warnings=False, **kwargs):
    """
    Execute the checkstyle CLI runner, interpret and log all resulting warnings
    and raise check50 Failure if there were warnings.

    Ideally, this would be replaced by a special check50.Failure subclass
    that encapsulates all warnings and is rendered nicely into html by check50.
    The problem is that check50 hard-codes its html template.

    :param rationale: the message given to the Failure raised in case there are
                      warnings. The substring "{report}" will be replaced by an
                      itemised list of warnings from checkstyle.
    :param log_msg: the message passed on to check50.log in case there are
                    warnings. Again, "{report}" will be substituted.
    :param log_individual_warnings: if true, each warning will be logged on its
                                    own.

    All other parameters are as for :func:`run_checkstyle`.
    """
    report = run_checkstyle(**kwargs)
    if report:
        # all warnings as one string
        report_itemised = "\n".join(["- " + str(w) for w in report])

        if log_msg:
            check50.log(log_msg.format(report=report_itemised))
        if log_individual_warnings:
            for w in report:
                check50.log("- " + str(w))
        if rationale:
            rationale = rationale.format(report=report_itemised)
        else:
            rationale = "issues found"
        raise Failure(rationale=rationale)


def run_checkstyle(checks_file=None, target=None,
                   java=JAVA, timeout=None):
    """
    Execute the Checkstyle CLI and return a report.

    The checkstyle standalone jar file will be added to the classpath.

    :param str checks_file: the path to the checks xml file to be used
    :param str target: the path to those files checkstyle should inspect
    :param java: interpreter to use (default :data:`check50_checkstyle.JAVA`)
    :param timeout: number of seconds after which to time out and fail

    The return value is a list of CheckstyleWarning, each of which represents
    a complaint, as read from the XML report produced by checkstyle.
    """

    cmd = [
        java,
        '-jar', CHECKSTYLE_JAR_PATH,
        '-c', checks_file,
        '-f xml',
        target
    ]
    cmdline = " ".join(cmd) + " 2>/dev/null"

    # call subprocess and wait until it's done
    report = check50._api.run(cmdline).stdout(timeout=timeout)

    # supress log message introduced in previous command
    # which logs the full shell command (java -cp ..)
    check50._api._log.clear()

    return read_checkstyle_xml(report)


def read_checkstyle_xml(report, remove_path_prefix=''):
    """turn checkstyle XML report string into a list of CheckstyleWarning """
    root = ET.fromstring(report)

    report = []
    for file in root.findall('file'):
        f = file.attrib
        filename = os.path.basename(f['name'])
        f['errors'] = []
        for error in file.findall('error'):
            e = error.attrib
            # show only relative path to not expose the system checks run on
            e['filename'] = filename

            report.append(CheckstyleWarning(**e))
    return report
