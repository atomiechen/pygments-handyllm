import re
from pygments.lexer import RegexLexer, bygroups, using, DelegatingLexer
from pygments.token import (
    Text, Name, String, Generic, Whitespace, Punctuation, Other
)
from pygments.lexers.data import YamlLexer
from pygments.lexers.markup import MarkdownLexer


class HpromptExtraProperties(RegexLexer):
    tokens = {
        'root': [
            (r'\s', Whitespace),
            (r'{', Punctuation, 'extra_properties'),
        ],
        'extra_properties': [
            (r'\s+', Whitespace),
            (r'}', Punctuation, '#pop'),
            (r'(\w+)(\s*)(=)(\s*)("[^"]*"|\'[^\']*\')', bygroups(Name.Attribute, Whitespace, Punctuation, Whitespace, String)),
        ],
    }


class HpromptRootLexer(RegexLexer):
    # match line start and end using ^ and $, respectively
    # match any character including newline using .
    flags = re.MULTILINE | re.DOTALL
    
    tokens = {
        'root': [
            (r'(\A---\s*$)(.*?)(^---\s*$)', bygroups(String.Delimiter, using(YamlLexer), String.Delimiter)),
            (
                r'^(\$\w+\$)(\s*)({[^{}]*?type\s*=[^{}]*})(\s*)$(.*?)((?=^\$\w+\$\s*({[^{}]*?})?\s*$)|\Z)', 
                bygroups(Generic.Heading, Whitespace, using(HpromptExtraProperties), Whitespace, using(YamlLexer))
            ),
            (
                r'^(\$\w+\$)(\s*)({[^{}]*?})?(\s*)$(.*?)((?=^\$\w+\$\s*({[^{}]*?})?\s*$)|\Z)', 
                bygroups(Generic.Heading, Whitespace, using(HpromptExtraProperties), Whitespace, using(MarkdownLexer))
            ),
            (r'.', Text),
        ],
    }


class HpromptVariableLexer(RegexLexer):
    # match line start and end using ^ and $, respectively
    # match any character including newline using .
    flags = re.MULTILINE | re.DOTALL
    tokens = {
        'root': [
            (r'%\w+%', Name.Variable),
            (r'.', Other),
        ],
    }


class HpromptLexer(DelegatingLexer):
    name = 'HandyPrompt'
    aliases = ['hprompt']
    filenames = ['*.hprompt', '*.hpr']
    
    def __init__(self, **options):
        super().__init__(HpromptRootLexer, HpromptVariableLexer, **options)

