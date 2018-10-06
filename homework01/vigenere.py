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
    ciphertext=''
    keyword *= len(plaintext)
    keyword=keyword.lower()
    for i,lett in enumerate(plaintext):
        n = ord(lett)
        if 'a' <= lett <= 'z' or 'A' <= lett <= 'Z':
            n += ord(keyword[i]) - ord('a')
            if (ord('Z') < n and lett <= 'Z') or n > ord('z'):
                n -= 26
        ciphertext+=chr(n)


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
    # PUT YOUR CODE HERE
    return plaintext
