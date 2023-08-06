from argparse import ArgumentParser
import os
from routers.tplink.tlw840n import TLWR840N


def listf():
    PATH_FABRICATOR = os.path.join(os.path.realpath(""),"routers")
    for fabricator in os.listdir(PATH_FABRICATOR):
       print(fabricator) 

def listm():
    PATH_FABRICATOR = os.path.join(os.path.realpath(""),"routers")
    for fabricator in os.listdir(PATH_FABRICATOR):
        print("=====================begin router fabricator {fabricator} =====================".format(fabricator = fabricator)) 
        for model in os.listdir(os.path.join(os.path.realpath(""),"routers",fabricator)):
            if model != "__pycache__":
                print(model.replace(".py",""))
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
    
    

    command[fabricator][model][option](config)


parser = ArgumentParser(description = "ROUTERS")


parser.add_argument('-f','--fabricator', help='fabricator name',type=str,required=True)
parser.add_argument('-m','--model',help='router name',type=str,required=True)
parser.add_argument('-u','--user', help='router user',type=str)
parser.add_argument('-p','--password', help="router password",type=str)
parser.add_argument('-o','--option', help="choose what run function (int or 'list')")
parser.add_argument('-c','--config', help="params config function",nargs="*")
parser.add_argument('-listf',help='list all fabricators',action="store_true")
parser.add_argument('-listm',help='list all router',action="store_true")


args = parser.parse_args()

if args.listf:
    listf()
elif args.listm:
    listm()
else:   
    run_command(args)

