#!/usr/bin/env python
# coding: utf-8

# # json -> csv

# In[1]:


import glob
import pandas as pd
import json
from csv import DictWriter
import re
import math
import collections


# In[2]:


targetDirectory = input('주소를 입력해주세요 : ')

files = glob.glob('{}/*.json'.format(targetDirectory))
print(files[:3])


# In[3]:


dataFrame = None

for index in range(0,len(files)):
    strencoding = "EUC-KR"
    with open(files[index], encoding="EUC-KR") as tmpfile:        
        try:       
            linedata = tmpfile.readline()  
        except:            
            strencoding = 'utf-8-sig'
            
    with open(files[index], encoding = strencoding) as openFile:        
        json_lodaedData = json.load(openFile)

        DataSet = json_lodaedData['Dataset']
        Images = json_lodaedData['images']
        AddInfo = json_lodaedData['addinfo']

        DataDictionaryList = [DataSet, Images, AddInfo]

        extendList = []
        for dictionaryValue in DataDictionaryList:
            sourcelist = list(dictionaryValue.values())
            extendList.extend(sourcelist)

        dataFrame = pd.concat([pd.DataFrame(extendList).transpose(), dataFrame])

keys_list = [list(DataSet.keys()), list(Images.keys()), list(AddInfo.keys())]

DataSet_AppendKeys = []
Images_AppendKeys = []
AddInfo_AppendKeys = []

for i in keys_list:
    for j in range(0,len(i)):
        if i==keys_list[0]:
            tempString = "DT_" + i[j]
            DataSet_AppendKeys.append(tempString)            
        elif i==keys_list[1]:
            tempString = "IM_" + i[j]
            Images_AppendKeys.append(tempString)
        else:
            tempString = "IF_" + i[j]
            AddInfo_AppendKeys.append(tempString)            

all_keys = DataSet_AppendKeys + Images_AppendKeys + AddInfo_AppendKeys

# columns 입력
dataFrame.columns = all_keys
ran = list(range(0,len(dataFrame.index)))
dataFrame.index = ran


# In[5]:


add_key = ['ownercode', 'Type size code', 'BIC_HORIZONTAL', 'BIC_VERTICAL',
                   'YT_HEADER', 'YT_CHASSIS_EMPTY', 'YT_CHASSIS_HALF', 'CONTAINER_20FT', 'CONTAINER_40FT', 'TANK_20FT', 'TANK_40FT']
YT_key = ['YT_HEADER', 'YT_CHASSIS_EMPTY', 'YT_CHASSIS_HALF', 'CONTAINER_20FT', 'CONTAINER_40FT', 'TANK_20FT', 'TANK_40FT']
dataFrame_add = None
df_column = []
dict_add={}

for index in range(0,len(files)):
    strencoding = "EUC-KR"
    with open(files[index], encoding="EUC-KR") as tmpfile:        
        try:       
            linedata = tmpfile.readline()  
        except:            
            strencoding = 'utf-8-sig'
            
    with open(files[index], encoding = strencoding) as openFile:        
        json_lodaedData = json.load(openFile)
        
        for item in json_lodaedData['annotations']:
            if item['bbox']['id'] == "BBX_01" :
                for i in add_key:
                    if i not in YT_key:
                        updateKeyValue = {'{}'.format(i) : None}
                        dict_add.update(updateKeyValue)
                    if i in YT_key:
                        updateKeyValue = {'{}'.format(i) : '0'}
                        dict_add.update(updateKeyValue)
            if json_lodaedData['addinfo']['dataregion'] == '0':
                if item['bbox']['classid']=='BIC' and re.match('[A-Z]{4}', item['bbox']['text']):
                    dict_add['ownercode'] = item['bbox']['text'][:3]
                if item['bbox']['classid']=='TYPE SIZE':
                    dict_add['Type size code'] = item['bbox']['text']
                try:
                    if re.match('0', item['bbox']['bicdirection']):
                        dict_add['BIC_HORIZONTAL'] = '1'
                        dict_add['BIC_VERTICAL'] = '0'
                    if re.match('1', item['bbox']['bicdirection']):
                        dict_add['BIC_HORIZONTAL'] = '0'
                        dict_add['BIC_VERTICAL'] = '1'
                except KeyError:
                    if re.match('1', str(dict_add['BIC_HORIZONTAL'])) or re.match('1', str(dict_add['BIC_VERTICAL'])):
                        pass
                    else:
                        dict_add['BIC_HORIZONTAL'] = '0'
                        dict_add['BIC_VERTICAL'] = '0'
            else:
                lis_counts = []
                for item in json_lodaedData["annotations"]:
                    for x in item['bbox'].values():
                        if x in YT_key:
                            lis_counts.append(x)
                    YT_counts = dict(collections.Counter(lis_counts))
                    dict_add.update(YT_counts)
                    

            
        DataDictionaryList = [dict_add]

        extendList = []
        df_columns=list(dict_add.keys())
        for dictionaryValue in DataDictionaryList:
            sourcelist = list(dictionaryValue.values())
            extendList.extend(sourcelist)

        dataFrame_add = pd.concat([pd.DataFrame(extendList).transpose(), dataFrame_add])

for i in df_columns:
    a = "IF_" + i
    df_column.append(a)
dataFrame_add.columns = df_column
ran = list(range(0,len(dataFrame_add.index)))
dataFrame_add.index = ran


# In[9]:


df = dataFrame.join(dataFrame_add)
df.to_csv("{}/makefromJson.csv".format(targetDirectory), sep=",", index=True, encoding="UTF-8-sig")

