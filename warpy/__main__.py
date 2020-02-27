#! /usr/bin/python3

import sys
from time import sleep

from pathlib import Path
import os
import re
import json

from warpy.cli import WarpPlus
from warpy.utils import Colored

warp_plus = WarpPlus()

home = str(Path.home())
config_dir = os.path.join(home, ".warpy")


def increase_user_quota(config, user):
    counter = 0
    _input = input("({}{}{}) Enter quota to increase: ".format(Colored.OKGREEN, user, Colored.ENDC))
    while not _input.isdigit() or int(_input) < 1:
        _input = input("({}{}{}) ({}Invalid{}) Enter quota to increase: ".format(Colored.OKGREEN, user, Colored.ENDC,
                                                                                 Colored.RED, Colored.ENDC))
    print("\nWait until the end, Do not close the script!")
    quota = int(_input)
    while counter != quota:
        increase = warp_plus.increase_quota(config)
        if not increase:
            print("60 seconds sleep..., (Do not close the script)")
            sleep(60)
        elif counter != quota and counter % 3 == 0 and counter != 0:
            print("60 seconds sleep..., (Do not close the script)")
            sleep(60)
        print("+1GB Added")
        counter += 1
        sleep(1)
    print("Done!")


def get_config(file_name):
    file_path = os.path.join(config_dir, file_name)
    file = open(file_path, 'r')
    conf = json.loads(file.read())
    file.close()
    return conf


def press_any_key():
    print()
    print(Colored.PINK + "press any key to continue..." + Colored.ENDC)
    sys.stdin.read(1)


def show_user_info(config):
    info = warp_plus.get_info(config["id"], config["token"])
    text = '\nID: {}\n'.format(config['id'])
    text += "Public Key: {}\n".format(config['key']['public_key'])
    text += "Account Type: {}\n".format(info['result']['account']['account_type'])
    text += "Quota: {}GB".format(round(int(info['result']['account']['quota']) / (10 ** 9), 2))
    print(text)


def user_details(file_name):
    _input = None
    while _input is not None or _input != 0:
        print(Colored.YELLOW + "1. Show WireGuard Config" + Colored.ENDC)
        print(Colored.YELLOW + "2. Show User Info" + Colored.ENDC)
        print(Colored.YELLOW + "3. Increase Quota" + Colored.ENDC)
        print(Colored.ENDC + "0. Back To Main Menu" + Colored.ENDC)
        print()
        user = file_name.replace('.json', '')
        conf = get_config(file_name)
        _input = input("({}{}{}) Please enter a number: ".format(Colored.OKGREEN, user, Colored.ENDC))
        while not _input.isdigit():
            _input = input("({}{}{}) ({}Invalid{}) Please enter a number: ".format(Colored.OKGREEN, user, Colored.ENDC,
                                                                                   Colored.RED, Colored.ENDC))
        _input = int(_input)
        if _input == 1:
            print(warp_plus.export_to_wireguard(conf))
            press_any_key()
        elif _input == 2:
            show_user_info(conf)
            press_any_key()
        elif _input == 3:
            increase_user_quota(conf, user)
            press_any_key()
        elif _input == 0:
            break


def show_users(remove=False):
    dir_files = [i for i in os.listdir(config_dir) if i.endswith(".json")]
    print("\n{}List of Users:{}".format(Colored.YELLOW, Colored.ENDC))
    if not dir_files:
        print("Empty\n")
        return
    counter = 1
    for i in dir_files:
        print(str(counter) + ". " + Colored.OKGREEN + i[:-5] + Colored.ENDC)
        counter += 1
    text = "Enter user number (0 to back): " if not remove else "Enter user number to " \
                                                                "{}remove{} (0 to back): ".format(Colored.RED,
                                                                                                  Colored.ENDC)
    _input = input("\n" + text)
    while not _input.isdigit() or int(_input) > len(dir_files) or int(_input) < 0:
        _input = input("({}Invalid{}) {}: ".format(Colored.RED, Colored.ENDC, text))
    _input = int(_input)
    if _input == 0:
        return
    _input -= 1
    if remove:
        return dir_files[_input]
    print()
    return user_details(dir_files[_input])


def make_filename(file_name):
    file_name = file_name.replace(" ", "_")
    file_name = file_name.replace(".", "_")
    file_name = re.sub(r"[^a-z0-9_]", "", file_name.lower().strip())
    return file_name


def save_config(file_name, config):
    file_name = file_name + ".json"
    if not os.path.isdir(config_dir):
        os.mkdir(config_dir)
    file_path = os.path.join(config_dir, file_name)
    file = open(file_path, "w")
    file.write(json.dumps(config))
    file.close()


def print_header():
    print(Colored.PINK + Colored.HEADER + " ====================== " + Colored.ENDC)
    print(Colored.PINK + Colored.HEADER + " WARP+ WireGuard Python " + Colored.ENDC)
    print(Colored.PINK + Colored.HEADER + " By Arian Amiramjadi    " + Colored.ENDC)
    print(Colored.PINK + Colored.HEADER + " ====================== " + Colored.ENDC)
    print()


def print_options():
    print(Colored.YELLOW + "1. Register User" + Colored.ENDC)
    print(Colored.YELLOW + "2. Show Users" + Colored.ENDC)
    print(Colored.RED + "3. Remove User" + Colored.ENDC)
    print(Colored.ENDC + "0. Exit Script" + Colored.ENDC)
    print()


def show_menu():
    print_header()
    print_options()


def register():
    user = input("Please specify a username: ")
    user = make_filename(user)
    while len(user) == 0:
        user = input("{}(Invalid){} Please specify a username: ".format(Colored.RED, Colored.ENDC))
        user = make_filename(user)
    while os.path.isfile(os.path.join(str(Path.home()), ".warpy", user + '.json')):
        user = input("({}UserExists{}) Please specify a username: ".format(Colored.RED, Colored.ENDC))
        user = make_filename(user)
    reg = warp_plus.register(warp_plus.generate_key())
    save_config(user, reg)
    print(warp_plus.export_to_wireguard(reg))
    warp_plus.increase_quota(reg)

def init():
    invalid = False
    _input = None
    show_menu()
    while _input is not None or _input != 0:
        if invalid:
            text = "({}Invalid{}) Please enter a number: ".format(Colored.RED, Colored.ENDC)
        else:
            text = "Please enter a number: "
        _input = input(text)
        while not _input.isdigit():
            _input = input("({}Invalid{}) Please enter a number: ".format(Colored.RED, Colored.ENDC))
        _input = int(_input)
        invalid = False
        if _input == 0:
            exit()
        elif _input == 1:
            register()
            press_any_key()
        elif _input == 2:
            show_users()
        elif _input == 3:
            user = show_users(remove=True)
            if user:
                sure = input(Colored.RED + "Are you sure you want to remove this user (y/n default: No) ? " +
                             Colored.ENDC).lower()
                if sure == "y" or sure == "yes":
                    os.remove(os.path.join(config_dir, user))
                    print("User `{}` removed successfully.".format(Colored.OKGREEN + user.replace(".json", "") +
                                                                   Colored.ENDC))
                    press_any_key()
        else:
            invalid = True
        if not invalid:
            show_menu()


init()
