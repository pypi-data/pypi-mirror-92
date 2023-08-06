#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, pexpect, random

# inc imports.
from fil3s import Files, Formats
from r3sponse import r3sponse
import cl1, syst3m

# fyunctions.
def __get_operating_system__():
	os = platform.system().lower()
	if os in ["darwin"]: return "osx"
	elif os in ["linux"]: return "linux"
	else: raise ValueError(f"Unsupported operating system: [{os}].")
def __get_file_path_base__(path, back=1):
	path = path.replace('//','/')
	if path[len(path)-1] == "/": path = path[:-1]
	string, items, c = "", path.split("/"), 0
	for item in items:
		if c == len(items)-(1+back):
			string += "/"+item
			break
		else:
			string += "/"+item
		c += 1
	return string+"/"
def __save_file__(path, data):
	file = open(path, "w+") 
	file.write(data)
	file.close()
def __check_alias__(source_name, source_path, version, _os_):
	alias = source_name.lower()
	path = f"/usr/local/bin/{alias}"
	if not os.path.exists(path):
		file = f"""package={source_path}/{version}/\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
		os.system(f"sudo touch {path}")
		os.system(f"sudo chmod 755 {path}")
		if _os_ in ["osx"]:
			os.system(f"sudo chown {os.environ.get('USER')}:wheel {path}")
		elif _os_ in ["linux"]:
			os.system(f"sudo chown {os.environ.get('USER')}:root {path}")
		__save_file__(f"{path}", file)
		os.system(f"sudo chmod 755 {path}")
		if '--silent' not in sys.argv:
			print(f'Successfully created alias: {alias}.')
			print(f"Check out the docs for more info $: {alias} -h")

# source.
ALIAS = "ssht00ls"
SOURCE_NAME = "ssht00ls"
VERSION = "v1"
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=4)
BASE = syst3m.defaults.get_source_path(SOURCE_PATH)
OS = syst3m.defaults.check_operating_system(supported=["linux", "osx"])
syst3m.defaults.check_alias(alias=ALIAS, executable=f"{SOURCE_PATH}/{VERSION}/")

# universal variables.
OWNER = os.environ.get("USER")
GROUP = "root"
HOME_BASE = "/home/"
HOME = f"/home/{os.environ.get('USER')}/"
MEDIA = f"/media/{os.environ.get('USER')}/"
if OS in ["osx"]: 
	HOME_BASE = "/Users/"
	HOME = f"/Users/{os.environ.get('USER')}/"
	MEDIA = f"/Volumes/"
	GROUP = "wheel"
