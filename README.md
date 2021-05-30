# multi-party-codefile-encryption
This is the final project for Modern Cryptography at NYU Tandon. The code provides an encryption method to work collaboratively on a coding project on a website such as Github, but retain full control over their security and privacy. The method prevents adversaries, including the file hosting site, from accessing the encrypted contents of posted files. In order to work on a Github project collaboratively, one person will be the administrator or admin, and be responsible for getting all users to use the same (private) symmetric encryption key. The set up is broken into steps for the admin and the user, which can be found below. 

# Requirements
``` 
$ pip install cryptography
```

# ADMIN SETUP:
1. Administrator should always start by running admin_main.py from the terminal using the following command:
python3 admin_main.py
2. Select the first option in the main menu, which is to generate a symmetric key and public/private signature scheme keys. 
3. Post the public signature scheme key file to the GitHub repository for all users to see. 
4. Keep the private signature scheme key and symmetric key in a safe place, and do not distribute it. 
5. Instruct each user to post an asymmetric key to the GitHub repository. (Users can see instructions for this under “User Setup”)
6. For each public key file (one per user), download the file, put it into your current working directory, and run the “Encrypt/sign symmetric key in order to send to user (a)” function from the main menu of admin_main.py. Note: The locally stored symmetric key, private signature key, and public key file from the given user all must be present in the current working directory.
7. Post each asymmetrically encrypted file produced in step 6 to the Github repository. 
8. Users can now decrypt the file, and use the symmetric key which it contained in order to symmetrically encrypt and decrypt all future code they post or download from GitHub. 
9. Admin can encrypt or decrypt the code posted to the server using either admin_main.py or user_main.py.

# USER SETUP:
1. User should always start by running user_main.py from the terminal using the following command:
python3 user_main.py
2. Select the first option in the main menu, which is to generate new asymmetric keys. 
3. Post the resulting public asymmetric key file to the GitHub repository, so that the admin can use it to encrypt the symmetric key and send it back to you. 
4. When the Admin has posted the encrypted symmetric key file to the Github repository, download this file and move it into your current working directory. 
5. Run the “Decrypt the symmetric key from the admin (a)” option from the main menu. Make sure to keep the resulting file (the symmetric key) in a secure location and do not distribute it. Note: the private asymmetric key must be present in your current working directory as well.
6. You now have a local copy of the symmetric key, which you can use to encrypt/ decrypt code files. 
7. To encrypt a code file, put the code file into your current working directory and run the “Encrypt code files (e)” function from the main menu. The encrypted file can now be safely posted to the GitHub repository. 
8. To decrypt a code file, download the encrypted code file, put it into your current working directory, and then run the “Encrypt code files (e)” function from the main menu. The decrypted file can now be read and worked on. 
