from seal import EncryptionParameters, scheme_type, CoeffModulus, PlainModulus, SEALContext, KeyGenerator, PublicKey, SecretKey, RelinKeys, GaloisKeys, Encryptor, Decryptor, Evaluator, BatchEncoder
from util.constant import KEYS_PATH


def generate_encryption_params():
    _parms = EncryptionParameters(scheme_type.bfv)
    poly_modulus_degree = 32768
    _parms.set_poly_modulus_degree(poly_modulus_degree)
    _parms.set_coeff_modulus(CoeffModulus.BFVDefault(poly_modulus_degree))
    _parms.set_plain_modulus(PlainModulus.Batching(poly_modulus_degree, 17))
    _context = SEALContext(_parms)
    keygen = KeyGenerator(_context)
    _public_key = keygen.create_public_key()
    _secret_key = keygen.secret_key()
    _relin_keys = keygen.create_relin_keys()
    _galois_keys = keygen.create_galois_keys()
    _public_key.save(f'{KEYS_PATH}\\public_key')
    _secret_key.save(f'{KEYS_PATH}\\secret_key')
    _relin_keys.save(f'{KEYS_PATH}\\relin_keys')
    _galois_keys.save(f'{KEYS_PATH}\\galois_keys')
    _parms.save(f'{KEYS_PATH}\\Encryption_params')


# load encryption parameters from memory
def load_params():
    parms = EncryptionParameters(scheme_type.bfv)
    parms.load(f'{KEYS_PATH}\\Encryption_params')
    context = SEALContext(parms)
    public_key = PublicKey()
    public_key.load(context, f'{KEYS_PATH}\\public_key')
    secret_key = SecretKey()
    secret_key.load(context, f'{KEYS_PATH}\\secret_key')
    relin_keys = RelinKeys()
    relin_keys.load(context, f'{KEYS_PATH}\\relin_keys')
    galois_keys = GaloisKeys()
    galois_keys.load(context, f'{KEYS_PATH}\\galois_keys')
    
    evaluator = Evaluator(context)
    encryptor = Encryptor(context, public_key)
    decryptor = Decryptor(context, secret_key)
    encoder = BatchEncoder(context)
    return evaluator, encryptor, decryptor, encoder, context, galois_keys, relin_keys


evaluator, encryptor, decryptor, encoder, context, galois_keys, relin_keys = load_params()
