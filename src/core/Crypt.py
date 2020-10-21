#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# CRYPT
######################################################################################################
# Description : Fonctions de cryptage/decryptage de chaine
# Date de Creation : 06/05/2020
######################################################################################################
# AIDE
# https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
######################################################################################################
# Globales
import base64

######################################################################################################
# CLASS
######################################################################################################


class Crypt:
    def __init__():
        pass

    @staticmethod
    def encode(key, string):
        """Encode une chaine à partir de la key"""
        encoded_chars = []
        string = str(string)
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 128)
            encoded_chars.append(encoded_c)
        encoded_string = "".join(encoded_chars)
        arr2 = bytes(encoded_string, 'utf-8')
        return base64.urlsafe_b64encode(arr2).decode('utf-8')

    @staticmethod
    def decode(key, string):
        """Decode une chaine à partir de la key"""
        encoded_chars = []
        string = base64.urlsafe_b64decode(string)
        string = string.decode('utf-8')
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) - ord(key_c) % 128)
            encoded_chars.append(encoded_c)
        encoded_string = "".join(encoded_chars)
        return str(encoded_string)
