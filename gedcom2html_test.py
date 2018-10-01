from gedcom2html import gedcom2html

g = Gedcom2html()
g.options.file_path = "demo/dutchroyalfamily.ged"
g.options.title = "Family tree of the Dutch Royal Family"
g.write_html()
