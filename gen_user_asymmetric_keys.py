''' This code should be run by the user when they want to join the project and
    get access to the symmetric key. In other words, this code creates the public and
    private keys for the asymmetric encryption scheme. Note, the private key is stored locally,
    and the user will need to choose a password to protect it with. '''

import cryptography
# General Notes: Fernet is part of cryptography package for high level tools,
#                hazmat is for low level primitives
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def generate_asymmetric_private_keys():
    ''' For regular users: Create private/public keys for asymmetric encryption'''
    from cryptography.hazmat.primitives.asymmetric import rsa
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend())
    return private_key


def serialize_asymmetric_keys(private_key, username):
    '''Serializes keys and writes them to a .pem file. Note: I should add an option to define filename etc.'''
    dirname = os.getcwd()
    tempfilename = ("public_asymmetric_key_" + username + ".pem")
    public_asymmetric_key_path = os.path.join(dirname, tempfilename)
    tempfilename = ("private_asymmetric_key_" + username + ".pem")
    private_asymmetric_key_path = os.path.join(dirname, tempfilename)
    if os.path.isfile(public_asymmetric_key_path) or os.path.isfile(private_asymmetric_key_path):
        query_resp = input("One or more symmetric key files already exists, do you wish to overwrite them? (Enter Y if yes, else enter any other key): ")
        if query_resp == "Y" or query_resp == "y":
            serialize_asymmetric_keys_guts(private_key, username, public_asymmetric_key_path, private_asymmetric_key_path)
        else:
            print("No asymmetric keys were created.")
    else:
        serialize_asymmetric_keys_guts(private_key, username, public_asymmetric_key_path, private_asymmetric_key_path)


def serialize_asymmetric_keys_guts(private_key, username, public_path, private_path):
    password = input("Enter a password for protecting locally stored private key for asymmetric scheme: ")
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    password = bytes(password, 'utf-8')
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )
    print('Path of public key is ' + public_path + ' and the path of the private key is ' + private_path)
    with open(public_path, "wb") as public_key_file:
        public_key_file.write(public_pem)
    with open(private_path, "wb") as private_key_file:
        private_key_file.write(private_pem)


def main():
    # For regular users: Create private/public keys for asymmetric encryption
    private_key = generate_asymmetric_private_keys()
    #                    Serialize and write keys to file.
    username = input("Enter Github username to use for filenames: ")
    serialize_asymmetric_keys(private_key, username)
