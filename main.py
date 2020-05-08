import argparse
import os
import shutil
import logging

from website import create_website_model
from logger import setup_logging
from utils import write_file_safe, get_all_files, create_directory
from template import load_templates
from render import render_templates

PARSER = argparse.ArgumentParser()

PARSER.add_argument('--path', type=str, required=True)
PARSER.add_argument('--collection', action='append', required=True, type=str)
PARSER.add_argument('--theme', type=str, required=True)
PARSER.add_argument('--static', type=str, action='append', required=False)

ARGS = PARSER.parse_args()

log_default = setup_logging(logging.getLogger(__name__))
        
if __name__ == "__main__":
    theme = ARGS.theme
    path = ARGS.path

    theme_path = os.path.join(path, 'themes', theme)
    dist_path = os.path.join(path, 'dist')

    website = create_website_model(path, ARGS.collection)
    
    log_default('Loading "%s" theme...', theme)
    templates = load_templates(theme_path)

    log_default('Rendering templates...')
    render_templates(dist_path, templates, website)
   
    # add static files
    if ARGS.static:
        log_default('Adding static files...')
        for static_dir in ARGS.static:
            log_default('\tAdding "%s" folder', static_dir)
            static_path = os.path.join(path, static_dir)
            static_dist_path = os.path.join(dist_path, static_dir)
        
            for static_file in get_all_files(static_path):
                log_default('\t\tAdding "%s"...', static_file)
                dest_path = static_file.replace(static_path, static_dist_path) 
                create_directory(os.path.dirname(dest_path))
                shutil.copy2(static_file, dest_path)

    # copy all non-html files from theme folder
    for theme_file in get_all_files(theme_path, '.html', negative=True):
        dest_path = theme_file.replace(theme_path, dist_path) 
        create_directory(os.path.dirname(dest_path))
        shutil.copy2(theme_file, dest_path)

    log_default('Done :thumbs_up:')
