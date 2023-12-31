import json
import os.path

from pwvcrypto import DecryptStrToStr
from pwvcrypto import EncryptStrToStr
from pwvcrypto import MakePasswordKey
from pwvcrypto import PWVCryptoExc


class PWVKey(object):
    ENCODED  = "ENCODED"
    ENTRIES  = "ENTRIES"
    ID       = "ID"
    MAGIC    = "PWVDOC"
    MAJOR    = "MAJOR"
    MINOR    = "MINOR"
    NOTES    = "NOTES"
    PSWD     = "PSWD"
    REVISION = "REVISION"
    URL      = "URL"
    USER     = "USER"
    VERSION  = "VERSION"


class PWVDocExc(Exception):
    INVALID_JSON = 1
    MISSING_VERSION = 2
    BAD_MAGIC    = 3
        
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code
        

class PWVDoc(object):
    
    def __init__(self, path=None):
        super().__init__()
        
        self._path = path
        self._docObj = {
          PWVKey.VERSION : {
            PWVKey.ID : PWVKey.MAGIC,
            PWVKey.MAJOR:    1,
            PWVKey.MINOR:    0,
            PWVKey.REVISION: 0
            },
          PWVKey.ENTRIES : []
        }

        self._modified = False
        
    def appendEntries(self, entries):
        docEnts = self.entries()
        if type(entries) is list:
            docEnts.extend(entries)
        else:
            docEnts.append(entries)
        self.setModified(True)

    def decrypt(self, pswd):
        if not self.isEncrypted():
            return ("ERROR", "Document not encrypted")

        try:
            encoded = self.encoded()
        except KeyError as keyx:
            return ("ERROR", "Nothing to decode")

        pswdKey = MakePasswordKey(pswd)
        pswd = None

        try:
            decEntStr = DecryptStrToStr(pswdKey, encoded)
        except PWVCryptoExc as decx:
            return ("ERROR", "Bad password")

        entObj = json.loads(decEntStr)
        print("ENT OBJ", repr(entObj))
        
        self._docObj[PWVKey.ENTRIES] = entObj
        self._docObj.pop(PWVKey.ENCODED)
        return "OK"
        
    def encrypt(self, pswd):
        encoded = self._docObj.get(PWVKey.ENCODED)
        if encoded:
            return ("ERROR", "Already encoded")
        try:
            entries = self._docObj.pop(PWVKey.ENTRIES)
        except KeyError as keyx:
            return ("ERROR", "No entries")

        jsonEntStr = json.dumps(entries, indent=4)

        pswdKey = MakePasswordKey(pswd)
        pswd = None

        encEntStr = EncryptStrToStr(pswdKey, jsonEntStr)

        self._docObj[PWVKey.ENCODED] = encEntStr
        return "OK"
        
    def encoded(self):
        if self._docObj:
            return self._docObj.get(PWVKey.ENCODED)
        return None

    def entries(self):
        if self._docObj:
            return self._docObj.get(PWVKey.ENTRIES)
        return None

    def fileName(self):
        if self._path:
            return os.path.basename(self._path)
        return self._path
            
    def insertEntries(self, index, entries):
        docEntries = self.entries()
        docEntries[:index] + entries + docEntries[index:]
        self._docObj[PWVKey.ENTRIES] = docEntries
        self.setModified(True)
        
    def isEncrypted(self):
        if not self.entries() and self.encoded():
            return True
        return False

    def modified(self):
        return self._modified

    def newEntry(self):
        nents = len(self.entries())
        entry = {
            PWVKey.ID : f"Entry-{nents}",
                PWVKey.URL: f"url - {nents}",
                PWVKey.USER : f"user - {nents}",
                PWVKey.PSWD : f"pswd - {nents}",
                PWVKey.NOTES: f"This is note {nents}"
            }
        return entry
        
    def openDoc(self, path=None):
        if path is None:
            path = self._path
        else:
            self._path = path
        
        self._loadDocJSON()
        self.setModified(False)

    def path(self):
        return self._path

    def saveDocAs(self, path):
        with open(path, "w") as docFP:
            json.dump(self._docObj, docFP, indent=4)
            self._path = path
            
    def setDocObject(self, docObj):
        self._docObj = docObj

    def setModified(self, changed):
        self._modified = changed

    def _loadDocJSON(self):
        self._docObj = None
        with open(self._path, "r") as docFP:
            self._docObj = json.load(docFP)

        if self._docObj:
            verObj = self._docObj.get(PWVKey.VERSION)
            if not verObj:
                raise PWVDocExc("No PWV Verion Marker",
                                PWVDoc.MISSING_VERSION)
            if verObj and verObj.get(PWVKey.ID) != PWVKey.MAGIC:
                raise PWVDocExc("Bad Magic Document Key Value",
                                PWVDocExc.BAD_MAGIC)
        

if __name__ == "__main__":
    pwvDoc = {
  PWVKey.VERSION : {
        PWVKey.ID : PWVKey.MAGIC,
        PWVKey.MAJOR:    1,
        PWVKey.MINOR:    0,
        PWVKey.REVISION: 0
        },

  PWVKey.ENTRIES : [

    {
      "ID": "Entry1",
      "URL" : "https://www.python.org/",
      "USER" : "tralfaz1",
      "PSWD" : "pswd1111",
      "NOTES" : {
        "SQ1" : ["Favorite color", "blue"],
        "SQ2" : ["Favorite number", "64" ]
      }
    },

    {
      "ID" : "Entry2",
      "URL" : "https://www.google.com/",
      "USER" : "Tralfaz2",
      "PSWD" : "PSWD2222",
      "NOTES" : {
        "SQ1" : ["Favorite Food", "Gnochi" ],
        "SQ2" : ["Favorite Bone", "Ulna" ]
      }
    }
  ]
}

    print(pwvDoc.keys())
    docVers = pwvDoc.get("Version")
    print("PWVDOC Version: %r" % docVers)

    docEnts = pwvDoc.get("Entries", [])
    for pwvEnt in docEnts:
        print(f"ID: {pwvEnt['ID']}")
        print(f"    URL: {pwvEnt['URL']}")
        print(f"    USER: {pwvEnt['USER']}")
        print(f"    PSWD: {pwvEnt['PSWD']}")
        entNotes = pwvEnt.get("NOTES", {})
        print("    NOTES")
        for key, val in entNotes.items():
            print(f"        {key} : {val} ")
        print()

    print(json.dumps(pwvDoc, indent=4))

    docFP = open("pwvdoc.json", "w")
    json.dump(pwvDoc, docFP, indent=4)
    docFP.close()

    docFP = open("pwvdoc.json", "r")
    docOBJ = json.load(docFP)
    print("=================")
    print(repr(docOBJ))
    print("=================")


    savePath = input("Save Path: ")
