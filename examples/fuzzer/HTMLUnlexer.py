# Generated by Grammarinator 17.5r

from itertools import chain
from grammarinator.runtime import *

charset_0 = list(chain(*multirange_diff(printable_unicode_ranges, [(60, 61)])))
charset_1 = list(chain(range(32, 33), range(9, 10), range(13, 14), range(10, 11)))
charset_2 = list(chain(range(97, 103), range(65, 71), range(48, 58)))
charset_3 = list(chain(range(48, 58)))
charset_4 = list(chain(range(58, 59), range(97, 123), range(65, 91)))
charset_5 = list(chain(range(32, 33)))
charset_6 = list(chain(range(48, 58), range(97, 123), range(65, 91)))
charset_7 = list(chain(range(48, 58), range(97, 103), range(65, 71)))
charset_8 = list(chain(range(48, 58)))
charset_9 = list(chain(*multirange_diff(printable_unicode_ranges, [(34, 35),(60, 61)])))
charset_10 = list(chain(*multirange_diff(printable_unicode_ranges, [(39, 40),(60, 61)])))


class HTMLUnlexer(Grammarinator):

    def __init__(self):
        super(HTMLUnlexer, self).__init__()
        self.lexer = self
        self.set_options()

    
    
    def style_sheet(self):
        return UnlexerRule(src='')
    
    def HTML_COMMENT(self):
        current = self.create_node(UnlexerRule(name='HTML_COMMENT'))
        current += self.create_node(UnlexerRule(src='<!--'))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.any_char())

        current += self.create_node(UnlexerRule(src='-->'))
        return current

    def HTML_CONDITIONAL_COMMENT(self):
        current = self.create_node(UnlexerRule(name='HTML_CONDITIONAL_COMMENT'))
        current += self.create_node(UnlexerRule(src='<!['))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.any_char())

        current += self.create_node(UnlexerRule(src=']>'))
        return current

    def XML_DECLARATION(self):
        current = self.create_node(UnlexerRule(name='XML_DECLARATION'))
        current += self.create_node(UnlexerRule(src='<?xml'))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.any_char())

        current += self.create_node(UnlexerRule(src='>'))
        return current

    def CDATA(self):
        current = self.create_node(UnlexerRule(name='CDATA'))
        current += self.create_node(UnlexerRule(src='<![CDATA['))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.any_char())

        current += self.create_node(UnlexerRule(src=']]>'))
        return current

    def DTD(self):
        current = self.create_node(UnlexerRule(name='DTD'))
        current += self.create_node(UnlexerRule(src='<!'))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.any_char())

        current += self.create_node(UnlexerRule(src='>'))
        return current

    def SCRIPTLET(self):
        current = self.create_node(UnlexerRule(name='SCRIPTLET'))
        weights = [1, 1]
        choice = self.choice(weights)
        if choice == 0:
            current += self.create_node(UnlexerRule(src='<?'))
            for _ in self.zero_or_more():
                current += UnlexerRule(src=self.any_char())

            current += self.create_node(UnlexerRule(src='?>'))
        elif choice == 1:
            current += self.create_node(UnlexerRule(src='<%'))
            for _ in self.zero_or_more():
                current += UnlexerRule(src=self.any_char())

            current += self.create_node(UnlexerRule(src='%>'))
        return current

    def SEA_WS(self):
        current = self.create_node(UnlexerRule(name='SEA_WS'))
        for _ in self.one_or_more():
            weights = [1, 1, 1]
            choice = self.choice(weights)
            if choice == 0:
                current += self.create_node(UnlexerRule(src=' '))
            elif choice == 1:
                current += self.create_node(UnlexerRule(src='\t'))
            elif choice == 2:
                for _ in self.zero_or_one():
                    current += self.create_node(UnlexerRule(src='\r'))

                current += self.create_node(UnlexerRule(src='\n'))

        return current

    def SCRIPT_OPEN(self):
        current = self.create_node(UnlexerRule(name='SCRIPT_OPEN'))
        current += self.create_node(UnlexerRule(src='<script'))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.any_char())

        current += self.create_node(UnlexerRule(src='>'))
        return current

    def STYLE_OPEN(self):
        current = self.create_node(UnlexerRule(name='STYLE_OPEN'))
        current += self.create_node(UnlexerRule(src='<style'))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.any_char())

        current += self.create_node(UnlexerRule(src='>'))
        return current

    def TAG_OPEN(self):
        current = self.create_node(UnlexerRule(name='TAG_OPEN'))
        current += self.create_node(UnlexerRule(src='<'))
        return current

    def HTML_TEXT(self):
        current = self.create_node(UnlexerRule(name='HTML_TEXT'))
        for _ in self.one_or_more():
            current += UnlexerRule(src=self.char_from_list(charset_0))

        return current

    def TAG_CLOSE(self):
        current = self.create_node(UnlexerRule(name='TAG_CLOSE'))
        current += self.create_node(UnlexerRule(src='>'))
        return current

    def TAG_SLASH_CLOSE(self):
        current = self.create_node(UnlexerRule(name='TAG_SLASH_CLOSE'))
        current += self.create_node(UnlexerRule(src='/>'))
        return current

    def TAG_SLASH(self):
        current = self.create_node(UnlexerRule(name='TAG_SLASH'))
        current += self.create_node(UnlexerRule(src='/'))
        return current

    def TAG_EQUALS(self):
        current = self.create_node(UnlexerRule(name='TAG_EQUALS'))
        current += self.create_node(UnlexerRule(src='='))
        return current

    def TAG_NAME(self):
        current = self.create_node(UnlexerRule(name='TAG_NAME'))
        current += self.lexer.TAG_NameStartChar()
        for _ in self.zero_or_more():
            current += self.lexer.TAG_NameChar()

        return current

    def TAG_WHITESPACE(self):
        current = self.create_node(UnlexerRule(name='TAG_WHITESPACE'))
        current += self.create_node(UnlexerRule(src=self.char_from_list(charset_1)))
        return current

    def HEXDIGIT(self):
        current = self.create_node(UnlexerRule(name='HEXDIGIT'))
        current += self.create_node(UnlexerRule(src=self.char_from_list(charset_2)))
        return current

    def DIGIT(self):
        current = self.create_node(UnlexerRule(name='DIGIT'))
        current += self.create_node(UnlexerRule(src=self.char_from_list(charset_3)))
        return current

    def TAG_NameChar(self):
        current = self.create_node(UnlexerRule(name='TAG_NameChar'))
        weights = [1, 1, 1, 1, 1, 1, 1, 1]
        choice = self.choice(weights)
        if choice == 0:
            current += self.lexer.TAG_NameStartChar()
        elif choice == 1:
            current += self.create_node(UnlexerRule(src='-'))
        elif choice == 2:
            current += self.create_node(UnlexerRule(src='_'))
        elif choice == 3:
            current += self.create_node(UnlexerRule(src='.'))
        elif choice == 4:
            current += self.lexer.DIGIT()
        elif choice == 5:
            current += self.create_node(UnlexerRule(src='\u00B7'))
        elif choice == 6:
            current += self.create_node(UnlexerRule(src=self.char_from_list(range(768, 879))))
        elif choice == 7:
            current += self.create_node(UnlexerRule(src=self.char_from_list(range(8255, 8256))))
        return current

    def TAG_NameStartChar(self):
        current = self.create_node(UnlexerRule(name='TAG_NameStartChar'))
        weights = [1, 1, 1, 1, 1, 1]
        choice = self.choice(weights)
        if choice == 0:
            current += self.create_node(UnlexerRule(src=self.char_from_list(charset_4)))
        elif choice == 1:
            current += self.create_node(UnlexerRule(src=self.char_from_list(range(8304, 8591))))
        elif choice == 2:
            current += self.create_node(UnlexerRule(src=self.char_from_list(range(11264, 12271))))
        elif choice == 3:
            current += self.create_node(UnlexerRule(src=self.char_from_list(range(12289, 55295))))
        elif choice == 4:
            current += self.create_node(UnlexerRule(src=self.char_from_list(range(63744, 64975))))
        elif choice == 5:
            current += self.create_node(UnlexerRule(src=self.char_from_list(range(65008, 65533))))
        return current

    def SCRIPT_BODY(self):
        current = self.create_node(UnlexerRule(name='SCRIPT_BODY'))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.any_char())

        current += self.create_node(UnlexerRule(src='</script>'))
        return current

    def SCRIPT_SHORT_BODY(self):
        current = self.create_node(UnlexerRule(name='SCRIPT_SHORT_BODY'))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.any_char())

        current += self.create_node(UnlexerRule(src='</>'))
        return current

    def STYLE_BODY(self):
        current = self.create_node(UnlexerRule(name='STYLE_BODY'))
        current += self.style_sheet()
        current += self.create_node(UnlexerRule(src='</style>'))
        return current

    def STYLE_SHORT_BODY(self):
        current = self.create_node(UnlexerRule(name='STYLE_SHORT_BODY'))
        current += self.style_sheet()
        current += self.create_node(UnlexerRule(src='</>'))
        return current

    def ATTVALUE_VALUE(self):
        current = self.create_node(UnlexerRule(name='ATTVALUE_VALUE'))
        for _ in self.zero_or_more():
            current += self.create_node(UnlexerRule(src=self.char_from_list(charset_5)))

        current += self.lexer.ATTRIBUTE()
        return current

    def ATTRIBUTE(self):
        current = self.create_node(UnlexerRule(name='ATTRIBUTE'))
        weights = [1, 1, 1, 1, 1]
        choice = self.choice(weights)
        if choice == 0:
            current += self.lexer.DOUBLE_QUOTE_STRING()
        elif choice == 1:
            current += self.lexer.SINGLE_QUOTE_STRING()
        elif choice == 2:
            current += self.lexer.ATTCHARS()
        elif choice == 3:
            current += self.lexer.HEXCHARS()
        elif choice == 4:
            current += self.lexer.DECCHARS()
        return current

    def ATTCHAR(self):
        current = self.create_node(UnlexerRule(name='ATTCHAR'))
        weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        choice = self.choice(weights)
        if choice == 0:
            current += self.create_node(UnlexerRule(src='-'))
        elif choice == 1:
            current += self.create_node(UnlexerRule(src='_'))
        elif choice == 2:
            current += self.create_node(UnlexerRule(src='.'))
        elif choice == 3:
            current += self.create_node(UnlexerRule(src='/'))
        elif choice == 4:
            current += self.create_node(UnlexerRule(src='+'))
        elif choice == 5:
            current += self.create_node(UnlexerRule(src=','))
        elif choice == 6:
            current += self.create_node(UnlexerRule(src='?'))
        elif choice == 7:
            current += self.create_node(UnlexerRule(src='='))
        elif choice == 8:
            current += self.create_node(UnlexerRule(src=':'))
        elif choice == 9:
            current += self.create_node(UnlexerRule(src=';'))
        elif choice == 10:
            current += self.create_node(UnlexerRule(src='#'))
        elif choice == 11:
            current += self.create_node(UnlexerRule(src=self.char_from_list(charset_6)))
        return current

    def ATTCHARS(self):
        current = self.create_node(UnlexerRule(name='ATTCHARS'))
        for _ in self.one_or_more():
            current += self.lexer.ATTCHAR()

        for _ in self.zero_or_one():
            current += self.create_node(UnlexerRule(src=' '))

        return current

    def HEXCHARS(self):
        current = self.create_node(UnlexerRule(name='HEXCHARS'))
        current += self.create_node(UnlexerRule(src='#'))
        for _ in self.one_or_more():
            current += self.create_node(UnlexerRule(src=self.char_from_list(charset_7)))

        return current

    def DECCHARS(self):
        current = self.create_node(UnlexerRule(name='DECCHARS'))
        for _ in self.one_or_more():
            current += self.create_node(UnlexerRule(src=self.char_from_list(charset_8)))

        for _ in self.zero_or_one():
            current += self.create_node(UnlexerRule(src='%'))

        return current

    def DOUBLE_QUOTE_STRING(self):
        current = self.create_node(UnlexerRule(name='DOUBLE_QUOTE_STRING'))
        current += self.create_node(UnlexerRule(src='"'))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.char_from_list(charset_9))

        current += self.create_node(UnlexerRule(src='"'))
        return current

    def SINGLE_QUOTE_STRING(self):
        current = self.create_node(UnlexerRule(name='SINGLE_QUOTE_STRING'))
        current += self.create_node(UnlexerRule(src='\''))
        for _ in self.zero_or_more():
            current += UnlexerRule(src=self.char_from_list(charset_10))

        current += self.create_node(UnlexerRule(src='\''))
        return current

    def set_options(self):
        self.options = dict(tokenVocab="HTMLLexer", dot="any_unicode_char")
