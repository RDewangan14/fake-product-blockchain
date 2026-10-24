import unittest
from app import app, blockchain

class BlockchainAntiCounterfeitTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"TrustChain", response.data)

    def test_verify_genuine_product(self):
        # We know PROD-AAPL-98210 was seeded
        response = self.client.get('/verify/PROD-AAPL-98210')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"100% Genuine Verified", response.data)

    def test_verify_counterfeit_product(self):
        response = self.client.get('/verify/FAKE-GUCCI-9999')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product Not Found on Blockchain", response.data)

    def test_manufacturer_page(self):
        response = self.client.get('/manufacturer')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product Genesis", response.data)

    def test_supply_chain_page(self):
        response = self.client.get('/supply-chain')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Supply Chain Checkpoint Logger", response.data)

    def test_explorer_page(self):
        response = self.client.get('/explorer')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Blockchain Explorer", response.data)

    def test_about_page(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"SSIPMT", response.data)
        self.assertIn(b"Rahul Dewangan", response.data)
        self.assertIn(b"Chirag Gajbhiye", response.data)

    def test_api_verify(self):
        response = self.client.get('/api/verify?product_id=PROD-AAPL-98210')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['result']['status'], 'GENUINE')

if __name__ == '__main__':
    unittest.main()
