import os

cwd = os.getcwd()
if not os.path.exists("%s/__init__.py" % cwd):
    with open("%s/__init__.py" % cwd, "w") as f:
        f.close()
