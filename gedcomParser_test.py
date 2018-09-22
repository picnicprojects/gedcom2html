from gedcomParser import GedcomParser
import unittest, datetime

class TestStringMethods(unittest.TestCase):
   def test_dutch(self):
      g = GedcomParser('demo/dutchroyalfamily.ged')
      self.p = g.get_persons()
      id_list = self.p.keys()
      id_list.sort()
      self.assertEqual(id_list[0], u'I1')
      self.assertEqual(len(id_list), 167)
      self.assertEqual(self.p[id_list[0]].first_name, u'Annemarie Cecilia')
      self.assertEqual(self.p[id_list[0]].surname, u'van Weezel')
      self.assertEqual(self.p[id_list[0]].nick_name, '')
      self.assertEqual(self.p[id_list[0]].birth_date, datetime.date(1977, 12, 18))
      self.assertEqual(self.p[id_list[0]].death_date, False)
      self.assertEqual(self.p[id_list[0]].family[0].spouse_id, u'I2698')
      self.assertEqual(len(self.p[id_list[0]].family), 1)
      self.assertEqual(len(self.p[id_list[0]].family[0].child_id), 3)
      self.assertEqual(self.p[id_list[0]].family[0].child_id[0], u'I2')
      self.assertEqual(self.p[id_list[0]].family[0].child_id[1], u'I3')
      self.assertEqual(self.p[id_list[0]].family[0].child_id[2], u'I4')

   def test_usa(self):
      g = GedcomParser('demo/americanpresidents.ged')
      self.p = g.get_persons()
      id_list = self.p.keys()
      id_list.sort()
      self.assertEqual(id_list[0], u'I1')
      self.assertEqual(len(id_list), 2145)
      print self.p[id_list[0]]
      self.assertEqual(self.p[id_list[0]].first_name, u'William Jefferson')
      self.assertEqual(self.p[id_list[0]].surname, u'CLINTON')
      self.assertEqual(self.p[id_list[0]].nick_name, '')
      self.assertEqual(self.p[id_list[0]].birth_date, datetime.date(1946, 8, 19))
      self.assertEqual(self.p[id_list[0]].death_date, False)
      self.assertEqual(self.p[id_list[0]].family[0].spouse_id, u'I2')
      self.assertEqual(len(self.p[id_list[0]].family), 1)
      self.assertEqual(len(self.p[id_list[0]].family[0].child_id), 1)
      self.assertEqual(self.p[id_list[0]].family[0].child_id[0], u'I66')

if __name__ == '__main__':
   unittest.main()
