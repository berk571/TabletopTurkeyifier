import requests
import json
import os
from sys import exit

from util import download_with_progress, get_file_properties
from localization import print_localized


def update_app(current_version):

    # get latest version from github api
    try:
        r = requests.get('https://api.github.com/repos/seyahdoo/TabletopTurkeyifier/releases/latest')
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print_localized("problem_checking_new_version")
        return False

    if r.ok:
        # parse json api data
        latest_release = json.loads(r.text or r.content)

        # if there is a newer version or we are in production
        if latest_release["tag_name"] is not current_version and current_version is not "development":
            print_localized("updating")

            exec_name = None
            # download all it's assets
            for asset in latest_release["assets"]:
                download_with_progress(asset["browser_download_url"], asset["name"])
                if asset["name"].endswith(".exe"):
                    exec_name = asset["name"]

            # start new version and exit program
            if exec_name is not None:
                print_localized("starting_new_version")
                os.startfile(exec_name)
                exit(0)
            else:
                print_localized("problem_downloading_new_ver")
                return False

        else:
            # Delete old versions if exists in same folder
            for filename in os.listdir():
                props = get_file_properties(filename)
                app_name = None
                try:
                    app_name = props["StringFileInfo"]["ProductName"]
                except:
                    pass

                prod_ver = None
                try:
                    prod_ver = props["StringFileInfo"]["ProductVersion"]
                except:
                    pass

                if filename.startswith("tabletop-turkeyifier") or app_name == "Tabletop Turkeyifier":
                    if prod_ver is not None:
                        if prod_ver < current_version:
                            print_localized("deleting_old_ver")
                            with open(filename, 'w'):
                                pass
                            os.remove(filename)
                            return True
                    else:
                        if filename[-9:-4] < current_version:
                            print_localized("deleting_old_ver")
                            with open(filename, 'w'):
                                pass
                            os.remove(filename)
                            return True

    return False

