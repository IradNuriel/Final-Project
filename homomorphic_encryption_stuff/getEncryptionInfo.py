from seal import *
from util.constant import KEYS_PATH


def generate_encryption_params():
    parms = EncryptionParameters(scheme_type.bfv)
    poly_modulus_degree = 32768
    parms.set_poly_modulus_degree(poly_modulus_degree)
    parms.set_coeff_modulus(CoeffModulus.BFVDefault(poly_modulus_degree))
    parms.set_plain_modulus(1024)
    
    _context = SEALContext(parms)
    keygen = KeyGenerator(_context)
    _public_key = keygen.create_public_key()
    _secret_key = keygen.secret_key()
    _public_key.save(f'{KEYS_PATH}\\public_key')
    _secret_key.save(f'{KEYS_PATH}\\secret_key')
    parms.save(f'{KEYS_PATH}\\Encryption_params')


# load encryption parameters from memory
parms = EncryptionParameters(scheme_type.bfv)
parms.load(f'{KEYS_PATH}\\Encryption_params')
context = SEALContext(parms)
public_key = PublicKey()
public_key.load(context, f'{KEYS_PATH}\\public_key')
secret_key = SecretKey()
secret_key.load(context, f'{KEYS_PATH}\\secret_key')


evaluator = Evaluator(context)
encryptor = Encryptor(context, public_key)
decryptor = Decryptor(context, secret_key)


