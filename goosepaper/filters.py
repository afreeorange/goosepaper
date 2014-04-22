from datetime import datetime
from re import split
from humanize import naturaltime

from goosepaper import app


@app.template_filter('paragraphs')
def paragraphs(body=None):
    paragraphs = split(r'[\n\n]+', body)
    html = '\n'.join([u'<p>%s</p>' % paragraph for paragraph in paragraphs])
    return html


@app.template_filter('humanized_datestamp')
def humanized_datestamp(time=False):
    """
    Return a human-readable timestamp
    """
    if not time:
        return ''
    return naturaltime(time)
