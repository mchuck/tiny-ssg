from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class WebsitePage:
    title: str
    body: str
    tags: List[str]
    created_at: str
    url: str
    slug: str
    meta: Dict

@dataclass
class WebsiteTag:
    name: str
    slug: str
    pages: List[WebsitePage]

@dataclass
class WebsiteCollection:
    name: str
    pages: List[WebsitePage]
    tags: List[WebsiteTag]

@dataclass
class Website:
    collections: Dict[str, WebsiteCollection]
    meta: Dict

@dataclass
class Templates:
    # TODO: Remove Any
    index_template: Any
    page_template: Any
    tag_template: Any
