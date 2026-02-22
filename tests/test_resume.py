import os
from html.parser import HTMLParser

class ResumeHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.h1 = ""
        self.subtitle = ""
        self.nav_links = []
        self.embed_src = ""
        self.in_title = False
        self.in_h1 = False
        self.in_subtitle = False
        self.in_nav = False
        self.current_a = None

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
        elif tag == "p":
            attrs_dict = dict(attrs)
            classes = attrs_dict.get("class", "").split()
            if "subtitle" in classes:
                self.in_subtitle = True
        elif tag == "nav":
            attrs_dict = dict(attrs)
            classes = attrs_dict.get("class", "").split()
            if "top-nav" in classes:
                self.in_nav = True
        elif tag == "a" and self.in_nav:
            attrs_dict = dict(attrs)
            if "href" in attrs_dict:
                self.current_a = {"text": "", "href": attrs_dict["href"]}
        elif tag == "embed":
            attrs_dict = dict(attrs)
            if "src" in attrs_dict:
                self.embed_src = attrs_dict["src"]

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
        elif tag == "p":
            self.in_subtitle = False
        elif tag == "nav":
            self.in_nav = False
        elif tag == "a":
            if self.current_a:
                self.nav_links.append(self.current_a)
                self.current_a = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_h1:
            self.h1 += data
        elif self.in_subtitle:
            self.subtitle += data
        elif self.current_a is not None:
            self.current_a["text"] += data

def test_resume_structure():
    resume_path = os.path.join("docs", "resume.html")
    assert os.path.exists(resume_path)

    with open(resume_path, "r", encoding="utf-8") as f:
        content = f.read()

    parser = ResumeHTMLParser()
    parser.feed(content)

    assert parser.title.strip() == "Benjamin Cox — Resume"
    assert parser.h1.strip() == "Benjamin Cox"
    assert parser.subtitle.strip() == "Mechatronics & Robotics Engineer"

    # Check navigation links
    expected_links = [
        {"text": "home", "href": "index.html"},
        {"text": "resume", "href": "resume.html"},
        {"text": "contact", "href": "index.html#contact"}
    ]

    assert len(parser.nav_links) == len(expected_links)
    for i in range(len(expected_links)):
        assert parser.nav_links[i]["text"].strip() == expected_links[i]["text"]
        assert parser.nav_links[i]["href"] == expected_links[i]["href"]

    # Check embed PDF
    assert parser.embed_src == "resources/Benjamin_Cox_Resume.pdf"
