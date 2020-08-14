import re
from .helpers import XPATH
from scrapy.selector import Selector


def extract_data(success_data):
    success_data = list(map(
        lambda x: {'URL': x[0],
                   'text': clear_text(Selector(text=x[1]).xpath(XPATH).extract_first(default=''))},
        success_data))
    return success_data


def clear_text(text):
    # remove html tags
    text = re.sub(r'\<[^>]*\>', '', str(text))
    # remove multiple whitespace
    text = re.sub(r'\s+', ' ', str(text).strip())
    return text
