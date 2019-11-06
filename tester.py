#!/usr/bin/python3

import os
import glob
from colorama import Fore, Back, Style

def main():
    task = "TASK"
    exe = "EXE"
    
    x = os.system("g++ -std=c++14 -DLOCAL -o {} {}".format(exe, task))
    
    if x == 0:
        inputs = glob.glob("in*")

        for i in range(len(inputs)):
            os.system("./{} < in{} > my_out{}".format(exe, str(i), str(i)))

        for i in range(len(inputs)):
            print("Case #{}:".format(i))
            if open("my_out{}".format(str(i))).read().strip() != open("out{}".format(str(i))).read().strip():
                print(Fore.RED + "WA! ")
                print("\nMy output:")
                print(open("my_out{}".format(str(i))).read())
                print("True output:")
                print(open("out{}".format(str(i))).read())

            else:
                print(Fore.GREEN + "AC! ")

            print("\n" + Style.RESET_ALL)


main()
