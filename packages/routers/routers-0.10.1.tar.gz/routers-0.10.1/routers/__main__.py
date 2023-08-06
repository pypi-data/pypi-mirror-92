from argparse import ArgumentParser
import os
from routers.tplink.tlw840n import TLWR840N


parser = ArgumentParser(description = "ROUTERS")


parser.add_argument('-f','--fabricator', help='fabricator name',type=str)
parser.add_argument('-m','--model',help='router name',type=str)
parser.add_argument('-u','--user', help='router user',type=str)
parser.add_argument('-p','--password', help="router password",type=str)
parser.add_argument('-o','--option', help="choose what run function (int or 'list')")
parser.add_argument('-c','--config', help="params config function",nargs="*")
parser.add_argument('-listf',help='list all fabricators',action="store_true")
parser.add_argument('-listm',help='list all router',action="store_true")


args = parser.parse_args()

FABRICATORS = {
    "tplink": ["tlw840n"]
}


def listf():
    for fabricator in FABRICATORS:
        print(fabricator)

    

def listm():
    print("=====================begin router fabricator {fabricator} =====================".format(fabricator = args.fabricator)) 
    for model in FABRICATORS[args.fabricator]:
        print(model)    
    print("=====================end=====================") 

def run_command(args):
    
    fabricator = args.fabricator
    user = args.user
    password = args.password
    model = args.model
    option = args.option
    config = args.config

    command = {
        "tplink": {
            "tlw840n": {
                "1": TLWR840N(user,password).config_ntp,
                "2": TLWR840N(user,password).security_remote_manage,
                "3": TLWR840N(user,password).wifi_basic_configuration,
                "4": TLWR840N(user,password).wifi_security_wireless,
                "help": TLWR840N("","").help
            }
        }
    }
    
    

    try:
        command[fabricator][model][option](config)
    except:
        print("command not found")



if args.listf:
    listf()
elif args.listm:
    listm()
else:   
    run_command(args)

