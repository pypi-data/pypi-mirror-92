""" Class to handle the encryption and decryption of strings """
import base64


def encode(key, string):
    """
    Encryption with a key attached to ensure the key is accurate
    :param key: bytes of the key to be encrypted
    :param string: bytes of the message to be encrypted
    :return: fully encoded value
    """
    # Encode message and reverse
    message_enc = base64.urlsafe_b64encode(string)
    message_enc_rev = message_enc[::-1]

    # Reverse key and encode
    key_rev = key[::-1]
    key_rev_enc = base64.urlsafe_b64encode(key_rev)

    # Build return and encode a final time
    response = f'{key_rev_enc.decode()}__BS__{message_enc_rev.decode()}'
    response = base64.urlsafe_b64encode(bytes(response, 'utf-8'))
    return response


def decode(key, encoded_string):
    """
    Decryption of the encoded string and validation with the key
    :param key: bytes of the key that should be decrypted
    :param encoded_string: fully encoded cookie set up by the encode method
    :return: fully decoded value
    """
    # First level decoding
    string = base64.urlsafe_b64decode(encoded_string)

    # Split the string
    values = string.split(b'__BS__')
    key_rev_enc = values[0]
    message_enc_rev = values[1]

    # Decode and validate key
    key_rev = base64.urlsafe_b64decode(key_rev_enc)
    chk_key = key_rev[::-1]
    if key != chk_key:
        return 'Invalid key'

    # Decode and return message
    message_enc = message_enc_rev[::-1]
    message = base64.urlsafe_b64decode(message_enc)
    return message
