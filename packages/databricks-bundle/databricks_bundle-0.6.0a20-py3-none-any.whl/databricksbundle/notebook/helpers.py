import sys
from databricksbundle.dbutils.IPythonDbUtilsResolver import resolveDbUtils
from databricksbundle.detector import isDatabricks

def getNotebookContext():
    return resolveDbUtils().notebook.entry_point.getDbutils().notebook().getContext()

def getUserEmail():
    return getNotebookContext().tags().get('user').get()

def getNotebookPath():
    return getNotebookContext().notebookPath().get()

def isNotebookEnvironment():
    return sys.argv and sys.argv[0][-15:] == '/PythonShell.py'

def isDatabricksNotebookEnvironment():
    return isDatabricks() and isNotebookEnvironment()
