from gedcomParser import GedcomParser
from datetime import datetime
import codecs, os, shutil, string, sys, getopt

class Html:
   def __init__(self, all_persons, p, sources, file_path):
      self.person = p
      self.all_persons = all_persons
      self.__filepath = file_path
      self.__fid = codecs.open('generated/' + p.link, encoding='utf-8',mode='w')
      self.write_header()
      self.__fid.write("<div class='row'>\n")
      self.write_person()
      self.__fid.write("</div><!-- row -->\n")
      self.__fid.write("<div class='row'>\n")
      self.__fid.write("<div class='col-sm-8'>\n")
      self.write_parents()
      self.write_families()
      self.write_siblings()
      self.__fid.write("</div><!-- col -->\n")
      self.__fid.write("<div class='col-sm-4' id='column-right'>\n")
      self.write_fan_chart()
      self.__fid.write("</div><!-- col -->\n")
      self.__fid.write("</div><!-- row -->\n")
      self.write_footer(sources)
 
   def __del__(self):
      self.__fid.close()

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
      self.__fid.write("<script type='text/javascript' src='js/d3.min.js'></script>\n")
      self.__fid.write("<script type='text/javascript' src='js/bootstrap.min.js'></script>\n")
      self.__fid.write("<script type='text/javascript' src='js/gedcom2html.js'></script>\n")
      self.__fid.write("<script type='text/javascript' src='js/fanchart.js'></script>\n")
      # self.__fid.write("<script type='text/javascript' src='../js/d3.min.js'></script>\n")
      # self.__fid.write("<script type='text/javascript' src='../js/d3plus.min.js'></script>\n")
      # self.__fid.write("<script type='text/javascript' src='../js/d3tree.js'></script>\n")
      self.__fid.write("</head>\n")
      self.__fid.write("<body>\n")
      self.__fid.write("<div class='container'>\n")
      
   def __write_parents(self, id, level):
      s  = '   '*level
      if level == 1:
         self.__fid.write("%s<ul class='tree' id='ul_parent_%s'>\n" % (s, id))
      else:
         self.__fid.write("%s<ul class='tree'>\n" % (s))
      for parent_id in self.all_persons[id].parent_id:
         arrow = ""
         p = self.all_persons[parent_id]
         if level == 0 and len(self.all_persons[p.id].parent_id) > 0:
            arrow = "<i class='fa fa-arrow-circle-right' id='parent_%s' onclick='toggle_tree(\"parent_%s\")'></i>" % (p.id, p.id)
         self.__fid.write("%s   <li>%s" % (s, arrow))
         self.__fid.write(" %s\n" % (p.string_long))
         if len(self.all_persons[p.id].parent_id) > 0:
            self.__write_parents(p.id, level + 1)
      self.__fid.write("%s</ul>\n" % s)
      
   def __write_family(self, id, level):
      white_space = '   '*(level+1)
      for index, family in enumerate(self.all_persons[id].family):
         # SPOUSE
         show_spouse = 0
         if len(family.spouse_id) > 0 and level == 0:
            show_spouse = 1
         if show_spouse:
            if index == 0:
               self.__fid.write("<ul class='tree'>\n")
            if len(family.spouse_id) > 0:
               self.__fid.write("   <li><i class='fa fa-heart' style='color:#faa'></i> %s\n" %  (self.all_persons[family.spouse_id].string_long))
         # CHILDREN
         if len(family.child_id) > 0:
            if level == 1:
               self.__fid.write("%s<ul class='tree' id='ul_children_%s'>\n" % (white_space, id))
            else:
               self.__fid.write("%s<ul class='tree'>\n" % (white_space))
            for child_id in family.child_id:
               arrow = ""
               if level == 0:
                  if len(self.all_persons[child_id].family) > 0:
                     arrow = "<i class='fa fa-arrow-circle-right' id='children_%s' onclick='toggle_tree(\"children_%s\")'></i>" % (child_id, child_id)
               self.__fid.write("%s   <li>%s" % (white_space, arrow))
               self.__fid.write(" %s\n" % (self.all_persons[child_id].string_long))
               if len(self.all_persons[child_id].family) > 0:
                  self.__write_family(child_id, level + 1)
            self.__fid.write("%s</ul>\n" % white_space)
         # SPOUSE
         if show_spouse and index == len(self.all_persons[id].family) - 1:
            self.__fid.write("</ul>\n")
                  
   def write_person(self):
      self.__fid.write("<div class='well'>\n")
      self.__fid.write("<h1>%s</h1>\n" %  self.person.string_short)
      self.__fid.write("<ul>\n")
      if len(self.person.string_dates)>0:
         self.__fid.write("<li>%s\n" %  self.person.string_dates)
      # if len(self.person.nick_name)>0:
      self.__fid.write("<li>First name(s): %s\n" %  self.person.first_name)
      if len(self.person.notes)>0:
         self.__fid.write("<li>%s\n" %  self.person.notes)
      self.__fid.write("<ul>\n")
      self.__fid.write("</div>\n")

   def write_parents(self):
      if len(self.person.parent_id) > 0:
         self.__fid.write("<h2>Parents</h2>\n")
         self.__write_parents(self.person.id, 0)

   def write_families(self):
      if len(self.all_persons[self.person.id].family) > 0:
         self.__fid.write("<h2>Families and children</h2>\n")
         self.__write_family(self.person.id, 0)

   def write_siblings(self):
      list_of_child_ids = []
      for parent_id in self.person.parent_id:
         for family in self.all_persons[parent_id].family:
            for child_id in family.child_id:
               if child_id not in list_of_child_ids:
                  if child_id <> self.person.id:
                     list_of_child_ids.append(str(child_id))
      if len(list_of_child_ids) > 0:
         self.__fid.write("<h2>Siblings</h2>\n")
         self.__fid.write("<ul>\n")
         for child_id in list_of_child_ids:
            self.__fid.write("<li>%s\n" % (self.all_persons[child_id].string_long))
         self.__fid.write("</ul>\n")

   def __write_json_for_fan_chart(self, id, level):
      # if level < 5:
         p = self.all_persons[id]
         white_space = '   '*level
         white_space2 = '   '*(level-1)
         
         self.__fid.write('%s{\n'% white_space2)
         self.__fid.write('%s"name": "%s",\n'% (white_space, p.shortest_name))
         self.__fid.write('%s"generation": "%d",\n'% (white_space, level))
         self.__fid.write('%s"gender": "%s",\n'% (white_space, p.gender))
         self.__fid.write('%s"href": "%s",\n'% (white_space, p.link))
         if p.birth_date == False:
            self.__fid.write('%s"born": "",\n' % (white_space))
         else:
            self.__fid.write('%s"born": "%s",\n'% (white_space, '{0.year:4d}'.format(p.birth_date)))
         self.__fid.write('%s"died": "%s",\n'% (white_space, ""))
         self.__fid.write('%s"gramps_id": "%s",\n'% (white_space, id))
         if len(p.parent_id) > 0:
            self.__fid.write('%s"children": [\n'% white_space)
            for pid in p.parent_id:
               self.__write_json_for_fan_chart(pid, level + 1)
            self.__fid.write("%s]\n"% white_space)
         self.__fid.write("%s},\n"% white_space2)
         
   def write_fan_chart(self):
      self.__fid.write("<div id='fanchart'></div>\n")
      self.__fid.write("<script>\n")
      self.__fid.write("var json = [")
      self.__write_json_for_fan_chart(self.person.id, 1)
      self.__fid.write("];\n")
      self.__fid.write("drawFanChart(json);\n")
      self.__fid.write("</script>\n")
         
   def write_hourglass_tree(self, j):
      self.__fid.write("<h2>Tree</h2>\n")
      self.__fid.write("<div class='tree'></div>\n")
      self.__fid.write("<script>\n")
      self.__fid.write("var json = " +j)
      self.__fid.write("drawTree(json);\n")
      self.__fid.write("</script>\n")
   
   def write_footer(self, sources):
      # self.__fid.write("<footer class='gedcominfo'>\n")
      self.__fid.write("<div class='row well well-sm gedcominfo'>\n")
      # self.__fid.write("<div class='well'>\n")
      self.__fid.write("<div class='col-sm-6'>\n")
      path, fname = os.path.split(self.__filepath)
      self.__fid.write("Gedcom file <a href='%s'>%s</a> contains %d persons\n" % (fname, fname , len(self.all_persons)))
      if len(sources) > 0:
         self.__fid.write("<b>Sources:</b>\n")
         self.__fid.write("<ul>\n")
         for index, s in sources.iteritems():
            self.__fid.write("   <li><a href='%s'>%s</a>\n" %(s.publication, s.title))
         self.__fid.write("</ul>\n")
      # self.__fid.write("</div><!-- well -->\n")
      self.__fid.write("</div><!-- col -->\n")
      self.__fid.write("<div class='col-sm-6'>\n")
      self.__fid.write("<center>\n")
      self.__fid.write("</center>\n")
      # self.__fid.write("</div><!-- well -->\n")
      self.__fid.write("</div><!-- col -->\n")
      self.__fid.write("</div><!-- row -->\n")
      # self.__fid.write("</footer>\n")
      self.__fid.write("<footer>\n")
      self.__fid.write("Made with <a href='https://github.com/picnicprojects/gedcom2html'>gedcom2html</a> by <a href='https://www.picnicprojects.com'>Picnic Projects</a>\n")
      self.__fid.write("</footer>\n")
      self.__fid.write("</div><!-- container -->\n")
      self.__fid.write("</body>\n")
      self.__fid.write("</html>\n")
      self.__fid.close()

def copy_assets(gedcom_file):
   try:
      shutil.rmtree('generated')
   except:
      pass
   path, fname = os.path.split(gedcom_file)
   os.makedirs('generated/js')
   os.makedirs('generated/css')
   shutil.copy2(gedcom_file, 'generated/'+fname)   
   shutil.copy2('gedcom2html.css','generated/css/')   
   shutil.copy2('gedcom2html.js', 'generated/js/')
   shutil.copy2('fanchart.js', 'generated/js/')
   shutil.copy2('assets/css/font-awesome.min.css', 'generated/css/')
   shutil.copy2('assets/css/bootstrap.min.css', 'generated/css/')
   shutil.copy2('assets/js/d3.min.js', 'generated/js/')
   shutil.copy2('assets/js/bootstrap.min.js', 'generated/js/')
   shutil.copy2('assets/js/jquery-3.1.1.min.js', 'generated/js/')
   shutil.copytree('assets/font-awesome/fonts', 'generated/fonts/')

def create_strings(p):
   #link
   s = "%s_%s_%s.html" % (p.id, p.first_name, p.surname) 
   s = s.replace(' ','_')
   valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
   p.link = ''.join(c for c in s if c in valid_chars)

   #shortest_name
   if len(p.nick_name) > 0:
      p.shortest_name = p.nick_name
   else:
      p.shortest_name = p.first_name.split(' ')[0]
      
   #short_name
   p.short_name = "%s %s " % (p.shortest_name, p.surname)
 
   #string_short
   if p.gender == 'M':
      s = "<i class='fa fa-mars'></i>"
   else:
      s = "<i class='fa fa-venus'></i>"
   p.string_short = "%s %s " % (s, p.short_name)
      
   #string_dates
   s = ""
   if p.birth_date <> False:
      s = s + "<i class='fa fa-star'></i> %s " % '{0.day:02d}-{0.month:02d}-{0.year:4d}'.format(p.birth_date)
   if p.death_date <> False:
      s = s + "<i class='fa fa-plus'></i> %s " % '{0.day:02d}-{0.month:02d}-{0.year:4d}'.format(p.death_date)
   if p.birth_date <> False and p.death_date <> False:
   # self.death_date.year - self.birth_date.year - ((today.month, today.day) < (born.month, born.day))
      age =  p.death_date.year - p.birth_date.year
      if age == 0:
         age =  p.death_date.month - p.birth_date.month
         s = s + "(%s months) " % age
      else:
         s = s + "(%s years) " % age
   p.string_dates = s
      
   #string_long
   if len(p.string_dates) > 0:
      p.string_long = ("<a href='%s'>%s</a> <span class='dates'>%s</span>" % (p.link, p.string_short, p.string_dates))
   else:
      p.string_long = ("<a href='%s'>%s</a>" % (p.link, p.string_short))

def write_index_html(link):
   fid = open('generated/index.html','w')
   fid.write('<meta http-equiv="refresh" content="0; url=%s">' % link)
   fid.close
   
def gedcom2html(file_path):
   copy_assets(file_path)
   g = GedcomParser(file_path)
   all_persons = g.get_persons()
   sources = g.get_sources()
   id_list = all_persons.keys()
   id_list.sort()
   for id in id_list:
      create_strings(all_persons[id])
   write_index_html(all_persons[id_list[0]].link)
   for id in id_list:
      p = all_persons[id]
      h = Html(all_persons, p, sources, file_path)
      # stop
   
if __name__ == "__main__":
   outputdir = ''
   try:
      inputfile = sys.argv[1]
      argv = sys.argv[2:] 
      opts, args = getopt.getopt(argv,"ho:",["outputdir="])
   except getopt.GetoptError:
      print 'gedcom2html.py inputfile -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'gedcom2html.py inputfile -o <outputdir>'
         sys.exit()
      elif opt in ("-o", "--outputdir"):
         outputdir = arg
   print inputfile
   gedcom2html(inputfile)