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
def parse(data) :
    # checksum = data["checksum"] 
    # version = data["version"]
    roots = data["roots"]
    l = []
    for (k, v) in roots.items() :
        # there are 2 values we don't want ( as of [ September 20, 2013 ] )
        # .1 meta_info
        # .2 synced
        if(k != "meta_info" and k != "synced") :
            l = l + parseRecursive(v, "root/"+k)    
    return l

