import re


def remove_html_tags(text: str) -> str:
    html_pattern = re.compile('<.*?>')
    clean_text = re.sub(html_pattern, '', text)
    return clean_text