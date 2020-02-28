#!/usr/bin/env python
# coding: utf-8

import pandas as pd

smartva = pd.read_csv("demodata.csv", low_memory=False)
list1=[]
lcol = smartva.columns.tolist()
for i in range(0,len(lcol)):
    lcol[i]=lcol[i].lower()
    if len(lcol[i].split("-"))>1:      
        st2= lcol[i].split("-")[len(lcol[i].split("-"))-1]
        list1.append(st2)
    else:
        st2= lcol[i].split(":")[len(lcol[i].split(":"))-1]
        list1.append(st2)
    
    #print(c)
list1
smartva.columns = list1


smartva2= smartva

def convert_yes_no_q():
    col1 = []
    col2 = []
    
    #create new columns
    for key, value in YES_NO_QUESTIONS.items():
        smartva2[value.lower()]=''
    
    #assign values to new column
    for key, value in YES_NO_QUESTIONS.items():    
        if key in smartva2.columns.tolist():
            smartva2[value.lower()][(smartva2[key]!='') & (pd.notna(smartva2[key]))] = smartva2[key][(smartva2[key]!='') & (pd.notna(smartva2[key]))]    
            smartva2[value.lower()]=smartva2[value.lower()].apply(checkYesNo)
        else:
            print("Column Not found: key "+key+" val "+str(value))

def checkYesNo(val):
    if val==1:
        return 'yes'
    elif val==0:
        return 'no'
    elif val==8:
        return 'dk'
    elif val==9:
        return 'ref'
    else:
        return ''

def recode_questions_q():
    col1 = []
    col2 = []
    for key, value in RECODE_QUESTIONS.items():
        col1.append(key)
    
    #create new columns
    for i in range(0,len(col1)):    
        str1=str(col1[i])
        str2 = str1[str.index(str1.lower(),'id'):str.index(str1,')')-1]
        smartva2[str2.lower()]=''
    
    #assign values to new column
    for key, value in RECODE_QUESTIONS.items():
        str1=str(key)
        str2 = str1[str.index(str1.lower(),'id'):str.index(str1,')')-1]
        str3 = str1[str.index(str1.lower(),'(')+2:str.index(str1,',')-1]
        #print(str3)
        for key1, value1 in value.items():       
            smartva2[str2.lower()][smartva2[str3]==value1] = key1    


def rename_questions_q():

    #create new columns
    for key, value in RENAME_QUESTIONS.items():
        smartva2[value.lower()]=''
        
    #assign values to new column
    for key1, value1 in RENAME_QUESTIONS.items():
        if key1 in smartva2.columns.tolist():
            smartva2[value1.lower()]=smartva2[key1.lower()]
        else:
            print("Column Not found: key "+key1+" val "+str(value1))

def reverse_one_hot_multiselect_q():
    for key, value in REVERSE_ONE_HOT_MULTISELECT.items():
        
        #create new columns
        str1 = REVERSE_ONE_HOT_MULTISELECT[key]
        for x in str1.keys():
            if x.lower() in smartva2.columns.tolist():
                print("column found")
            else:
                smartva2[x.lower()]=''
            
            
    #assign values to new column
    for key, value in REVERSE_ONE_HOT_MULTISELECT.items():
        str1 = REVERSE_ONE_HOT_MULTISELECT[key]
        for x in str1.keys():
            if key in smartva2.columns.tolist():
                if str1[x]==1 or str(str1[x])=='1':
                    smartva2[x.lower()][(smartva2[key].astype(str).str.contains(str(str1[x]))) & ~(smartva2[key].astype(str).str.contains('11')) ] = 'yes'
                elif str1[x]==11 or str(str1[x])=='11':
                    smartva2[x.lower()][(smartva2[key].astype(str).str.contains(str(str1[x])))  ] = 'yes'
                else:
                    smartva2[x.lower()][(smartva2[key].astype(str).str.contains(str(str1[x]))) ] = 'yes'       
            else:
                print("column not found2 "+key.lower())


def recode_multiselect_q():
    for key, value in RECODE_MULTISELECT.items():
        str1=str(key)
        str4 = RECODE_MULTISELECT[key]
        who = str1[str.index(str1.lower(),'id'):str.index(str1,')')-1]
        phmrc = str1[str.index(str1.lower(),'(')+2:str.index(str1,',')-1]
        
        #create new columns
        if who.lower() in smartva2.columns.tolist():
            smartva2[who.lower()]=smartva2[phmrc]
        else:
            smartva2[who.lower()]=smartva2[phmrc]

        #col2.append(value)
        for x in str4.items():
            if phmrc in smartva2.columns.tolist():
                #print("column found2")
                opt = x[0]
                optval = x[1]
                if str(optval)=='1':
                    smartva2[who.lower()]= smartva2[who.lower()].replace(regex=['1'], value=opt)                    
                elif str(optval)=='11':
                    smartva2[who.lower()]= smartva2[who.lower()].replace(regex=['11'], value=opt)
                else:
                    smartva2[who.lower()]= smartva2[who.lower()].replace(regex=[str(optval)], value=opt)
            else:
                print("column not found2 "+phmrc.lower())


def one_hot_from_multiselect():
    for key, value in ONE_HOT_FROM_MULTISELECT.items():
        #col1.append(key)
        phmrc=str(key)
        str4 = str(ONE_HOT_FROM_MULTISELECT[key])
        who = str4[str.index(str4.lower(),'id'):str.index(str4,',')-1]
        val = str4[str.index(str4.lower(),',')+3:str.index(str4,')')-1]
        
        #create new columns
        if who.lower() in smartva2.columns.tolist():
            print("column found")
        else:
            #print("column not found "+who.lower())
            smartva2[who.lower()]=''
        #print("who "+str4+"---"+val)
        if phmrc in smartva2.columns.tolist():
            smartva2[who.lower()][smartva2[phmrc]==1] = smartva2[who.lower()][smartva2[phmrc]==1]+val+" "   
        else:
            print("column not found2 "+phmrc.lower())



def other_custom_mappings():
    #create new columns with blank as deafult
    smartva2['id10221'] = ''
    smartva2['id10221'] = ''
    smartva2['id10303']  =''
    smartva2['id10309'] = ''
    smartva2['id10332'] = ''
    smartva2['id10415']  =''
    smartva2['id10366']  =''
    smartva2['id10366']  =''
    smartva2['id10352_a'] = ''
    smartva2['id10352_a'] =''
    smartva2['id10352_b'] = ''
    smartva2['id10382'] = ''
    smartva2['id10161_0'] = ''
    smartva2['id10161'] = ''
    smartva2['id10167_a'] = ''
    smartva2['id10167_b'] = ''
    smartva2['id10167'] = ''
    smartva2['id10285'] = ''
    smartva2['id10183'] = ''
    smartva2['id10234'] = ''
    smartva2['id10232_a'] = ''
    smartva2['id10232'] = ''
    smartva2['id10359'] = ''
    smartva2['id10358'] = ''
    smartva2['id10148_a'] = ''
    smartva2['id10148_b'] = ''
    smartva2['id10148'] = ''
    smartva2['id10154_a'] = ''
    smartva2['id10154'] = ''
    smartva2['age_group']=''
    
    smartva2['id10362'] =''
    smartva2['id10363'] =''
    smartva2['id10364'] =''
    smartva2['id10365'] =''
    
    smartva2['id10162'] =''
    smartva2['id10163'] =''

    smartva2['id10342'] =''
    smartva2['id10343'] =''
    smartva2['id10344'] =''
    smartva2['id10105'] =''
    smartva2['id10106'] =''
    
    smartva2['id10216'] =''
    smartva2['id10216_a'] =''
    smartva2['id10216_b'] =''
    smartva2['id10178'] =''
    smartva2['id10179'] =''
    smartva2['id10179_1'] =''
    smartva2['id10021'] =''
    smartva2['id10023'] =''
    
    #do custom mapping assigments
    smartva2['id10221'][smartva2['adult_2_83']==6] = smartva2['adult_2_83a'][smartva2['adult_2_83']==6]
    smartva2['id10221'][smartva2['adult_2_83']==5] = (smartva2['adult_2_83b'][smartva2['adult_2_83']==5])*30
    smartva2['id10303'][smartva2['adult_3_8']==3] = smartva2['adult_3_8a'][smartva2['adult_3_8']==6]
    smartva2['id10309'][smartva2['adult_3_11']==2] = smartva2['adult_3_11a'][smartva2['adult_3_11']==2]
    smartva2['id10332'][smartva2['adult_3_16']==5] = smartva2['adult_3_16a'][smartva2['adult_3_16']==5]
    smartva2['id10415'][smartva2['adult_4_4']==1] = smartva2['adult_4_4a'][smartva2['adult_4_4']==1]
    smartva2['id10366'][smartva2['child_1_8']==1] = (smartva2['child_1_8a'][smartva2['child_1_8']==1])/1000 #grammes
    smartva2['id10366'][smartva2['child_1_8']==2] = (smartva2['child_1_8b'][smartva2['child_1_8']==2]) #Kg
    smartva2['id10352_a'][smartva2['child_1_20']==4] = (smartva2['child_1_20a'][smartva2['child_1_20']==4])/30.5  #days
    smartva2['id10352_a'][smartva2['child_1_20']==2] = (smartva2['child_1_20b'][smartva2['child_1_20']==2])  #months
    smartva2['id10352_b'][smartva2['child_1_20']==1] = (smartva2['child_1_20c'][smartva2['child_1_20']==1])  #years
    smartva2['id10382'][smartva2['child_2_10']==5] = (smartva2['child_2_10a'][smartva2['child_2_10']==5])
    smartva2['id10161_0'][smartva2['child_3_19']==4] = (smartva2['child_3_19a'][smartva2['child_3_19']==4])
    smartva2['id10161'][smartva2['child_3_19']==4] = (smartva2['child_3_19a'][smartva2['child_3_19']==4])
    smartva2['id10167_a'][smartva2['child_3_22']==4] = (smartva2['child_3_22a'][smartva2['child_3_22']==4])
    smartva2['id10167_b'][smartva2['child_3_22']==4] = (smartva2['child_3_22a'][smartva2['child_3_22']==4])
    smartva2['id10167'][smartva2['child_3_22']==4] = (smartva2['child_3_22a'][smartva2['child_3_22']==4])
    smartva2['id10285'][smartva2['child_3_30']==4] = (smartva2['child_3_30a'][smartva2['child_3_30']==4])
    smartva2['id10183'][smartva2['child_4_7']==1] = (smartva2['child_4_7a'][smartva2['child_4_7']==1])
    smartva2['id10234'][smartva2['child_4_33']==4] = (smartva2['child_4_33a'][smartva2['child_4_33']==4])
    smartva2['id10232_a'][smartva2['adult_2_15']==4] = (smartva2['adult_2_15a'][smartva2['adult_2_15']==4])
    smartva2['id10232'][smartva2['adult_2_15']==4] = (smartva2['adult_2_15a'][smartva2['adult_2_15']==4])
    smartva2['id10359'][smartva2['child_1_5']==4] = (smartva2['child_1_5a'][smartva2['child_1_5']==4]) #days
    smartva2['id10358'][smartva2['child_1_5']==2] = (smartva2['child_1_5b'][smartva2['child_1_5']==2]) #months
    smartva2['id10148_a'][smartva2['child_4_2']==2] = (smartva2['child_4_2a'][smartva2['child_4_2']==2]) #days
    smartva2['id10148_b'][smartva2['child_4_2']==2] = (smartva2['child_4_2a'][smartva2['child_4_2']==2]) #days
    smartva2['id10148'][smartva2['child_4_2']==2] = (smartva2['child_4_2a'][smartva2['child_4_2']==2]) #days
    smartva2['id10148_a'][smartva2['child_4_2']==1] = 0 #days
    smartva2['id10148_b'][smartva2['child_4_2']==1] = 0 #days
    smartva2['id10148'][smartva2['child_4_2']==1] = 0 #days
    smartva2['id10154_a'][smartva2['child_4_13']==4] = (smartva2['child_4_13a'][smartva2['child_4_13']==4])
    smartva2['id10154'][smartva2['child_4_13']==4] = (smartva2['child_4_13a'][smartva2['child_4_13']==4])
    smartva2['age_group'][smartva2['gen_5_4d']==1] ='neonate'
    smartva2['age_group'][smartva2['gen_5_4d']==2] ='child'
    smartva2['age_group'][smartva2['gen_5_4d']==3] ='adult'
    smartva2['age_group'][smartva2['gen_5_4d']==8] ='ref'
    smartva2['age_group'][smartva2['gen_5_4d']==9] ='dk'

    
    smartva2['id10362'][smartva2['child_1_7']==3] ='yes'
    smartva2['id10363'][smartva2['child_1_7']==2] ='yes'
    smartva2['id10364'][smartva2['child_1_7']==1] ='yes'
    smartva2['id10365'][smartva2['child_1_7']==4] ='yes'
    smartva2['id10342'][smartva2['child_2_17']==2] ='yes'
    smartva2['id10343'][smartva2['child_2_17']==1] ='yes'
    smartva2['id10344'][smartva2['child_2_17']==4] ='yes'
    
    smartva2['id10105'][smartva2['child_3_8']==4] ='no'
    smartva2['id10106'][smartva2['child_3_8']==1] = 4
    smartva2['id10106'][smartva2['child_3_8']==2] = 10
    smartva2['id10106'][smartva2['child_1_7']==4] = 35
    
    smartva2['id10216_a'][smartva2['child_4_27']==1] =3
    smartva2['id10216'][smartva2['child_4_27']==1] =3
    smartva2['id10216_a'][smartva2['child_4_27']==2] =12
    smartva2['id10216'][smartva2['child_4_27']==2] =12
    smartva2['id10216_b'][smartva2['child_4_27']==3] =1
    smartva2['id10216'][smartva2['child_4_27']==3] = 24
    
    smartva2['id10178'][smartva2['adult_2_44']==1] =15
    smartva2['id10179'][smartva2['adult_2_44']==1] =0
    smartva2['id10178'][smartva2['adult_2_44']==2] =40
    smartva2['id10179'][smartva2['adult_2_44']==2] =2
    smartva2['id10179_1'][smartva2['adult_2_44']==3] =1
    
    smartva2['ageinyears'] = smartva2['gen_5_4a'] 
    smartva2['ageinyears2'] = smartva2['gen_5_4a'] 
    smartva2['ageinmonths'] = smartva2['gen_5_4b'] 
    smartva2['ageindays'] = smartva2['gen_5_4c'] 
    
    smartva2['ischild'] = smartva2['child'] 
    smartva2['isneonatal'] = smartva2['neonate'] 
    smartva2['isadult'] = smartva2['adult'] 
    
    smartva2['gen_5_1a'][pd.isna(smartva2['gen_5_1a'])]='9999'
    smartva2['gen_5_1b'][pd.isna(smartva2['gen_5_1b'])]='99'
    smartva2['gen_5_1c'][pd.isna(smartva2['gen_5_1c'])]='99'
    smartva2['gen_5_3a'][pd.isna(smartva2['gen_5_3a'])]='9999'
    smartva2['gen_5_3b'][pd.isna(smartva2['gen_5_3b'])]='99'
    smartva2['gen_5_3c'][pd.isna(smartva2['gen_5_3c'])]='99'
    smartva2['gen_5_1a']=pd.to_numeric(smartva2['gen_5_1a'], downcast="integer")
    smartva2['gen_5_1b']=pd.to_numeric(smartva2['gen_5_1b'], downcast="integer")
    smartva2['gen_5_1c']=pd.to_numeric(smartva2['gen_5_1c'], downcast="integer")
    smartva2['gen_5_3a']=pd.to_numeric(smartva2['gen_5_3a'], downcast="integer")
    smartva2['gen_5_3b']=pd.to_numeric(smartva2['gen_5_3b'], downcast="integer")
    smartva2['gen_5_3c']=pd.to_numeric(smartva2['gen_5_3c'], downcast="integer")
    smartva2['id10021'] = (smartva2['gen_5_1a']).astype(str)+"-"+(smartva2['gen_5_1b']).astype(str)+"-"+(smartva2['gen_5_1c']).astype(str)
    smartva2['id10023'] = (smartva2['gen_5_3a']).astype(str)+"-"+(smartva2['gen_5_3b']).astype(str)+"-"+(smartva2['gen_5_3c']).astype(str)




def initializeOtherCols():
    #create new columns; these are columns required by InterVA but there is no mapping in the PHMRC Shortened questionnaire
    smartva['age_adult'] = '.'
    smartva['age_child_unit'] = '.'
    smartva['age_child_days'] = '.'
    smartva['age_child_months'] = '.'
    smartva['age_neonate_days'] = '.'
    smartva['age_child_years'] = '.'

    smartva['id10022'] = ''
    smartva['id10093'] = ''
    smartva['id10120'] = ''
    smartva['id10139'] = ''
    smartva['id10154'] = ''
    smartva['id10169'] = ''
    smartva['id10182'] = ''
    smartva['id10197'] = ''
    smartva['id10212'] = ''
    smartva['id10227'] = ''
    smartva['id10245'] = ''
    smartva['id10254'] = ''
    smartva['id10274'] = ''
    smartva['id10298'] = ''
    smartva['id10317'] = ''
    smartva['id10324'] = ''
    smartva['id10337'] = ''
    smartva['id10354'] = ''
    smartva['id10367'] = ''
    smartva['id10388'] = ''
    smartva['id10400'] = ''
    smartva['id10420'] = ''
    smartva['id10427'] = ''
    smartva['id10455'] = ''
    smartva['id10004'] = ''
    smartva['id10288'] = ''
    smartva['id10059'] = ''
    smartva['id10094'] = ''
    smartva['id10123'] = ''
    smartva['id10140'] = ''
    smartva['id10154'] = ''
    smartva['id10170'] = ''
    smartva['id10182'] = ''
    smartva['id10201'] = ''
    smartva['id10213'] = ''
    smartva['id10232'] = ''
    smartva['id10246'] = ''
    smartva['id10259'] = ''
    smartva['id10275'] = ''
    smartva['id10306'] = ''
    smartva['id10318'] = ''
    smartva['id10326'] = ''
    smartva['id10338'] = ''
    smartva['id10355'] = ''
    smartva['id10368'] = ''
    smartva['id10389'] = ''
    smartva['id10406'] = ''
    smartva['id10421'] = ''
    smartva['id10428'] = ''
    smartva['id10456'] = ''
    smartva['id10108'] = ''
    smartva['id10132'] = ''
    smartva['id10152'] = ''
    smartva['id10168'] = ''
    smartva['id10178'] = ''
    smartva['id10195'] = ''
    smartva['id10211'] = ''
    smartva['id10226'] = ''
    smartva['id10244'] = ''
    smartva['id10253'] = ''
    smartva['id10273'] = ''
    smartva['id10283'] = ''
    smartva['id10323'] = ''
    smartva['id10334'] = ''
    smartva['id10347'] = ''
    smartva['id10365'] = ''
    smartva['id10387'] = ''
    smartva['id10398'] = ''
    smartva['id10419'] = ''
    smartva['id10426'] = ''
    smartva['id10454'] = ''
    smartva['id10082'] = ''
    smartva['id10095'] = ''
    smartva['id10128'] = ''
    smartva['id10142'] = ''
    smartva['id10158'] = ''
    smartva['id10171'] = ''
    smartva['id10184_units'] = ''
    smartva['id10184_a'] = ''
    smartva['id10184_b'] = ''
    smartva['id10184_c'] = ''
    smartva['id10205'] = ''
    smartva['id10215'] = ''
    smartva['id10236'] = ''
    smartva['id10248'] = ''
    smartva['id10262'] = ''
    smartva['id10276'] = ''
    smartva['id10310'] = ''
    smartva['id10319'] = ''
    smartva['id10327'] = ''
    smartva['id10340'] = ''
    smartva['id10361'] = ''
    smartva['id10369'] = ''
    smartva['id10391'] = ''
    smartva['id10408'] = ''
    smartva['id10422'] = ''
    smartva['id10450'] = ''
    smartva['id10457'] = ''
    smartva['id10087'] = ''
    smartva['id10096'] = ''
    smartva['id10129'] = ''
    smartva['id10143'] = ''
    smartva['id10161'] = ''
    smartva['id10173'] = ''
    smartva['id10188'] = ''
    smartva['id10207'] = ''
    smartva['id10216'] = ''
    smartva['id10237'] = ''
    smartva['id10249'] = ''
    smartva['id10266'] = ''
    smartva['id10277'] = ''
    smartva['id10313'] = ''
    smartva['id10320'] = ''
    smartva['id10330'] = ''
    smartva['id10342'] = ''
    smartva['id10362'] = ''
    smartva['id10376'] = ''
    smartva['id10393'] = ''
    smartva['id10411'] = ''
    smartva['id10423'] = ''
    smartva['id10451'] = ''
    smartva['id10458'] = ''
    smartva['id10092'] = ''
    smartva['id10106'] = ''
    smartva['id10131'] = ''
    smartva['id10148'] = ''
    smartva['id10167'] = ''
    smartva['id10176'] = ''
    smartva['id10193'] = ''
    smartva['id10210'] = ''
    smartva['id10225'] = ''
    smartva['id10243'] = ''
    smartva['id10251'] = ''
    smartva['id10270'] = ''
    smartva['id10282'] = ''
    smartva['id10316'] = ''
    smartva['id10322'] = ''
    smartva['id10333'] = ''
    smartva['id10344'] = ''
    smartva['id10364'] = ''
    smartva['id10384'] = ''
    smartva['id10394'] = ''
    smartva['id10418'] = ''
    smartva['id10425'] = ''
    smartva['id10453'] = ''
    smartva['id10091'] = ''
    smartva['id10098'] = ''
    smartva['id10130'] = ''
    smartva['id10144'] = ''
    smartva['id10165'] = ''
    smartva['id10175'] = ''
    smartva['id10190_units'] = ''
    smartva['id10190_a'] = ''
    smartva['id10190_b'] = ''
    smartva['id10198'] = ''
    smartva['id10209'] = ''
    smartva['id10223'] = ''
    smartva['id10242'] = ''
    smartva['id10250'] = ''
    smartva['id10269'] = ''
    smartva['id10279'] = ''
    smartva['id10314'] = ''
    smartva['id10321'] = ''
    smartva['id10331'] = ''
    smartva['id10343'] = ''
    smartva['id10363'] = ''
    smartva['id10383'] = ''
    smartva['id10394'] = ''
    smartva['id10413'] = ''
    smartva['id10424'] = ''
    smartva['id10452'] = ''
    smartva['id10459'] = ''


#these are mappings showing relationship between PHMRC questions and WHO VA 2016 Questions
YES_NO_QUESTIONS = {
    'adult_5_1': 'Id10077',
    'adult_5_3': 'Id10099',
    'adult_5_4': 'Id10100',
    'child_4_47': 'Id10077',
    'child_4_49': 'Id10100',

    'adult_1_1a': 'Id10135',
    'adult_1_1c': 'Id10137',
    'adult_1_1m': 'Id10138',
    'adult_1_1g': 'Id10134',
    'adult_1_1h': 'Id10136',
    'adult_1_1i': 'Id10133',
    'adult_1_1d': 'Id10125',
    'adult_1_1l': 'Id10141',
    'adult_1_1n': 'Id10127',

    'adult_2_2': 'Id10147',
    'adult_2_7': 'Id10233',
    'adult_2_10': 'Id10228',
    'adult_2_11': 'Id10229',
    'adult_2_13': 'Id10230',
    'adult_2_14': 'Id10231',
    'adult_2_21': 'Id10265',
    'adult_2_25': 'Id10247',
    'adult_2_27': 'Id10252',
    'adult_2_29': 'Id10255',
    'adult_2_30': 'Id10256',
    'adult_2_31': 'Id10257',
    'adult_2_32': 'Id10153',
    'adult_2_34': 'Id10155',
    'adult_2_35': 'Id10157',
    'adult_2_36': 'Id10159',
    'adult_2_43': 'Id10174',
    'adult_2_47': 'Id10181',
    'adult_2_50': 'Id10186',
    'adult_2_51': 'Id10187',
    'adult_2_52': 'Id10224',
    'adult_2_53': 'Id10189',
    'adult_2_55': 'Id10191',
    'adult_2_56': 'Id10192',
    'adult_2_57': 'Id10261',
    'adult_2_60': 'Id10264',
    'adult_2_61': 'Id10194',
    'adult_2_64': 'Id10200',
    'adult_2_67': 'Id10204',
    'adult_2_72': 'Id10208',
    'adult_2_74': 'Id10214',
    'adult_2_75': 'Id10217',
    'adult_2_77': 'Id10218',
    'adult_2_82': 'Id10219',
    'adult_2_84': 'Id10222',
    'adult_2_85': 'Id10258',

    'adult_3_1': 'Id10294',
    'adult_3_2': 'Id10295',
    'adult_3_3a': 'Id10296',
    'adult_3_3': 'Id10299',
    'adult_3_4': 'Id10300',
    'adult_3_5': 'Id10297',
    'adult_3_6': 'Id10301',
    'adult_3_7': 'Id10302',
    'adult_3_9': 'Id10304',
    'adult_3_10': 'Id10305',
    'adult_3_12': 'Id10335',
    'adult_3_13': 'Id10325',
    'adult_3_14': 'Id10328',
    'adult_3_15': 'Id10312',
    'adult_3_17': 'Id10336',
    'adult_3_18': 'Id10315',
    'adult_3_19': 'Id10329',

    'adult_4_1': 'Id10412',

    'adult_6_1': 'Id10432',
    'adult_6_3a': 'Id10435',
    'adult_6_4': 'Id10437',
    'adult_6_5': 'Id10438',

    'child_1_3': 'Id10356',
    'child_1_12': 'Id10104',
    'child_1_13': 'Id10109',
    'child_1_14': 'Id10110',
    'child_1_16': 'Id10115',
    'child_1_17': 'Id10116',
    'child_1_18': 'Id10370',

    'child_2_4': 'Id10377',

    'child_3_2': 'Id10370',
    'child_3_4': 'Id10111',
    'child_3_5': 'Id10112',
    'child_3_6': 'Id10113',
    'child_3_7': 'Id10105',
    'child_3_9': 'Id10107',
    'child_3_11': 'Id10271',
    'child_3_12': 'Id10272',
    'child_3_17': 'Id10159',
    'child_3_20': 'Id10166',
    'child_3_23': 'Id10172',
    'child_3_29': 'Id10284',
    'child_3_32': 'Id10286',
    'child_3_33': 'Id10281',
    'child_3_35': 'Id10287',
    'child_3_40': 'Id10240',
    'child_3_47': 'Id10289',
    'child_3_49': 'Id10290',

    'child_4_1': 'Id10147',
    'child_4_3': 'Id10149',
    'child_4_6': 'Id10181',
    'child_4_9': 'Id10185',
    'child_4_12': 'Id10153',
    'child_4_14': 'Id10156',
    'child_4_16': 'Id10159',
    'child_4_18': 'Id10166',
    'child_4_20': 'Id10172',
    'child_4_25': 'Id10220',
    'child_4_26': 'Id10214',
    'child_4_28': 'Id10208',
    'child_4_29': 'Id10278',
    'child_4_30': 'Id10233',
    'child_4_38': 'Id10238',
    'child_4_39': 'Id10267',
    'child_4_40': 'Id10200',
    'child_4_41': 'Id10268',
    'child_4_42': 'Id10256',
    'child_4_44': 'Id10241',
    'child_4_46': 'Id10239',

    'child_5_0a': 'Id10435',
    'child_5_1': 'Id10432',
    'child_5_4': 'Id10437',
    'child_5_5': 'Id10438',
    'child_5_10': 'Id10462',
    'child_5_17': 'Id10445',
    'child_5_19': 'Id10446',
}

RECODE_QUESTIONS = {
    ('gen_5_2', 'Id10019'): {'male': 1, 'female': 2, 'undetermined': 8},
    ('adult_2_4', 'Id10150'): {'mild': 1, 'moderate': 2, 'severe': 3,
                               'DK': 9, 'Ref': 8},
    ('adult_2_5', 'Id10151'): {'continuous': 1, 'on_and_off': 2, 'nightly': 3,
                               'DK': 9, 'Ref': 8},
    ('adult_2_9', 'Id10235'): {'face': 1, 'trunk': 2, 'extremities': 3,
                               'everywhere': 4, 'DK': 9, 'Ref': 8},
    ('adult_2_22', 'Id10266_units'): {'days': 4, 'months': 2, 'DK': 9, 'ref': 8},
    ('adult_2_26', 'Id10248_units'): {'days': 4, 'months': 2, 'DK': 9, 'ref': 8},
    ('adult_2_58', 'Id10262_units'): {'days': 4, 'months': 2, 'DK': 9, 'ref': 8},
    ('adult_2_62', 'id10196_unit'): {'hours': 5, 'days': 4, 'months': 2, 'DK': 9,
                                     'ref': 8},
    ('adult_2_65', 'Id10201_unit'): {'days': 4, 'months': 2, 'DK': 9, 'ref': 8},
    ('adult_2_59', 'Id10263'): {'solids': 1, 'liquids': 2, 'both': 3, 'DK': 9,
                                'Ref': 8},
    ('adult_2_63', 'Id10199'): {'upper_abdomen': 1, 'lower_abdomen': 2,
                                'upper_lower_abdomen': 9, 'DK': 9, 'Ref': 8},
    ('adult_2_66', 'Id10203'): {'rapidly': 1, 'slowly': 2, 'DK': 9, 'Ref': 8},
    ('adult_2_68', 'Id10205_unit'): {'days': 4, 'months': 2, 'DK': 9, 'ref': 8},
    ('adult_4_2', 'Id10414'): {
        'cigarettes': 1,
        'pipe': 2,
        'chewing_tobacco': 3,
        'local_form_of_tobacco': 4,
        'other': 11,
    },

    ('child_1_4', 'Id10357'): {'during_delivery': 1, 'after_delivery': 2,
                               'DK': 9, 'Ref': 8},
    ('child_1_6', 'Id10360'): {
        'hospital': 1,
        'other_health_facility': 2,
        'home': 4,
        'on_route_to_hospital_or_facility': 3,
        'other': 5,
        'DK': 9,
        'Ref': 8,
    },
    ('child_1_11', 'Id10114'): {'yes': 2, 'no': 1, 'dk': 9, 'ref': 8},
    ('child_2_8', 'Id10385'): {'green_or_brown': 1, 'clear': 2, 'other': 3,
                               'dk': 9, 'ref': 8},
    ('child_2_15', 'Id10339'): {
        'Doctor': 1,
        'Midwife': 2,
        'Nurse': 2,
        'Relative': 3,
        'Self_mother': 4,
        'Traditional_birth_attendant': 5,
        'Other': 6,
        'DK': 9,
        'ref': 8,
    },
    ('child_2_15', 'Id10339'): {
        'Doctor': 1,
        'Midwife': 2,
        'Nurse': 2,
        'Relative': 3,
        'Self_mother': 4,
        'Traditional_birth_attendant': 5,
        'Other': 6,
        'DK': 9,
        'ref': 8,
    },
    ('child_4_4', 'Id10150'): {'mild': 1, 'moderate': 2, 'severe': 3,
                               'DK': 9, 'Ref': 8},
}


RENAME_QUESTIONS = {
    'gen_6_7': 'Id10073',
    'gen_5_0': 'Id10017',
    'gen_5_0a': 'Id10018',
    'interviewdate': 'Id10012',
    'gen_2_3a': 'Id10057',
    
    'adult_2_22a': 'Id10266_a',
    'adult_2_22b': 'Id10266_b',
    'adult_2_26a': 'Id10248_a',
    'adult_2_26b': 'Id10248_b',
    'adult_2_58a': 'Id10262_a',
    'adult_2_58b': 'Id10262_b',
    'adult_2_62a': 'Id10196',
    'adult_2_62b': 'Id10197_a',
    'adult_2_62c': 'Id10198',
    'adult_2_65a': 'Id10201_a',
    'adult_2_65b': 'Id10202',
    'adult_2_68a': 'Id10205_a',
    'adult_2_68b': 'Id10206',
    'adult_2_83a': 'Id10221',
    'adult_3_8a': 'Id10303',
    'adult_3_11a': 'Id10309',
    'adult_3_16a': 'Id10332',
    'adult_4_4a': 'Id10415',
    'adult_6_3b': 'Id10436',
    'adult_6_8': 'Id10444',
    'adult_6_11': 'Id10464',
    'adult_6_12': 'Id10466',
    'adult_6_13': 'Id10468',
    'adult_6_14': 'Id10470',
    'adult_6_15': 'Id10472',
    'adult_7_c': 'Id10476',
    'child_1_8a': 'Id10366',
    'child_1_20a': 'Id10351',
    'child_1_20b': 'Id10352_a',
    'child_1_20c': 'Id10352_b',
    'child_2_10a': 'Id10382',
    'child_3_19a': 'Id10161_0',
    'child_3_22a': 'Id10167_a',
    'child_3_30a': 'Id10285',
    'child_4_7a': 'Id10183',
    'child_4_33a': 'Id10234',
    'child_5_0b': 'Id10436',
    'child_5_9': 'Id10444',
    'child_5_12': 'Id10464',
    'child_5_13': 'Id10466',
    'child_5_14': 'Id10468',
    'child_5_15': 'Id10470',
    'child_5_16': 'Id10472',
    'child_6_c': 'Id10476',
}

"""Create multiselect questions from a series of questions codes as yes/no.
Schema
------
PHMRC_COL: {PHMRC_VALUE: WHO_COL}
"""
REVERSE_ONE_HOT_MULTISELECT = {
    'adult_5_2': {
        'Id10079': 1,
        'Id10083': 2,
        'Id10085': 3,
        'Id10084': 4,
        'Id10086': 5,
        'Id10089': 6,
        'Id10090': 7,
        'Id10097': 11,
    },
    'child_4_48': {
        'Id10079': 1,
        'Id10083': 2,
        'Id10085': 3,
        'Id10084': 4,
        'Id10086': 5,
        'Id10089': 6,
        'Id10090': 7,
        'Id10097': 11,
    },
    'child_1_19': {
        'Id10373': 1,
        'Id10372': 2,
        'Id10371': 3,
    },
    'child_2_1': {
        'Id10399': 1,
        'Id10396': 2,
        'Id10401': 3,
        'Id10397': 4,
        'Id10403': 5,
        'Id10405': 6,
        'Id10404': 7,
        'Id10402': 8,
        'Id10395': 9,
    },
    'child_3_3': {
        'Id10373': 1,
        'Id10372': 2,
        'Id10371': 3,
    },
}

"""Change the values of multiselect questions.
Schema:
(PHMRC_COL, WHO_COL) : {WHO_VALUE: PHMRC_VALUE}
"""
RECODE_MULTISELECT = {
    ('adult_2_9', 'Id10235'): {
        'face': 1,
        'trunk': 2,
        'extremities': 3,
        'everywhere': 4,
        'DK': 9,
        'Ref': 8,
    },
    ('adult_2_87', 'Id10260'): {
        'right_side': 1,
        'left_side': 2,
        'lower_part_of_body': 3,
        'upper_part_of_body': 4,
        'one_leg_only': 5,
        'one_arm_only': 6,
        'whole_body': 7,
        'other': 11,
        'DK': 9,
        'Ref': 8,
    }
}


"""Create a yes/no columns from the value in a multiselect
Schema
------
PHMRC_COL: (WHO_COL, WHO_VALUE)
"""
ONE_HOT_FROM_MULTISELECT = {
    'child_4_23': ('Id10173_nc', 'grunting'),
    'adult_7_1': ('Id10477', 'Chronic_kidney_disease'),
    'adult_7_2': ('Id10477', 'Dialysis'),
    'adult_7_3': ('Id10477', 'Fever'),
    'adult_7_4': ('Id10477', 'Heart_attack'),
    'adult_7_5': ('Id10477', 'Heart_problem'),
    'adult_7_6': ('Id10477', 'Jaundice'),
    'adult_7_7': ('Id10477', 'Liver_failure'),
    'adult_7_8': ('Id10477', 'Malaria'),
    'adult_7_9': ('Id10477', 'Pneumonia'),
    'adult_7_10': ('Id10477', 'Renal_kidney_failure'),
    'adult_7_11': ('Id10477', 'Suicide'),
    'child_6_1': ('Id10478', 'abdomen'),
    'child_6_2': ('Id10478', 'cancer'),
    'child_6_3': ('Id10478', 'dehydration'),
    'child_6_4': ('Id10478', 'dengue'),
    'child_6_5': ('Id10478', 'diarrhea'),
    'child_6_6': ('Id10478', 'fever'),
    'child_6_7': ('Id10478', 'heart_problem'),
    'child_6_8': ('Id10478', 'jaundice'),
    'child_6_9': ('Id10478', 'pneumonia'),
    'child_6_10': ('Id10478', 'rash'),
    'neonate_6_1': ('Id10479', 'asphyxia'),
    'neonate_6_2': ('Id10479', 'incubator'),
    'neonate_6_3': ('Id10479', 'lung_problem'),
    'neonate_6_4': ('Id10479', 'pneumonia'),
    'neonate_6_5': ('Id10479', 'preterm_delivery'),
    'neonate_6_6': ('Id10479', 'respiratory_distress'),
}

"""Fill in unit columns based on the presence of a numeric value.
Schema   
------
PHMRC_COL: (WHO_COL, UNIT)
The unit is the value the PHMRC_COL should take if the value in WHO_COL is
greater than one.   
"""
UNIT_IF_AMOUNT = {
    'adult_2_83': ('Id10221', 6),
    'adult_3_8': ('Id10303', 3),
    'adult_3_11': ('Id10309', 2),
    'adult_3_16': ('Id10332', 5),
    'adult_4_4': ('Id10415', 1),
    'child_1_8': ('Id10366', 1),
    'child_1_20': {'Id10352_a': 2, 'Id10352_b': 1},
    'child_2_10': ('Id10382', 5),
    'child_3_19': ('Id10161_0', 4),
    'child_3_22': ('Id10167_a', 4),
    'child_3_30': ('Id10285', 4),
    'child_4_7': ('Id10183', 1),
    'child_4_33': ('Id10234', 4),
}


"""Convert durations variables where the units do not align across surveys.
Schema
------
(PHMRC_UNIT_COL, PHMRC_VALUE_COL, PHMRC_UNIT): {WHO_VALUE_COL: SCALAR}
The scalar is applied to the WHO value column to convert to the PHMRC unit
specific. The PHMRC unit column is filled if there is a non-zero value in any
of the WHO value columns.
"""
DURATION_CONVERSIONS = {
    ('adult_2_15', 'adult_2_15a', 4): {'Id10232_a': 1, 'Id10232_b': 30},
    ('child_1_5', 'child_1_5a', 4): {'Id10358': 30, 'Id10359': 1,
                                     'Id10359_a': 7},
    ('child_4_2', 'child_4_2a', 1): {'Id10148_b': 1, 'Id10148_c': 30},
    ('child_4_13', 'child_4_13a', 1): {'Id10154_a': 1, 'Id10154_b': 30},
}


def CompleteAndOutput():
    list1=[]
    lcol = smartva2.columns.tolist()
    for i in range(0,len(lcol)):
        if  ("gen_" in lcol[i]):
            exit
        else:
            list1.append(lcol[i])
        #print(c)
    list1
    smartva3 = smartva2[list1]
    smartva3.to_csv("final_who_demo.csv")
    
#Run all functions together
initializeOtherCols()
convert_yes_no_q()
other_custom_mappings()
one_hot_from_multiselect()
recode_multiselect_q()
reverse_one_hot_multiselect_q()
rename_questions_q()
recode_questions_q()
CompleteAndOutput()


#finalize all steps and produce final file

#smartva.columns = list1




