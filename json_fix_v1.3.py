#!/usr/bin/env python
# coding: utf-8

# # json

# In[ ]:


import glob
import pandas as pd
import json
import re
import math


# In[ ]:


targetDirectory = input('주소를 입력해주세요 : ')

files = glob.glob('{}/*.json'.format(targetDirectory))
print(files[:3])


# In[ ]:


def distance(x1, y1, x2, y2):
    result = math.sqrt( math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return result


# In[ ]:


key = ['camid', 'time', 'biccode', 'typesize', 'imdg', 'isloaded', 'bicdirection', 'ownercode', 'dataregion']
key_del = ['biccode', 'typesize', 'isloaded', 'bicdirection', 'ownercode']

for index in range(0,len(files)):
    strencoding = "EUC-KR"
    with open(files[index], encoding="EUC-KR") as tmpfile:        
        try:       
            linedata = tmpfile.readline()  
        except:            
            strencoding = 'UTF-8'
            
    with open(files[index], encoding = strencoding) as openFile:        
        json_lodaedData = json.load(openFile)
        
        for keyValue in key:
            #필요없는 부분 삭제
            if keyValue in key_del:
                try:
                    del json_lodaedData['addinfo'][keyValue]
                    
                except KeyError:
                    pass
            
            #키 추가
            if keyValue not in key_del:
                if keyValue not in json_lodaedData['addinfo'].keys():
                    updateKeyValue = {'{}'.format(keyValue) : ''}
                    json_lodaedData['addinfo'].update(updateKeyValue)

            #값 수정
            condition = json_lodaedData['addinfo']
            
            # addinfo > camid
            if json_lodaedData['images']['identifier'].split('_')[1]=='SAF':
                json_lodaedData['addinfo']['camid'] = None
            elif json_lodaedData['images']['identifier'].split('_')[1]=='CON':
                if re.search(r'\d', json_lodaedData['addinfo']['camid'])==None:
                    condition['camid'] = json_lodaedData['images']['identifier'][-1]
                else:
                    pass
                
            # addinfo > time
            condition['time'] = json_lodaedData['images']['filename'].split('_')[5][0:14]
            
            # addinfo > imdg
            for j in range(0,len(json_lodaedData['annotations'])):
                condition2 = list(json_lodaedData['annotations'][j].values())
                if condition2[0]['classid'] == 'IMDG':
                    condition['imdg'] = 'Y'
                    break
                else:
                    condition['imdg'] = 'N'
                    
            # addinfo > dataregion
            condition['dataregion'] = '0' if json_lodaedData['images']['identifier'].split('_')[1]=='CON' else '1'

            # annotation > bicdirection
            for item in json_lodaedData["annotations"] :            
                if item["bbox"]["classid"] in 'BIC':                  
                    if len(item["bbox"]["points"]) >=4 :
                        if 'classid' in item["bbox"] and 'text' in item["bbox"]:
                            x1 = item["bbox"]["points"][0][0]
                            y1 = item["bbox"]["points"][0][1]
                            x2= item["bbox"]["points"][1][0]
                            y2 = item["bbox"]["points"][1][1]
                            x3= item["bbox"]["points"][2][0]
                            y3 = item["bbox"]["points"][2][1]
                            
                            lenx = distance(x1,y1,x2,y2)
                            leny = distance(x2,y2,x3,y3) 

                            if lenx >= leny:
                                item["bbox"]['bicdirection'] = '0'
                            else:
                                item["bbox"]['bicdirection'] = '1'
            #save .json
            with open(files[index], "w", encoding="UTF-8-sig") as saveFile:
                json.dump(json_lodaedData, saveFile, indent= 2, ensure_ascii=False)

