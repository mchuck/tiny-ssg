import argparse
import os
import markdown
import yaml

from dataclasses import dataclass
from typing import List, Dict
from jinja2 import Template
from slugify import slugify
from models import Website, WebsiteCollection, WebsitePage, WebsiteTag

PARSER = argparse.ArgumentParser()

PARSER.add_argument('--path', type=str, required=True)
PARSER.add_argument('--collection', action='append', required=True, type=str)
PARSER.add_argument('--theme', type=str, required=True)

ARGS = PARSER.parse_args()

def create_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def get_all_md_files(path: str):
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.md'):
                yield os.path.join(dirpath, filename)

def write_html_safe(path, html):
    directory = os.path.dirname(path)
    create_directory(directory)
    with open(path, 'w') as out_file:
        out_file.write(html)

def get_template_from_file(path):
    with open(path, 'r') as template_file:
        return Template(template_file.read())

# TODO: post -> page
def create_page(post_file: str, collection:str) -> WebsitePage:
    with open(post_file, 'r') as post_f:
        post_text = post_f.read()
        md = markdown.Markdown(extensions = ['meta'], output_format='html5')
        post_html = md.convert(post_text) 
        post_meta = md.Meta
        post_title = post_meta['title'][0]
        return WebsitePage(post_title,
                           post_html,
                           post_meta['tags'],
                           post_meta['createdat'][0],
                           os.path.join('/', collection, 'pages',
                                        '{}.html'.format(slugify(post_title))),
                           slugify(post_title),
                           post_meta)
        
if __name__ == "__main__":
    theme = ARGS.theme
    path = ARGS.path

    meta = {}

    with open(os.path.join(path, 'meta.yaml')) as meta_file:
        meta = yaml.load(meta_file, Loader=yaml.BaseLoader)
    
    collections = {}

    for collection in ARGS.collection:
        collection_md_files = get_all_md_files(os.path.join(path, collection))
        pages = [create_page(f, collection) for f in collection_md_files]

        tags = {}
    
        for page in pages:
            for tag in page.tags:
                tag_entry = tags.get(tag, [])
                tag_entry.append(page)
                tags[tag] = tag_entry

        tag_list = [WebsiteTag(n,p) for n,p in tags.items()]

        collections[collection] = WebsiteCollection(collection, pages, tag_list)

    website = Website(collections, meta)

    theme_path = os.path.join(path, 'themes', theme)
    dist_path = os.path.join(path, 'dist')
    create_directory(dist_path)

    # write index.html
    template = get_template_from_file(os.path.join(theme_path, 'index.html'))
    output = template.render(website=website)
    write_html_safe(os.path.join(dist_path, 'index.html'), output)

    for collection_name, collection in website.collections.items():

        # write collection_name/pages/...html
        template = get_template_from_file(os.path.join(theme_path, 'page.html'))
        for page in collection.pages: 
            output = template.render(page=page, website=website)
            page_directory = os.path.join(dist_path, collection_name, 'pages')
            page_path = os.path.join(page_directory, '{}.html'.format(page.slug))
            write_html_safe(page_path, output)

        # write collection_name/tags/...html
        template = get_template_from_file(os.path.join(theme_path, 'tag.html'))
        for tag in collection.tags: 
            output = template.render(tag=tag, website=website)
            tag_directory = os.path.join(dist_path, collection_name, 'tags')
            tag_path = os.path.join(tag_directory, '{}.html'.format(tag.name.lower()))
            write_html_safe(tag_path, output)

