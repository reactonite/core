import os


def saveHtml(content, loc):
    """
    Takes body of the POST response from GrapesJS and saves HTML File

    Parameters
    ----------
    content : str
        HTML Content
    loc : str
        Location where we have to save the HTML File
    """

    html_front = '<!doctype html><html lang="en"><head><meta charset="utf-8"/><title>The HTML5 Herald</title><meta name="description" content="The HTML5 Herald"/><meta name="author" content="SitePoint"/><link rel="stylesheet" href="./main.css"/></head><body>'
    html_back = '</body></html>'
    html_content = html_front + content + html_back
    text_file = open(os.path.join(loc, 'index.html'), "w")
    text_file.write(html_content)
    text_file.close()


def saveCss(content, loc):
    """
    Takes body of the POST response from GrapesJS and saves CSS File

    Parameters
    ----------
    content : str
        CSS Content
    loc : str
        Location where we have to save the CSS File
    """

    text_file = open(os.path.join(loc, 'main.css'), "w")
    text_file.write(content)
    text_file.close()
