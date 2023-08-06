This is a module for decoding/encoding text in various ciphers.

Usage:
Current commands available are:

Encoders:-

text2bin(text)
text2oct(text)
text2hex(text)
text2atbash(text)
text2caesar(text, shift)
text2railfence(text, key=3)

Decoders:-

bin2text(binary_text)
oct2text(oct_text)
hex2text(hex_text)
atbash2text(encrypted_text)
caesar2text(encrypted_text, shift)
caesarBruteforce(encrypted_text)
railfence2text(cipher, key=3)
reverse(text)