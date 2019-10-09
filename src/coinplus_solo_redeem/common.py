"""common functions for coinplus solo redeem program"""
import math
import hashlib
import ecdsa
import sha3

try:
    from hashlib import scrypt
    def scrypt_func(data):
        """Scrypt function simplification"""
        return scrypt(data.encode("ascii"), salt=b"", n=16384, r=8, p=8, dklen=32)

except ImportError:
    import pyscrypt as scrypt
    def scrypt_func(data):
        """Scrypt function simplification"""
        scrypt.hash(data.encode("ascii"), salt=b"", N=16384, r=8, p=8, dkLen=32)

BITCOIN_B58CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
RIPPLE_B58CHARS = 'rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz'
N = int("FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141".replace(" ", ""), 16)
LITECOIN_PUBKEY_ADDRESS_MAIN = 48
PUBKEY_ADDRESS_MAIN = 0

BITCOIN_B58CHARS_VALUES = dict((c, val) for val, c in enumerate(BITCOIN_B58CHARS))
RIPPLE_B58CHARS_VALUES = dict((c, val) for val, c in enumerate(RIPPLE_B58CHARS))

class Base58DecodingError(Exception):
    """Base 58 decoding error"""

class ChecksumError(Exception):
    """checksum error"""

def verify_solo_check(string, size=1):
    """verify if the string has a valid checksum"""
    raw = string[:-size]
    check = int.from_bytes(doublesha256(raw.encode("ascii")), "little") % 58**size
    return base58encode(check, length=1) == string[-size:]

#### BASE 58
def count_leading_base58_zeros(b58str, ripple):
    """count the number of zero in the base58"""
    b58chars = RIPPLE_B58CHARS if ripple else  BITCOIN_B58CHARS
    return count_leading_values(b58str, b58chars[0])

def count_leading_values(lst, char):
    """count the number of char at the beginnig of the string/bytearray lst"""
    n = 0
    l = len(lst)
    while n < l and lst[n] == char:
        n += 1
    return n

def base58decode(b58str, ripple=False):
    """convert a base 58 into an integer"""
    b58chars_values = RIPPLE_B58CHARS_VALUES if ripple else BITCOIN_B58CHARS_VALUES
    value = 0
    for c in b58str:
        if c not in b58chars_values:
            raise Base58DecodingError("Invalid character: %s" % (c))
        value = value * 58 + b58chars_values[c]
    return value

def base58encode(value, leading_zeros=None, ripple=False, length=None):
    """convert an integer in base 58 with a certain number of zeros at the beginning"""
    b58chars = RIPPLE_B58CHARS if ripple else  BITCOIN_B58CHARS
    result = ""
    while value != 0:
        div, mod = divmod(value, 58)
        result = b58chars[mod] + result
        value = div
    if leading_zeros:
        return b58chars[0] * leading_zeros + result
    if length is not None:
        result = b58chars[0] * (length-len(result)) + result
    return result

def encode_base58check(content, preserve_leading_zeros=True, ripple=False):
    """ Encode a bytestring (bid endian) as base58 with checksum.
        preserve_leading_zeros: argument used for MAIN bitcoin addresses (e.g.ADDRESSVERSION == 0)
        to preserve base256 leading zeros as base58 zeros ('1').
        For example:
            addrversion=00,hash160=00602005b16851c4f9d0e2c82fa161ac8190e04c will give the bitcoin address:
            112z9tWej11X94khKKzofFgWbdhiXLeHPD
    """
    data = content + doublesha256(content)[:4]
    leading_zeros = None
    if preserve_leading_zeros:
        leading_zeros = count_leading_values(data, 0)
    return base58encode(int.from_bytes(data, "big"), leading_zeros=leading_zeros, ripple=ripple)

def decode_base58check(data, preserve_leading_zeros=True, ripple=False):
    """Verify the checksum + decode """
    raw = b""
    if preserve_leading_zeros:
        raw = bytes(count_leading_base58_zeros(data, ripple) * [0])
    integer = base58decode(data, ripple=ripple)
    if integer == 0:
        raise ChecksumError("Empty")
    if integer == 1:
        print(integer)
        raise ChecksumError("Empty")
    raw += integer.to_bytes(math.ceil(math.log(integer, 256)), "big")
    if len(raw) < 5:
        print(raw)
        raise ChecksumError("Empty")
    content, check = raw[:-4], raw[-4:]
    digest2 = doublesha256(content)
    if digest2[:4] != check:
        raise ChecksumError("base58check: checksum error %s != %s" % (digest2[:4].hex(), check.hex()))
    return content

def is_b58_string(str_value, size=None):
    """verifies that all the character present in the string are indeed a valid
       base58 character
    """
    if size is not None and len(str_value) != size:
        return False
    return all([c in BITCOIN_B58CHARS for c in str_value])

#### Ethereum checksum
def checksum_encode(addr_hex):
    """Takes a 40-byte hex address as input and set upper and lower case for the letters to included
       checksum"""
    output = ''
    addr_hex_low = addr_hex.lower()
    v = int.from_bytes(sha3.keccak_256(addr_hex_low.encode("ascii")).digest(), 'big')
    for i, c in enumerate(addr_hex_low):
        if c in '0123456789':
            output += c
        else:
            output += c.upper() if (v & (2**(255 - 4*i))) else c.lower()
    return '0x' + output

#### HASH
def hash_160(public_key):
    """perform the sha256 operation followed by the ripemd160 operation"""
    hash256 = hashlib.sha256(public_key).digest()
    return hashlib.new('ripemd160', hash256).digest()

def doublesha256(data):
    """perform double sha operation often used in bitcoin"""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

#### Elliptic Curve
def compute_privatekey_sec256k1(secret1_b58, secret2_b58):
    """ from two secret in base 58, creates 2 big integers
        and compute the ECC private key by adding them"""
    assert all(map(lambda c: c in BITCOIN_B58CHARS, secret1_b58))
    assert all(map(lambda c: c in BITCOIN_B58CHARS, secret2_b58))
    hashed_secret1 = scrypt_func(secret1_b58)
    hashed_secret2 = scrypt_func(secret2_b58)
    n_1 = int.from_bytes(hashed_secret1, 'big')
    n_2 = int.from_bytes(hashed_secret2, 'big')
    n_0 = (n_1 + n_2) % N
    privkey_b256 = int.to_bytes(n_0, 32, 'big')
    return privkey_b256

def compute_public_key_sec256k1(privkey_b256, compressed=True):
    """compute the public key on the curve sec256k1 from the private key"""
    key = ecdsa.SigningKey.from_string(privkey_b256, curve=ecdsa.SECP256k1)
    if compressed:
        pubpoint = key.get_verifying_key().pubkey.point
        c_bit = pubpoint.y() % 2 + 2
        x_point = pubpoint.x()
        return c_bit.to_bytes(1, "big") + x_point.to_bytes(32, "big")
    return key.get_verifying_key().to_string()

#### Addresses
def verify_address(addr, currency="BTC"):
    """verify the validity of an address"""
    if currency == "ETH":
        return checksum_encode(addr[2:]) == addr
    try:
        if currency in ["BTC", "LTC"]:
            content = decode_base58check(addr)
            if currency == "BTC":
                return content[0] == PUBKEY_ADDRESS_MAIN
            if currency == "LTC":
                return content[0] == LITECOIN_PUBKEY_ADDRESS_MAIN
        if currency == "XRP":
            content = decode_base58check(addr, ripple=True)
            return content[0] == PUBKEY_ADDRESS_MAIN
    except Base58DecodingError:
        pass
    except ChecksumError:
        pass
    return False

def address_from_publickey_bitcoin(public_key):
    """generate a bitcoin address from a public key"""
    return encode_base58check(PUBKEY_ADDRESS_MAIN.to_bytes(1, "big") + hash_160(public_key), preserve_leading_zeros=True)

def address_from_publickey_ethereum(public_key):
    """generate a ethereum address from a public key"""
    address = sha3.keccak_256(public_key).hexdigest()[24:]
    return checksum_encode(address)

def address_from_publickey_litecoin(public_key):
    """generate a litecoin address from a public key"""
    return encode_base58check(LITECOIN_PUBKEY_ADDRESS_MAIN.to_bytes(1, "big") + hash_160(public_key), preserve_leading_zeros=True)

def address_from_publickey_ripple(publickey):
    """generate a ripple address from a public key"""
    hpk = b"\x00" + hash_160(publickey)
    address = encode_base58check(hpk, preserve_leading_zeros=True, ripple=True)
    return address

#### Private key format
def wif_export_bitcoin(privkey_bytearray):
    """convert a private key in bytearray into the bitcoin wif format"""
    first = b"\x80"
    privkey = first + privkey_bytearray
    privkey = privkey + b"\x01"
    privkey = privkey + doublesha256(privkey)[:4]
    privkey_num = int.from_bytes(privkey, "big")
    privkey_wif = base58encode(privkey_num)
    return privkey_wif

def wif_export_litecoin(privkey_bytearray):
    """convert a private key in bytearray into the litecoin wif format"""
    first = b"\xb0"
    privkey = first + privkey_bytearray
    privkey = privkey + b"\x01"
    privkey = privkey + doublesha256(privkey)[:4]
    privkey_num = int.from_bytes(privkey, "big")
    privkey_wif = base58encode(privkey_num)
    return privkey_wif
