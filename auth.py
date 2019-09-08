#!/usr/bin/python
#-*- coding utf8 -*-
username = input("Login:")
password = input("Password:")

f = open("config.py", "w")
f.write("username = '" + username + "'\n")
f.write("password = '" + password + "'\n")
f.close()
print()
print("Done.")
print()
