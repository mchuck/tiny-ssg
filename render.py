import os
import logging
import shutil

from utils import write_file_safe
from logger import setup_logging


log_default = setup_logging(logging.getLogger(__name__))


def __render_collection_item(template, path, slug, render_kwargs):
    output = template.render(**render_kwargs)
    page_path = os.path.join(path, '{}.html'.format(slug))
    log_default('\t\tRendering %s', page_path)
    write_file_safe(page_path, output)

def __render_collection(dist_path, collection_name, collection, website, templates):
    log_default('\tRendering pages...')
    page_directory = os.path.join(dist_path, collection_name, 'pages')
    
    for page in collection.pages:
        render_kwargs = {"page": page, "website": website}
        __render_collection_item(templates.page_template,
                                 page_directory,
                                 page.slug,
                                 render_kwargs)

    log_default('\tRendering tags...')
    tag_directory = os.path.join(dist_path, collection_name, 'tags')

    for tag in collection.tags: 
        render_kwargs = {"tag": tag, "website": website}
        __render_collection_item(templates.tag_template,
                                 tag_directory,
                                 tag.slug,
                                 render_kwargs)

def render_templates(dist_path, templates, website):
    # wipe dist folder
    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)

    output = templates.index_template.render(website=website)
    log_default('\tRendering index.html')
   
    write_file_safe(os.path.join(dist_path, 'index.html'), output)

    for collection_name, collection in website.collections.items():
        __render_collection(dist_path, collection_name, collection, website, templates)
