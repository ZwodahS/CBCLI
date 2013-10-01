#!/usr/bin/env python
# every node in roots will have a key. meta_info and synced is not part of the bookmarks
# every node after that , the node are stored like a tree, with their key being "childrens".
# each node will have
# .1 date_added
# .2 date_modified
# .3 id ?? probably the id that is registed.
# .4 meta_info ?? not sure what this is for
# .5 type   - I only saw 2 value so far, "url" and "folder"
# .6 name   - The name of this bookmark/folder <-- possibly the 1 that we want to search
# .7 url    - url to open.
# this parse should return each object individually as a dict
# with an additional attribute , the abs path to the bookmark.
import re
import os
root = os.path.dirname(os.path.abspath(__file__))

# load the cached and return the list of urls that was last searched.
# I want to keep both the url and name and other information in the future,
# to allow me to display the last search results but for now this will do
def loadCache() :
    actualpath = os.path.join(root, "cached")
    if os.path.isfile(actualpath) :
        fin = open(actualpath, "r")
        l = fin.readlines()
        final = []
        for item in l :
            final.append(item.strip())
        fin.close()
        return final
    else :
        return []
# cache the result and write it to the cached file
# the cached file is used when opening a link
def cache(result):
    actualpath = os.path.join(root, "cached")
    if os.path.isfile(actualpath):
        os.remove(actualpath)
    fout = open(actualpath, "w")
    for value in result:
        fout.write(value["url"] + "\n")
    fout.close()

# this will open with default browser
# this is the mac function to open a link
# create one for each OS that is needed
def macopen(link, background):
    cmd = "open " + link + " "
    if background :
        cmd += "-g"
    os.system(cmd)

# public call to open a link
# switch to different os if necessary.
def openlink(link, background=False) :
    # if you want to extend to linux or other os, you can check it here.
    macopen(link, background)

##### all the match functions should be put into this area #####

# generic match for regex
def match(data, searchstring):
    return re.search(searchstring, data["name"]) != None

# regex match but convert all to lower case first.
def matchignorecase(data, searchstring):
    return re.search(searchstring.lower(), data["name"].lower()) != None

#################################################################
# filter into dictionary instead of list
def tag_filterdict(data, taglist) :
    newdata = {}
    for d in data :
        tokens = d["name"].split()
        for t in taglist :
            if "#"+t in tokens :
                newdata[d["id"]] = d;
                break
    return newdata
# tag list is always a AND operator now
def tag_filter(data, taglist) :
    if len(taglist) == 0 :
        return data
    
    newdata = []
    for d in data :
        tokens = d["name"].split()
        for t in taglist :
            if "#"+t in tokens :
                newdata.append(d);
                break
    return newdata

# This is for the string search option .
def stringsearch(data, searchstring, taglist = []):
    return search(tag_filter(data, taglist), searchstring, matchignorecase)

# the generic search function. 
# pass in the match function to use.
def search(data, searchstring, matchfunction=match):
    l = {}
    for d in data:
        if matchfunction(d, searchstring) :
            l[d["id"]] = d
    return l

def findtags(data) :
    hashtags = {}
    for d in data :
        tokens = d["name"].split()
        for token in tokens :
            if token[0] == "#" :
                if token[1:] in hashtags :
                    hashtags[token[1:]] += 1
                else :
                    hashtags[token[1:]] = 1
    return hashtags




################ JSON parsing code ##############################

def createChild(data, parent):
    childData = {}
    childData["name"] = data["name"]
    childData["url"] = data["url"]
    childData["id"] = data["id"]
    childData["parent"] = parent
    return childData

def parseRecursive(data, parent) :
    #if you are here, means you are a folder
    name = data["name"]
    output = []
    for child in data["children"] :
        if("children" in child) : # if the child has a children, means it is a folder
            l = parseRecursive(child, parent+"/"+name)
            output += l
        else :
            output.append(createChild(child, parent+"/"+name))
    return output

# parse the whole json file and return a list of url objects.
# This is the main parse function
# returns a list of dictionary with
#   "name"   : for the name of the bookmark
#   "url"    : url of the bookmark
#   "id"     : id given to this by chrome
#   "parent" : the parent of this bookmark, a.k.a. the directory path in the bookmark manager.
def parse(data) :
    checksum = data["checksum"] 
    version = data["version"]
    roots = data["roots"]
    l = []
    for (k, v) in roots.items() :
        # there are 2 values we don't want ( as of [ September 20, 2013 ] )
        # .1 meta_info
        # .2 synced
        if(k != "meta_info" and k != "synced") :
            l = l + parseRecursive(v, "root/"+k)    
    return (l, checksum, version)

