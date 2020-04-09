from cryptography.fernet import Fernet

key = "DbMMQtBeJvVtB-QU21FCLpVuDyTxWEEPPdxYum4PSzs="
systeminfo_enc = 'sysinfo_enc.txt'
clipboardinfo_enc = 'clipboard_enc.txt'
keylogs_enc = 'keylogs_enc.txt'



encrypted_files = [systeminfo_enc, clipboardinfo_enc, keylogs_enc]
count = 0


for decrypting_files in encrypted_files:

    with open(encrypted_files[count], 'rb') as file:
        data = file.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as file:
        file.write(decrypted)

    count += 1
