import unittest
from coinplus_solo_redeem.common import wif_export_bitcoin, compute_public_key_sec256k1, address_from_publickey_ripple

class TestRipple(unittest.TestCase):
    """test of the bitcoin conversion from private key to wif"""
    def setUp(self):
        self.test_add_vector = [("03cb3e5f30245658e1e3615f1620e5b40f7d9016c0edb3611dd786327dd5e40caa", "rwJyJ6YJJCvbrytALhnXxLePG8G56jXtyg"),
                                ("03c2773e19b0cd4175832d781d521390e5aac7b0841904f93211bf114786f5a145", "rsHJEyXM42YhxRevxzTkGUFLaJT82ZAtqB"),
                                ("0277c3757e791426b7fa43cf64197bfd5c2fe277ece721b12558a52729f6b68b8a", "rn7DwMYQEDANo6AHZQSP67NCM8txq6RAyU"),
                                ("02d93dfcd93a76d7bac5b0fa394ad4bfd6cd92d10a64728b4b5f707d87db9cd2aa", "rJW6UpnUxDFT6SqSb52xZcUuSDsWrkB7e7"),
                                ("037049004c5ad576beb518dcc74506df3faf520109a489886b7d1435a63b9b0b88", "r3D8v7AAQojNrn4mhyP11FFUkvt6Qij6tr"),
                                ("0260bbacc03555af21f062ff04e9fbde36bcf0ae7396812d336e7f2e5292306f2b", "rE3pn5cztzf5Se6N1nksvFfhPmLP4MheYK"),
                                ("0343710601de0710dd81a0b7102bf1b794809a330caf4e1b4ae6567923c00df6a5", "rLiHMaynE22jNdir7aRt9CiJYidsj7JP2E"),
                                ("028c48ff458287f34cc1ad5c58a441500f8f315e9cabe34ff1601a5a0f791e4d0a", "rGREJLzAZ3hU4BGxic6ceV16jhtGA4xruL"),
                                ("0258cdabe1dad468dda6a7d62bee9e0cddadfe87d664e62df9143e769c017dd651", "rD18yMU8EcUM9hJDZ499EPG2U1Srxxj5hf"),
                                ("0289a6d2272382ceec291674530eebb1b05dadab88ebf1bc45569ba612a4e3973a", "rUF523RVuyF8cpQMEjq5Z143kZT9x7YxT1"),]


    def test_address_testvector(self):
        for publickey_hex, address_expected in self.test_add_vector:
            publickey = bytearray.fromhex(publickey_hex)
            address = address_from_publickey_ripple(publickey)
            self.assertEqual(address, address_expected)