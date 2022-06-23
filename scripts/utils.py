import re

def get_date_from_name(string):
    """
        Return matched date in format yyyy-mm-dd or '' if there is no match

        args
            - string containing text with date
    """
    return re.search('([0-9]{2}\-[0-9]{2}\-[0-9]{4})', string) or ''

def to_snake_case(string):
    """
        Convert string from camelCase to snake_case, used for renaming columns automation

        args:
            - string in CamelCase
    """
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    string = re.sub('__([A-Z])', r'_\1', string)
    string = re.sub('([a-z0-9])([A-Z])', r'\1_\2', string)
    return string.lower()