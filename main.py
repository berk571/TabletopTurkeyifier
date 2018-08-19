from tkinter import Tk
from tkinter import filedialog
import os
import shutil


def get_root_path():
    path = os.path.expanduser("~/Documents/My Games/Tabletop Simulator/")
    while True:
        if os.path.isdir(path + "/Mods"):
            break
        elif path == "":
            print("No folder selected, exiting program.")
            exit(0)
        else:
            print(
                "You must show the folder inside Documents "
                "named \"Tabletop Simulator\" with \"Mods\" folder inside it."
            )

        root = Tk()
        root.withdraw()
        path = filedialog.askdirectory(
            initialdir='~/Documents/My Games/Tabletop Simulator',
            title='Choose root of Tabletop Simulator Mods folder.'
        )
    return path


def do_backup(file_path):
    if not os.path.isdir(file_path + "BACKUP"):
        print("No Backup Found: Backing up to -> " + file_path + "BACKUP")
        shutil.copytree(file_path, file_path + "BACKUP")


def inplace_change(file_path, old_string, new_string):
    with open(file_path, 'r', encoding='utf8', errors='ignore') as f:
        s = f.read()
        if old_string not in s:
            return
    with open(file_path, 'w', encoding='utf8') as f:
        s = s.replace(old_string, new_string)
        f.write(s)


def replace_mod_files(file_path):
    # Replace http imgur and pastebin links to https
    json_files = [pos_json for pos_json in os.listdir(file_path) if pos_json.endswith('.json')]
    for file_name in json_files:
        inplace_change(file_path + file_name, "http://imgur.com", "https://imgur.com")
        inplace_change(file_path + file_name, "http://i.imgur.com", "https://i.imgur.com")
        inplace_change(file_path + file_name, "http://pastebin.com", "https://pastebin.com")


def rename_downloaded_files(file_path):
    for filename in os.listdir(file_path):
        dst = filename
        dst = dst.replace("httpimgurcom", "httpsimgurcom")
        dst = dst.replace("httppastebincom", "httpsiimgurcom")
        dst = dst.replace("httpiimgurcom", "httpsiimgurcom")

        src = file_path + filename
        dst = file_path + dst

        if src != dst:
            if not os.path.isfile(dst):
                os.rename(src, dst)


if __name__ == "__main__":

    print("Getting root mods path")
    root_path = get_root_path()
    print("Got root mods path")

    print("Backing up intial data")
    do_backup(root_path + "/Mods/Workshop")
    do_backup(root_path + "/Saves")

    print("Turkeyifying json mod files")
    replace_mod_files(root_path + "/Mods/Workshop/")
    replace_mod_files(root_path + "/Saves/")

    print("Fixing previously downloaded Image and Model cache")
    rename_downloaded_files(root_path + "/Mods/Images/")
    rename_downloaded_files(root_path + "/Mods/Models/")

    print("DONE!")

    input("Press Enter to continue...")

