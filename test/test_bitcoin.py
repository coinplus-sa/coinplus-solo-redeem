import unittest
from coinplus_solo_redeem.common import wif_export_bitcoin, compute_public_key_sec256k1, address_from_publickey_bitcoin

class TestBitcoin(unittest.TestCase):
    """test of the bitcoin conversion from private key to wif"""
    def setUp(self):
        self.test_vector = [("28cb1bccdc33f93c94b73360cef14f0bb0c60774c4819dde1df8e268982851e5", "Kxb1QrK7mFtGayzV2HvuvuoMgbPbCwmJdtPnK4kbcC3XBMXVQbV1"),
                            ("222d6d37a7bff05733340c9636fed4c14f053a78c2dd7c12a270b9efe2ceb668", "KxN9W22CsiquFpLkBLjzsh366BvQnKdEkumTv9jgB3FKHSwF2Zqy"),
                            ("7db31eb00f5136087b914f5725de8f4117be56387aaf5ff5455ee5a5d6c02088", "L1S485xivNwoN8t93rprLfWNA77Egj2G8JJWY8GLWXJmi973Aqsp"),
                            ("a1d01da3cacb1766a78692ccba8fff6a1bca9de088581c284a8ce3aa4711f666", "L2eFh6gDsQEStWY9PjvKNnGEyTwKirQ3mHKh6HXLeieNFpWwFrFa"),
                            ("4f234357b42745698ff9121ed828228005fcc776d18ddd790c525375815a9a77", "KysYXLo4xE37wZE6GPM3Fzfnv4WTmXVVnkAoy9QbfZebMqe5CQtE"),
                            ("ecc33ce35dccef1ec35c8faec5b60024cc506feae3f1a626d4d9f6ada196dce8", "L59wrNzSjE634RuYZVA2iTL2yUg6MwUJa8CbBvSM14693CtQFysg"),
                            ("63f9f5c10e933165ec6af5213abe8ff9e28010b3ada3718db3171fb8cc08a4a0", "Kza3y1piJGUFox6Wn8jN5xhepMVi8S5UHW73XN51zriDE3Dxx7yd"),
                            ("05dd119ad6b50855abd178d843f93ea39d84c6ed13fa0e7d376d57efdddddde0", "KwR7GSmo8XC7GuZrV3sHneKXHt3M2epoqaep1cb3jHTMxs5Rte8g"),
                            ("c9e19496da7f4e6bed5f4c3e7ae79708bfe53baecbf87b1f4a87999343e9ab47", "L3z9AGPQsc9GWPL16mDgb7rBGjN2geLcERAichQ4G6DPoXCvbBuB"),
                            ("14c1e83152c2d4c810d67a66e36c45f596a63ff1324b5d7044f2ce12d74318c3", "Kwv4UHDn9HChQWUJWvASGmU4zymjotoUC8pUcS3p5i6XB9jCkWS2")]
        self.test_add_vector = [("03cb3e5f30245658e1e3615f1620e5b40f7d9016c0edb3611dd786327dd5e40caa", "1AJyJhYJJfvb1ytwL45XxLePGnGihjXtyg"),
                                ("03c2773e19b0cd4175832d781d521390e5aac7b0841904f93211bf114786f5a145", "13HJFyXMNaY4xRevxzTkGCpL6JTnaZwtqB"),
                                ("0277c3757e791426b7fa43cf64197bfd5c2fe277ece721b12558a52729f6b68b8a", "15UDAMYQFDwEohwHZQSPhUEfMntxqhRwyC"),
                                ("02d93dfcd93a76d7bac5b0fa394ad4bfd6cd92d10a64728b4b5f707d87db9cd2aa", "1JWhC25CxDpThSqSbiaxZcCuSD3W1kBUeU"),
                                ("037049004c5ad576beb518dcc74506df3faf520109a489886b7d1435a63b9b0b88", "18DnvUwwQojE15Nm4yPssppCkvthQrjht1"),
                                ("0260bbacc03555af21f062ff04e9fbde36bcf0ae7396812d336e7f2e5292306f2b", "1F825icztz7iSehEs5k3vp74PmLPNM4eYK"),
                                ("0343710601de0710dd81a0b7102bf1b794809a330caf4e1b4ae6567923c00df6a5", "1LrHM6y5FaajEdr1U6Rt9frJYrd3jUJPaF"),
                                ("028c48ff458287f34cc1ad5c58a441500f8f315e9cabe34ff1601a5a0f791e4d0a", "1GRFJLzwZ84CNBGxrchceVshj4tGwNx1uL"),
                                ("0258cdabe1dad468dda6a7d62bee9e0cddadfe87d664e62df9143e769c017dd651", "1DsnyMCnFcCM94JDZN99FPGaCsS1xxji47"),
                                ("0289a6d2272382ceec291674530eebb1b05dadab88ebf1bc45569ba612a4e3973a", "1Cpia8RVuypnc2QMFjqiZsN8kZT9xUYxTs")]

    def test_compute_testvector(self):
        for privatekey_hex, privatekey_wif in self.test_vector:
            privatekey = bytearray.fromhex(privatekey_hex)
            self.assertEqual(wif_export_bitcoin(privatekey), privatekey_wif)


    def test_address_testvector(self):
        for publickey_hex, address_expected in self.test_add_vector:
            publickey = bytearray.fromhex(publickey_hex)
            address = address_from_publickey_bitcoin(publickey)
            self.assertEqual(address, address_expected)
