
from typing import Optional, List, Union

from lark import Lark, Transformer, v_args
from lark.indenter import Indenter

from preql import Preql
from runtype import dataclass


def indent_str(indent):
    return ' ' * (indent)

@dataclass
class Text:
    lines: List[str]

    def _print_text(self, indent, inline=False):
        s = indent_str(indent)
        if inline:
            yield self.lines[0] + '\n'
        else:
            yield s + self.lines[0] + '\n'
        for line in self.lines[1:]:
            yield s + line + '\n'

    def _print_html(self):
        for line in self.lines:
            yield line
            yield '<br/>\n'


@dataclass
class Decl:
    name: str
    attrs: Optional[List[str]]
    text: Text

    def _print_text(self, indent):
        if self.attrs:
            attrs = '(%s)' % ', '.join(self.attrs)
        else:
            attrs = ''
        decl = f'{self.name}{attrs}'
        yield f'{indent_str(indent)}{decl}: '
        yield from self.text._print_text(indent+len(decl)+2, True)

    def _print_html(self):
        if self.attrs:
            attrs = '<em>(%s)</em>' % ', '.join(self.attrs)
        else:
            attrs = ''
        yield f'<b>{self.name}</b>{attrs}'
        yield from self.text._print_html()


@dataclass
class Section:
    name: str
    items: List[Union[Decl, Text]]

    def _print_text(self, indent):
        l = [f'{indent_str(indent)}{self.name}\n']
        for item in self.items:
            l += item._print_text(indent+4)
        return l

    def _print_html(self):
        yield '<div class="section">\n'
        yield '<h3>'
        yield self.name
        yield '</h3>\n'
        for item in self.items:
            yield from item._print_html()
        yield '</div>\n'

@dataclass
class DocString:
    header: Text
    sections: List[Section]

    def _print_text(self, indent):
        yield from self.header._print_text(indent)
        yield '\n'
        for section in self.sections:
            yield from section._print_text(indent)
            yield '\n'

    def _print_html(self):
        yield '<div class="doc">\n'
        for section in self.sections:
            yield from section._print_html()
        yield '</div>\n'

    def print_text(self):
        return ''.join(self._print_text(0))

    def print_html(self):
        return ''.join(self._print_html())



_inline = v_args(inline=True)
class DocTransformer(Transformer):
    def as_list(self, items):
        return items

    attrs = as_list
    section_items = as_list
    sections = as_list

    text = Text
    decl = _inline(Decl)
    section = _inline(Section)
    start = _inline(DocString)


class DocIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 1


parser = Lark.open('docstring.lark', rel_to=__file__,
                    parser='lalr', postlex=DocIndenter(),
                    maybe_placeholders=True,
                    )


def parse(s):
    tree = parser.parse(s)
    return DocTransformer().transform(tree)


def test_parser():
    s ="""
    Ok

    Parameters:
        Test_1: whatever
        Param2(int, optional): LALALA
                            BLA BLA BLA
                            YESYES
                                WHAT NOW???

    See Also:
        Whatever
            OK
        This counts too

    """
    res = parse(s)
    print(res.print_html())

def test_func():
    p = Preql()
    print(doc_func(p.sum))

test_parser()