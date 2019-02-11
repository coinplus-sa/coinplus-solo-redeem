"""Recomputation of the shamir secrets present on the cards for the SOLO PRO"""
import functools
from operator import mul

from coinplus_solo_redeem.common import base58decode, base58encode

P14 = 4875194084160298409672797
P28 = 23767517358231570773047645414309870043308402671871
VERBOSE = 0

def secret1_reconstruct_base58(shares):
    """reconstruct the secret 1 of the solo pro using the shares
       Params
           shares: list of shares [(num, base58_secret)]
    """
    return shamir_reconstruct_base58(shares, P28, 28)

def secret2_reconstruct_base58(shares):
    """reconstruct the secret 2 of the solo pro using the shares
       Params
           shares: list of shares [(num, base58_secret)]
    """
    return shamir_reconstruct_base58(shares, P14, 14)

def extended_gcd(n_1, n_2):
    """ Returns (bezout_a, bezout_b, gcd) using the extended euclidean algorithm.
        Params
            n1: int
            n2: int
        Returns
            bezout_a: int
            bezout_b: int
            gcd: int """
    x = 0
    x_old = 1
    y = 1
    y_old = 0
    while n_2 != 0:
        q = n_1 // n_2 #quotient
        n_1, n_2 = n_2, n_1%n_2
        x, x_old = x_old - q*x, x
        y, y_old = y_old - q*y, y
    bezout_a = x_old
    bezout_b = y_old
    gcd = n_1
    return (bezout_a, bezout_b, gcd)

def lagrange(points, modulus):
    """ Evaluation at x=0 without computing the polynomial
        Params
            points: list of Share
        Returns
            y: int """

    value_p = lambda x: ZpValue(x, modulus)
    ls = []
    for i, pj in enumerate(points):
        factors = []
        for j, pm in enumerate(points):
            if i != j:
                factors.append((value_p(0) - value_p(pm.x)) / (value_p(pj.x) - value_p(pm.x)))
        l = functools.reduce(mul, factors)
        ls.append(l)
    lagrange_list = map(mul, ls, [p.y for p in points])
    y = int(sum(lagrange_list, value_p(0)))
    return y

class ZpValue():
    """Class for a value used to perform arithmetic operations in Zp"""
    def __init__(self, value, modulus):
        self.value = value
        self.modulus = modulus
        assert 0 <= value < modulus
    def __neg__(self):
        return ZpValue((-self.value) % self.modulus, self.modulus)
    def __add__(self, other):
        return ZpValue((self.value + other.value) % self.modulus, self.modulus)
    def __cmp__(self, other):
        a = self.value
        b = other.value
        return (a > b) - (a < b)
    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        return self.value == other.value
    def __hash__(self):
        return hash(self.value)
    def __sub__(self, other):
        return ZpValue((self.value - other.value) % self.modulus, self.modulus)
    def __mul__(self, other):
        return ZpValue((self.value * other.value) % self.modulus, self.modulus)
    def __pow__(self, other):
        return ZpValue(pow(self.value, other.value, self.modulus), self.modulus)
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return 'V('+repr(self.value)+')'
    def __invert__(self):
        if self.value == 0:
            raise ZeroDivisionError()
        bezout_a, _, _ = extended_gcd(self.value, self.modulus)
        return ZpValue(bezout_a % self.modulus, self.modulus)
    def __truediv__(self, other):
        return self * ~other
    def __int__(self):
        return self.value

class Share():
    """Share object representing a point (x, y)
        This object is used for the Shamir secret reconstruction process
    """
    def __init__(self, x, y):
        """
        This data structure can be a Shamir or an IDA share, containing
        its x, which is the index, and its y=P(x) which is the share.
        Params
            x: int
            y: field.ZpValue
        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __repr__(self):
        rep = '['+type(self).__name__+'] '
        rep += 'Index x = '+str(self.x)+', Share y = P(x) = '+str(self.y)
        return rep

class ReconstructionError(Exception):
    """Exception raised when the shamir reconstruction process failed"""

def shamir_reconstruct_base58(shares, modulus, length):
    """ Reconstructs the secret using Lagrange polynomial interpolation.
        Params
            shares: [(int_x, base58_y) , ...]
            modulus:
            length: (of base58)
        Returns
            secret: string """
    recovershares = [Share(x, ZpValue(base58decode(b58y), modulus)) for x, b58y in shares]

    s = shamir_reconstruct(recovershares, modulus)
    return base58encode(s, length=length)

def shamir_reconstruct(shares, modulus):
    """ Reconstructs the secret using Lagrange polynomial interpolation.
        Params
            shares: list of Share (at least 2 Shares as k > 1 for SSSS)
        Returns
            secret: string """
    if len(shares) < 2:
        raise ReconstructionError('Shares are not correct, reconstruction did not work.')
    secret_int = lagrange(shares, modulus)
    return secret_int
