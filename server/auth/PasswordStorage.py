import secrets
import pbkdf2
import unpaddedbase64


class InvalidHashException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CannotPerformOperationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PasswordStorage:
    PBKDF2_ALGORITHM = "PBKDF2WithHmacSHA1"
    SHA1 = "sha1"
    SALT_BYTE_SIZE = 24
    HASH_BYTE_SIZE = 18
    PBKDF2_ITERATIONS = 64000

    HASH_SECTIONS = 5
    HASH_ALGORITHM_INDEX = 0
    ITERATION_INDEX = 1
    HASH_SIZE_INDEX = 2
    SALT_INDEX = 3
    PBKDF2_INDEX = 4

    def createHash(self, password):
        # Generate a random salt
        salt = secrets.token_bytes(PasswordStorage.SALT_BYTE_SIZE)
        # Hash the password
        hash = self.create_pbkdf2(password, salt, PasswordStorage.PBKDF2_ITERATIONS, PasswordStorage.HASH_BYTE_SIZE)
        hashSize = len(hash)
        saltBase64 = self.convertToBase64(salt)
        hashBase64 = self.convertToBase64(hash)
        # format: algorithm:iterations: hashSize:salt: hash
        return '{0}:{1}:{2}:{3}:{4}'.format(PasswordStorage.SHA1, PasswordStorage.PBKDF2_ITERATIONS,
                                            hashSize, saltBase64, hashBase64)

    def verifyPassword(self, password, correctHash):
        # Decode the hash into its parameters
        params = correctHash.split(":")
        if len(params) != PasswordStorage.HASH_SECTIONS:
            raise InvalidHashException("Fields are missing from the password hash") from None
        if params[PasswordStorage.HASH_ALGORITHM_INDEX] != PasswordStorage.SHA1:
            raise CannotPerformOperationException("Unsupported hash type") from None
        try:
            iterations = int(params[PasswordStorage.ITERATION_INDEX])
        except RuntimeError:
            raise InvalidHashException("Could not parse the iteration count as an integer") from None
        if iterations < 1:
            raise InvalidHashException("Invalid number of iterations. Must be >= 1") from None
        try:
            salt = self.convertFromBase64(params[PasswordStorage.SALT_INDEX])
        except RuntimeError:
            raise RuntimeError("Base64 decoding of salt failed") from None
        try:
            hash = self.convertFromBase64(params[PasswordStorage.PBKDF2_INDEX])
        except RuntimeError:
            raise RuntimeError("Base64 decoding of pbkdf2 output failed") from None
        try:
            storedHashSize = int(params[PasswordStorage.HASH_SIZE_INDEX])
        except RuntimeError:
            raise RuntimeError("Could not parse the hash size as an integer") from None
        if storedHashSize != len(hash):
            raise InvalidHashException("Hash length doesn't match stored hash length") from None
        testHash = self.create_pbkdf2(password, salt, iterations, len(hash))
        return self.Equals(hash, testHash)

    def Equals(self, a, b):
        diff = len(a) ^ len(b)
        i = 0
        while i < len(a) and i < len(b):
            diff = diff or int(a[i]) ^ int(b[i])
            i += 1
        return diff == 0

    def create_pbkdf2(self, password, salt, iterations, bytes):
        try:
            return pbkdf2.PBKDF2(password, salt, iterations).read(bytes)
        except RuntimeError:
            raise RuntimeError("Couldn't create PBKDF2 key") from None

    def convertFromBase64(self, array):
        return unpaddedbase64.decode_base64(array)

    def convertToBase64(self, array):
        return unpaddedbase64.encode_base64(array)


