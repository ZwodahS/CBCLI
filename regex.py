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
import re
# match only one type of regex. 
# will return output in the following form
# (segments,matchcode)
# segments will be the list of strings that are broken down
# matchcode would be a similar size list that state if the segment match or not
# matchcode will be ranged from -1 to num of regexpression -1
# in the case of regmatch, it will be -1 or 0 , where -1 is miss and 0 is match.
# if overlap specified, then it will have a list of number which state which overlapped.
MISS = -1
# ?!-[block]regex
def regmatch(text,reg,regcode=0):
    segmented = []
    matchcode = []
    temp=text
    match = re.search(reg,temp) 
    while match != None :
        start = match.start(0)
        end = match.end(0)
        # for those that never match , add it to the segment with no match
        add_segment(temp[0:start],MISS,segmented,matchcode)
        # add the code for those that matches
        add_segment(match.group(0),regcode,segmented,matchcode)
        temp = temp[end:]
        match = re.search(reg,temp)
    add_segment(temp,MISS,segmented,matchcode)
    return (segmented,matchcode)
# ?!-[endblock]
# refactor to make it "clearer" what this is
def add_segment(text,code,segmented,matchcodes):
    segmented.append(text)
    matchcodes.append(code)
# this is the code for deciphering multiple matches.
def breakIntoSegments(matchedIndexes,matches,start,end) :
    # start with a index of miss
    outputindex = []
    for i in range(0,(end-start)) :
        outputindex.append(MISS)
    # for each index in matched index , 
    for index in matchedIndexes :
        matchstart = matches[index].start(0)
        matchend = matches[index].end(0)
        for s in range(matchstart,matchend) :
            i = s - start
            if outputindex[i] == MISS :
                outputindex[i] = index
            elif outputindex[i].__class__ == [].__class__ : # if already has overlap, just add to it 
                outputindex[i].append(index)
            else : # no overlap , create that list
                temp = [outputindex[i]]
                temp.append(index)
                outputindex[i] = temp
    segments = []
    # group the similar indexes together and return them
    curr_segmentstart = 0
    curr_matchcode = outputindex[0]
    # group all of them together
    for i in range(1,len(outputindex)) :
        if curr_matchcode == outputindex[i] : #same i do nothing
            pass
        else :
            segments.append((start+curr_segmentstart,start+i,curr_matchcode))
            curr_segmentstart = i
            curr_matchcode = outputindex[i]
    segments.append((start+curr_segmentstart,start+len(outputindex),curr_matchcode))     
    return segments
# to know if there is a match, sum(matchcode) = len(matchcode) * -1 <-- this will be no match 
def parallelmatch(text,regex) :
    segmented = []
    matchcode = []
    temp = text
    matches = [] 
    # initial search
    for reg in regex :
        matches.append(re.search(reg,temp) if reg != None else None)
    # find all the matches
    index = findTheNonNone(matches)
    while len(index) != 0 :
        if len(index) == 1 :
            # since there is only one match, use regmatch to do the rest
            (singlesegments,singlematchcode) = regmatch(temp,regex[index[0]],index[0])
            segmented.extend(singlesegments)
            matchcode.extend(singlematchcode)
            # append the text to the output and return
            return (segmented,matchcode)
        else : # more than one
            # find the first guy that matches. If overlapped then handle them
            overlaps = findFirstMatch(index,matches) 
            if len(overlaps) == 1 : # no overlap, add the first guy to the segment
                matchedindex = overlaps[0]
                start = matches[matchedindex].start(0)
                end = matches[matchedindex].end(0)
                add_segment(temp[0:start],MISS,segmented,matchcode)
                add_segment(matches[matchedindex].group(0),matchedindex,segmented,matchcode)
                temp = temp[end:]
            else :
                # 3 parts of the output  
                matchedIndexes = overlaps[0]
                start = overlaps[1] # take the start position that is processed
                end = overlaps[2] # take the end position that is processed
                # add the none involved stuffs first
                add_segment(temp[0:start],MISS,segmented,matchcode)
                segments = breakIntoSegments(matchedIndexes,matches,start,end)
                for segment in segments :
                    # for each segment break them down and add that part into the output
                    (seg_start , seg_end, seg_matchcode) = segment
                    add_segment(temp[seg_start:seg_end],seg_matchcode,segmented,matchcode)
                # process the rest
                temp = temp[end:]
        matches = [] 
        for reg in regex :
            matches.append(re.search(reg,temp) if reg != None else None)
        index = findTheNonNone(matches)
    add_segment(temp,MISS,segmented,matchcode)
    return (segmented,matchcode)

def findFirstMatch(indexes,matches):
    assert len(indexes) > 0 
    start = matches[indexes[0]].start(0)
    end = matches[indexes[0]].end(0)
    curr = indexes[0]
    lapped = []
    for i in indexes :
        if i == indexes[0] : 
            continue
        # if the match starts after the current ends , no overlap
        if matches[i].start(0) >= end :
            continue
        # if the curr is after the new guy change the new guy to current
        elif matches[i].end(0) <= start :
            start = matches[i].start(0)
            end = matches[i].end(0)
            curr = i
        else : 
            start = min(start,matches[i].start(0))
            end = max(end,matches[i].end(0))
            if curr != None :
                lapped.append(curr)
                curr = None
            lapped.append(i)
    if curr == None:
        return [lapped,start,end]       
    # else just add the earliest and return
    else :
        return [curr]

def countNonNone(list) :
    count = 0
    for f in list :
        if f != None :
            count+=1
    return count
def findTheNonNone(list) :
    t = []
    for f in range(0,len(list)):
        if list[f] != None :
            t.append(f)
    return t
def hasmatch(matchcode) :
    for i in matchcode :
        if i != -1 :
            return True
    return False
def is_overlap(code):
    return code.__class__ == [].__class__ 

def merge_match(matchcodes):
    expr = []
    for match in matchcodes :
        if match != -1 :
            if match.__class__ == [].__class__ :
                for m in match :
                    if m not in expr :
                        expr.append(m)
            else:
                if match not in expr :
                    expr.append(match)
    return expr
