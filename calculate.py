def cal(list,a):
    final_l=[]
    s_m=0 #校定必修
    s_m_l=[]
    boya=0 #通識
    boya_l=[]
    p_m=0 #專業必修
    p_m_l=[]
    p_s=0 #專業選修
    p_s_l=[]
    other_s=0 #跨系
    other_s_l=[]
    for i in range(len(list)):
        if list[i][6].isdigit() and float(list[i][6])>=60 or list[i][6]=='抵免':
            if '14010' in list[i][3]:
                #微積分算專業必修
                p_m+=float(list[i][5])
            elif list[i][1]=='選':
                if list[i][3][0:2]==str(a):
                    #專業選修
                    p_s+=float(list[i][5])
                    p_s_l.append(list[i][2])
                else:
                    #他系選修
                    other_s+=float(list[i][5])
                    other_s_l.append(list[i][2])
            elif list[i][1]=='通':
                boya+=float(list[i][5])
                boya_l.append(list[i][2])
            elif list[i][1]=='必':
                if list[i][3][0:2]==str(a):
                    p_m+=float(list[i][5])
                    p_m_l.append(list[i][2])
                else:
                    s_m+=float(list[i][5])
                    s_m_l.append(list[i][2])
            else:
                #暑修必修或英文學分抵免
                if list[i][3][0:2]==str(a):
                    p_m+=float(list[i][5])
                    p_m_l.append(list[i][2])
                elif list[i][3][0:2]=='14':
                    s_m+=float(list[i][5])
                    s_m_l.append(list[i][2])
    final_l=[0,s_m+boya,0,0,p_m,p_s,other_s,'']
    print(final_l)
##    print('校定必修:',s_m+boya,'\n',s_m_l,boya_l)
##    print('博雅通識:',boya,'\n',boya_l)
##    print('專業必修',p_m,'\n',p_m_l)
##    print('專業選修',p_s,'\n',p_s_l)
    return final_l


'''
#test
list2=[]
f=open('data.csv','r+')
data=f.readlines()

for i,line in enumerate (data):
    line=line.strip()
    if i==0:
        line=line.split(',')
        list2.append(line[0])
    else:
        line=line.split(',')
        list2.append(line)
print(list2)
f.close()

cal(list2)
'''
