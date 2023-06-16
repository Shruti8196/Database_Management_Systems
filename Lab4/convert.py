from sys import argv
import json

f = open(argv[1],'r')
x = json.load(f)
f.close()

for k,v in x.items():
    
    if k=="StudentID": 
        val = int(list(v.values())[0])
    
    elif k=="Contact":
        val = [list(cno.values())[0] for cno in list(v.values())[0]]
        for i in range(len(val)):
            try:
                val[i] = int(val[i])
            except:
                pass     
       
    elif k=="CourseID":
        val = [int(i) for i in list(v.values())[0]]
        
    elif k=="CourseName" or k=="StudentName":
        val = list(v.values())[0]

    elif k=="Scores":
        val = list(v.values())[0]    
        for skey,sval in val.items():
            val[skey] = int(list(sval.values())[0])
        
    x[k] = val
    
with open(argv[2], 'w') as f:
    json.dump(x,f)