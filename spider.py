import http.client

import re

import unidecode as unidecode
from bs4 import BeautifulSoup
import nbformat
nbf = nbformat.v4 # import version directly


def clean(text):
    return unidecode.unidecode(text)


def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'\W+', '-', text)


c = http.client.HTTPSConnection("projecteuler.net")


for n in range(200, 0, -1):
    print(n)
    c.request("GET", "/problem=%d" % (n,))
    response = c.getresponse()
    data = response.read()
    html = BeautifulSoup(data, 'html.parser')
    title = html.h2.text
    description = html.find(role="problem")
    title = clean(title)
    description = str(description.encode("ascii"), 'ascii')
    nb = nbf.new_notebook()
    #print(description)
    markdown = "# %s\n## Problem %d \n\n%s" % (title, n, description)
    cells = [nbf.new_markdown_cell(markdown),
             nbf.new_code_cell("def solve():\n    # Your code here\n    \n"),
             nbf.new_markdown_cell("## Solution"),
             nbf.new_code_cell('solve()')
             ]
    nb['cells'].extend(cells)
    filename = "%03d-%s.ipynb" % (n, slugify(title))
    with open(filename, 'w') as f:
        nbformat.write(nb, f, version=4)


