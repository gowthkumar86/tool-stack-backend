from app.modules.html_parser.processor import HTMLParserProcessor
from app.modules.html_parser.schemas import HTMLParseResponse


_parser_processor = HTMLParserProcessor()


def parse_html(html: str) -> HTMLParseResponse:
    parsed = _parser_processor.parse(html)
    return HTMLParseResponse(**parsed)
