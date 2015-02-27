# -*- coding: utf-8 -*-
import unittest
import urllib

from xxtea import encrypt

def bin216(s):
    o = []

    def char_to_hex(char):
        hex_string = hex(ord(char))[2:]
        return hex_string if len(hex_string) == 2 else '0' + hex_string

    for c in s:
        o.append(char_to_hex(c))

    return "".join(o)

def list_get(lst, i):
    try:
        return lst[i]
    except IndexError:
        return "\00"


def encode32(input):
    keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    input = urllib.quote_plus(input)
    output = []
    i = 0
    while (i < len(input)):
        chr1 = ord(input[i])
        chr2 = ord(list_get(input, i + 1))
        chr3 = ord(list_get(input, i + 2))
        i += 3

        enc1 = chr1 >> 2
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
        enc4 = chr3 & 63;
        if chr2 == 0:
            enc3 = enc4 = 64
        elif chr3 == 0:
            enc4 = 64
        output.extend([keyStr[enc1], keyStr[enc2], keyStr[enc3], keyStr[enc4]])

    return "".join(output)


class JSFunctionsTest(unittest.TestCase):

    def test_bin216(self):
        self.assertEqual(bin216("5"), "35")
        self.assertEqual(bin216("sam"), "73616d")
        self.assertEqual(bin216("sa"), "7361")
        self.assertEqual(bin216("0"), "30")
        self.assertNotEqual(bin216("0"), "31")

#    def test_encrypt(self):
#        self.assertEqual(encrypt("12306sucksballs", "test"), "¯h¾öûþóé?WO¶¯Â+è")

    def test_encode32(self):
        self.assertEquals(encode32("12306sucksballs"), "MTIzMDZzdWNrc2JhbGxz")
        self.assertEquals(encode32("1234"), "MTIzNA==")
        self.assertEquals(encode32("12345"), "MTIzNDU=")

    def test_all_together(self):
        # encode32(bin216(Base32.encrypt(keyVlues[1], keyVlues[0])))
        key = "OTY5Njcz"
        value = "MmNhZTZmMTZhNjVmYTY1Mg=="

        self.assertEquals(encode32(bin216(encrypt("1111", "OTY5Njcz"))), value)

        # bin216(Base32.encrypt("1111", "MjI5NjI0")); = 65aa7df5874e66a5
        self.assertEquals(bin216(encrypt("1111", "MjI5NjI0")), "65aa7df5874e66a5")

        # MjI5NjI0, 1111 (Post: MjI5NjI0:NjVhYTdkZjU4NzRlNjZhNQ==)
        self.assertEquals(encode32(bin216(encrypt("1111", "MjI5NjI0"))), "NjVhYTdkZjU4NzRlNjZhNQ==")


if __name__ == '__main__':
    unittest.main()

