import os
import pytest
from html.parser import HTMLParser

class ProjectHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.projects = []
        self.in_project_section = False
        self.view_more_button_exists = False
        self.hidden_projects_count = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "").split()
        div_id = attrs_dict.get("id", "")

        if tag == "section" and div_id == "projects":
            self.in_project_section = True

        if self.in_project_section:
            if tag == "div" and "project" in classes:
                self.projects.append(attrs_dict)
                if "hidden-project" in classes:
                    self.hidden_projects_count += 1

            if tag == "button" and attrs_dict.get("id") == "view-more-projects":
                self.view_more_button_exists = True

    def handle_endtag(self, tag):
        if tag == "section" and self.in_project_section:
            self.in_project_section = False

def test_projects_visibility():
    index_path = os.path.join("docs", "index.html")
    assert os.path.exists(index_path), "index.html not found"

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    parser = ProjectHTMLParser()
    parser.feed(content)

    # Verify total number of projects is 6
    assert len(parser.projects) == 6, f"Expected 6 projects, found {len(parser.projects)}"

    # Verify that the last 3 projects are initially hidden
    # Note: This checks for the class 'hidden-project'
    assert parser.hidden_projects_count == 3, f"Expected 3 hidden projects, found {parser.hidden_projects_count}"

    # Verify that the view more button exists
    assert parser.view_more_button_exists, "View More Projects button not found"
