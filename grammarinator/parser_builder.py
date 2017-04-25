# Copyright (c) 2017 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import logging

from antlr4 import *
from os import listdir
from os.path import basename, commonprefix, join, split, splitext
from pkgutil import get_data
from subprocess import CalledProcessError, Popen, PIPE

logger = logging.getLogger(__name__)

# Override ConsoleErrorListener to suppress parse issues in non-verbose mode.
class ConsoleListener(error.ErrorListener.ConsoleErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        logger.debug('line %d:%d %s' % (line, column, msg))
error.ErrorListener.ConsoleErrorListener.INSTANCE = ConsoleListener()


def build_grammars(out, antlr):
    """
    Build lexer and grammar from ANTLRv4 grammar files in Python3 target.

    :param out: Output directory.
    :param antlr: Path to the ANTLR4 tool (Java jar binary).
    :return: List of references/names of the lexer, parser and listener classes of the target.
    """
    try:
        # TODO: support Java parsers too.
        languages = {
            'python': {'antlr_arg': '-Dlanguage=Python3',
                       'ext': 'py',
                       'listener_format': 'Listener',
                       'sources': ['ANTLRv4Lexer.g4', 'ANTLRv4Parser.g4', 'LexBasic.g4', 'LexerAdaptor.py']
                       }
        }

        # Copy the grammars from the package to the given working directory.
        for resource in languages['python']['sources']:
            with open(join(out, resource), 'wb') as f:
                f.write(get_data(__package__, join('resources', 'antlr', resource)))

        grammars = tuple([file for file in languages['python']['sources'] if file.endswith('.g4')])

        # Generate parser and lexer in the target language and return either with
        # python class ref or the name of java classes.
        cmd = 'java -jar {antlr} {lang} {grammars}'.format(antlr=antlr,
                                                           lang=languages['python']['antlr_arg'],
                                                           grammars=' '.join(grammars))

        with Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, cwd=out) as proc:
            stdout, stderr = proc.communicate()
            if proc.returncode:
                logger.error('Building grammars %r failed!\n%s\n%s\n', grammars,
                             stdout.decode('utf-8', 'ignore'),
                             stderr.decode('utf-8', 'ignore'))
                raise CalledProcessError(returncode=proc.returncode, cmd=cmd, output=stdout + stderr)

        files = listdir(out)
        filename = basename(grammars[0])

        def file_endswith(end_pattern):
            return splitext(split(list(
                filter(lambda x: len(commonprefix([filename, x])) > 0 and x.endswith(end_pattern), files))[0])[1])[0]

        # Extract the name of lexer and parser from their path.
        lexer = file_endswith('Lexer.{ext}'.format(ext=languages['python']['ext']))
        parser = file_endswith('Parser.{ext}'.format(ext=languages['python']['ext']))
        # The name of the generated listeners differs if Python or other language target is used.
        listener = file_endswith('{listener_format}.{ext}'.format(listener_format=languages['python']['listener_format'], ext=languages['python']['ext']))

        return (getattr(__import__(x, globals(), locals(), [x], 0), x) for x in [lexer, parser, listener])
    except Exception as e:
        logger.error('Exception while loading parser modules', exc_info=e)
        raise e
