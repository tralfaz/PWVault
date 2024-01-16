import argparse
import getpass 
import sys

from pwvdoc import PWVDoc
from pwvdoc import PWVDocExc


def FormatEntry(entry, args):
    entID   = entry.get("ID")
    entURL  = entry.get("URL")
    entUSER = entry.get("USER")
    entPSWD = entry.get("PSWD")
    print(f"ID:   {entID}")
    print(f"URL:  {entURL}")
    print(f"USER: {entUSER}")
    print(f"PSWD: {entPSWD}")
    print()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PWVault")
#    parser.add_argument("--id", dest="idPattern",

#    parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                        help='an integer for the accumulator')
#    parser.add_argument('--sum', dest='accumulate', action='store_const',
#                        const=sum, default=max,
#                        help='sum the integers (default: find the max)')

    parser.add_argument("--fields", choices=["id","url","user","pswd","notes"],
                        nargs="+")
    parser.add_argument("--id", dest="idpat",
                        help="limit output to entries matching ID pattern")
    parser.add_argument("pwvpath", type=str, nargs=1,
                        help="Path to PWVault file")

    args = parser.parse_args()
#    print(args.accumulate(args.integers))
    print(f"PATH: {args.pwvpath}")
    print(f"IDPAT: {args.idpat}")
    print(f"FIELDS: {args.fields}")

    if args.pwvpath:
        pwvDoc = PWVDoc()
        pwvDoc.openDoc(args.pwvpath[0])

        if pwvDoc.encoded():
            pswd = getpass.getpass("Password: ")
            if pswd:
                status = pwvDoc.decrypt(pswd)
                print(f"Decrypt status: {status}")
                if status != "OK":
                    print("Bad Password: {status}")
                    sys.exit(1)

                print(f"ENTRY COUNT: {len(pwvDoc.entries())}")
                for entry in pwvDoc.entries():
                    FormatEntry(entry, args)
