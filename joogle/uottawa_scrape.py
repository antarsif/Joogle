import requests
import bs4 as soup
import json
import re

_DOC_ID = -1
_EN_COURSE_PATTERN = re.compile(r"^CSI (\d[1,2,3,4]\d*).*$", re.M)

f = open("courses.txt", "w")


def parse(c):
    h, d = c
    h = h.replace(u'\xa0', ' ')
    d = d.replace("\n", '')

    if not bool(re.match(_EN_COURSE_PATTERN, h)):
        return None

    global _DOC_ID
    _DOC_ID += 1

    return dict(id=_DOC_ID, title=h, body=d)

def make_soup(html):
        return soup.BeautifulSoup(html, "lxml").find("body")

def scrape(url="https://catalogue.uottawa.ca/en/courses/csi/", html=None, to_file=True):
    if html is None:
        r = requests.get(url)
        html = r.text
        
        if to_file:
            with open("data/uottawa.html", "w") as f:
                    f.write(r.text)
    
    if not html:
            return None
        
    return make_soup(html)
        
def to_json(html, filename="data/catalogue-uottawa-ca.json"):
    courses = []
    for c in html.find_all("div", {"class":"courseblock"}):
        title_find = c.find("p", {"class": "courseblocktitle noindent"})
        title_txt = (title_find and title_find.text) or ""

        desc_find = c.find("p", {"class": "courseblockdesc noindent"})
        desc_txt = (desc_find and desc_find.text) or ""

        out = parse((title_txt, desc_txt))
        if out:
            courses.append(out)
    
    js_file = json.dumps(courses, indent=2)
    
    if filename:
        with open(filename, "w") as f:
            f.write(js_file)
        
    return courses


def run():
    with open("data/uottawa.html") as f:
        html = f.read()
    
    my_soup = scrape(html=html)
    to_json(my_soup)
    
    
if __name__ == "__main__":
    run()
    
