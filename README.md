Tiny Static Site Generator
=====

Static site generator with [jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templates and [markdown](https://en.wikipedia.org/wiki/Markdown) support.

To run example, type in terminal:

```
python main.py --path ./example_site --theme example --collection posts
```

Website will be rendered inside `dist` folder in `example_site`. You can now serve it by typing:

```
cd ./example_site/dist && python -m http.server
```

Or you can rely on included server with [livereload](https://github.com/lepture/python-livereload):

```
python main.py --path ./example_site --theme example --collection posts --serve --port 8000
```

Example theme design based on [web design in 4 minutes](https://jgthms.com/web-design-in-4-minutes/).

## TODO

- [x] auto-reload
- [x] code syntax highlighting 
- [x] latex support
- [ ] zettelkasten support
- [ ] single file parsing
