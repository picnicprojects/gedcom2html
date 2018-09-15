from gedcom import Gedcom
from datetime import datetime
import codecs, json, os, shutil, string

class Person:
   def __init__(self,e,g):
      self.__e = e
      self.__g = g
      self.id = e.get_pointer().replace("@","")
      self.first_name = e.get_name()[0]
      self.surname = e.get_name()[1]
      self.notes = e.get_notes()
      self.family = []
      self.siblings = []
      try:
         self.birth_date = datetime.strptime(e.get_birth_data()[0], '%d %b %Y').date()
      except:
         pass
      try:
         self.death_date = datetime.strptime(e.get_death_data()[0], '%d %b %Y').date()
      except:
         pass
      if e.get_gender() == 'M':
         self.gender = "<i class='fa fa-mars'></i>"
      else:
         self.gender = "<i class='fa fa-venus'></i>"
      self.__create_link()

   def __get_parents(self, current_element, current_person):
      m = self.__g.get_parents(current_element)
      if len(m) > 0:
         current_person.parents = []
         for parent_element in m:
            new_person = Person(parent_element, self.__g)
            self.__get_parents(parent_element, new_person)
            current_person.parents.append(new_person)
      
   def get_parents(self):
      self.__get_parents(self.__e, self)
      
   def __get_families(self, current_element, current_person):
      fl = self.__g.get_families(current_element)
      if len(fl) > 0:
         for f in fl:
            found = 0
            fam = Family()
            fam.id = f.get_pointer().replace("@","")
            h = self.__g.get_family_members(f, 'HUSB')
            if len(h) > 0:
               if (current_element <> h[0]):
                  fam.spouse = Person(h[0], self.__g)
                  found = 1
            w = self.__g.get_family_members(f, 'WIFE')
            if len(w) > 0:
               if (current_element <> w[0]):
                  fam.spouse = Person(w[0], self.__g)
                  found = 1
            c = self.__g.get_family_members(f, 'CHIL')
            if len(c) > 0:
               fam.children = []
               for p in c:
                  child = Person(p, self.__g)
                  fam.children.append(child)
                  child = self.__get_families(p, child)
                  found = 1
            if found == 1:
               current_person.family.append(fam)
            
   def get_families(self):
      self.__get_families(self.__e, self)
      
   def get_siblings(self):
      pl = self.__g.get_parents(self.__e)
      list_of_child_ids = []
      if len(pl) > 0:
         for parent_element in pl:
            fl = self.__g.get_families(parent_element)
            if len(fl) > 0:
               for family_element in fl:
                  c = self.__g.get_family_members(family_element, 'CHIL')
                  if len(c) > 0:
                     for p in c:
                        child = Person(p, self.__g)
                        if child.id not in list_of_child_ids:
                           if child.id <> self.id:
                              list_of_child_ids.append(str(child.id))
                              self.siblings.append(child)
      
   def __json_value(self,p):
      s = '"name": "%s",\n' %(p.first_name)
      s = s+ '"surname": "%s",\n' %(p.surname)
      s = s + '"id": "%s",\n' %(p.id)
      return(s)
      
   def json(self):
      s = "{\n"
      s = s + self.__json_value(self)
      if hasattr(self, 'parents'):
         s = s + '"_parents": [\n'
         for p in self.parents:
            s = s + '{\n'
            s = s + self.__json_value(p)
            s = s + '},\n'
         s = s + '],\n'
      if hasattr(self, 'family'):
         for f in self.family:
            if hasattr(f, 'children'):
               s = s + '"_children": [\n'
               for c in f.children:
                  s = s + '{\n'
                  s = s + self.__json_value(c)
                  s = s + '},\n'
               s = s + '],\n'
      s = s + '};\n'
      return(s)
               
   def __create_link(self):
      self.link = self.id + '_'
      self.link = self.link + self.first_name + '_'
      self.link = self.link + self.surname + '.html'
      self.link = self.link.replace(' ','_')
      valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
      self.link = ''.join(c for c in self.link if c in valid_chars)
      
class Family:
   def __init__(self):
      self.children = []

class Html:
   def __init__(self, p, file_path):
      self.person = p
      self.__filepath = file_path
      self.__fname = self.__create_filename()
      self.__fid = codecs.open(self.__fname, encoding='utf-8',mode='w')

   def __del__(self):
      self.__fid.close()

   def __create_filename(self):
      str = 'generated/' + self.person.link
      return str
      
   def __create_person_single_line_short(self, p):
      s = "%s %s %s " % (p.gender, p.first_name, p.surname)
      return(s)
      
   def __create_person_single_line_dates(self, p):
      s = ""
      if hasattr(p,'birth_date'):
         s = s + "<i class='fa fa-star'></i> %s " % '{0.day:02d}-{0.month:02d}-{0.year:4d}'.format(p.birth_date)
      if hasattr(p,'death_date'):
         s = s + "<i class='fa fa-plus'></i> %s " % '{0.day:02d}-{0.month:02d}-{0.year:4d}'.format(p.death_date)
      if hasattr(p,'birth_date') & hasattr(p,'death_date'):
      # self.death_date.year - self.birth_date.year - ((today.month, today.day) < (born.month, born.day))
         age =  p.death_date.year - p.birth_date.year
         if age == 0:
            age =  p.death_date.month - p.birth_date.month
            s = s + "(%s months) " % age
         else:
            s = s + "(%s years) " % age
      return(s)
   def __create_person_single_line_long(self, p):
      s = self.__create_person_single_line_dates(p)
      if len(s) > 0:
         s = ("<a href='%s'>%s</a> <span class='dates'>%s</span>" % (p.link, self.__create_person_single_line_short(p), s))
      else:
         s = ("<a href='%s'>%s</a>" % (p.link, self.__create_person_single_line_short(p)))
      return(s)

      
   def write_header(self):
      self.__fid.write("<!DOCTYPE html>\n")
      self.__fid.write("<html lang='en'>\n")
      self.__fid.write("<head>\n")
      self.__fid.write("<title>%s</title>\n" % self.person.first_name)
      self.__fid.write("<meta name=\"description\" content=\"gedcom2html\" /><meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
      self.__fid.write("<meta http-equiv='Content-Type' content='text/html;charset=utf-8' />\n")
      self.__fid.write("<link rel='stylesheet' type='text/css' href='css/gedcom2html.css' media='screen, projection, print' />\n")
      self.__fid.write("<link rel='stylesheet' type='text/css' href='css/font-awesome.min.css' />\n")
      self.__fid.write("<link rel='stylesheet' type='text/css' href='css/bootstrap.min.css' />\n")
      self.__fid.write("<script type='text/javascript' src='js/jquery-3.1.1.min.js'></script>\n")
      self.__fid.write("<script type='text/javascript' src='js/bootstrap.min.js'></script>\n")
      self.__fid.write("<script type='text/javascript' src='js/gedcom2html.js'></script>\n")
      # self.__fid.write("<script type='text/javascript' src='../js/d3.min.js'></script>\n")
      # self.__fid.write("<script type='text/javascript' src='../js/d3plus.min.js'></script>\n")
      # self.__fid.write("<script type='text/javascript' src='../js/d3tree.js'></script>\n")
      self.__fid.write("</head>\n")
      self.__fid.write("<body>\n")
      self.__fid.write("<div class='container'>\n")
      self.__fid.write("<div class='row'>\n")
      
   def __write_parents(self, person, level):
      s  = '   '*level
      if level == 1:
         self.__fid.write("%s<ul class='tree' id='ul_parent_%s'>\n" % (s,person.id))
      else:
         self.__fid.write("%s<ul class='tree'>\n" % (s))
      for f in person.parents:
         arrow = ""
         if hasattr(f, 'parents'):
            if level == 0:
               arrow = "<i class='fa fa-arrow-circle-right' id='parent_%s' onclick='toggle_tree(\"parent_%s\")'></i>" % (f.id, f.id)
         self.__fid.write("%s   <li>%s" % (s, arrow))
         self.__fid.write(" %s\n" % (self.__create_person_single_line_long(f)))
         if hasattr(f, 'parents'):
            self.__write_parents(f, level + 1)
      self.__fid.write("%s</ul>\n" % s)
      
   def __write_family(self, current_person, level):
      s = '   '*level
      n = len(current_person.family)
      for index, family in enumerate(current_person.family):
         # SPOUSE
         show_spouse = 0
         if level == 0:
            if hasattr(family,'spouse'):
               show_spouse = 1
         if show_spouse:
            if index == 0:
               self.__fid.write("<ul class='tree'>\n")
            if len(family.spouse.surname) > 0:
               self.__fid.write("<li><i class='fa fa-heart' style='color:#faa'></i> %s\n" %  (self.__create_person_single_line_long(family.spouse)))
         # CHILDREN
         if hasattr(family,'children'):
            if level == 1:
               self.__fid.write("%s<ul class='tree' id='ul_children_%s'>\n" % (s, current_person.id))
            else:
               self.__fid.write("%s<ul class='tree'>\n" % (s))
            for p in family.children:
               arrow = ""
               if level == 0:
                  if len(p.family) > 0:
                     arrow = "<i class='fa fa-arrow-circle-right' id='children_%s' onclick='toggle_tree(\"children_%s\")'></i>" % (p.id, p.id)
               self.__fid.write("%s   <li>%s" % (s, arrow))
               self.__fid.write(" %s\n" % (self.__create_person_single_line_long(p)))
               if hasattr(p, 'family'):
                  self.__write_family(p, level + 1)
            self.__fid.write("%s</ul>\n" % s)
         # SPOUSE
         if show_spouse:
            if index == (n-1):
               self.__fid.write("</ul>\n")
                  
   def __write_siblings(self, p):
      self.__fid.write("<ul>\n")
      for s in p.siblings:
         self.__fid.write("<li>%s\n" % (self.__create_person_single_line_long(s)))
      self.__fid.write("</ul>\n")
         
      
   def write_section_person(self):
      self.__fid.write("<div class='well'>\n")
      self.__fid.write("<h1>%s</h1>\n" %  self.__create_person_single_line_short(self.person))
      self.__fid.write("<ul>\n")
      s = self.__create_person_single_line_dates(self.person)
      if len(s)>0:
         self.__fid.write("<li>%s\n" %  s)
      s = self.person.notes
      if len(s)>0:
         self.__fid.write("<li>%s\n" %  s)
      self.__fid.write("<ul>\n")
      self.__fid.write("</div>\n")
      self.__fid.write("</div><!-- row -->\n")
      self.__fid.write("<div class='row'>\n")
      # self.__fid.write("<div class='col-sm-12'>\n")
      if hasattr(self.person, 'parents'):
         self.__fid.write("<h2>Parents</h2>\n")
         self.__write_parents(self.person, 0)
      self.__fid.write("<h2>Families and children</h2>\n")
      self.__write_family(self.person, 0)
      self.__fid.write("<h2>Siblings</h2>\n")
      self.__write_siblings(self.person)
      # self.__fid.write("</div><!-- col -->\n")

   def write_section_statistics(self, n):
      self.__fid.write("</div><!-- row -->\n")
      # self.__fid.write("<div class='col-sm-1'>\n")
      # self.__fid.write("</div>\n")
      self.__fid.write("</div>\n")
      
   def write_hourglass_tree(self, j):
      self.__fid.write("<div class='col-sm-6'>\n")
      self.__fid.write("<h2>Tree</h2>\n")
      self.__fid.write("<div class='tree'></div>\n")
      self.__fid.write("<script>\n")
      self.__fid.write("var json = " +j)
      self.__fid.write("drawTree(json);\n")
      self.__fid.write("</script>\n")
      self.__fid.write("</div>\n")
      
   
   def write_footer(self,n):
      self.__fid.write("</div><!-- row -->\n")
      self.__fid.write("</div><!-- container -->\n")
      self.__fid.write("<footer>\n")
      self.__fid.write("<a href=''>%s</a> contains %d persons\n" % ( self.__filepath, n))
      self.__fid.write("<center>gedcom2html</center>\n")
      self.__fid.write("</footer>\n")
      self.__fid.write("</body>\n")
      self.__fid.write("</html>\n")
      self.__fid.close()

def copy_assets():
   shutil.rmtree('generated')
   os.makedirs('generated/js')
   os.makedirs('generated/css')
   shutil.copy2('gedcom2html.css','generated/css/')   
   shutil.copy2('gedcom2html.js', 'generated/js/')
   shutil.copy2('assets/css/font-awesome.min.css', 'generated/css/')
   shutil.copy2('assets/css/bootstrap.min.css', 'generated/css/')
   shutil.copy2('assets/js/bootstrap.min.js', 'generated/js/')
   shutil.copy2('assets/js/jquery-3.1.1.min.js', 'generated/js/')
   shutil.copytree('assets/font-awesome/fonts', 'generated/fonts/')

   
file_path = 'demo/dutchroyalfamily.ged' 
# file_path = 'demo/englishtudorhouse2.ged' 
# file_path = 'demo/americanpresidents.ged' 
# file_path = 'demo/kees.ged' 
gedcom = Gedcom(file_path)
copy_assets()
n = 0
for e in gedcom.get_element_list():
   if e.is_individual():
      n = n + 1
for e in gedcom.get_element_list():
   if e.is_individual():
      p = Person(e,gedcom)
      p.get_parents()
      p.get_families()
      p.get_siblings()
      h = Html(p, file_path)
      h.write_header()
      h.write_section_person()
      # h.write_section_statistics(n)
      h.write_footer(n)
      # stop
      
