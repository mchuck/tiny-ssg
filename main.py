import argparse
import os
import shutil
import logging

from website import create_website_model
from logger import get_logger, configure_logging
from utils import write_file_safe, get_all_files, create_directory
from template import load_templates
from render import render_templates
from server import run_server

PARSER = argparse.ArgumentParser()

PARSER.add_argument('--path', type=str, required=True)
PARSER.add_argument('--collection', action='append', required=True, type=str)
PARSER.add_argument('--theme', type=str, required=True)
PARSER.add_argument('--static', type=str, action='append', required=False)
PARSER.add_argument('--serve', default=False, action='store_true')
PARSER.add_argument('--port', type=int, default=8000)
PARSER.add_argument('--verbose', default=False, action='store_true')

ARGS = PARSER.parse_args()

configure_logging(ARGS.verbose)

log_default = get_logger(__name__)

def build_website(path, dist_path, theme_path, theme, collections, statics):
  
    website = create_website_model(path, collections)

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

    log_default('Done :thumbs_up:', not_verbose=True)

if __name__ == "__main__":
    theme = ARGS.theme
    path = ARGS.path

    dist_path = os.path.join(path, 'dist')
    theme_path = os.path.join(path, 'themes', theme)
    
    def init_build(path, dist_path, theme_path, theme, collections, statics):
        def rebuild():
            log_default('Building website at: %s...', path, not_verbose=True)
            build_website(path, dist_path, theme_path, theme, collections, statics)
        return rebuild

    build_fn = init_build(path, dist_path, theme_path, theme, ARGS.collection, ARGS.static)
    build_fn()

    if ARGS.serve:
        run_server(ARGS.port, dist_path, path, build_fn)
