''' This code should be run when the administratior is first setting up the encrytpion scheme.
    It will generate a symmetric key, and store it to a file.
    It will also generate public and private keys for the asymmetric signature scheme,
    and store each to a separate file. '''

import cryptography
# General Notes: Fernet is part of cryptography package for high level tools,
#                hazmat is for low level primitives
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def generate_symmetric_key():
    ''' For Administrator (Alice): Create key for symmetric encryption'''
    symmetric_key = Fernet.generate_key()
    # Write symmetric key to local file so that it can be encrypted and sent to users in the future
    dirname = os.getcwd()
    username = input("Enter Github username to use for filenames: ")
    tempfilename = ("local_symmetric_key_" + username + ".pem")
    symmetric_key_path = os.path.join(dirname, tempfilename)
    if os.path.isfile(symmetric_key_path):
        query_resp = input("Symmetric key file already exists, do you wish to overwrite it? (Enter Y if yes, else enter any other key): ")
        if query_resp == "Y" or query_resp == "y":
            with open(symmetric_key_path, "wb") as local_symmetric_key_file:
                local_symmetric_key_file.write(symmetric_key)
            print("Symmetric key was created and stored in the follwing file: ")
            print(symmetric_key_path)
        else:
            print("No symmetric key was created.")
    else:
        with open(symmetric_key_path, "wb") as local_symmetric_key_file:
            local_symmetric_key_file.write(symmetric_key)
        print("Symmetric key was created and stored in the follwing file: ")
        print(symmetric_key_path)


def create_signature_keys():
    '''For Administrator (Alice): Create public/private keys for signing messages.'''
    dirname = os.getcwd()
    # Write keys to file
    public_key_path = os.path.join(dirname, "sig_public_key.pem")
    private_key_path = os.path.join(dirname, "sig_private_key.pem")
    if os.path.isfile(public_key_path) or os.path.isfile(private_key_path):
        query_resp = input("One or more signature key files already exists, do you wish to overwrite them? (Enter Y if yes, else enter any other key): ")
        if query_resp == "Y" or query_resp == "y":
            create_signature_keys_guts(public_key_path, private_key_path)
        else:
            print("No signature keys were created.")
    else:
        create_signature_keys_guts(public_key_path, private_key_path)


def create_signature_keys_guts(public_key_path, private_key_path):
    password = input("Enter a password to encrypt your locally stored private signature keys: ")
    password = bytes(password, 'utf-8')
    sig_private_key = Ed25519PrivateKey.generate()
    sig_public_key = sig_private_key.public_key()
    # Get serialized, binary form of public key
    sig_public_key = sig_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    # Get serialized, encrypted, binary form of private key
    sig_private_key = sig_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )
    with open(public_key_path, "wb") as sig_public_key_file:
        sig_public_key_file.write(sig_public_key)
    with open(private_key_path, "wb") as sig_private_key_file:
        sig_private_key_file.write(sig_private_key)
    print("Signature keys were created and stored in the follwing files: ")
    print(public_key_path, private_key_path)


def main():
    generate_symmetric_key()
    create_signature_keys()
