import re
def parse(text: str) -> dict:
    meta = {"title": "", "text": "", "link": []}
    for line in text.splitlines():
        line = line.strip()
        if m := re.match(r'^(\w+)\s+"(.+)"$', line):
            tag, content = m.groups()
            if tag == "link":
                meta["link"].append(content.split('" "') if '"' in content else [content, content])
            else:
                meta[tag] = content
    return meta
