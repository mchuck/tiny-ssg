import markdown


EXT_CONFIG = {
    'codehilite': {
        'linenums': True, 
    }
}

MD = markdown.Markdown(extensions=['meta', 'codehilite','fenced_code', 'mdx_math'],
                       extension_configs=EXT_CONFIG,
                       output_format='html5'
)

def render_md(text):
    page_html = MD.convert(text) 
    page_meta = MD.Meta
    return page_html, page_meta
   
