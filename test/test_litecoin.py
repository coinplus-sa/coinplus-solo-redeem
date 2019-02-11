import unittest
from coinplus_solo_redeem.common import wif_export_bitcoin, compute_public_key_sec256k1, address_from_publickey_litecoin

class TestLitecoin(unittest.TestCase):
    """test of the bitcoin conversion from private key to wif"""
    def setUp(self):
        self.test_add_vector = [("03cb3e5f30245658e1e3615f1620e5b40f7d9016c0edb3611dd786327dd5e40caa", "LUXvZur8PLAeGnb6WC4qEMi9Uzdzpsg5KC"),
                                ("03c2773e19b0cd4175832d781d521390e5aac7b0841904f93211bf114786f5a145", "LMWFXBqBTEn8DEM698T3YDt6JWq4eKnosA"),
                                ("0277c3757e791426b7fa43cf64197bfd5c2fe277ece721b12558a52729f6b68b8a", "LPhARZrEKtBJ4WdSjYRgyVJRa1GEytTmKM"),
                                ("02d93dfcd93a76d7bac5b0fa394ad4bfd6cd92d10a64728b4b5f707d87db9cd2aa", "LcjeTEP32t4WxFXbmraFqdGfeRQn7u6kVP"),
                                ("037049004c5ad576beb518dcc74506df3faf520109a489886b7d1435a63b9b0b88", "LSSkBhFmVTyHFt4vF7PB9qsxy9FyVthFRT"),
                                ("0260bbacc03555af21f062ff04e9fbde36bcf0ae7396812d336e7f2e5292306f2b", "LZLyLvvpyeMmhTPQ3DjMCqApbyhfX6Tuvc"),
                                ("0343710601de0710dd81a0b7102bf1b794809a330caf4e1b4ae6567923c00df6a5", "Lf5EcKGuLEpnVSYAeERBRgv4m4zKoxBkSA"),
                                ("028c48ff458287f34cc1ad5c58a441500f8f315e9cabe34ff1601a5a0f791e4d0a", "LaeCZZJmdnJFcyy82kguvWwTwHFZ3hjU9k"),
                                ("0258cdabe1dad468dda6a7d62bee9e0cddadfe87d664e62df9143e769c017dd651", "LY6kEZWcLGSQPrzNjW8SXQLLR5oJ9dNZPg"),
                                ("0289a6d2272382ceec291674530eebb1b05dadab88ebf1bc45569ba612a4e3973a", "LX3fqLjKze4qrq6WRsq1qtRtxmpS6HbXdC")]


    def test_address_testvector(self):
        for publickey_hex, address_expected in self.test_add_vector:
            publickey = bytearray.fromhex(publickey_hex)
            address = address_from_publickey_litecoin(publickey)
            self.assertEqual(address, address_expected)
