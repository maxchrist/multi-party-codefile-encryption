'''This code should be run when a user wants to encrypt their code before uploading to Github.  '''
import cryptography
# General Notes: Fernet is part of cryptography package for high level tools,
#                hazmat is for low level primitives
import os
from cryptography.fernet import Fernet


def encrypt_code_file():
    '''Enrypts the contents of a code file'''
    username = input("Enter your username: ")
    loop_var = True
    dirname = os.getcwd()
    tempfilename = ("local_symmetric_key_" + username + ".pem")
    symmetrickeyfilepath = os.path.join(dirname, tempfilename)
    if not os.path.isfile(symmetrickeyfilepath):
        loop_var = False
        print("Your symmetric key file " + symmetrickeyfilepath + " was not found. Please put the symmetric key file into the current working directory. Also verify that you used your Github username when creating the symmetric key file.")
    while loop_var is True:
        file = input("Enter the name of a code file in the current working directory (without the .[extention]): ")
        file_ext = input("Enter the file extention of a code file (without the period): ")
        tempfilename = (file + "." + file_ext)
        filepath = os.path.join(dirname, tempfilename)
        tempfilename = (file + "_encrypted." + file_ext)
        ciphertextfilepath = os.path.join(dirname, tempfilename)
        if not os.path.isfile(filepath):
            input_query = ("The inputted code file " + filepath + " was not found. Please ensure the file is in the current working directory, and the filename is correct. Press y to try again, or press any other key to quit. ")
            query_resp = input(input_query)
            if query_resp == "Y" or query_resp == "y":
                pass
            else:
                print("The code file was not encrypted.")
                loop_var = False
        elif os.path.isfile(ciphertextfilepath):
            input_query = ("The encrypted code file " + ciphertextfilepath + " already exists, do you wish to overwrite it? (Enter Y if yes, else enter any other key): ")
            query_resp = input(input_query)
            if query_resp == "Y" or query_resp == "y":
                encrypt_code_file_guts(symmetrickeyfilepath, filepath, ciphertextfilepath)
                print('The encrypted code file is ' + ciphertextfilepath + '.')
                loop_var = False
            else:
                print("The code file was not encrypted.")
                loop_var = False
        else:
            encrypt_code_file_guts(symmetrickeyfilepath, filepath, ciphertextfilepath)
            print('The encrypted code file is ' + ciphertextfilepath + '.')
            loop_var = False


def encrypt_code_file_guts(symmetrickeyfilepath, filepath, ciphertextfilepath):
    # Import locally stored symmetric key
    with open(symmetrickeyfilepath, "rb") as symmetric_key_file:
        symmetric_key = symmetric_key_file.read()
    # Import local code file
    with open(filepath, "r") as code_file:
        code = code_file.read()
    # Convert to bytes
    code = bytes(code, 'utf-8')
    # Encrypt the code with the symmetric key
    f = Fernet(symmetric_key)
    ciphertext = f.encrypt(code)
    # Save encrypted file to disk
    with open(ciphertextfilepath, "wb") as encrypted_file:
        encrypted_file.write(ciphertext)


def main():
    encrypt_code_file()
