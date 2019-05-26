import unittest
from unittest.mock import patch
from Reception import Reception,Client
from MyError import *
from LocalDB import localdb
from searchByCondition import SearchRecognition
from Master import Master
        
class Test(unittest.TestCase):
    r = Reception(localdb(),Client("127.0.0.1",12346),
    SearchRecognition("Sound Blaster Play! 3: USB Audio (hw:1,0)"))

    @patch('builtins.input', return_value='abc@bcd.com')
    def test_email_validation(self,output):
        self.assertEqual(TestReception.r.email_validation(), 'abc@bcd.com')
    
    @patch('builtins.input', return_value='abc_dw')
    def test_name_validation(self,output):
        self.assertEqual(TestReception.r.name_validation(), 'abc_dw')
    
    @patch('builtins.input', return_value='Rock_123')
    def test_username_validation(self,output):
        self.assertEqual(TestReception.r.username_validation(), 'Rock_123')
    
    @patch('builtins.input', return_value='ac@bd.com')
    def test_email_validation(self,output):
        self.assertNotEqual(TestReception.r.email_validation(), 'abc@bcd.com')
    
    @patch('builtins.input', return_value='ab_dw')
    def test_name_validation(self,output):
        self.assertNotEqual(TestReception.r.name_validation(), 'abc_dw')
    
    @patch('builtins.input', return_value='Roc_123')
    def test_username_validation(self,output):
        self.assertNotEqual(TestReception.r.username_validation(), 'Rock_123')

    @patch('builtins.input', return_value='ac@bd.com')
    def test_email_validation(self,output):
        self.assertFalse(TestReception.r.email_validation() == 'abc@bcd.com')
    
    @patch('builtins.input', return_value='ab_dw')
    def test_name_validation(self,output):
        self.assertFalse(TestReception.r.name_validation() == 'abc_dw')
    
    @patch('builtins.input', return_value='Roc_123')
    def test_username_validation(self,output):
        self.assertFalse(TestReception.r.username_validation() == 'Rock_123')
    
    @patch('builtins.input', return_value='abc@bcd.com')
    def test_email_validation(self,output):
        self.assertTrue(TestReception.r.email_validation() == 'abc@bcd.com')
    
    @patch('builtins.input', return_value='abc_dw')
    def test_name_validation(self,output):
        self.assertTrue(TestReception.r.name_validation() == 'abc_dw')
    
    @patch('builtins.input', return_value='Rock_123')
    def test_username_validation(self,output):
        self.assertTrue(TestReception.r.username_validation() == 'Rock_123')
    

if __name__ == '__main__':
    unittest.main()