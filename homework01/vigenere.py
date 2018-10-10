def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    keyword *= len(plaintext)
    keyword = keyword.lower()
    for i, lett in enumerate(plaintext):
        n = ord(lett)
        if 'a' <= lett <= 'z' or 'A' <= lett <= 'Z':
            n += ord(keyword[i]) - ord('a')
            if (ord('Z') < n and lett <= 'Z') or n > ord('z'):
                n -= 26
        ciphertext += chr(n)


    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    keyword *= len(ciphertext)
    keyword = keyword.lower()
    for i, lett in enumerate(ciphertext):
        n = ord(lett)
        if 'a' <= lett <= 'z' or 'A' <= lett <= 'Z':
            n -= ord(keyword[i]) - ord('a')
            if (ord('a') > n and lett >= 'a') or n < ord('A'):
                n += 26
        plaintext += chr(n)

    return plaintext
