import psutil
import os
import sys
import yaml
import ctypes
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

def get_running_processes():
    processes = set()
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name']:
                proc.cpu_affinity()
                processes.add(proc.info['name'])
        except:
            continue
    return [Choice(name) for name in sorted(list(processes))]

def updateyaml():
     with open("config.yaml", "w") as f:
         yaml.safe_dump(configurations, f, sort_keys=False, default_flow_style=False)

def exit():
    input("Press Enter to exit...")
    sys.exit()

def program():
    targetf = False
    affinity = ''

    involved = 0
    fail_noperms = 0
    fail_nosuch = 0
    fail_noreason = 0
    processes = psutil.process_iter(['pid', 'name', 'exe'])
    for proc in processes:
        try: 
            if proc.info['name'] == configurations["target"]["process"]:
                targetf = True
                affinity = psutil.Process(proc.info['pid']).cpu_affinity()
        except:
            continue

    processes = psutil.process_iter(['pid', 'name', 'exe'])
    for proc in processes:
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            if pid == 0 or pid == os.getpid():
                continue
            if configurations["target"]["process"] == name and targetf == True and not affinity == configurations["target"]["affinity"]: # Apply to all
                psutil.Process(pid).cpu_affinity(configurations["target"]["affinity"])
            elif targetf == True and affinity == configurations["target"]["affinity"]: # Restore
                psutil.Process(pid).cpu_affinity(list(range(psutil.cpu_count())))
            elif not configurations["target"]["process"] == name and targetf == True:
                psutil.Process(pid).cpu_affinity(configurations["others"]["affinity"])

            involved += 1
        except psutil.AccessDenied:
            fail_noperms += 1
        except psutil.NoSuchProcess:
            fail_nosuch += 1
        except:
            fail_noreason += 1
            continue

    if involved == 0:
        print("[-] Target process not found. No changes made.")
    if involved > 0 and targetf == True:
        if affinity == configurations["target"]["affinity"]:
            print(f"[+] Restored: {involved} processes to full CPU")
        else:
            print(f"[+] Applied to {involved} process")
            print(f"Target Process modified: 1 {configurations["target"]["process"]}")
            print(f"Normal Processes modified: {involved - 1}")
            
        print(f"\n[-] Failed ")
        print(f"{fail_noperms} of no permission to apply")
        print(f"{fail_nosuch} of process terminated")
        print(f"{fail_noreason} of other reason")
    exit()
def startup():
    setup()
    if configurations["admin"] == "Always yes":
        restart_uac()
    elif configurations["admin"] == "Always ask":
        if inquirer.confirm(message="Run this program as admin?", default=False).execute():
            restart_uac()
    program()

def restart_uac():
    if not bool(ctypes.windll.shell32.IsUserAnAdmin()):
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        if result <= 32:
            print("Starting as admin failed.")
        sys.exit()

def setup():
    global configurations
    if not os.path.exists("config.yaml"):
        with open("config.yaml", "w") as f:
            pass
    with open("config.yaml", "r") as f:
        configurations = yaml.safe_load(f)
    if configurations is None:
        configurations = {}
        configurations["setup"] = False
    if configurations.get("setup") == False:
        if configurations.get("admin") == "Always yes":
            restart_uac()
        if configurations.get("tutorial") != "completed":
            welcome = inquirer.confirm(message="Welcome to setup, in this process we will be configuring how this app works.\nPress enter to continue", default=True).execute()
            tutorial = inquirer.confirm(message="Tutorial of how to use this app.\n 1. Use arrow up/down to move between selections\n 2. Press enter to confirm selections\n 3. In checkboxes, use space to select, use enter to confirm\nPress enter to continue.", default=True).execute()
            if tutorial : configurations["tutorial"] = "completed"
            updateyaml()

        if "target" not in configurations:
            configurations["target"] = {}
        if "others" not in configurations:
            configurations["others"] = {}
            
        os.system('cls')
        if not "admin" in configurations:
            admin=inquirer.select(
                message="Step 1: Should this program run as admin?\n  Running as admin/administrator gains more permission better affinity control.",
                choices=["Always yes", "Always no", "Always ask"],
                default="Always no"
            ).execute()
            configurations["admin"] = admin
            updateyaml()

            if admin == "Always yes":
                restart_uac()
            elif admin == "Always ask":
                ans = inquirer.confirm(message="Run this program as admin?", default=False).execute()
                if ans:
                    restart_uac()
        else:
            os.system('cls')
            print("Continue setup :")

        configurations["target"]["process"]=inquirer.fuzzy(
                    message="Step 1: Select process to prioritize: ",
                    choices=get_running_processes(),
                    match_exact=False,
        ).execute()

        configurations["target"]["affinity"]=inquirer.checkbox(
            message="Step 2: Select affinity for prioritized process",
            choices=list(range(round(psutil.cpu_count() * 1))),
            validate=lambda result: len(result) >= 1,
            invalid_message="select at least one",
            instruction=f"\nRecommended {list(range(round(psutil.cpu_count() * 0.6)))} ",
        ).execute()

        configurations["others"]["affinity"]=inquirer.checkbox(
            message="Step 3: Select affinity for other process",
            choices=list(range(round(psutil.cpu_count() * 1))),
            validate=lambda result: len(result) >= 1,
            invalid_message="Select at least one",
            instruction=f"\nRecommended {list(range(round(psutil.cpu_count() * 1)))[round(len(list(range(round(psutil.cpu_count())))) * 0.6):]} ",
        ).execute()

        os.system('cls')
        print("Saving settings to config file ( config.yaml )")
        configurations["setup"] = True
        updateyaml()
        



def main():
    os.system('cls')
    startup()    
if __name__ == "__main__":
    main()