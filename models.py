from dataclasses import dataclass
from typing import List, Dict


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
