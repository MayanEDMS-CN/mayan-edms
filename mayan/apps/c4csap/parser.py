from __future__ import unicode_literals, absolute_import

from document_parsing.parsers import Parser


class LibreOfficeDocumentTextParser(Parser):

    def __init__(self):
        pass

    def execute(self, file_object, page_number):
        pass


Parser.register("", LibreOfficeDocumentTextParser)