import unittest
from name_function import get_formatted_name

class NamesTestCase(unittest.TestCase):
    '''测试name.function.py'''
    def test_first_last_name(self):
        '''能正确处理想janis joplin这样的姓名吗'''
        formatted_name = get_formatted_name('janis', 'joplin')
        self.assertEqual(formatted_name, 'Janis Joplin')


#unittest.main()