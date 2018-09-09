from gedcom import Gedcom
from datetime import datetime
import codecs, json, os, shutil

class Person:
   def __init__(self,e,g):
      self.__e = e
      self.__g = g
      self.id = e.get_pointer().replace("@","")
      self.first_name = e.get_name()[0]
      self.surname = e.get_name()[1]
      self.family = []
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
      
   # def __get_families(self, current_element, current_person):
      # fl = self.__g.get_families(self.__e)
      # if len(fl) > 0:
         # self.family = []
         # for f in fl:
            # fam = Family()
            # h = self.__g.get_family_members(f, 'HUSB')
            # if len(h) > 0:
               # if (self.__e <> h[0]):
                  # fam.spouse = Person(h[0], self.__g)
            # w = self.__g.get_family_members(f, 'WIFE')
            # if len(w) > 0:
               # if (self.__e <> w[0]):
                  # fam.spouse = Person(w[0], self.__g)
            # c = self.__g.get_family_members(f, 'CHIL')
            # if len(c) > 0:
               # fam.children = []
               # for p in c:
                  # fam.children.append(Person(p, self.__g))
            # self.family.append(fam)
            
   def __get_families(self, current_element, current_person):
      fl = self.__g.get_families(current_element)
      if len(fl) > 0:
         for f in fl:
            fam = Family()
            fam.id = f.get_pointer().replace("@","")
            h = self.__g.get_family_members(f, 'HUSB')
            if len(h) > 0:
               if (current_element <> h[0]):
                  fam.spouse = Person(h[0], self.__g)
            w = self.__g.get_family_members(f, 'WIFE')
            if len(w) > 0:
               if (current_element <> w[0]):
                  fam.spouse = Person(w[0], self.__g)
            c = self.__g.get_family_members(f, 'CHIL')
            if len(c) > 0:
               fam.children = []
               for p in c:
                  child = Person(p, self.__g)
                  fam.children.append(child)
                  child = self.__get_families(p, child)
            current_person.family.append(fam)
            
   def get_families(self):
      self.__get_families(self.__e, self)
      
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
      self.link = self.link.replace('@','')

class Family:
   def __init__(self):
      self.spouse = ""
      self.children = []

class Html:
   def __init__(self, p):
      self.person = p
      self.__fname = self.__create_filename()
      fid = codecs.open(self.__fname, encoding='utf-8',mode='w')
      fid.close()

   def __create_filename(self):
      str = 'generated/' + self.person.link
      return str
      
   def __create_person_single_line_short(self, p):
      s = "%s %s %s " % (p.gender, p.first_name, p.surname)
      return(s)
      
   def __create_person_single_line_dates(self, p):
      s = ""
      if hasattr(p,'birth_date'):
         s = s + "<i class='fa fa-star'></i> %s " % p.birth_date
      if hasattr(p,'death_date'):
         s = s + "<i class='fa fa-plus'></i> %s " % p.death_date
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
      s = self.__create_person_single_line_short(p) + self.__create_person_single_line_dates(p)
      return(s)

      
   def write_header(self):
      fid = codecs.open(self.__fname, encoding='utf-8',mode='a')
      fid.write("<!DOCTYPE html>\n")
      fid.write("<html lang='en'>\n")
      fid.write("<head>\n")
      fid.write("<title>%s</title>\n" % self.person.first_name)
      fid.write("<meta name=\"description\" content=\"gedcom2html\" /><meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
      fid.write("<meta http-equiv='Content-Type' content='text/html;charset=utf-8' />\n")
      fid.write("<link rel='stylesheet' type='text/css' href='css/gedcom2html.css' media='screen, projection, print' />\n")
      fid.write("<link rel='stylesheet' type='text/css' href='css/font-awesome.min.css' />\n")
      fid.write("<link rel='stylesheet' type='text/css' href='css/bootstrap.min.css' />\n")
      fid.write("<script type='text/javascript' src='js/jquery-3.1.1.min.js'></script>\n")
      fid.write("<script type='text/javascript' src='js/bootstrap.min.js'></script>\n")
      fid.write("<script type='text/javascript' src='js/gedcom2html.js'></script>\n")
      # fid.write("<script type='text/javascript' src='../js/d3.min.js'></script>\n")
      # fid.write("<script type='text/javascript' src='../js/d3plus.min.js'></script>\n")
      # fid.write("<script type='text/javascript' src='../js/d3tree.js'></script>\n")
      fid.write("</head>\n")
      fid.write("<body>\n")
      fid.write("<div class='container'>\n")
      fid.write("<div class='row'>\n")
      fid.close()
      
   def __write_parents(self, person, fid, level):
      s  = '   '*level
      if level == 0:
         fid.write("%s<ul class='tree'>\n" % (s))
      else:
         fid.write("%s<ul class='tree' id='ul_parent_%s'>\n" % (s,person.id))
      for f in person.parents:
         if hasattr(f, 'parents'):
            arrow = "<i class='fa fa-arrow-circle-right' id='parent_%s' onclick='toggle_tree(\"parent_%s\")'></i>" % (f.id, f.id)
         else:
            arrow = ""
         fid.write("%s   <li>%s" % (s, arrow))
         fid.write(" <a href='%s'>%s</a>\n" % (f.link, self.__create_person_single_line_long(f)))
         if hasattr(f, 'parents'):
            self.__write_parents(f, fid, level + 1)
      fid.write("%s</ul>\n" % s)
      
   def __write_family(self, current_person, fid, level):
      s = '   '*level
      n = len(current_person.family)
      for index, family in enumerate(current_person.family):
         if level == 0:
            if hasattr(family,'spouse'):
               if index == 0:
                  fid.write("<ul class='tree'>\n")
               fid.write("<li><a href='%s'><i class='fa fa-heart'></i> %s</a>\n" %  (family.spouse.link, self.__create_person_single_line_long(family.spouse)))
         if hasattr(family,'children'):
            if level == 0:
               fid.write("%s<ul class='tree'>\n" % (s))
            else:
               fid.write("%s<ul class='tree' id='ul_children_%s'>\n" % (s, current_person.id))
            for p in family.children:
               if hasattr(p, 'family'):
                  arrow = "<i class='fa fa-arrow-circle-right' id='child_%s' onclick='toggle_tree(\"children_%s\")'></i>" % (p.id, p.id)
               else:
                  arrow = ""
               fid.write("%s   <li>%s" % (s, arrow))
               fid.write(" <a href='%s'>%s</a>\n" % (p.link, self.__create_person_single_line_long(p)))
               if hasattr(p, 'family'):
                  self.__write_family(p, fid, level + 1)
            fid.write("%s</ul>\n" % s)
         if level == 0:
            if hasattr(family,'spouse'):
               if index == (n-1):
                  fid.write("</ul>\n")
                  
      
   def write_section_person(self):
      fid = codecs.open(self.__fname, encoding='utf-8',mode='a')
      fid.write("<h1>%s</h1>\n" %  self.__create_person_single_line_short(self.person))
      fid.write("%s\n" %  self.__create_person_single_line_dates(self.person))
      fid.write("</div>\n")
      fid.write("<div class='row'>\n")
      # fid.write("<div class='col-sm-12'>\n")
      if hasattr(self.person, 'parents'):
         fid.write("<h2>Parents</h2>\n")
         self.__write_parents(self.person, fid, 0)
      fid.write("<h2>Families</h2>\n")
      self.__write_family(self.person, fid, 0)
            # fid.write("<ul>\n")
            # for p in f.children:
               # fid.write("<li><a href='%s'>%s</a>\n" % (p.link, self.__create_person_single_line_long(p)))
            # fid.write("</ul>\n")
      fid.write("<h2>Siblings</h2>\n")
      # fid.write("</div><!-- col -->\n")
      # fid.write("<script>drawTree();</script>\n")

   def write_hourglass_tree(self, j):
      fid = codecs.open(self.__fname, encoding='utf-8',mode='a')
      fid.write("<div class='col-sm-6'>\n")
      fid.write("<h2>Tree</h2>\n")
      fid.write("<div class='tree'></div>\n")
      fid.write("<script>\n")
      fid.write("var json = " +j)
      fid.write("drawTree(json);\n")
      fid.write("</script>\n")
      fid.write("</div>\n")
      
   
   def write_footer(self):
      fid = codecs.open(self.__fname, encoding='utf-8',mode='a')
      fid.write("</div><!-- row -->\n")
      fid.write("</div><!-- container -->\n")
      fid.write("<footer>\n")
      fid.write("<center>gedcom2html</center>\n")
      fid.write("</footer>\n")
      # fid.write("<script>updateParents();updateChildren();</script>\n")
      fid.write("</body>\n")
      fid.write("</html>\n")
      fid.close()

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
      # fid.write("<link rel='stylesheet' type='text/css' href='css/gedcom2html.css' media='screen, projection, print' />\n")
      # fid.write("<link rel='stylesheet' type='text/css' href='css/font-awesome.min.css' />\n")
      # fid.write("<link rel='stylesheet' type='text/css' href='css/bootstrap.min.css' />\n")
      # fid.write("<script type='text/javascript' src='../js/jquery-3.1.1.min.js'></script>\n")
      # fid.write("<script type='text/javascript' src='../js/bootstrap.min.js'></script>\n")
      # fid.write("<script type='text/javascript' src='../js/gedcom2html.js'></script>\n")

   
file_path = 'demo/koninklijkhuis.ged' 
file_path = 'demo/kees.ged' 
gedcom = Gedcom(file_path)
copy_assets()
for e in gedcom.get_element_list():
   if e.is_individual():
      p = Person(e,gedcom)
      p.get_parents()
      p.get_families()
      h = Html(p)
      h.write_header()
      h.write_section_person()
      # h.write_hourglass_tree(p.json())
      h.write_footer()
      # stop
      
      # name = person.get_name()
      # gender = person.get_gender()
      # birth = person.get_birth_data()
      # death = person.get_death_data()
      # m = g.get_parents(e)
      # print m[0].get_name()
      # print m[1].get_name()
      # m = g.get_families(e)
      # print name
      # for j in m:
         # k = g.get_family_members(j,'PARENTS')
         # for l in k:
            # print "P   " + l.get_name()[0]
         # k = g.get_family_members(j,'CHIL')
         # for l in k:
            # print "C   " + l.get_name()[0]
      # stostop
      # if person.is_family():
      # print e.get_family_members()
         
