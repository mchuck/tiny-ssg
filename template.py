

from jinja2 import Environment, FileSystemLoader

from models import Templates

def load_templates(theme_path: str) -> Templates:
    

    jinja_env = Environment(
        loader=FileSystemLoader(theme_path)
    )
    
    index_template = jinja_env.get_template('index.html')
    tag_template = jinja_env.get_template('tag.html')
    page_template = jinja_env.get_template('page.html')

    return Templates(index_template,
                     page_template,
                     tag_template)
