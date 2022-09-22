from typing import Optional, Union

from base.converters.base import Converter


class PythonDataToHTMLConverter(Converter):
    """
    Singleton Converter from python dictionary to html tags

    Attrs:
        `data`: python dictionary data
        `**kwargs`: format for dictionary keys to be changed to given values

    Note:
        Don't pass any key-word arguments (`**kwargs`) if you want keys to be tags.

    Examples:
        >>> PythonDataToHTMLConverter({"title": "Hello", "subtitle": "World"}, title="h1", subtitle="p").convert()
        '<h1>Hello</h1><p>World</p>'

    """
    data: Union[dict, list]
    table_like: Optional[bool] = False
    html_like_text: Optional[bool] = True
    tag_options: Optional[bool] = False
    kwargs: str

    def __init__(self, data, table_like, html_like_text, tag_options, **kwargs):
        self.data = data
        self.table_like = table_like
        self.html_like_text = html_like_text
        self.tag_options = tag_options
        self.format = kwargs
        self.html_entities = {"<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;", "'": "&apos;"}
        self.check_type()

    def convert(self) -> str:
        """
        Main function for converting dict to html

        Get keys of passed dict and then get values of format by those keys.
        We will eventually end up having tags instead of passed keys
        ({"title": "Hello World"}, title="h1") -> get key title in {"title": "Hello World"}.
        Then get value of **kwargs (format) by this key -> h1
        Add html like tags and close it.

        Note:
            If format with given key doesn't exist tag then it will be just key of data.

        Returns:
            result - HTML tags
        """
        result = ''

        if isinstance(self.data, dict):
            for key in self.data.keys():
                result += self.convert_helper(self.format.get(key, key), self.data[key])
        else:
            if self.table_like:
                result += self.table_like_converter(self.data)
            else:
                for datum in self.data:
                    for key in datum:
                        result += self.convert_helper(self.format.get(key, key), datum[key])
        return result

    def convert_helper(self, tag, text):
        if self.html_like_text:
            text = self.validate_text(text)
        if self.tag_options:
            tag_with_options, tag = self.separate_tag_options(tag)
            return f"<{tag_with_options}>{text}</{tag}>"
        return f"<{tag}>{text}</{tag}>"

    def table_like_converter(self, data: list):
        """
        Recursive function if list will be appeared.

        :param data: List json data
        :type: list
        :return:
        """
        result = ""
        for datum in data:
            result += "<li>"
            for key in datum.keys():

                if isinstance(datum[key], list):
                    # If value is list then recursion happens.
                    result += self.convert_helper(self.format.get(key, key), self.table_like_converter(datum[key]))
                else:
                    result += self.convert_helper(self.format.get(key, key), datum[key])
            result += "</li>"
        result = f"<ul>{result}</ul>"
        return result

    def validate_text(self, text: str):
        """
        Validator function in order to except bugs when <> symbols are passed as value
        :param text: Value of json
        :return: Validated text without making tags break
        :rtype: str
        """
        result = ''
        for letter in text:
            if value := self.html_entities.get(letter, False):
                result += value
            else:
                result += letter
        return result

    def check_type(self):
        if not any((isinstance(self.data, dict), isinstance(self.data, list))):
            raise ValueError("source.json file contains not json like text.")

    @staticmethod
    def separate_tag_options(tag: str) -> (str, str):
        separated_classes = tag.split(".")              # ['p', 'my-class-1', 'my-class-2#my-id']
        real_tag = separated_classes[0]                 # -> 'p'

        classes = " ".join(separated_classes[1:-1])     # -> 'my-class-1'.
        # Note: We are eradicating last one, because it contains #
        separate_ids = separated_classes[~0].split("#")            # ['my-class-2, my-id']
        if not classes:                                 # If '' then add without space
            classes += separate_ids[0]
        else:
            classes += " " + separate_ids[0]
        ids = " ".join(separate_ids[1:])                # Eradicating first index (class value)
        tag_with_options_result = real_tag + (f' id="{ids}"' if ids else "") + (f' class="{classes}"' if classes else "")
        return tag_with_options_result, real_tag
