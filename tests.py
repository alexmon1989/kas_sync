import unittest
import configparser
import pyodbc
import requests


class TestConnections(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read('settings.testing.ini')
        # Web-адрес API
        self.API_URL = config['API']['URL']
        # Строка подключения к БД КАС
        self.KAS_CONNECTION_STRING = config['DB']['KAS_CONNECTION_STRING']
        # Строка подключения к БД ГЛОК
        self.GLOC_CONNECTION_STRING = config['DB']['GLOC_CONNECTION_STRING']

    def test_gloc_connection(self):
        """Тест подключения к БД GLOC (SQL Server)"""
        cnxn = pyodbc.connect(self.GLOC_CONNECTION_STRING)
        cursor = cnxn.cursor()
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
        self.assertEqual(row[0], 1)
        cnxn.close()

    def test_kas_connection(self):
        """Тест подключения к БД КАС (MySQL)"""
        cnxn = pyodbc.connect(self.KAS_CONNECTION_STRING)
        cursor = cnxn.cursor()
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
        self.assertEqual(row[0], 1)
        cnxn.close()

    def test_api_connection(self):
        """Тест подключения к API."""
        r = requests.get(f"{self.API_URL}/claims/raw-claim-ids")
        self.assertIsInstance(r.json(), list)


if __name__ == '__main__':
    unittest.main()
