"""
Copyright (c) 2020 Penguin0093
Released under the MIT license
https://opensource.org/licenses/mit-license.php
"""

import re


def iopen(inipath,mode,section="",item="",value=""):
    returntxt = ""
    
    if(mode=="r"):
        returntxt = ini_get(inipath,section,item)
    elif(mode=="w"):
        returntxt = ini_write(inipath,section,item,value)
    elif(mode=="d"):
        returntxt = ini_del(inipath,section,item)
        
    return(returntxt)


def open_ini(openpath):

    root = []
    secn = 0
    
    with open(openpath,encoding='utf-8') as f:
        for line in f:

            line = line.rstrip("\n")
            m = re.search(r'[+[a-zA-Z0-9ぁ-んァ-ン一-龥]+]', line)
            
            if m is None:
                if(line != ""):
                    item = line.split(r" = ")
                    root[secn - 1].append(item)
            else:
                sectiontxt = m.group().lstrip("[").rstrip("]")
                root.append([sectiontxt])
    return(root)


def ini_join(join_array,cln):
    
    joinsec = []
    joinopt = []
    returntxt = ""

    if(cln == 0):
        for o in range(len(join_array)):
            for p in range(len(join_array[o])):
                if(p == 0):
                   joinopt.append("["+join_array[o][0]+"]")

                else:
                   joinopt.append(" = ".join(join_array[o][p]))

            joinsec.append("\n".join(joinopt))
            joinopt=[]
        returntxt = "\n\n".join(joinsec)

    elif(cln == 1):
        for p in range(len(join_array)):
            if(p == 0):
                joinopt.append("["+join_array[0]+"]")

            else:
                joinopt.append(" = ".join(join_array[p]))

        returntxt = "\n".join(joinopt)

    elif(cln == 2):
        for p in range(len(join_array)):
            if(p != 0):
                joinopt.append(" = ".join(join_array[p]))

        returntxt = "\n".join(joinopt)

    return(returntxt)


def ini_get(inipath,section="",item=""):

    returntxt = ""
    iniroot = open_ini(inipath)
    flag = False

    if(section != ""):
        n = 0
        for findsec in iniroot:
            if(findsec[0] == section):
                if(item != ""):
                    for m in range(len(findsec)):
                        if(findsec[m][0] == item):
                            flag = True
                            returntxt = findsec[m][1]
                            break

                    if flag:
                        break

                    else:
                        raise Exception('Not Found')
                else:
                    returntxt = ini_join(findsec,2)
                    break

            n = n + 1
        
        else:
            raise Exception('Not Found')

    else:
        returntxt = ini_join(iniroot,0)
        
    return(returntxt)


def ini_write(inipath,section="",item="",value=""):
    
    returntxt = ""
    iniroot = open_ini(inipath)
    flag = False

    if(section != ""):
        n = 0
        for findsec in iniroot:
            if(findsec[0] == section):
                if(item != ""):
                    for m in range(len(findsec)):
                        if(findsec[m][0] == item):
                            flag = True
                            findsec[m][1] = value
                            break

                    if flag:
                        break

                    else:
                        findsec.append([item,value])
                        break
                        
                else:
                    raise Exception('ERROR')

            n = n + 1
        
        else:
            if(item != ""):
                iniroot.append([section,[item,value]])
            else:
                iniroot.append([section])

            

    else:
        raise Exception('ERROR')
        
    returntxt = ini_join(iniroot,0)
    file_write(inipath,returntxt) 
    return


def ini_del(inipath,section="",item=""):
    
    returntxt = ""
    iniroot = open_ini(inipath)
    flag = False

    if(section != ""):
        n = 0
        for n in range(len(iniroot)):
            if(iniroot[n][0] == section):
                if(item != ""):
                    for m in range(len(iniroot[n])):
                        if(iniroot[n][m][0] == item):
                            flag = True
                            del iniroot[n][m]
                            break

                    if flag:
                        break

                    else:
                        raise Exception('Not Found')
                        
                else:
                    del iniroot[n]
                    break

            n = n + 1
        
        else:
            raise Exception('Not Found')

    else:
        raise Exception('ERROR')
        
    returntxt = ini_join(iniroot,0)
    #print("returntxt : "+returntxt)
    file_write(inipath,returntxt) 
    return



def file_write(path,text):
    with open(path, mode='w',encoding='utf-8') as fw:
        fw.write(text+"\n\n")
