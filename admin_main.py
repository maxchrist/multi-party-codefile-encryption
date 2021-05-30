import admin_encrypt_and_sign
import encrypt
import decrypt
import gen_admin_keys
main_loop = True
while main_loop is True:
    action = input("Choose an action: Generate new symmetric/signature keys (g); Encrypt/sign symmetric key in order to send to user (a); Encrypt code files (e); Decrypt code files (d); Quit (q).  ")
    if(action == "G" or action == 'g'):
        gen_admin_keys.main()
    elif(action == "A" or action == 'a'):
        admin_encrypt_and_sign.main()
    elif(action == "E" or action == 'e'):
        encrypt.main()
    elif(action == "D" or action == 'd'):
        decrypt.main()
    elif(action == "Q" or action == 'q'):
        main_loop = False
    else:
        print("Incorrect input value.")
