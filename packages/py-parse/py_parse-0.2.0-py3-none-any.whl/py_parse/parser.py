from typing import List

from py_parse import Nodes, WrongHTMLFormatError
from py_parse.base import RelaxedHTMLParser, MyHTMLParser


class Parser:
    def __init__(self):
        self.comments: List = []
        self.unclosed_nodes = Nodes()
        self.all_nodes: Nodes = Nodes()

    def parse(self, html: str, show_unclosed_tags: bool = True, strict_parsing: bool = True,
              auto_close: List[str] = None) -> Nodes:
        """
        Main functions to parse html source. Returns Nodes object back to use it with queries
        :param html: string html-content
        :param show_unclosed_tags: flag to show all unclosed tags on parsing error. If strict_parsing is False, then will
        be ignored
        :param strict_parsing: flag to check markup (closing tag must be for same opened tag etc.) if False then nothing
        checks and all relative-style query will return None or Error
        :param auto_close: list of tags for auto-closing when parse, can be used to fix markup issues
        :return: Nodes object
        :raises WrongHTMLFormatError if wrong format and strict_parsing is True
        """
        parser = MyHTMLParser(self, auto_close) if strict_parsing else RelaxedHTMLParser(self)
        self.comments.clear()
        self.unclosed_nodes = Nodes()
        parser.feed(html)
        if strict_parsing:
            if show_unclosed_tags and self.unclosed_nodes:
                message = "\nUNCLOSED TAGS:\n" + "\n".join(e.__repr__() for e in self.unclosed_nodes)
                print(message)
            unclosed_at_all = [e for e in self.all_nodes._flatten() if not e.closed]
            if unclosed_at_all:
                message = "\nThese tags was not closed (even by its parent):\n" + \
                          "\n".join(e.__repr__() for e in unclosed_at_all)
                print(message)
                raise WrongHTMLFormatError(
                    f'Some tags was not closed itself or by parents, count= {len(unclosed_at_all)}')
        return self.all_nodes

    def get_comments(self) -> List[str]:
        return self.comments[:]
