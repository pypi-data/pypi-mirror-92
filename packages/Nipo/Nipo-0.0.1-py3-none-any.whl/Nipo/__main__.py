from sys import argv
import os
os.makedirs(argv[1] + "/templates")
os.chdir(argv[1])
open("urls.py", "w").write("from Nipo.urls import urlpath\nurls = [\n# Urls Here!\n\t\n]").close()
open("views.py", "w").write("from Nipo.views import *\n# Views Here!").close()
open("__init__.py", "x").close()
f = open("run.py","w")
f.write(open("runner.py").read())