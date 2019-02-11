import unittest
from coinplus_solo_redeem.pro import secret2_reconstruct_base58, secret1_reconstruct_base58

class TestPro(unittest.TestCase):
    """test of the bitcoin conversion from private key to wif"""
    def setUp(self):
        self.test_vector = [((1, "977TZTQjLNUP1zUn9A5CoPtZ4mAU", "RJTu5AYkaycyxF"),
                             (2, "GbmQxU1SMqnzpYRHC2XBgUfQs8cA", "okSoTKKXdQRDnd"),
                             (3, "Q6RNMUc9PK7cd6MnEtyAZZSGfW3r", "CCRhqU6JfqDTbQ"), 
                             ("1cTWASp2Ju9mDSYH6HdDvK7hGPin", "2rUzh1myYYpk7s")),
                            ((1, "2sMCBaiUXqyHyo7zo9j59NG6KrvH", "E9uNmTGdBedb2q"),
                             (2, "skRUjse6PEHUuQzAoqnFUsbPrf9K", "hPkNwoG73UNWxT"),
                             (3 , "idVmJAZiEcbfq2rLpXqRpNvhPTHx", "AdbP89FauJ7SrU"), 
                             ("BzGudHnrgTf74BFpnTftorvno4me", "kv4Nb7H9Kptf8p")),
                            ((1, "eQLpcVquFKBpozZC8SfHufUzCQk8", "Avz9zxaeU12yZS"),
                             (2, "67W7g7hTXQe4Az8c4ZUZzRjWDkeA", "fa8bPDLqm4ZDcc"),
                             (3, "XpfQjjZ1oW6HXyi1zgHr5Bz2F6cb", "ADH2mU73485TeB"),
                             ("ChBXYszLyDjbSzynCKr1puEUB4mh", "gHqichpTAwWjXs")),
                            ]

    def test_pro_vector_valid(self):
        for card1, card2, card3, resutl_expected in self.test_vector:

            s_1_12 = secret1_reconstruct_base58([(card1[0], card1[1]), (card2[0], card2[1])])
            s_1_23 = secret1_reconstruct_base58([(card2[0], card2[1]), (card3[0], card3[1])])
            s_1_13 = secret1_reconstruct_base58([(card1[0], card1[1]), (card3[0], card3[1])])

            s_2_12 = secret2_reconstruct_base58([(card1[0], card1[2]), (card2[0], card2[2])])
            s_2_23 = secret2_reconstruct_base58([(card2[0], card2[2]), (card3[0], card3[2])])
            s_2_13 = secret2_reconstruct_base58([(card1[0], card1[2]), (card3[0], card3[2])])

            self.assertEqual(s_1_12, resutl_expected[0])
            self.assertEqual(s_1_23, resutl_expected[0])
            self.assertEqual(s_1_13, resutl_expected[0])

            self.assertEqual(s_2_12, resutl_expected[1])
            self.assertEqual(s_2_23, resutl_expected[1])
            self.assertEqual(s_2_13, resutl_expected[1])
