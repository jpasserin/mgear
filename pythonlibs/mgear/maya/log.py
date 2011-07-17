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

## @package mgear.maya.log
# @author Jeremie Passerin
#

def matrix4(m, msg="matrix4"):

    s = msg + " : \n"\
	+"| %s , %s , %s , %s |\n"%(m[0][0], m[0][1], m[0][2], m[0][3])\
	+"| %s , %s , %s , %s |\n"%(m[1][0], m[1][1], m[1][2], m[1][3])\
	+"| %s , %s , %s , %s |\n"%(m[2][0], m[2][1], m[2][2], m[2][3])\
	+"| %s , %s , %s , %s |"%(m[3][0], m[3][1], m[3][2], m[3][3])

    print (s)

