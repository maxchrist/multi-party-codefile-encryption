
import cryptography
# General Notes: Fernet is part of cryptography package for high level tools,
#                hazmat is for low level primitives
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding


def decrypt_symmetric_key():
    # Raises InvalidSignature if verification fails
    username = input("Enter the username you chose when setting up asymmetric keys: ")
    dirname = os.getcwd()
    tempfilename = ("encrypted_symmetric_key_" + username + ".pem")
    encrypted_symmetric_key_path = os.path.join(dirname, tempfilename)
    tempfilename = ("private_asymmetric_key_" + username + ".pem")
    privatekeyfilepath = os.path.join(dirname, tempfilename)
    tempfilename = ("encrypted_symmetric_key_signature_" + username + ".pem")
    signature_path = os.path.join(dirname, tempfilename)
    tempfilename = ("local_symmetric_key_" + username + ".pem")
    local_symmetric_key = os.path.join(dirname, tempfilename)
    sigpublickeyfilepath = os.path.join(dirname, "sig_public_key.pem")
    if not os.path.isfile(encrypted_symmetric_key_path):
        print("Encrypted symmetric key file from the admin " + encrypted_symmetric_key_path + " not found. Please put the encrypted symmetric key file into the current working directory. Also verify that the admin used your Github username when encrypting the symmetric key file.")
    elif not os.path.isfile(privatekeyfilepath):
        print("User's asymmetric private key file " + privatekeyfilepath + " not found. Please put the asymmetric private key file into the current working directory. Also verify that you used your Github username when creating the asymmetric private key file.")
    elif not os.path.isfile(signature_path):
        print("Signature file from the admin " + signature_path + " not found. Please put the signature file into the current working directory. Also verify that the admin used your Github username when creating the signature file.")
    elif not os.path.isfile(sigpublickeyfilepath):
        print("Public signature key file from the admin " + sigpublickeyfilepath + " not found. Please put the public signature key file into the current working directory. Also verify that the admin used your Github username when creating the public signature key file.")
    elif os.path.isfile(local_symmetric_key):
        input_query = ("The decrypted file containing the symmetric key " + local_symmetric_key + " already exists, do you wish to overwrite it? (Enter Y if yes, else enter any other key): ")
        query_resp = input(input_query)
        if query_resp == "Y" or query_resp == "y":
            decrypt_symmetric_key_guts(encrypted_symmetric_key_path, privatekeyfilepath, signature_path, local_symmetric_key, sigpublickeyfilepath)
            print('The decrypted file containing the symmetric key is ' + local_symmetric_key + '. Please store this file in a safe place, and do not distribute.')
        else:
            print("The symmetric key was not decrypted.")
    else:
        decrypt_symmetric_key_guts(encrypted_symmetric_key_path, privatekeyfilepath, signature_path, local_symmetric_key, sigpublickeyfilepath)
        print('The decrypted file containing the symmetric key is ' + local_symmetric_key + '. Please store this file in a safe place, and do not distribute.')


def decrypt_symmetric_key_guts(encrypted_symmetric_key_path, privatekeyfilepath, signature_path, local_symmetric_key, sigpublickeyfilepath):
    # Import public signature key
    with open(sigpublickeyfilepath, "rb") as sig_public_key_file:
        sig_public_key = serialization.load_pem_public_key(
            sig_public_key_file.read(),
            backend=default_backend()
        )
    # Import encrypted symmetric key
    with open(encrypted_symmetric_key_path, "rb") as symmetric_key_file:
        ciphertext = symmetric_key_file.read()
    # Import asymmetric private key
    password = input("Enter the password for your locally stored asymmetric private key: ")
    password = bytes(password, 'utf-8')
    with open(privatekeyfilepath, "rb") as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=password,
            backend=default_backend()
        )
    # Import signature
    with open(signature_path, "rb") as signature_file:
        signature = signature_file.read()
    plaintext_symmetric_key = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # Verify signature
    sig_public_key.verify(signature, ciphertext)
    # Write unencrypted symmetric key to local file
    with open(local_symmetric_key, "wb") as user_local_symmetric_key_file:
        user_local_symmetric_key_file.write(plaintext_symmetric_key)


def main():
    decrypt_symmetric_key()
