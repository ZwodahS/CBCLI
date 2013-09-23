#           DO WHAT THE **** YOU WANT TO PUBLIC LICENSE
#                   Version 2, December 2004
# 
# Copyright (C) 2013 ZwodahS(ericnjf@gmail.com) 
# zwodahs.wordpress.com
# 
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
# 
#           DO WHAT THE **** YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
# 
#  0. You just DO WHAT THE **** YOU WANT TO.
# 
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details. 

### color constant ###
black = 0
red = 1
green = 2
yellow = 3
blue = 4
magenta = 5
cyan = 6
white = 7
### stuffs that other file shouldn't care ###
reset = "\033[0m"
bold_code  = "\033[1m"
underline_code  = "\033[4m"
def __color(color):
    return "\033[3"+str(color)+"m"
### standard method ###
def wrap_color(text,color,bold=False,underline=False):
    tmp = ""
    if color != None :
        tmp = __color(color)
    if bold :
        tmp = tmp + bold_code
    if underline :
        tmp = tmp + underline_code
    tmp = tmp + text
    tmp = tmp + reset
    return tmp
