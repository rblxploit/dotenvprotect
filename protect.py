"""
DISCLAIMER!
This code is super super bad
it works tho

oh and also it has no external dependencies, it only uses integrated python modules (random, shutil and os (subprocess in the future))

Also it's made by Wabz and its for nodejs code not python
"""

import random
import shutil
import os
DEST_FOLDER_NAME = "dep_build"
print(f"Deleting {DEST_FOLDER_NAME} (if it exists)...")

try:
    shutil.rmtree('./'+DEST_FOLDER_NAME)
except:
    pass
os.mkdir(DEST_FOLDER_NAME)

# change that to the name you want


def wabzEncode(s):
    # named badly, it's just using something already in python
    ns = ""
    fc = True
    for c in s:
        if not fc:
            ns += "|"
        else:
            fc = False
        ns += str(ord(c))

    return ns


def getFiles():
    f = []
    # Thx stackoverflow
    for root, dirs, files in os.walk(".\\", topdown=False):
        for name in files:
            if "\\node_modules\\" not in root:
                f.append(os.path.join(root, name))

    return f


def makeFolders(dfile):
    folders = dfile.split("\\")
    if len(folders) > 2:
        ll = folders[0:len(folders)-1]
        cc = []
        for tt in ll:
            cc.append(tt)
            try:
                os.mkdir("\\".join(cc))
            except:
                pass


def calculatePath(fileLocation):
    flds = fileLocation.split("\\")
    if len(flds) > 2:
        return "../"*(len(flds)-2)+".env"
    else:
        return "./.env"


print("Setting up DOTENVPROTECT...")

tfiles = getFiles()
files = []
for f in tfiles:
    files.append(os.path.join(DEST_FOLDER_NAME, f[slice(2, len(f))]))
# Starts converting

dotenv = None
try:
    with open('.\\.env', 'r', encoding='utf-8') as f:
        dotenv = f.read().split('\n')
except:
    dotenv = []

print(f"Recopying files to {DEST_FOLDER_NAME}")
for i in range(len(files)):
    sfile = tfiles[i]
    dfile = files[i]
    # print(calculatePath(sfile))
    makeFolders(dfile)
    if sfile.endswith(".js"):
        with open(sfile, 'r', encoding='utf-8') as fop:
            op = fop.read()
        value = wabzEncode(op)
        key = "".join([chr(random.randint(65, 90))
                       for i in range(random.randint(13, 16))])
        dotenv.append(f'{key}="{value}"')
        fnc = """function wabzDecode(r){var e="",t=r.split("|");for(let r=0;r<t.length;r++)e+=String.fromCharCode(t[r]);return e}"""
        code = f"require(\"dotenv\").config({{path: \"{calculatePath(sfile)}\"}})\n{fnc}\neval(wabzDecode(process.env.{key}));"
        try:
            with open(".\\"+dfile, "w+", encoding='utf-8') as fi:
                fi.write(code)
        except:
            pass
    else:
        with open(".\\"+dfile, "w+", encoding='utf-8') as fii:
            with open(sfile, "r", encoding='utf-8') as lol:
                fii.write(lol.read())
print("Saving environment variables")
# save .env
newenv = "\n".join(dotenv)
with open(DEST_FOLDER_NAME + "\\.env", "w+", encoding='utf-8') as env:
    env.write(newenv)

print("Installing modules")
os.chdir(os.path.abspath(DEST_FOLDER_NAME))
os.system("npm install")
os.system("npm install dotenv")

print(f"Done! Check the {DEST_FOLDER_NAME} folder")
