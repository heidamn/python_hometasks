def encrypt_caesar(plaintext, shift):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    shift %= 26
    ciphertext = ''
    n = 0
    for i in plaintext:
        n = ord(i)
        if 'a' <= i <= 'z' or 'A' <= i <= 'Z':
            n += shift
            if ord('Z') < n and i<='Z' or n > ord('z'):
                n -= 26
        ciphertext += chr(n)
    return ciphertext


def decrypt_caesar(ciphertext, shift):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    shift %= 26
    plaintext = ''
    n = 0
    for i in ciphertext:
        n = ord(i)
        if 'a' <= i <= 'z' or 'A' <= i <= 'Z':
            n -= shift
            if n < ord("a") and i>='a' or n < ord('A'):
                n += 26
        plaintext += chr(n)
    return plaintext