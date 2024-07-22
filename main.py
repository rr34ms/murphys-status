import webbrowser
import os
webbrowser.open("https://discord.gg/vyr27Hnnxc")
try:
    import requests
    import time
    import json
    from datetime import datetime
    from tqdm import tqdm
    from colorama import Fore, Style, init
    from pystyle import Colorate, Colors
except ImportError:
    os.system('pip install requests')
    os.system('datetime')
    os.system('tqdm')
    os.system('colorama')
    os.system('pystyle')
    import requests
    import time
    import json
    from datetime import datetime
    from tqdm import tqdm
    from colorama import Fore, Style, init
    from pystyle import Colorate, Colors

init(autoreset=True)

def timestamp():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def sprint(message, type):
    if type == "One":
        print(f"{Fore.RESET}{timestamp()} [{Style.BRIGHT}{Fore.GREEN}+{Fore.RESET}] {message}")
    elif type == "Two":
        print(f"{Fore.RESET}{timestamp()} [{Style.BRIGHT}{Fore.RED}-{Fore.RESET}] {message}")
    elif type == "Zero":
        print(f"{Fore.RESET}{timestamp()} [{Style.BRIGHT}{Fore.YELLOW}-{Fore.RESET}] {message}")

print(Colorate.Horizontal(Colors.rainbow, """
███╗   ███╗██╗   ██╗██████╗ ██████╗ ██╗  ██╗██╗   ██╗███████╗    ███████╗████████╗ █████╗ ████████╗██╗   ██╗████████╗███████╗
████╗ ████║██║   ██║██╔══██╗██╔══██╗██║  ██║╚██╗ ██╔╝██╔════╝    ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║   ██║╚══██╔══╝██╔════╝
██╔████╔██║██║   ██║██████╔╝██████╔╝███████║ ╚████╔╝ ███████╗    ███████╗   ██║   ███████║   ██║   ██║   ██║   ██║   ███████╗
██║╚██╔╝██║██║   ██║██╔══██╗██╔═══╝ ██╔══██║  ╚██╔╝  ╚════██║    ╚════██║   ██║   ██╔══██║   ██║   ██║   ██║   ██║   ╚════██║
██║ ╚═╝ ██║╚██████╔╝██║  ██║██║     ██║  ██║   ██║   ███████║    ███████║   ██║   ██║  ██║   ██║   ╚██████╔╝   ██║   ███████║
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝    ╚═════╝    ╚═╝   ╚══════╝
                          
                          discord.gg/vyr27Hnnxc
"""))

def load_config():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print(Colorate.Horizontal(Colors.red_to_blue, "\nFichier de configuration introuvable.\n\n"))
        return None

def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

config = load_config()
if config is None:
    num_statuts = int(input("Entrez le nombre de statuts que vous souhaitez alterner : "))
    while num_statuts <= 0:
        print("Veuillez entrer un nombre de statuts supérieur à zéro.")
        num_statuts = int(input("Entrez le nombre de statuts que vous souhaitez alterner : "))

    status = []
    for i in range(num_statuts):
        statut = input(f"Entrez le statut {i+1} : ")
        status.append(statut)

    interval = int(input("Entrez l'intervalle de temps entre chaque changement de statut (en secondes, minimum 5) : "))
    while interval < 5:
        print("L'intervalle de temps doit être d'au moins 5 secondes.")
        interval = int(input("Entrez l'intervalle de temps entre chaque changement de statut (en secondes, minimum 5) : "))
    
    token = input("Renseignez le token discord du compte sur lequel vous voulez modifier le statut :")

    config = {"status": status, "interval": interval, "token": token}
    save_config(config)
else:
    print(Colorate.Horizontal(Colors.red_to_blue, "\nFichier de configuration chargé avec succès.\n\n\n"))

status = config["status"]
interval = config["interval"]
token = config["token"]

started_token = token[:5] + '*' * 6

url = "https://discord.com/api/v9/users/@me/settings"
headers = {
    "Authorization": token,
}

uri = "https://discord.com/api/v9/users/@me"
header = {
    "Authorization": token,
    "Content-Type": "application/json"
}
rep = requests.get(uri, headers=header)
data = rep.json()
global_name = data.get('username')

while True:
    for stat in status:
        payload = {"custom_status": {"text": stat}}
        try:
            response = requests.patch(url, headers=headers, json=payload)
            if response.status_code == 200:
                sprint(f"Account : {Fore.RED}{started_token} {Fore.RESET}({Fore.RED}{global_name}{Fore.RESET}) | Status : {Fore.CYAN}{stat}{Fore.RESET}", "Zero")
            else:
                sprint(response.text, "Two")
        except Exception as e:
            sprint(str(e), "Two")
        time.sleep(interval)
