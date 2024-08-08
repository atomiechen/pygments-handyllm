import re
from pygments.lexer import RegexLexer, bygroups, using
from pygments.token import (
    Text, Name, String, Generic, Whitespace, Punctuation
)
from pygments.lexers.data import YamlLexer
from pygments.lexers.markup import MarkdownLexer


class HpromptLexer(RegexLexer):
    name = 'HandyPrompt'
    aliases = ['hprompt']
    filenames = ['*.hprompt', '*.hpr']

    # match line start and end using ^ and $, respectively
    # match any character including newline using .
    flags = re.MULTILINE | re.DOTALL
    
    tokens = {
        'root': [
            (r'\A---\s*$', String.Delimiter, 'frontmatter'),
            (r'^(\$\w+\$)(\s*)({)', bygroups(Generic.Heading, Whitespace, Punctuation), ('block_text', 'extra_properties')),
            (r'^(\$\w+\$)(\s*)$', bygroups(Generic.Heading, Whitespace), 'block_text'),
            (r'.+?', Text),
        ],
        'frontmatter': [
            (r'(.*?)(^---\s*$)', bygroups(using(YamlLexer), String.Delimiter), '#pop'),
        ],
        'extra_properties': [
            (r'\s+', Whitespace),
            (r'}', Punctuation, '#pop'),
            (r'(type)(\s*)(=)(\s*)("[^"]*"|\'[^\']*\')', bygroups(Name.Attribute, Whitespace, Punctuation, Whitespace, String), ('#pop', '#pop', 'block_yaml', 'extra_properties')),
            (r'(\w+)(\s*)(=)(\s*)("[^"]*"|\'[^\']*\')', bygroups(Name.Attribute, Whitespace, Punctuation, Whitespace, String)),
        ],
        'block_yaml': [
            (r'(.*?)(?=^\$\w+\$[^\S\r\n]*({[^{}]*?})?[^\S\r\n]*$)', bygroups(using(YamlLexer)), '#pop'),
            (r'(.*?)\Z', bygroups(using(YamlLexer)), '#pop'),
        ],
        'block_text': [
            (r'(.*?)(?=^\$\w+\$[^\S\r\n]*({[^{}]*?})?[^\S\r\n]*$)', bygroups(using(MarkdownLexer)), '#pop'),
            (r'(.*?)\Z', bygroups(using(MarkdownLexer)), '#pop'),
        ],
    }
