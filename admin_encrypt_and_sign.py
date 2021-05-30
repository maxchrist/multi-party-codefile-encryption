''' This code should be run after the administratior receives a public key from a user
    who wants to participate in the project.
    The code will use the users public key to publicly encrypt the symmetric key.
    It will also create a digital signature using the administrators public and private
    signature keys. In order to sign, it will ask for the admins password to the locally
    stored private signature key. '''

import cryptography
# General Notes: Fernet is part of cryptography package for high level tools,
#                hazmat is for low level primitives
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


def publicly_encrypt_symmetric_key(symmetrickeyfilepath, keyfilepath, sigprivatekeyfilepath, ciphertextfilepath, signaturefilepath, password):
    '''For Administrator (Alice): Encrypt the symmetric key using the public key from a given user'''
    '''Using a given user's public key file, import the public key, encrypt the symmetric key and write it to file'''
    # Import public key from .pem file
    with open(keyfilepath, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    # Import symmetric key
    with open(symmetrickeyfilepath, "rb") as symmetric_key_file:
        symmetric_key = symmetric_key_file.read()
    # Encrypt symmetric Key
    ciphertext = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # Import private signature key
    password = bytes(password, 'utf-8')
    with open(sigprivatekeyfilepath, "rb") as sig_private_key_file:
        sig_private_key = serialization.load_pem_private_key(
            sig_private_key_file.read(),
            password=password,
            backend=default_backend()
        )
    signature = sig_private_key.sign(ciphertext)
    # Write encrypted symmetric key to file
    print('Path of encrypted symmetric key is ' + ciphertextfilepath)
    with open(ciphertextfilepath, "wb") as symmetric_file:
        symmetric_file.write(ciphertext)
    with open(signaturefilepath, "wb") as symmetric_sig_file:
        symmetric_sig_file.write(signature)
    return ciphertext, signature


def main():
    admin_username = input("Enter your Github username: ")
    filename = input("Enter the Github username of the chosen user: ")
    dirname = os.getcwd()
    tempfilename = ("local_symmetric_key_" + admin_username + ".pem")
    symmetrickeyfilepath = os.path.join(dirname, tempfilename)
    tempfilename = ("public_asymmetric_key_" + filename + ".pem")
    keyfilepath = os.path.join(dirname, tempfilename)
    tempfilename = ("encrypted_symmetric_key_" + filename + ".pem")
    ciphertextfilepath = os.path.join(dirname, tempfilename)
    tempfilename = ("encrypted_symmetric_key_signature_" + filename + ".pem")
    signaturefilepath = os.path.join(dirname, tempfilename)
    sigprivatekeyfilepath = os.path.join(dirname, "sig_private_key.pem")
    if not os.path.isfile(sigprivatekeyfilepath):
        print("Admin private signature key file " + sigprivatekeyfilepath + " not found. Please put the signature key file into the current working directory.")
    elif not os.path.isfile(symmetrickeyfilepath):
        print("Admin symmetric key file " + symmetrickeyfilepath + " not found. Please put the symmetric key file into the current working directory.")
    elif not os.path.isfile(keyfilepath):
        print("User's public asymmetric key file " + keyfilepath + " not found. Please put the symmetric key file of the chosen user into the current working directory. Also verify that they used their Github username when creating the symmetric key file.")
    elif os.path.isfile(ciphertextfilepath) or os.path.isfile(signaturefilepath):
        input_query = ("Either the encrypted file containing the symmetric key " + ciphertextfilepath + " or the assocaited signature file " + signaturefilepath + " already exists, do you wish to overwrite them? (Enter Y if yes, else enter any other key): ")
        query_resp = input(input_query)
        if query_resp == "Y" or query_resp == "y":
            password = input("Enter the password for your private key for signatures: ")
            # For Administrator (Alice): Encrypt the symmetric key and write it to a file for user
            ciphertext, signature = publicly_encrypt_symmetric_key(symmetrickeyfilepath, keyfilepath, sigprivatekeyfilepath, ciphertextfilepath, signaturefilepath, password)
            print('The encrypted file containing the symmetric key is ' + ciphertextfilepath + '.')
        else:
            print("The symmetric key was not encrypted and no signature was created.")
    else:
        password = input("Enter the password for your private key for signatures: ")
        # For Administrator (Alice): Encrypt the symmetric key and write it to a file for user
        ciphertext, signature = publicly_encrypt_symmetric_key(symmetrickeyfilepath, keyfilepath, sigprivatekeyfilepath, ciphertextfilepath, signaturefilepath, password)
        print('The encrypted file containing the symmetric key is ' + ciphertextfilepath + '.')
