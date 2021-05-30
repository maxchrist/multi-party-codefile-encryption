import decrypt_users_symmetric_key
import encrypt
import decrypt
import gen_user_asymmetric_keys
main_loop = True
while main_loop is True:
    action = input("Choose an action: Generate new asymmetric keys (g); Decrypt the symmetric key from the admin (a); Encrypt code files (e); Decrypt code files (d); Quit (q).  ")
    if(action == "G" or action == 'g'):
        gen_user_asymmetric_keys.main()
    elif(action == "A" or action == 'a'):
        decrypt_users_symmetric_key.main()
    elif(action == "E" or action == 'e'):
        encrypt.main()
    elif(action == "D" or action == 'd'):
        decrypt.main()
    elif(action == "Q" or action == 'q'):
        main_loop = False
    else:
        print("Incorrect input value.")
