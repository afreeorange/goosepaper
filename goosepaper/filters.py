from datetime import datetime
from re import split
import locale

import arrow
from goosepaper import app


@app.template_filter('paragraphs')
def paragraphs(body=None):
    paragraphs = split(r'[\n\n]+', body)
    html = '\n'.join([u'<p>%s</p>' % paragraph for paragraph in paragraphs])
    return html


@app.template_filter('humanized_timestamp')
def humanized_timestamp(timestamp=False):
    """
    Return a human-readable timestamp
    """
    if not timestamp:
        return ''
    return arrow.get(timestamp).humanize()


@app.template_filter('iso_timestamp')
def iso_timestamp(timestamp=False):
    """
    Return an ISO8601 timestamp
    """
    if not timestamp:
        return ''
    return arrow.get(timestamp).isoformat()


@app.template_filter('number_with_commas')
def number_with_commas(number=0):
    """
    Return a number with comma separators
    """
    return locale.format('%d', number, grouping=True)
