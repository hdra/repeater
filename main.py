import markdown
import os
import codecs
from jinja2 import Environment, FileSystemLoader


def generate_contexts():
    md = markdown.Markdown(extensions=['meta'])
    contexts = list()
    files = ['content/{0}'.format(file)
             for file in os.listdir('content') if file.endswith('.md')]

    for f in files:
        content = codecs.open(f, encoding='utf-8').read()
        html = md.convert(content)
        context = dict()
        context['title'] = md.Meta['title'][0]
        context['date'] = md.Meta['date'][0]
        context['content'] = html
        contexts.append(context)
        md.reset()

    return contexts


def render(contexts):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')
    html = template.render(context=contexts)
    output = codecs.open('output.html', 'w', encoding='utf-8',
                         errors='xmlcharreplace')
    output.write(html)


def main():
    contexts = generate_contexts()
    render(contexts)


if __name__ == "__main__":
    main()
