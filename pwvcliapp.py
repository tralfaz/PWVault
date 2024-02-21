import getpass 
import re
import sys
    
from pwvdoc import PWVDoc
from pwvdoc import PWVKey
from pwvdoc import PWVDocExc


def FormatEntry(entry, opts):
    entID   = entry.get("ID")
    entURL  = entry.get("URL")
    entUSER = entry.get("USER")
    entPSWD = entry.get("PSWD")

    fields = opts.get("fields")

    if "id" in fields:
        print(f"ID:   {entID}")
    if "url" in fields:
        print(f"URL:  {entURL}")
    if "user" in fields:
        print(f"USER: {entUSER}")
    if "pswd" in fields:
        print(f"PSWD: {entPSWD}")
    if "notes" in fields:
        print(f"NOTES:\n{entry.get(PWVKey.NOTES, '')}")
    print()
    

def Usage(errmsg):
    if errmsg:
        print(f"{errmsg}\n")

    print("""Usage

PWVault [--help] [options] pwvpath

Where pwvpath is a file path to a PWVault file.

[options] are:
    
    --idfilter {regex}
    Filter the displayed entries with ID fields matching the supplied regular
    expression.

    --fields {id,url,user,pswd,notes,all}
    Selects the fields to display for each selected entry.  Multiple field
    names must be separated by commas.  The special field name all selects
    all fields in the entrty.  The default fields are id,url.
""")

    if errmsg:
        sys.exit(1)

        
optPwvpath = None
optFields  = ["id", "url"]
optIdFilter = None

    
def ParseArgs(argv):
    opts = { "pwvpath": None,
             "fields": ["id","url"],
             "idfilter": None }

    argc = len(argv)
    argx = 1
    while argx < argc:
        arg = argv[argx]
        if arg == "--fields":
            optFields = []
            if argx < argc-2:
                argx += 1
                validFields = ["id", "url", "user", "pswd", "notes", "all"]
                optFields = argv[argx].split(",")
                for fld in optFields[:]:
                    print(f"FLD: {fld}")
                    if fld not in validFields:
                        Usage(f"{fld} is not a valid field selector")
                    elif fld == "all":
                        optFields = ["id", "url", "user", "pswd", "notes"]
                    else:
                        optFields.append(fld)
                opts["fields"] = optFields
            else:
                Usage("Missing pattern regex for --idfilter argument")

        elif arg == "--idfilter":
            if argx < argc-2:
                argx += 1
                regex = argv[argx]
                try:
                    opts["idfilter"] = re.compile(regex)
                except re.error as rex:
                    Usage(f"ERROR: Bad --idfilter regex {rex}")
            else:
                Usage("Missing pattern regex for --idfilter argument")

        elif arg == "--help":
            Usage(None)
            sys.exit(0)

        elif argx == argc-1 and arg[:1] != "-":
            opts["pwvpath"] = arg

        else:
             Usage("ERROR: Invalid option: {repr(arg)}")

        argx += 1

    return opts


def CLIMain(argv):
    opts = ParseArgs(argv)

    pwvpath = opts.get("pwvpath")
    if not pwvpath:
        Usage("pwvpath is not specified")

    pwvDoc = PWVDoc()
    pwvDoc.openDoc(pwvpath)

    if pwvDoc.encoded():
        pswd = getpass.getpass("Password: ")
        if pswd:
            status = pwvDoc.decrypt(pswd)
            if status != "OK":
                print("Bad Password: {status}")
                sys.exit(1)

    idFilter = opts.get("idfilter")
    for entry in pwvDoc.entries():
        if idFilter and idFilter.search(entry.get(PWVKey.ID, "")):
            FormatEntry(entry, opts)
        elif not idFilter:
            FormatEntry(entry, opts)


if __name__ == "__main__":
    CLIMain(sys.argv)
