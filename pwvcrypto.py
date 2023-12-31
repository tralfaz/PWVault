import base64
import hashlib
import json

# cryptography
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken



class PWVCryptoExc(Exception):
    INVALID_TOKEN = 1
        
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


def DecryptFile(keyPath, srcPath, tgtPath):
    # opening the key
    with open(keyPath, 'rb') as filekey:
        key = filekey.read()

    # using the key
    fernet = Fernet(key)

    # opening the encrypted file
    with open(srcPath, 'rb') as srcFP:
        encrypted = srcFP.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open(tgtPath, 'wb') as tgtFP:
        tgtFP.write(decrypted)


def EncryptFile(keyPath, srcPath, tgtPath):
    # opening the key
    with open(keyPath, 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(srcPath, 'rb') as srcFP:
        original = srcFP.read()
    with open(srcPath, 'rb') as srcFP:
        original = srcFP.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(tgtPath, 'wb') as tgtFP:
        tgtFP.write(encrypted)

def DecryptStrToStr(encKey, srcStr):
    cypher = Fernet(encKey)
    srcBuf = srcStr.encode("utf-8")
    try:
        encBuf = cypher.decrypt(srcBuf)
    except InvalidToken as decx:
        print("DECX: ", decx)
        print("DECX: ", repr(dir(decx)))
        raise PWVCryptoExc("Bad decryption key", PWVCryptoExc.INVALID_TOKEN)
    return encBuf.decode("utf-8")

def EncryptStrToStr(encKey, srcStr):
    cypher = Fernet(encKey)
    srcBuf = srcStr.encode("utf-8")
    encBuf = cypher.encrypt(srcBuf)
    return encBuf.decode("utf-8")
    
    
def GenerateKey(keyPath=None):
    if not keyPath:
        keyPath = 'filekey.key'

    # key generation
    key = Fernet.generate_key()

    if keyPath:
        # write string key to file
        with open(keyPath, 'wb') as keyFP:
            keyFP.write(key)
    return key


def JSONDecryptFile(keyPath, srcPath, tgtPath):
    # opening the key
    with open(keyPath, 'rb') as filekey:
        key = filekey.read()

    # using the key
    fernet = Fernet(key)

    # opening the JSON file with encrypted value
    with open(srcPath, "r") as srcFP:
        jsonObj = json.load(srcFP)

    # Get ENCODED key value string, convert byte buffer
    encstr = jsonObj.get("ENCODED")
    encrypted = encstr.encode("utf-8")

    # decrypting value
    decrypted = fernet.decrypt(encrypted)

    # write decrypted value to target file
    with open(tgtPath, 'wb') as tgtFP:
        tgtFP.write(decrypted)



def JSONEncryptFile(keyPath, srcPath, tgtPath):
    # opening the key
    with open(keyPath, 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(srcPath, 'rb') as srcFP:
        original = srcFP.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)
    print(f"ENCRYPTED: {repr(encrypted)}")
    
    # Create JSON object
    encdstr = encrypted.decode("utf-8")
    jsonObj = {
        "FOO": "BAR",
        "ENCODED": encdstr
        }

    with open(tgtPath, "w") as tgtFP:
        json.dump(jsonObj, tgtFP, indent=4)


def MakePasswordKey(pswd):
    pswd = pswd.encode("utf-8")
    m = hashlib.sha3_384(b"utf-17")
    hlen = 0
    while hlen < 64:
        m.update(pswd)
        hlen += len(pswd)
    hash = m.digest()
    key = base64.urlsafe_b64encode(hash[0:32])
    return key


def PasswordEncodeFile(pswd, tgtPath):
    pwkey = MakePasswordKey(pswd)
    cypher = Fernet(pwkey)

    with open(tgtPath, 'rb') as tgtFP:
        origBytes = tgtFP.read()
    print(f"pswd={pswd} len orig={len(origBytes)}")

    encBytes = cypher.encrypt(origBytes)

    with open(tgtPath, 'wb') as tgtFP:
        tgtFP.write(encBytes)


def PasswordDecodeFile(pswd, tgtPath):
    pwkey = MakePasswordKey(pswd)
    cypher = Fernet(pwkey)

    with open(tgtPath, 'rb') as tgtFP:
        origBytes = tgtFP.read()

    encBytes = cypher.decrypt(origBytes)

    with open(tgtPath, 'wb') as tgtFP:
        tgtFP.write(encBytes)




if __name__ == "__main__":
    import sys

    argc = len(sys.argv)
    argx = 1
    while argx < argc:
        arg = sys.argv[argx]
        #print(f"argx={argx} arg={arg}")

        if arg == "keygen":
            # keygen {keypath}
            keyPath = None
            if argc > argx+1:
                argx += 1
                keyPath = sys.argv[argx]
            key = GenerateKey(keyPath)
            print(f"KEY: {repr(key)}")
            
        elif arg == "encrypt":
            # encrypt {keyPath} {srcPath} [tgtPath]
            if argc > argx+2:
                keyPath = sys.argv[argx+1]
                srcPath = sys.argv[argx+2]
                tgtPath = srcPath
                argx += 2
            else:
                print(f"Error: encrypt command missing required arguments")
            if argc > argx+1:
                tgtPath = sys.argv[argx+1]
                argx += 1
            EncryptFile(keyPath, srcPath, tgtPath)

        elif arg == "decrypt":
            # decrypt {keyPath} {srcPath} [tgtPath]
            if argc > argx+2:
                keyPath = sys.argv[argx+1]
                srcPath = sys.argv[argx+2]
                tgtPath = srcPath
                argx += 2
            else:
                print(f"Error: decrypt command missing required argemnts")
            if argc > argx+1:
                tgtPath = sys.argv[argx+1]
                argx += 1
            DecryptFile(keyPath, srcPath, tgtPath)

        elif arg == "jsondec":
            # jsondec {keyPath} {srcPath} [tgtPath]
            if argc > argx+2:
                keyPath = sys.argv[argx+1]
                srcPath = sys.argv[argx+2]
                tgtPath = srcPath
                argx += 2
            else:
                print(f"Error: jsondec command missing required arguments")
            if argc > argx+1:
                tgtPath = sys.argv[argx+1]
                argx += 1
            JSONDecryptFile(keyPath, srcPath, tgtPath)

        elif arg == "jsonenc":
            # encrypt {keyPath} {srcPath} [tgtPath]
            if argc > argx+2:
                keyPath = sys.argv[argx+1]
                srcPath = sys.argv[argx+2]
                tgtPath = srcPath
                argx += 2
            else:
                print(f"Error: encrypt command missing required arguments")
            if argc > argx+1:
                tgtPath = sys.argv[argx+1]
                argx += 1
            JSONEncryptFile(keyPath, srcPath, tgtPath)

        elif arg == "mkpwkey":
            pswd = input("Password: ")
            key = MakePasswordKey(pswd)
            print(f"Key: {key}")

        elif arg == "pwencode":
            if argc > argx+1:
                tgtPath = sys.argv[argx+1]
                argx += 1
            else:
                tgtPath =  input("Filename: ")
            pswd = getpass.getpass("Password: ")
            PasswordEncodeFile(pswd, tgtPath)

        elif arg == "pwdecode":
            if argc > argx+1:
                tgtPath = sys.argv[argx+1]
                argx += 1
            else:
                tgtPath =  input("Filename: ")
            pswd = getpass.getpass("Password: ")
            PasswordDecodeFile(pswd, tgtPath)

        else:
            print(f"Unknown command: {arg}")
            sys.exit(1)

        argx += 1
