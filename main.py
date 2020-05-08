import argparse
import os
import markdown
import yaml
import shutil

from jinja2 import Environment, FileSystemLoader
from slugify import slugify
from models import Website, WebsiteCollection, WebsitePage, WebsiteTag

PARSER = argparse.ArgumentParser()

PARSER.add_argument('--path', type=str, required=True)
PARSER.add_argument('--collection', action='append', required=True, type=str)
PARSER.add_argument('--theme', type=str, required=True)
PARSER.add_argument('--static', type=str, action='append', required=False)

ARGS = PARSER.parse_args()

def create_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def get_all_files(path: str, extension: str='', negative=False):
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            condition = filename.endswith("{}".format(extension))
            if condition ^ negative:
                yield os.path.join(dirpath, filename)

def write_html_safe(path, html):
    directory = os.path.dirname(path)
    create_directory(directory)
    with open(path, 'w') as out_file:
        out_file.write(html)

def create_page(page_file: str, collection:str) -> WebsitePage:
    with open(page_file, 'r') as page_f:
        page_text = page_f.read()
        md = markdown.Markdown(extensions = ['meta'], output_format='html5')
        page_html = md.convert(page_text) 
        page_meta = md.Meta
        page_title = page_meta['title'][0]
        return WebsitePage(page_title,
                           page_html,
                           page_meta['tags'],
                           page_meta['createdat'][0],
                           os.path.join('/', collection, 'pages',
                                        '{}.html'.format(slugify(page_title))),
                           slugify(page_title),
                           page_meta)
        
if __name__ == "__main__":
    theme = ARGS.theme
    path = ARGS.path

    meta = {}

    with open(os.path.join(path, 'meta.yaml')) as meta_file:
        meta = yaml.load(meta_file, Loader=yaml.BaseLoader)
    
    collections = {}

    for collection in ARGS.collection:
        collection_md_files = get_all_files(os.path.join(path, collection), '.md')
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

    # wipe dist folder
    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)
    create_directory(dist_path)

    jinja_env = Environment(
        loader=FileSystemLoader(theme_path)
    )
    
    # write index.html
    template = jinja_env.get_template('index.html')
    output = template.render(website=website)
    write_html_safe(os.path.join(dist_path, 'index.html'), output)

    for collection_name, collection in website.collections.items():

        # write collection_name/pages/...html
        template = jinja_env.get_template('page.html')
        for page in collection.pages: 
            output = template.render(page=page, website=website)
            page_directory = os.path.join(dist_path, collection_name, 'pages')
            page_path = os.path.join(page_directory, '{}.html'.format(page.slug))
            write_html_safe(page_path, output)

        # write collection_name/tags/...html
        template = jinja_env.get_template('tag.html')
        for tag in collection.tags: 
            output = template.render(tag=tag, website=website)
            tag_directory = os.path.join(dist_path, collection_name, 'tags')
            tag_path = os.path.join(tag_directory, '{}.html'.format(tag.name.lower()))
            write_html_safe(tag_path, output)

    # add static files
    if ARGS.static:
        for static_dir in ARGS.static:
            static_path = os.path.join(path, static_dir)
            static_dist_path = os.path.join(dist_path, static_dir)
        
            for static_file in get_all_files(static_path):
                dest_path = static_file.replace(static_path, static_dist_path) 
                create_directory(os.path.dirname(dest_path))
                shutil.copy2(static_file, dest_path)

    # copy all non-html files from theme folder
    for theme_file in get_all_files(theme_path, '.html', negative=True):
        dest_path = theme_file.replace(theme_path, dist_path) 
        create_directory(os.path.dirname(dest_path))
        shutil.copy2(theme_file, dest_path)
