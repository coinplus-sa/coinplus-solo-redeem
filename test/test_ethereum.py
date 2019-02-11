import unittest
from coinplus_solo_redeem.common import wif_export_bitcoin, compute_public_key_sec256k1, address_from_publickey_ethereum

class TestEthereum(unittest.TestCase):
    """test of the bitcoin conversion from private key to wif"""
    def setUp(self):
        self.test_add_vector = [("03cb3e5f30245658e1e3615f1620e5b40f7d9016c0edb3611dd786327dd5e40caa", "0xfd965bB8907566c550D8C0325207a1cB744f2fc2"),
                                ("03c2773e19b0cd4175832d781d521390e5aac7b0841904f93211bf114786f5a145", "0xDB1F8a8B668F15B9e696dDfF30Ce233703f9eC97"),
                                ("0277c3757e791426b7fa43cf64197bfd5c2fe277ece721b12558a52729f6b68b8a", "0x6C4DCd1f900d89a7A70C9A5bA9F7a24a4Bd70878"),
                                ("02d93dfcd93a76d7bac5b0fa394ad4bfd6cd92d10a64728b4b5f707d87db9cd2aa", "0x42F7C7ccD753055c219B85ddc5F05512b3f94528"),
                                ("037049004c5ad576beb518dcc74506df3faf520109a489886b7d1435a63b9b0b88", "0x0af4DbEf58063AEd75e6fF57610348E55954E8FB"),
                                ("0260bbacc03555af21f062ff04e9fbde36bcf0ae7396812d336e7f2e5292306f2b", "0xd13AA41456549AAf4F00C681e014E8CEd8c04d60"),
                                ("0343710601de0710dd81a0b7102bf1b794809a330caf4e1b4ae6567923c00df6a5", "0x011934E5d9EE8C230BBFccF33Ab83c62E5486d91"),
                                ("028c48ff458287f34cc1ad5c58a441500f8f315e9cabe34ff1601a5a0f791e4d0a", "0x98447B7aC721BDeb197a7e72780f6f41BECA2919"),
                                ("0258cdabe1dad468dda6a7d62bee9e0cddadfe87d664e62df9143e769c017dd651", "0xaA5EacE5be0D09B09BAf66df62b0D85EA20b4ee4"),
                                ("0289a6d2272382ceec291674530eebb1b05dadab88ebf1bc45569ba612a4e3973a", "0x79B4044CeB2DFAa123FbE5B4da43BF7cFF01718c")]


    def test_address_testvector(self):
        for publickey_hex, address_expected in self.test_add_vector:
            publickey = bytearray.fromhex(publickey_hex)
            address = address_from_publickey_ethereum(publickey)
            self.assertEqual(address, address_expected)
