from typing import Optional

from base.file_handlers import JSonFileHandler, HTMLFileHandler
from base.converters import JSonToPythonConverter, PythonDataToHTMLConverter


def converter(json_file_path: str,
              html_file_path: str,
              table_like: Optional[bool] = False,
              html_like_text: Optional[bool] = True,
              tag_options: Optional[bool] = False,
              **kwargs):
    """
    Main converter function

    Attrs:
        `json_file_path`: Path of json file
        `html_file_path`: Path of html file
        `kwargs`: Format of converter (See DictToHTMLConverter class for details)
    """

    parsed_str_json = JSonFileHandler(json_file_path).parse_json()
    json_data = JSonToPythonConverter(parsed_str_json).convert()
    final_html_text = PythonDataToHTMLConverter(json_data, table_like, html_like_text, tag_options, **kwargs).convert()
    HTMLFileHandler(html_file_path, final_html_text).create()

