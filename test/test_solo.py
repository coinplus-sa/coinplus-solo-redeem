"""test of the common functions of COINPLUS SOLO REDEEM"""
import unittest
from coinplus_solo_redeem.common import compute_privatekey_sec256k1

class TestSOLO(unittest.TestCase):
    """test of the bitcoin conversion from private key to hex
    """
    def setUp(self):
        self.test_vector = [("qxknCqsD18GLvkV8FNrabuFicmbz", "G7DRagygVQzVmE", "28cb1bccdc33f93c94b73360cef14f0bb0c60774c4819dde1df8e268982851e5"),
                            ("BH8bGpAr15UCcmifwwaa5xpazquX", "y7Qk6H8Vj7s8YR", "222d6d37a7bff05733340c9636fed4c14f053a78c2dd7c12a270b9efe2ceb668"),
                            ("9K6PToqvqUJejbCnkFuBUn5BMkZX", "Vh5W2GDhAdWTPw", "7db31eb00f5136087b914f5725de8f4117be56387aaf5ff5455ee5a5d6c02088"),
                            ("rfYWVfczv8grJ6mB2NvaWjt22EB9", "RxaFe5tioF3z14", "a1d01da3cacb1766a78692ccba8fff6a1bca9de088581c284a8ce3aa4711f666"),
                            ("irkehV3KG6CX36MNU53dBAiFtbuv", "aMJjVmwY9wBp8U", "4f234357b42745698ff9121ed828228005fcc776d18ddd790c525375815a9a77"),
                            ("6ZYAWTddRS4wgfiH8eWFM3cVxK59", "V8i49C1GQU3vUM", "ecc33ce35dccef1ec35c8faec5b60024cc506feae3f1a626d4d9f6ada196dce8"),
                            ("hb39oriMrCygxZ39UZZmT7HXsGHs", "ZZMSUAReHf6roM", "63f9f5c10e933165ec6af5213abe8ff9e28010b3ada3718db3171fb8cc08a4a0"),
                            ("ZdkwUnux677LihM9z6PLqttsbDif", "n2qmqPTayrmqQ4", "05dd119ad6b50855abd178d843f93ea39d84c6ed13fa0e7d376d57efdddddde0"),
                            ("EHPFuURVTuDCSMBxfuR5KmLvrQ3A", "nsKmyejKsZoDkT", "c9e19496da7f4e6bed5f4c3e7ae79708bfe53baecbf87b1f4a87999343e9ab47"),
                            ("dRVTettPEdzauEuVS6bYU89Cn5U8", "fSc2XDgewxhf7r", "14c1e83152c2d4c810d67a66e36c45f596a63ff1324b5d7044f2ce12d74318c3")]

    def test_compute_testvector(self):
        for secret1, secret2, privatekey in self.test_vector:
            self.assertEqual(compute_privatekey_sec256k1(secret1, secret2), bytearray.fromhex(privatekey))
