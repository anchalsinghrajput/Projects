from cryptography.fernet import Fernet
from tkinter import messagebox, simpledialog, Tk
import re
import os

alphabets = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
             'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')


# ------- start of encrypting message ----------


def encryptMessage():
    while(True):
        choice1 = (simpledialog.askstring(
            'Your choice', "Type 'encode' to encrypt and 'decode' to decrypt your message : \n")).lower()
        if(choice1 == 'encode' or choice1 == 'decode'):
            break
    msg = (simpledialog.askstring('Your message',
                                  "Type your secret code/message here : \n")).lower()
    shift = simpledialog.askinteger(
        'Shift value', "Type your shift number :\n")
    shift = shift % 25
    messagebox.showinfo("Your secret code/message is : ",
                        cypher(choice1, msg, shift))


def cypher(choice, msg, shift):
    cypherMsg = ""
    if choice == 'decode':
        shift *= -1
    for letter in msg:
        if letter in alphabets:
            position = alphabets.index(letter)
            cypherMsg += alphabets[position + shift]
        else:
            cypherMsg += letter
    return cypherMsg

# -------- end of encrypting message ----------

# -------- start of encrypting file ------------


def encryptTextFile():
    try:
        while(True):
            filename = (simpledialog.askstring(
                'File Name', "Enter your filename: \n"))
            valid = re.search(".*txt$", filename)
            if(valid and os.path.isfile('./' + filename)):
                break
            else:
                messagebox.showinfo(
                    "Error", "Invalid File Name or file does not exist")
        choice2 = (simpledialog.askstring(
            'File Encryption', "Type 'encode' to encrypt and 'decode' to decrypt your file : \n")).lower()
    except:
        pass
    else:
        keyFile = filename[:-4] + '.key'

        if (choice2 == 'encode'):
            encodeFile(keyFile, filename)
        elif(choice2 == 'decode'):
            decodeFile(keyFile, filename)
        else:
            messagebox.showinfo("Error", "Invalid Choice")


def encodeFile(keyFile, filename):
    key = Fernet.generate_key()
    f = Fernet(key)

    with open(keyFile, 'wb') as mykey:
        mykey.write(key)

    with open(filename, 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decodeFile(keyFile, filename):
    with open(keyFile, 'rb') as mykey:
        loadKey = mykey.read()

    f = Fernet(loadKey)

    with open(filename, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = f.decrypt(encrypted)
    with open(filename, 'wb') as decrypt_file:
        decrypt_file.write(decrypted)

# ---------- end of encrypting file ------------

# ---------- starting of encrypting any file - audio, video and image -----------


def encryptMiscFile():
    while(True):
        miscFilePath = (simpledialog.askstring(
            'Image Path', 'Enter path of audio/video/image file: \n'))
        valid = re.search(".*(jpeg|jpg|gif|png|mp4|flac)$", miscFilePath)
        if(valid and os.path.isfile('./' + miscFilePath)):
            break
        else:
            messagebox.showinfo(
                "Error", "Invalid File Name or file does not exist")

    MiscEncryptionKey = (simpledialog.askinteger(
        'Key', 'Enter your encryption key: '))

    fin = open(miscFilePath, 'rb')
    MiscFile = fin.read()
    fin.close()

    MiscFile = bytearray(MiscFile)

    for index, values in enumerate(MiscFile):
        MiscFile[index] = values ^ MiscEncryptionKey

    fin = open(miscFilePath, 'wb')
    fin.write(MiscFile)
    fin.close()

# -------- end of encrypting any file -------------


if __name__ == "__main__":
    window = Tk()
    window.withdraw()

    Reply = True
    while Reply:
        try:
            while(True):
                choice = (simpledialog.askstring(
                    'What to do?', "Type 'text' to encrypt a text-file, 'message' to encrypt a text message, 'misc' to encrypt an image/audio/video file, 'exit' to exit: \n")).lower()
                if(choice == 'text' or choice == 'message' or choice == 'misc' or choice == 'exit'):
                    break
                else:
                    messagebox.showinfo(
                        "Error", "Invalid choice")
            if (choice == 'text'):
                encryptTextFile()
            elif (choice == 'message'):
                encryptMessage()
            elif(choice == 'misc'):
                encryptMiscFile()
        except Exception:
            pass
        Reply = messagebox.askquestion('Continue?', "Do you want to Exit? ")
        if Reply.lower() == 'yes':
            Reply = False
