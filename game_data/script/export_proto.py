#-- coding:UTF-8 --
import xlrd
import sys
import os

def read_excel(filename, writepath, types):
    data = xlrd.open_workbook(filename)
    print(u"所有book的工作表名: %s" % data.sheet_names())

    table = data.sheet_by_index(0)

    keylist = []
    keymap = {}
    valuelist = []
    structname = ""

    writefilename = ""
    headInfo = []


    for i in range(0,table.nrows):
        eachrow = table.row_values(i)
        if eachrow[0] == "KEY":
            t = 0
            for cell in eachrow:
                keymap[cell]= t
                t=t+1

        if eachrow[0] == "VALUE" :
            valuelist.append(eachrow)
        if eachrow[0] == "FRO_NAME" and types == "c":
            structname = eachrow[1]
        if eachrow[0] == "FRO_FILE" and types == "c":
            writefilename = eachrow[1]

        if eachrow[0] == "END_NAME" and types == "s":
            structname = eachrow[1]
        if eachrow[0] == "END_FILE" and types == "s":
            writefilename = eachrow[1]
    
    BodyH = "" 
    B1 = ""
    BodyE = ""
    if types == "c": 
        BodyH = "let %s: object ={\n" %structname
        
        iff = True
        for i in valuelist:
            Id = str(int(i[keymap['id']]))
            B1 += "    %s:{" %Id
            vf = True
            for v in i[keymap['parm']].split("\n"):
                if vf:
                    cell1 = " " +v.split(" ")[0]
                    vf = False
                else:
                    cell1 = ", " +v.split(" ")[0]
                if cell1 == " ":
                    continue
                cell1 += ": undefined"
                B1 += cell1
            B1 += " },\n"
        B1 = B1[:-2] + "\n"
        BodyE = "};\nexport default %s;" %structname 
    else:
        BodyH = ""
        for i in valuelist:
            Rc = i[keymap['record']]
            B1 += "type %s struct { \n" %(str.title(Rc).replace("_", ""))
            for v in i[keymap['parm']].split("\n"):
                cell1 = v.split(" ")[0]  
                if cell1 == "":
                    continue
                cell1 = "    " + cell1 + "  interface{} `json:\"%s\"` \n" %cell1
                B1 += cell1
            B1 += "}\n\n"

    
    
    WriteBody = BodyH + B1 + BodyE

    HeadH = ""
    H1 = ""
    HeadE = ""
    if types == "c":
        HeadH = "export class %s{\n" % str.upper(structname)
       
        for i in valuelist:
            Id = str(int(i[keymap['id']]))
            Rc = i[keymap['record']]
            Rdesc = i[keymap['desc']]
            H1 += "     public static readonly %s = %s; // %s\n" %(Rc,Id,Rdesc)
        HeadE = "}"
    else:
        HeadH = "package %s" %structname
        HeadH += "\n\nvar (\n"
        for i in valuelist:
            Id = str(int(i[keymap['id']]))
            Rc = i[keymap['record']]
            H1 += "    MSG%s = %s\n" %(str.title(Rc).replace("_", ""),Id)
        HeadE = "\n)"

    WriteHead = HeadH + H1 + HeadE

    WR = WriteHead +"\n\n\n" + WriteBody
    towrite(writepath, writefilename, WR)


    

def towrite(writepath, filename, s):
    fo = open(writepath + filename, "wb")
    fo.write(str.encode(s))
    fo.close()


if __name__ == "__main__":
    obj = sys.argv[1]
    desc = sys.argv[2]
    types = sys.argv[3]
    read_excel(obj,desc,types)