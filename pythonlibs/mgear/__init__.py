'''

    This file is part of MGEAR.

    MGEAR is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.

    Author:     Jeremie Passerin      geerem@hotmail.com
    Url:        http://www.jeremiepasserin.com
    Date:       2011 / 07 / 13

'''

## @package mgear
# @author Jeremie Passerin
#
##########################################################
# GLOBAL
##########################################################
# built-in
import os
import sys, string, exceptions

## Debug mode for the logger
logDebug = False

# Severity for logged messages
sev_fatal = 1
sev_error = 2
sev_warning = 4
sev_info = 8
sev_verbose = 16
sev_comment = 32

# gear version
VERSION = [0,1,0]

## Log version of Gear
def logInfos():
    print "GEAR version : "+getVersion()
    
def getVersion():
    return ".".join([str(i) for i in VERSION])
    
##########################################################
# METHODS
##########################################################
# ========================================================
## reload a module and its sub-modules from a given module name.
# @param name String - The name of the module to reload.
def reloadModule(name="mgear"):

    debugMode = setDebug(False)
    module = __import__(name, globals(), locals(), ["*"], -1)

    path = module.__path__[0]

    __reloadRecursive(path, name)

    setDebug(debugMode)

def __reloadRecursive(path, parentName):

    for root, dirs, files in os.walk(path, True, None):

        # parse all the files of given path and reload python modules
        for sfile in files:
            if sfile.endswith(".py"):
                if sfile == "__init__.py":
                    name = parentName
                else:
                    name = parentName+"."+sfile[:-3]

                log("reload : %s"%name)
                try:
                    module = __import__(name, globals(), locals(), ["*"], -1)
                    reload(module)
                except ImportError, e:
                    for arg in e.args:
                        log(arg, sev_error)
                except Exception, e:
                    for arg in e.args:
                        log(arg, sev_error)

        # Now reload sub modules
        for dirName in dirs:
            __reloadRecursive(path+"/"+dirName, parentName+"."+dirName)
        break

##########################################################
# LOGGER
##########################################################
# ========================================================
## Set the debug mode to given value.
# @param b Boolean
# @return Boolean - The previous value of the debug mode
def setDebug(b):
    global logDebug
    original_value = logDebug
    logDebug = b
    return original_value

## Toggle the debug mode value.
# @param Boolean - The new debug mode value.
def toggleDebug():
    global logDebug
    logDebug = not logDebug
    return logDebug

# ========================================================
## Log a message using severity and additional info from the file itself.\n
## Severity has been taken from Softimage one : \n
## 1.Fatal\n
## 2.Error\n
## 4.Warning\n
## 8.Info\n
## 16.Verbose\n
## 32.Comment\n
# @param message String
# @param severity Int4
# @param infos Boolean - Add extra infos from the module, class, method and line number.
def log(message, severity=sev_comment, infos=False):

    message = str(message)

    if infos or logDebug:
        message = getInfos(1) +"\n"+ message

    sys.stdout.write(message + "\n")

# ========================================================
## Exception
class FakeException(exceptions.Exception):
    pass

## Get information from where the method has been fired. \n
## Such as module name, method, line number...
# @param level
# @return String
def getInfos(level):

    try:
        raise FakeException("this is fake")
    except Exception, e:
        #get the current execution frame
        f = sys.exc_info()[2].tb_frame

    #go back as many call-frames as was specified
    while level >= 0:
        f = f.f_back
        level = level-1

    infos = ""

    # Module Name
    moduleName = f.f_globals["__name__"]
    if moduleName != "__ax_main__":
        infos += moduleName + " | "

    # Class Name
    #if there is a self variable in the caller's local namespace then
    #we'll make the assumption that the caller is a class method
    obj = f.f_locals.get("self", None)
    if obj:
        infos += obj.__class__.__name__+"::"

    # Function Name
    functionName = f.f_code.co_name
    if functionName != "<module>":
        infos += functionName+"()"

    # Line Number
    lineNumber = str(f.f_lineno)
    infos += " line "+lineNumber+""

    if infos:
        infos = "["+infos+"]"

    return infos