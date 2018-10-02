from gedcom2html import Gedcom2html

# g = Gedcom2html()
# g.options.file_path = "demo/dutchroyalfamily.ged"
# g.options.title = "Family tree of the Dutch Royal Family"
# g.options.home_person_id = "I1208"
# g.write_html()


g = Gedcom2html()
g.options.file_path = "demo/americanpresidents.ged"
g.options.title = "American Presidents"
g.write_html()
