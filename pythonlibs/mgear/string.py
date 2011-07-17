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

## @package mgear.string
# @author Jeremie Passerin
#
# @brief string management methods

##########################################################
# GLOBAL
##########################################################
import re

##########################################################
# FUNCTIONS
##########################################################
# ========================================================
## Replace all invalid characters with "_"
# @param string String - A string to normalize.
# return String - Normalized string.
def normalize(string):

    string = str(string)

    if re.match("^[0-9]", string):
        string = "_"+string

    return re.sub("[^A-Za-z0-9_-]", "_", str(string))

# ========================================================
## Remove all invalid character.
# @param string String - A string to normalize.
# return String - Normalized string.
def removeInvalidCharacter(string):
     return re.sub("[^A-Za-z0-9]", "", str(string))

# ========================================================
## Replace a list of # symbol with properly padded index. (ie. count_### > count_001 )
# @param string String - A string to set. Should include '#'
# @param index Integer - Index to replace.
# return String - Normalized string.
def replaceSharpWithPadding(string, index):

    if string.count("#") == 0:
        string += "#"

    digit = str(index)
    while len(digit) < string.count("#"):
        digit = "0"+digit

    return re.sub("#+", digit, string)
