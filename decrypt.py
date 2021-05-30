'''This code should be run when a user wants to decrypt code they downloaded from Github. '''
import cryptography
# General Notes: Fernet is part of cryptography package for high level tools,
#                hazmat is for low level primitives
import os
from cryptography.fernet import Fernet


def decrypt_code_file():
    '''Derypts the contents of a code file'''
    username = input("Enter your username: ")
    loop_var = True
    dirname = os.getcwd()
    tempfilename = ("local_symmetric_key_" + username + ".pem")
    symmetrickeyfilepath = os.path.join(dirname, tempfilename)
    if not os.path.isfile(symmetrickeyfilepath):
        loop_var = False
        print("Your symmetric key file " + symmetrickeyfilepath + " was not found. Please put the symmetric key file into the current working directory. Also verify that you used your Github username when creating the symmetric key file.")
    while loop_var is True:
        encrypted_file_name = input("Enter the name of the encrytpted file in the current working directory (without the .[extention]): ")
        encrypted_file_ext = input("Enter the file extention of the encrytpted file (without the period): ")
        tempfilename = (encrypted_file_name + "." + encrypted_file_ext)
        encrypted_file_path = os.path.join(dirname, tempfilename)
        tempfilename = (encrypted_file_name + "_decrypted." + encrypted_file_ext)
        unencrypted_file_path = os.path.join(dirname, tempfilename)
        if not os.path.isfile(encrypted_file_path):
            input_query = ("The encrypted file " + encrypted_file_path + " was not found. Please ensure the file is in the current working directory, and the filename is correct. Press y to try again, or press any other key to quit. ")
            query_resp = input(input_query)
            if query_resp == "Y" or query_resp == "y":
                pass
            else:
                print("The code file was not decrypted.")
                loop_var = False
        elif os.path.isfile(unencrypted_file_path):
            input_query = ("The decrypted code file " + unencrypted_file_path + " already exists, do you wish to overwrite it? (Enter Y if yes, else enter any other key): ")
            query_resp = input(input_query)
            if query_resp == "Y" or query_resp == "y":
                decrypt_code_file_guts(symmetrickeyfilepath, encrypted_file_path, unencrypted_file_path)
                print('The decrypted code file is ' + unencrypted_file_path + '.')
                loop_var = False
            else:
                print("The code file was not decrypted.")
                loop_var = False
        else:
            decrypt_code_file_guts(symmetrickeyfilepath, encrypted_file_path, unencrypted_file_path)
            print('The decrypted code file is ' + unencrypted_file_path + '.')
            loop_var = False


def decrypt_code_file_guts(symmetrickeyfilepath, encrypted_file_path, unencrypted_file_path):
    '''Decrypts the contents of an encrypted file'''
    # Import locally stored symmetric key
    with open(symmetrickeyfilepath, "rb") as symmetric_key_file:
        symmetric_key = symmetric_key_file.read()
    # Import contents of encrypted file
    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted_file_contents = encrypted_file.read()
    # Decrypt the contents of the encrypted file
    f = Fernet(symmetric_key)
    unencrypted_file_contents = f.decrypt(encrypted_file_contents).decode("utf-8")
    # Write unencrypted code to local file
    with open(unencrypted_file_path, "w") as user_decrypted_code_file:
        user_decrypted_code_file.write(unencrypted_file_contents)


def main():
    decrypt_code_file()
