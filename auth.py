#!/usr/bin/python
#-*- coding utf8 -*-
username = raw_input("Login:")
password = raw_input("Password:")

f = open("config.py", "w")
f.write("username = '" + username + "'\n")
f.write("password = '" + password + "'\n")
f.close()
print
print "Done."
print
