import unittest
from coinplus_solo_redeem.common import compute_public_key_sec256k1

class TestECC(unittest.TestCase):
    """test of the ecc"""
    def setUp(self):
        self.test_vector = [("28cb1bccdc33f93c94b73360cef14f0bb0c60774c4819dde1df8e268982851e5", "03cb3e5f30245658e1e3615f1620e5b40f7d9016c0edb3611dd786327dd5e40caa"),
                            ("222d6d37a7bff05733340c9636fed4c14f053a78c2dd7c12a270b9efe2ceb668", "03c2773e19b0cd4175832d781d521390e5aac7b0841904f93211bf114786f5a145"),
                            ("7db31eb00f5136087b914f5725de8f4117be56387aaf5ff5455ee5a5d6c02088", "0277c3757e791426b7fa43cf64197bfd5c2fe277ece721b12558a52729f6b68b8a"),
                            ("a1d01da3cacb1766a78692ccba8fff6a1bca9de088581c284a8ce3aa4711f666", "02d93dfcd93a76d7bac5b0fa394ad4bfd6cd92d10a64728b4b5f707d87db9cd2aa"),
                            ("4f234357b42745698ff9121ed828228005fcc776d18ddd790c525375815a9a77", "037049004c5ad576beb518dcc74506df3faf520109a489886b7d1435a63b9b0b88"),
                            ("ecc33ce35dccef1ec35c8faec5b60024cc506feae3f1a626d4d9f6ada196dce8", "0260bbacc03555af21f062ff04e9fbde36bcf0ae7396812d336e7f2e5292306f2b"),
                            ("63f9f5c10e933165ec6af5213abe8ff9e28010b3ada3718db3171fb8cc08a4a0", "0343710601de0710dd81a0b7102bf1b794809a330caf4e1b4ae6567923c00df6a5"),
                            ("05dd119ad6b50855abd178d843f93ea39d84c6ed13fa0e7d376d57efdddddde0", "028c48ff458287f34cc1ad5c58a441500f8f315e9cabe34ff1601a5a0f791e4d0a"),
                            ("c9e19496da7f4e6bed5f4c3e7ae79708bfe53baecbf87b1f4a87999343e9ab47", "0258cdabe1dad468dda6a7d62bee9e0cddadfe87d664e62df9143e769c017dd651"),
                            ("14c1e83152c2d4c810d67a66e36c45f596a63ff1324b5d7044f2ce12d74318c3", "0289a6d2272382ceec291674530eebb1b05dadab88ebf1bc45569ba612a4e3973a")]

    def test_address_testvector(self):
        """check the test vector"""
        for privatekey_hex, publickey_hex in self.test_vector:
            privatekey = bytearray.fromhex(privatekey_hex)
            publickey = compute_public_key_sec256k1(privatekey)
            publickey_expected = bytes(bytearray.fromhex(publickey_hex))
            self.assertEqual(publickey, publickey_expected)