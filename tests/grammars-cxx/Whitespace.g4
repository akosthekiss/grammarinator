/*
 * Copyright (c) 2017-2025 Renata Hodovan, Akos Kiss.
 *
 * Licensed under the BSD 3-Clause License
 * <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
 * This file may not be copied, modified, or distributed except
 * according to those terms.
 */

/*
 * This test checks whether the simple space transformer properly inserts spaces
 * in the output of generator. (If the transformer misbehaves, the ID rule will
 * consume all characters in the ANTLR-generated lexer and the parser will not
 * be able to match the input to the start rule.)
 */

// TEST-PROCESS-CXX: {grammar}.g4 -o {tmpdir}
// TEST-BUILD-CXX: --generator={grammar}Generator --serializer=grammarinator::runtime::SimpleSpaceSerializer --includedir={tmpdir} --builddir={tmpdir}/build
// TEST-GENERATE-CXX: {tmpdir}/build/bin/grammarinator-generate-{grammar_lower} -r start -o {tmpdir}/{grammar}%d.txt
// TEST-ANTLR: {grammar}.g4 -o {tmpdir}
// TEST-REPARSE: -p {grammar}Parser -l {grammar}Lexer -r start {tmpdir}/{grammar}%d.txt

grammar Whitespace;

start: 'keywords' 'must' 'be' 'separated' 'by' 'whitespace';

ID: [a-z]+;

WHITESPACE: [ \t\r\n] -> skip;
