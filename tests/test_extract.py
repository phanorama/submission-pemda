import unittest
from bs4 import BeautifulSoup
from datetime import datetime
from utils.extract import data_products  # Ganti sesuai path file asli
import re

class TestDataProducts(unittest.TestCase):

    def setUp(self):
        self.html = '''
        <div class="product">
            <h3 class="product-title">Cool T-shirt</h3>
            <span class="price">$19.99</span>
            <p>Rating: 4.5 out of 5</p>
            <p>5 Colors</p>
            <p>Size: L</p>
            <p>Gender: Men</p>
        </div>
        '''
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.item = self.soup.find('div', class_='product')

    def test_data_products_output(self):
        result = data_products(self.item)

        self.assertEqual(result['Title'], 'Cool T-shirt')
        self.assertEqual(result['Price'], '$19.99')
        self.assertEqual(result['Rating'], 4.5)
        self.assertEqual(result['Colors'], '5')
        self.assertEqual(result['Size'], 'L')
        self.assertEqual(result['Gender'], 'Men')

        # Pastikan timestamp formatnya valid ISO dan tipe string
        self.assertTrue(isinstance(result['Timestamp'], str))
        self.assertRegex(result['Timestamp'], r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')

if __name__ == '__main__':
    unittest.main()
