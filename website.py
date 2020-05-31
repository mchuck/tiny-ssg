import os
import logging
import yaml
import markdown

from typing import List
from datetime import datetime
from slugify import slugify

from logger import get_logger
from models import WebsitePage, WebsiteTag, Website, WebsiteCollection
from utils import get_all_files

log_default = get_logger(__name__)

def __create_page(page_file: str, collection:str) -> WebsitePage:
    with open(page_file, 'r') as page_f:
        page_text = page_f.read()
        md = markdown.Markdown(extensions = ['meta'], output_format='html5')
        page_html = md.convert(page_text) 
        page_meta = md.Meta
        page_title = page_meta['title'][0]
        return WebsitePage(page_title,
                           page_html,
                           page_meta['tags'],
                           datetime.strptime(page_meta['createdat'][0], "%Y-%m-%d"),
                           os.path.join('/', collection, 'pages',
                                        '{}.html'.format(slugify(page_title))),
                           slugify(page_title),
                           page_meta)


def __create_collection(base_path: str, collection: str) -> WebsiteCollection:
    log_default('\t%s', collection)
    collection_md_files = get_all_files(os.path.join(base_path, collection), '.md')
    pages = [__create_page(f, collection) for f in collection_md_files]
    pages = sorted(pages, key=lambda p: p.created_at, reverse=True)

    tags = {}

    for page in pages:
        for tag in page.tags:
            tag_entry = tags.get(tag, [])
            tag_entry.append(page)
            tags[tag] = tag_entry

    tag_list = [WebsiteTag(n, slugify(n), p) for n,p in tags.items()]

    return WebsiteCollection(collection, pages, tag_list)


def create_website_model(base_path: str, collections: List[str]) -> Website:
    meta = {}
    with open(os.path.join(base_path, 'meta.yaml')) as meta_file:
        meta = yaml.load(meta_file, Loader=yaml.BaseLoader)
    
    log_default('Creating collections...')

    collections = {c: __create_collection(base_path, c) for c in collections}
    website = Website(collections, meta)
    return website
