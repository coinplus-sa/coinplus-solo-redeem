"""Solo redeem with command line interface"""
import sys
from coinplus_solo_redeem.common import compute_privatekey_sec256k1, compute_public_key_sec256k1, wif_export_bitcoin,\
    address_from_publickey_bitcoin, wif_export_litecoin, address_from_publickey_litecoin, address_from_publickey_ethereum, address_from_publickey_ripple,\
    is_b58_string
from coinplus_solo_redeem.pro import secret1_reconstruct_base58, secret2_reconstruct_base58

def validate_int(string_input):
    """by pass the ValueError exception for the int convertion and return True or False"""
    try:
        int(string_input)
    except ValueError:
        return False
    return True

CRYPTO = ["BTC", "ETH", "LTC", "XRP"]
SOLO_TYPE = ["SOLO", "SOLO PRO"]

def selector(possibilities):
    """Selector Menu"""
    selected = None
    print("possible value:"+", ".join(possibilities) + " or quit/q/Q:")
    while selected not in possibilities:
        selected = input()
        if selected in ["quit", "q", "Q"]:
            sys.exit(0)
        if  selected not in possibilities:
            print("Wrong selection")
    return selected

def crypto_menu():
    """Menu to select crypto"""
    selected_crypto = selector(CRYPTO)
    return selected_crypto

def type_menu():
    """Menu to select type of solo"""
    selected_type = selector(SOLO_TYPE)
    return selected_type

def secret_input(size):
    """Wait for a valid secret input"""
    s = ""
    while not is_b58_string(s, size):
        s = input("First secret (length="+str(size)+")"+ " or quit/q/Q:")
        if s in ["quit", "q", "Q"]:
            sys.exit(0)
        if not is_b58_string(s, size):
            print("Wrong length or invalid character")
    return s

def pro_input():
    """Wait for a valid pro number input"""
    s = ""
    while not validate_int(s):
        s = input("SOLO PRO number (#) or quit/q/Q:")
        if s in ["quit", "q", "Q"]:
            sys.exit(0)
        if not validate_int(s):
            print("Wrong integer")
    return int(s)

def number_of_pro_input():
    """Wait for a valid number of Pro required"""
    s = ""
    while not validate_int(s):
        s = input("number of PRO:")
        if s in ["quit", "q", "Q"]:
            sys.exit(0)
        if not validate_int(s):
            print("Wrong integer")
    return int(s)

def solo_pro_menu():
    """Solo pro input menu"""
    number_of_pro = number_of_pro_input()
    prs = []
    for _ in range(number_of_pro):
        num = pro_input()
        s1 = secret_input(28)
        s2 = secret_input(14)
        prs.append((num, s1, s2))
    return prs

def main():
    """program for the redemption of the SOLO and SOLO pro private keys"""
    print("This program is for the redemption SOLO private keys")

    selected_type = type_menu()
    selected_crypto = crypto_menu()

    if selected_type == "SOLO PRO":
        prs = solo_pro_menu()
        secrets_1pro = [(num, secret_1) for num, secret_1, secret_2 in prs]
        secrets_2pro = [(num, secret_2) for num, secret_1, secret_2 in prs]
        secret1_b58 = secret1_reconstruct_base58(secrets_1pro)
        secret2_b58 = secret2_reconstruct_base58(secrets_2pro)
    else:
        secret1_b58 = secret_input(28)
        secret2_b58 = secret_input(14)

    privkey256 = compute_privatekey_sec256k1(secret1_b58, secret2_b58)
    public_key = compute_public_key_sec256k1(privkey256)


    if selected_crypto == "BTC":
        privatekey_wif = wif_export_bitcoin(privkey256)
        address = address_from_publickey_bitcoin(public_key)
    if selected_crypto == "LTC":
        privatekey_wif = wif_export_litecoin(privkey256)
        address = address_from_publickey_litecoin(public_key)
    if selected_crypto == "ETH":
        privatekey_wif = privkey256.hex()
        public_key_un = compute_public_key_sec256k1(privkey256, compressed=False)
        address = address_from_publickey_ethereum(public_key_un)
    if selected_crypto == "XRP":
        privatekey_wif = privkey256.hex()
        address = address_from_publickey_ripple(public_key)

    print(privatekey_wif)
    print(address)

if __name__ == "__main__":
    main()
