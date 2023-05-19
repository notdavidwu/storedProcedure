from django.shortcuts import render
from django.http import JsonResponse
from django.template import loader
from mark.models import *
from mark.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
import pyodbc
import json
import pandas as pd 
import pymssql

DATABASE_NAME = 'buildVocabulary' 


@csrf_exempt
def getTag(request):
    cursor = connections[DATABASE_NAME].cursor()
    query = "SELECT [token],[tokenID] FROM [Vocabulary] where tokenType='T' order by tokenID"
    cursor.execute(query,[])
    res = cursor.fetchall()
    token = [row[0] for row in res]
    tokenID = [row[1] for row in res]
    connections[DATABASE_NAME].close()
    return JsonResponse({'token':token,'tokenID':tokenID})

@csrf_exempt
def getItemDefinition(request):
    server = '172.31.6.22' 
    database = 'buildVocabulary' 
    username = 'N824' 
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    query = "SELECT * FROM [itemDefinition2] order by itemID"
    cursor.execute(query,[])
    res = cursor.fetchall()
    itemID = [row.itemID for row in res]
    rootID = [row.rootID for row in res]
    itemName = [row.itemName for row in res]
    engName = [row.engName for row in res]
    chtName = [row.chtName for row in res]
    itemType = [row.itemType for row in res]
    conn.close()
    return JsonResponse({'itemID':itemID,
                         'rootID':rootID,
                         'itemName':itemName,
                         'engName':engName,
                         'chtName':chtName,
                         'itemType':itemType,
                         })

@csrf_exempt
def getStasticTable(request):
    server = '172.31.6.22' 
    database = 'buildVocabulary' 
    username = 'N824' 
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    result = {"status":"1"}
    raw = request.body.decode('utf-8')
    try:
        print("in")
        body = json.loads(raw)
        print("in")
        string = body['string']

        
        # number = body['number']
        if string == "":
            raise Exception("輸入不可為空")
        

        

        tokenList = string.split(" ")
        IDList = []
        print(len(tokenList))
        if (len(tokenList) != 3):
            raise Exception("必須輸入3字")
        for i in tokenList:
            query = "select * from Vocabulary where token = ?"
            args = [i]
            cursor.execute(query, args)
            VocabularyData = cursor.fetchone()
            IDList.append(VocabularyData.tokenID)
            
        print("innnnnnnnnnnn")


        
        # query = f'''select  count(distinct a.reportID) as 'numReports', count(*) as 'times', min(a.reportID) as 'exReportID', c.word1, c.word2, c.word3, b.word4, b.word5, b.word6 , a.targetWord1, a.targetWord2, a.targetWord3
		# 					from (
		# 									select a.reportID, a.posStart, b.token as 'targetWord1', c.token as 'targetWord2', d.token as 'targetWord3'
		# 									from (
		# 													select a.reportID, a.posStart, a.tokenID as 'target1', b.tokenID as 'target2', c.tokenID as 'target3'
		# 													from textToken as a inner join textToken as b
		# 																			on a.reportID=b.reportID and b.posStart=(a.posEnd+1) and a.tokenID={IDList[0]} and b.tokenID={IDList[1]}
		# 																	inner join textToken as c
		# 																			on b.reportID=c.reportID and c.posStart=(b.posEnd+1) and c.tokenID={IDList[2]}
		# 												) as a inner join Vocabulary as b on a.target1=b.tokenID
		# 															inner join Vocabulary as c on a.target2=c.tokenID
		# 															inner join Vocabulary as d on a.target3=d.tokenID
		# 								) as a inner join
		# 								(
		# 										select a.reportID, a.posEnd, a.startT4,
		# 														IIF(a.word4=1, b1.extractedValue, b.token) as 'word4',
		# 														IIF(a.word5=1, c1.extractedValue, c.token) as 'word5',
		# 														IIF(a.word6=1, d1.extractedValue, d.token) as 'word6'
		# 										from (
		# 														select a.reportID, c.posEnd, a.tokenID as 'word4', b.tokenID as 'word5', c.tokenID as 'word6', a.posStart as 'startT4', b.posStart as 'startT5', c.posStart as 'startT6'
		# 														from textToken as a inner join textToken as b on a.reportID=b.reportID and b.posStart=(a.posEnd+1)
		# 																		inner join textToken as c on b.reportID=c.reportID and c.posStart=(b.posEnd+1)
		# 													) as a inner join Vocabulary as b on a.word4=b.tokenID
		# 																		left outer join extractedValueFromToken as b1 on a.reportID=b1.reportID and a.startT4=b1.posStart
		# 																inner join Vocabulary as c on a.word5=c.tokenID
		# 																		left outer join extractedValueFromToken as c1 on a.reportID=c1.reportID and a.startT5=c1.posStart
		# 																inner join Vocabulary as d on a.word6=d.tokenID
		# 																		left outer join extractedValueFromToken as d1 on a.reportID=d1.reportID and a.startT6=d1.posStart
		# 								) as b on a.reportID=b.reportID and b.posEnd=(a.posStart-1) inner join
		# 								(
		# 										select a.reportID, a.posEnd,
		# 														IIF(a.word1=1, b1.extractedValue, b.token) as 'word1',
		# 														IIF(a.word2=1, c1.extractedValue, c.token) as 'word2',
		# 														IIF(a.word3=1, d1.extractedValue, d.token) as 'word3'
		# 										from (
		# 														select a.reportID, c.posEnd, a.tokenID as 'word1', b.tokenID as 'word2', c.tokenID as 'word3', a.posStart as 'startT1', b.posStart as 'startT2', c.posStart as 'startT3'
		# 														from textToken as a inner join textToken as b on a.reportID=b.reportID and b.posStart=(a.posEnd+1)
		# 																		inner join textToken as c on b.reportID=c.reportID and c.posStart=(b.posEnd+1)
		# 													) as a inner join Vocabulary as b on a.word1=b.tokenID
		# 																		left outer join extractedValueFromToken as b1 on a.reportID=b1.reportID and a.startT1=b1.posStart
		# 																inner join Vocabulary as c on a.word2=c.tokenID
		# 																		left outer join extractedValueFromToken as c1 on a.reportID=c1.reportID and a.startT2=c1.posStart
		# 																inner join Vocabulary as d on a.word3=d.tokenID
		# 																		left outer join extractedValueFromToken as d1 on a.reportID=d1.reportID and a.startT3=d1.posStart
		# 								) as c on b.reportID=c.reportID and c.posEnd=(b.startT4-1)
		# 				group by a.targetWord1, a.targetWord2, a.targetWord3,
		# 									b.word6, b.word5, b.word4, c.word3, c.word2, c.word1
		# 				order by 9,8,7,6,5,4
        # '''
        # cursor.execute(query,[])
        # print("in")
        # res = cursor.fetchall()
        # print("in")
        # if res != []:
        #     print("resssssssssssssssssssssssssssssssssssssss", res[0])

        # reportID = [row.exReportID for row in res]
        # numReports = [row.numReports for row in res]
        # times = [row.times for row in res]
        # word1 = [row.word1 for row in res]
        # word2 = [row.word2 for row in res]
        # word3 = [row.word3 for row in res]
        # word4 = [row.word4 for row in res]
        # word5 = [row.word5 for row in res]
        # word6 = [row.word6 for row in res]
        # targetWord1 = [row.targetWord1 for row in res]
        # targetWord2 = [row.targetWord2 for row in res]
        # targetWord3 = [row.targetWord3 for row in res]
        # result = {'numReports':numReports,
        #                  'times':times,
        #                  'word1':word1,
        #                  'word2':word2,
        #                  'word3':word3,
        #                  'word4':word4,
        #                  'word5':word5,
        #                  'word6':word6,
        #                  'targetWord1':targetWord1,
        #                  'targetWord2':targetWord2,
        #                  'targetWord3':targetWord3,
        #                  'reportID':reportID,
        #                  'status':"0",
        #                  }
        

        query = '''
        select  a.reportID as 'numReports', a.reportID as 'exReportID', c.word1, c.word2, c.word3, b.word4, b.word5, b.word6 , a.targetWord1, a.targetWord2, a.targetWord3
        from (
                select a.reportID, a.posStart, b.token as 'targetWord1', c.token as 'targetWord2', d.token as 'targetWord3'
                from (
                    select a.reportID, a.posStart, a.tokenID as 'target1', b.tokenID as 'target2', c.tokenID as 'target3'
                    from textToken as a inner join textToken as b
                            on a.reportID=b.reportID and b.posStart=(a.posEnd+1) and a.tokenID=10 and b.tokenID=1
                        inner join textToken as c
                            on b.reportID=c.reportID and c.posStart=(b.posEnd+1) and c.tokenID=11
                    ) as a inner join Vocabulary as b on a.target1=b.tokenID
                        inner join Vocabulary as c on a.target2=c.tokenID
                        inner join Vocabulary as d on a.target3=d.tokenID
                ) as a inner join
                (
                    select a.reportID, a.posEnd, a.startT4,
                        IIF(a.word4=1, b1.extractedValue, b.token) as 'word4',
                        IIF(a.word5=1, c1.extractedValue, c.token) as 'word5',
                        IIF(a.word6=1, d1.extractedValue, d.token) as 'word6'
                    from (
                        select a.reportID, c.posEnd, a.tokenID as 'word4', b.tokenID as 'word5', c.tokenID as 'word6', a.posStart as 'startT4', b.posStart as 'startT5', c.posStart as 'startT6'
                        from textToken as a inner join textToken as b on a.reportID=b.reportID and b.posStart=(a.posEnd+1)
                            inner join textToken as c on b.reportID=c.reportID and c.posStart=(b.posEnd+1)
                    ) as a inner join Vocabulary as b on a.word4=b.tokenID
                            left outer join extractedValueFromToken as b1 on a.reportID=b1.reportID and a.startT4=b1.posStart
                        inner join Vocabulary as c on a.word5=c.tokenID
                            left outer join extractedValueFromToken as c1 on a.reportID=c1.reportID and a.startT5=c1.posStart
                        inner join Vocabulary as d on a.word6=d.tokenID
                            left outer join extractedValueFromToken as d1 on a.reportID=d1.reportID and a.startT6=d1.posStart
                ) as b on a.reportID=b.reportID and b.posEnd=(a.posStart-1) inner join
                (
                    select a.reportID, a.posEnd,
                        IIF(a.word1=1, b1.extractedValue, b.token) as 'word1',
                        IIF(a.word2=1, c1.extractedValue, c.token) as 'word2',
                        IIF(a.word3=1, d1.extractedValue, d.token) as 'word3'
                    from (
                        select a.reportID, c.posEnd, a.tokenID as 'word1', b.tokenID as 'word2', c.tokenID as 'word3', a.posStart as 'startT1', b.posStart as 'startT2', c.posStart as 'startT3'
                        from textToken as a inner join textToken as b on a.reportID=b.reportID and b.posStart=(a.posEnd+1)
                            inner join textToken as c on b.reportID=c.reportID and c.posStart=(b.posEnd+1)
                    ) as a inner join Vocabulary as b on a.word1=b.tokenID
                            left outer join extractedValueFromToken as b1 on a.reportID=b1.reportID and a.startT1=b1.posStart
                        inner join Vocabulary as c on a.word2=c.tokenID
                            left outer join extractedValueFromToken as c1 on a.reportID=c1.reportID and a.startT2=c1.posStart
                        inner join Vocabulary as d on a.word3=d.tokenID
                            left outer join extractedValueFromToken as d1 on a.reportID=d1.reportID and a.startT3=d1.posStart
                ) as c on b.reportID=c.reportID and c.posEnd=(b.startT4-1)
        '''
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        
        res = cursor.fetchall()
        # print(columns)
        # print(res)
        Array = []
        print(len(columns), len(res[0]))
        print("搜尋完畢")
        for i in res:
            Array.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10]])
        print(Array[0], len(Array[0]), len(Array))
        cal = pd.DataFrame(Array,columns=columns)
        # 分組
        grouped = cal.groupby(['targetWord1','targetWord2','targetWord3','word6', 'word5','word4','word3','word2','word1'])

        cal = grouped.agg({'exReportID': lambda x: ','.join(x.astype(str).unique()), 'numReports': lambda x: len(x.unique())}).reset_index()  
        print("分組完畢")
        # 計算每個分組的數量  
        group_count = grouped.size().reset_index(name='count by group')  
        print("計算每個分組的數量完畢")
        
        # 合併計數每個分組的數量的 DataFrame  
        cal = pd.merge(cal, group_count, on=['targetWord1','targetWord2','targetWord3','word6', 'word5','word4','word3','word2','word1'])  
        print("合併計數每個分組的數量的 DataFrame完畢")
        
        # 重新命名列名  
        cal = cal.rename(columns={'count by group': 'times'})  
        print("重新命名列名完畢")
        
        # 按照 count by group 欄位進行排序  
        cal = cal.sort_values(by=['word6', 'word5', 'word4', 'word3', 'word2', 'word1'], ascending=True)
        print("count by group完畢")

        exReportID = []
        numReports = [] 
        times = []
        word1 = []
        word2 = []
        word3 = []
        word4 = []
        word5 = []
        word6 = []
        targetWord1 = []
        targetWord2 = []
        targetWord3 = []
        for index, row in cal.iterrows():
            exReportID.append(row['exReportID'])
            numReports.append(row['numReports'])
            times.append(row['times'])
            word1.append(row['word1'])
            word2.append(row['word2'])
            word3.append(row['word3'])
            word4.append(row['word4'])
            word5.append(row['word5'])
            word6.append(row['word6'])
            targetWord1.append(row['targetWord1'])
            targetWord2.append(row['targetWord2'])
            targetWord3.append(row['targetWord3'])
            # ... access other columns as needed
            print(exReportID, numReports, times, word1, word2, word3, word4, word5, word6, targetWord1, targetWord2, targetWord3)

        result = {'numReports':numReports,
                         'times':times,
                         'word1':word1,
                         'word2':word2,
                         'word3':word3,
                         'word4':word4,
                         'word5':word5,
                         'word6':word6,
                         'targetWord1':targetWord1,
                         'targetWord2':targetWord2,
                         'targetWord3':targetWord3,
                         'reportID':exReportID,
                         'status':"0",
                         'MSG': "查詢成功"
                         }
        
        # # 顯示結果  
        # # print(cal)
        print(result)
        
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        # print("rollbacked, error message : ", e)
        
        result['ERRMSG'] = str(e)
        print("error", e)
    
    conn.close()
    return JsonResponse(result)


@csrf_exempt
def getStasticTable2(request):
    server = '172.31.6.22' 
    database = 'buildVocabulary' 
    username = 'N824' 
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    result = {"status":"1"}
    raw = request.body.decode('utf-8')
    try:
        print("in")
        body = json.loads(raw)
        print("in")
        string = body['string']

        
        # number = body['number']
        if string == "":
            raise Exception("輸入不可為空")
        

        

        tokenList = string.split(" ")
        IDList = []
        print(len(tokenList))
        if (len(tokenList) != 5):
            raise Exception("必須輸入5字")
        for i in tokenList:
            query = "select * from Vocabulary where token = ?"
            args = [i]
            cursor.execute(query, args)
            VocabularyData = cursor.fetchone()
            IDList.append(VocabularyData.tokenID)
            
        print("in")


        
        # query = f'''select count(distinct a.reportID) as 'numReports', count(*) as 'times', min(a.reportID) as 'exReportID', c.word1, c.word2, c.word3, b.word4, b.word5, b.word6 as 'word6', a.targetWord1, a.targetWord2, a.targetWord3, a.targetWord4, a.targetWord5
		# 					from (
		# 									select a.reportID, a.posStart, b.token as 'targetWord1', c.token as 'targetWord2', d.token as 'targetWord3', e.token as 'targetWord4', f.token as 'targetWord5'
		# 									from (
		# 													select a.reportID, a.posStart, a.tokenID as 'target1', b.tokenID as 'target2', c.tokenID as 'target3', d.tokenID as 'target4', e.tokenID as 'target5'
		# 													from textToken as a inner join textToken as b
		# 																			on a.reportID=b.reportID and b.posStart=(a.posEnd+1) and a.tokenID={IDList[0]} and b.tokenID={IDList[1]}
		# 																	inner join textToken as c
		# 																			on b.reportID=c.reportID and c.posStart=(b.posEnd+1) and c.tokenID={IDList[2]}
		# 																	inner join textToken as d
		# 																			on d.reportID=c.reportID and d.posStart=(c.posEnd+1) and d.tokenID={IDList[3]}
		# 																	inner join textToken as e
		# 																			on e.reportID=d.reportID and e.posStart=(d.posEnd+1) and e.tokenID={IDList[4]}
		# 												) as a inner join Vocabulary as b on a.target1=b.tokenID
		# 															inner join Vocabulary as c on a.target2=c.tokenID
		# 															inner join Vocabulary as d on a.target3=d.tokenID
		# 															inner join Vocabulary as e on a.target4=e.tokenID
		# 															inner join Vocabulary as f on a.target5=f.tokenID
		# 								) as a inner join
		# 								(
		# 										select a.reportID, a.posEnd, a.startT4,
		# 														IIF(a.word4=1, b1.extractedValue, b.token) as 'word4',
		# 														IIF(a.word5=1, c1.extractedValue, c.token) as 'word5',
		# 														IIF(a.word6=1, d1.extractedValue, d.token) as 'word6'
		# 										from (
		# 														select a.reportID, c.posEnd, a.tokenID as 'word4', b.tokenID as 'word5', c.tokenID as 'word6', a.posStart as 'startT4', b.posStart as 'startT5', c.posStart as 'startT6'
		# 														from textToken as a inner join textToken as b on a.reportID=b.reportID and b.posStart=(a.posEnd+1)
		# 																		inner join textToken as c on b.reportID=c.reportID and c.posStart=(b.posEnd+1)
		# 													) as a inner join Vocabulary as b on a.word4=b.tokenID
		# 																		left outer join extractedValueFromToken as b1 on a.reportID=b1.reportID and a.startT4=b1.posStart
		# 																inner join Vocabulary as c on a.word5=c.tokenID
		# 																		left outer join extractedValueFromToken as c1 on a.reportID=c1.reportID and a.startT5=c1.posStart
		# 																inner join Vocabulary as d on a.word6=d.tokenID
		# 																		left outer join extractedValueFromToken as d1 on a.reportID=d1.reportID and a.startT6=d1.posStart
		# 								) as b on a.reportID=b.reportID and b.posEnd=(a.posStart-1) inner join
		# 								(
		# 										select a.reportID, a.posEnd,
		# 														IIF(a.word1=1, b1.extractedValue, b.token) as 'word1',
		# 														IIF(a.word2=1, c1.extractedValue, c.token) as 'word2',
		# 														IIF(a.word3=1, d1.extractedValue, d.token) as 'word3'
		# 										from (
		# 														select a.reportID, c.posEnd, a.tokenID as 'word1', b.tokenID as 'word2', c.tokenID as 'word3', a.posStart as 'startT1', b.posStart as 'startT2', c.posStart as 'startT3'
		# 														from textToken as a inner join textToken as b on a.reportID=b.reportID and b.posStart=(a.posEnd+1)
		# 																		inner join textToken as c on b.reportID=c.reportID and c.posStart=(b.posEnd+1)
		# 													) as a inner join Vocabulary as b on a.word1=b.tokenID
		# 																		left outer join extractedValueFromToken as b1 on a.reportID=b1.reportID and a.startT1=b1.posStart
		# 																inner join Vocabulary as c on a.word2=c.tokenID
		# 																		left outer join extractedValueFromToken as c1 on a.reportID=c1.reportID and a.startT2=c1.posStart
		# 																inner join Vocabulary as d on a.word3=d.tokenID
		# 																		left outer join extractedValueFromToken as d1 on a.reportID=d1.reportID and a.startT3=d1.posStart
		# 								) as c on b.reportID=c.reportID and c.posEnd=(b.startT4-1)
		# 				group by a.targetWord1, a.targetWord2, a.targetWord3, a.targetWord4, a.targetWord5,
		# 									b.word6, b.word5, b.word4, c.word3, c.word2, c.word1
		# 				order by 9,8,7,6,5,4
        # '''
        # cursor.execute(query,[])
        # res = cursor.fetchall()
        # # print(res)
        # # reportID = [row.exReportID for row in res]
        # # numReports = [row.numReports for row in res]
        # # times = [row.times for row in res]
        # # word1 = [row.word1 for row in res]
        # # word2 = [row.word2 for row in res]
        # # word3 = [row.word3 for row in res]
        # # count4 = [row.count4 for row in res]
        # # word4 = [row.word4 for row in res]
        # # count5 = [row.count5 for row in res]
        # # word5 = [row.word5 for row in res]
        # # count6 = [row.count6 for row in res]
        # # word6 = [row.word6 for row in res]
        # # countTarget = [row.countTarget for row in res]
        # # targetWord1 = [row.targetWord1 for row in res]
        # # targetWord2 = [row.targetWord2 for row in res]
        # # targetWord3 = [row.targetWord3 for row in res]
        # # targetWord4 = [row.targetWord4 for row in res]
        # # targetWord5 = [row.targetWord5 for row in res]
        # # result = {'numReports':numReports,
        # #                  'times':times,
        # #                  'word1':word1,
        # #                  'word2':word2,
        # #                  'word3':word3,
        # #                  'count4':count4,
        # #                  'word4':word4,
        # #                  'count5':count5,
        # #                  'word5':word5,
        # #                  'count6':count6,
        # #                  'word6':word6,
        # #                  'countTarget':countTarget,
        # #                  'targetWord1':targetWord1,
        # #                  'targetWord2':targetWord2,
        # #                  'targetWord3':targetWord3,
        # #                  'targetWord4':targetWord4,
        # #                  'targetWord5':targetWord5,
        # #                  'reportID':reportID,
        # #                  'status':"0",
        # #                  }

        
        # reportID = [row.exReportID for row in res]
        # numReports = [row.numReports for row in res]
        # times = [row.times for row in res]
        # word1 = [row.word1 for row in res]
        # word2 = [row.word2 for row in res]
        # word3 = [row.word3 for row in res]
        # word4 = [row.word4 for row in res]
        # word5 = [row.word5 for row in res]
        # word6 = [row.word6 for row in res]
        # targetWord1 = [row.targetWord1 for row in res]
        # targetWord2 = [row.targetWord2 for row in res]
        # targetWord3 = [row.targetWord3 for row in res]
        # targetWord4 = [row.targetWord4 for row in res]
        # targetWord5 = [row.targetWord5 for row in res]
        # result = {'numReports':numReports,
        #                  'times':times,
        #                  'word1':word1,
        #                  'word2':word2,
        #                  'word3':word3,
        #                  'word4':word4,
        #                  'word5':word5,
        #                  'word6':word6,
        #                  'targetWord1':targetWord1,
        #                  'targetWord2':targetWord2,
        #                  'targetWord3':targetWord3,
        #                  'targetWord4':targetWord4,
        #                  'targetWord5':targetWord5,
        #                  'reportID':reportID,
        #                  'status':"0",
        #                  }

        query = f'''select a.reportID as 'numReports', a.reportID as 'exReportID', c.word1, c.word2, c.word3, b.word4, b.word5, b.word6 as 'word6', a.targetWord1, a.targetWord2, a.targetWord3, a.targetWord4, a.targetWord5
							from (
											select a.reportID, a.posStart, b.token as 'targetWord1', c.token as 'targetWord2', d.token as 'targetWord3', e.token as 'targetWord4', f.token as 'targetWord5'
											from (
															select a.reportID, a.posStart, a.tokenID as 'target1', b.tokenID as 'target2', c.tokenID as 'target3', d.tokenID as 'target4', e.tokenID as 'target5'
															from textToken as a inner join textToken as b
																					on a.reportID=b.reportID and b.posStart=(a.posEnd+1) and a.tokenID={IDList[0]} and b.tokenID={IDList[1]}
																			inner join textToken as c
																					on b.reportID=c.reportID and c.posStart=(b.posEnd+1) and c.tokenID={IDList[2]}
																			inner join textToken as d
																					on d.reportID=c.reportID and d.posStart=(c.posEnd+1) and d.tokenID={IDList[3]}
																			inner join textToken as e
																					on e.reportID=d.reportID and e.posStart=(d.posEnd+1) and e.tokenID={IDList[4]}
														) as a inner join Vocabulary as b on a.target1=b.tokenID
																	inner join Vocabulary as c on a.target2=c.tokenID
																	inner join Vocabulary as d on a.target3=d.tokenID
																	inner join Vocabulary as e on a.target4=e.tokenID
																	inner join Vocabulary as f on a.target5=f.tokenID
										) as a inner join
										(
												select a.reportID, a.posEnd, a.startT4,
																IIF(a.word4=1, b1.extractedValue, b.token) as 'word4',
																IIF(a.word5=1, c1.extractedValue, c.token) as 'word5',
																IIF(a.word6=1, d1.extractedValue, d.token) as 'word6'
												from (
																select a.reportID, c.posEnd, a.tokenID as 'word4', b.tokenID as 'word5', c.tokenID as 'word6', a.posStart as 'startT4', b.posStart as 'startT5', c.posStart as 'startT6'
																from textToken as a inner join textToken as b on a.reportID=b.reportID and b.posStart=(a.posEnd+1)
																				inner join textToken as c on b.reportID=c.reportID and c.posStart=(b.posEnd+1)
															) as a inner join Vocabulary as b on a.word4=b.tokenID
																				left outer join extractedValueFromToken as b1 on a.reportID=b1.reportID and a.startT4=b1.posStart
																		inner join Vocabulary as c on a.word5=c.tokenID
																				left outer join extractedValueFromToken as c1 on a.reportID=c1.reportID and a.startT5=c1.posStart
																		inner join Vocabulary as d on a.word6=d.tokenID
																				left outer join extractedValueFromToken as d1 on a.reportID=d1.reportID and a.startT6=d1.posStart
										) as b on a.reportID=b.reportID and b.posEnd=(a.posStart-1) inner join
										(
												select a.reportID, a.posEnd,
																IIF(a.word1=1, b1.extractedValue, b.token) as 'word1',
																IIF(a.word2=1, c1.extractedValue, c.token) as 'word2',
																IIF(a.word3=1, d1.extractedValue, d.token) as 'word3'
												from (
																select a.reportID, c.posEnd, a.tokenID as 'word1', b.tokenID as 'word2', c.tokenID as 'word3', a.posStart as 'startT1', b.posStart as 'startT2', c.posStart as 'startT3'
																from textToken as a inner join textToken as b on a.reportID=b.reportID and b.posStart=(a.posEnd+1)
																				inner join textToken as c on b.reportID=c.reportID and c.posStart=(b.posEnd+1)
															) as a inner join Vocabulary as b on a.word1=b.tokenID
																				left outer join extractedValueFromToken as b1 on a.reportID=b1.reportID and a.startT1=b1.posStart
																		inner join Vocabulary as c on a.word2=c.tokenID
																				left outer join extractedValueFromToken as c1 on a.reportID=c1.reportID and a.startT2=c1.posStart
																		inner join Vocabulary as d on a.word3=d.tokenID
																				left outer join extractedValueFromToken as d1 on a.reportID=d1.reportID and a.startT3=d1.posStart
										) as c on b.reportID=c.reportID and c.posEnd=(b.startT4-1)'''
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        
        res = cursor.fetchall()
        # print(columns)
        # print(res)
        Array = []
        print(len(columns), len(res[0]))
        print("搜尋完畢")
        for i in res:
            Array.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12]])
        print(Array[0], len(Array[0]), len(Array))
        cal = pd.DataFrame(Array,columns=columns)
        # 分組
        grouped = cal.groupby(['targetWord1','targetWord2','targetWord3', 'targetWord4', 'targetWord5','word6', 'word5','word4','word3','word2','word1'])

        cal = grouped.agg({'exReportID': lambda x: ','.join(x.astype(str).unique()), 'numReports': lambda x: len(x.unique())}).reset_index()  
        print("分組完畢")
        # 計算每個分組的數量  
        group_count = grouped.size().reset_index(name='count by group')  
        print("計算每個分組的數量完畢")
        
        # 合併計數每個分組的數量的 DataFrame  
        cal = pd.merge(cal, group_count, on=['targetWord1','targetWord2','targetWord3', 'targetWord4', 'targetWord5','word6', 'word5','word4','word3','word2','word1'])  
        print("合併計數每個分組的數量的 DataFrame完畢")
        
        # 重新命名列名  
        cal = cal.rename(columns={'count by group': 'times'})  
        print("重新命名列名完畢")
        
        # 按照 count by group 欄位進行排序  
        cal = cal.sort_values(by=['word6', 'word5', 'word4', 'word3', 'word2', 'word1'], ascending=True)
        print("count by group完畢")

        exReportID = []
        numReports = [] 
        times = []
        word1 = []
        word2 = []
        word3 = []
        word4 = []
        word5 = []
        word6 = []
        targetWord1 = []
        targetWord2 = []
        targetWord3 = []
        targetWord4 = []
        targetWord5 = []
        for index, row in cal.iterrows():
            exReportID.append(row['exReportID'])
            numReports.append(row['numReports'])
            times.append(row['times'])
            word1.append(row['word1'])
            word2.append(row['word2'])
            word3.append(row['word3'])
            word4.append(row['word4'])
            word5.append(row['word5'])
            word6.append(row['word6'])
            targetWord1.append(row['targetWord1'])
            targetWord2.append(row['targetWord2'])
            targetWord3.append(row['targetWord3'])
            targetWord4.append(row['targetWord4'])
            targetWord5.append(row['targetWord5'])
            # ... access other columns as needed
            print(exReportID, numReports, times, word1, word2, word3, word4, word5, word6, targetWord1, targetWord2, targetWord3)

        result = {'numReports':numReports,
                         'times':times,
                         'word1':word1,
                         'word2':word2,
                         'word3':word3,
                         'word4':word4,
                         'word5':word5,
                         'word6':word6,
                         'targetWord1':targetWord1,
                         'targetWord2':targetWord2,
                         'targetWord3':targetWord3,
                         'targetWord4':targetWord4,
                         'targetWord5':targetWord5,
                         'reportID':exReportID,
                         'status':"0",
                         'MSG': "查詢成功"
                         }
        # result['MSG'] = "查詢成功"
        
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        # print("rollbacked, error message : ", e)
        
        result['ERRMSG'] = str(e)
        print("error")

    conn.close()
    return JsonResponse(result)


@csrf_exempt
def reExtraction(request):
    server = '172.31.6.22' 
    database = 'buildVocabulary '
    username = 'N824'
    password = 'test81218'
    
    result = {'status': "1"}
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes; as_dict=True;')
    cursor = conn.cursor()

    raw = request.body.decode('utf-8')

    try:
        body = json.loads(raw)
        token = body['token']
        insertcount = 0
        #---------------------------------------------------------------存RE.groups-----------------------------------------------------------------
        RE = body['RE']
        nWordForRE = body['nWord']
        query = "select * from Vocabulary where token = ?"
        args = [token]
        cursor.execute(query, args)
        VocabularyRes = cursor.fetchone()
        if VocabularyRes == None:
            raise Exception("token不存在")
        else:
            tokenID = VocabularyRes.tokenID

        query = 'select * from [vocabularyRE] where tokenID = ? and RE = ?;'
        args = [tokenID, RE]
        cursor.execute(query, args)
        tokenREID_original = cursor.fetchall()

        # # # # # print("tokenREID_original : ", tokenREID_original)
        if tokenREID_original == []:
            #插入資料表
            query = 'INSERT into [vocabularyRE] (tokenID, RE, nWord) OUTPUT [INSERTED].REID VALUES (?, ?, ?);'
            args = [tokenID, RE, nWordForRE]
            cursor.execute(query, args)
            vocabularyRERes = cursor.fetchall()
        else:
            raise Exception("RE已經存在")
        REID = vocabularyRERes[0].REID

        itemName = body['itemName[]']
        print(itemName)
        for ind,i in enumerate(itemName):
            print("itemName : ", i)
            
            query = 'select * from [itemDefinition2] where itemName = ?;'
            args = [i]
            cursor.execute(query, args)
            itemDefinition2Res = cursor.fetchone()
            if itemDefinition2Res == None:
                raise Exception("ItemName 不存在")
            # print("itemID : ", itemDefinition2Res)
            #插入資料表
            query = 'INSERT into [REItem2] (REID, seqNo, itemID) OUTPUT [INSERTED].* VALUES (?, ?, ?);'
            args = [REID, ind+1, itemDefinition2Res.itemID]
            # # # # # print(args)
            cursor.execute(query, args)
            tokenREItemID = cursor.fetchone()
            # print("插入tokenREItem : ", tokenREItemID)
        
        #---------------------------------------------------------------替換textToken-----------------------------------------------------------------
        word = body['word']
        
        print("token : ", token)
        if (word == "2"):
            string = '10 1 17 1 11'
            
            reportIDArray = body['reportID[]']
            for reportID in reportIDArray:
                value1 = body['value1']
                value2 = body['value2']
                value = "(" + value1 + "/" + value2 + ")"
                query = "select * from reExtraction(?) where reportID = ? and getData = ?"
                args = [string, reportID, value]
                print(args)
                cursor.execute(query, args)
                getdata = cursor.fetchall()
                if getdata == []:
                    continue

                deleteArray = []
                
                times = 0
                for ind, i in enumerate(getdata):
                    number = i.getData[1:len(i.getData)-1]
                    print("number", number)
                    deleteArray.append(i)
                    # if string.split("/")[0] == num1 and string.split("/")[1] == num2:
                    #     print(i)
                    #     deleteArray.append(i)
                    print(deleteArray)

                    reportID = i[0]
                    posStart = i[1]
                    posEnd = i[2]
                    
                    times += i[3]
                    num1 = number.split("/")[0]
                    num2 = number.split("/")[1]

                    print("data : ", reportID, posStart, posEnd, times, num1, num2)
                    query = "SELECT * FROM [Vocabulary] where token = ?"
                    args = [token]
                    cursor.execute(query, args)
                    VocabularyRes = cursor.fetchone()
                    tokenID = VocabularyRes.tokenID
                    print("tokenID : ", tokenID)

                    
                    # 只做一次
                    if ind == 0:
                        query = '''delete a output deleted.* from textToken as a inner join reExtraction(?) as b on a.reportID=b.reportID and a.posStart between b.posStart and b.posEnd
                        where a.reportID = ? and b.getData = ?'''
                        args = [string, reportID, value]
                        cursor.execute(query, args)
                        deletedData = cursor.fetchall()
                        print("deletedData : ", deletedData)
                        print("times : ", times, len(deletedData))
                        print("deletedData[ind] : ", deletedData)
                        print("ind : ", ind, len(getdata)-1)
                    #最後一次迴圈看刪除總數
                    if (int(times) != len(deletedData) and ind == len(getdata)-1):
                        raise Exception(f'''查詢textToken數量不等於刪除textToken數量<br>查詢 : {int(times)}<br>刪除 : {len(deletedData)}''')
                    else:
                        print("長度相等")

                    query = '''insert into textToken (reportID, posStart, posEnd, tokenID) output inserted.* values (?, ?, ?, ?)'''
                    args = [reportID, posStart, posEnd, tokenID]
                    cursor.execute(query, args)
                    insertedData = cursor.fetchone()
                    print("insertedData : ", insertedData)

                    if insertedData == None:
                        raise Exception("插入textToken錯誤")
                    
                    group1 = body['group1']
                    group2 = body['group2']
                    print(group1, group2)
                    
                    query = '''insert into extractedValueFromToken (reportID, posStart, REItemID, extractedValue) output inserted.* values (?, ?, ?, ?)'''
                    args = [reportID, posStart, group1, num1]
                    cursor.execute(query, args)
                    insertedData = cursor.fetchone()
                    print("insertedData : ", insertedData)
                    insertcount += 1
                    
                    query = '''insert into extractedValueFromToken (reportID, posStart, REItemID, extractedValue) output inserted.* values (?, ?, ?, ?)'''
                    args = [reportID, posStart, group2, num2]
                    cursor.execute(query, args)
                    insertedData = cursor.fetchone()
                    print("insertedData : ", insertedData)
                    insertcount += 1


            
        elif (word == "1"):
            
            string = '10 1 11'
            
            reportIDArray = body['reportID[]']
            print("reportIDArray : ", reportIDArray)
            for reportID in reportIDArray:
                value1 = body['value1']
                value = "(" + value1 + ")"

                query = "select * from reExtraction(?) where reportID = ? and getData = ?"
                args = [string, reportID, value]
                cursor.execute(query, args)
                getdata = cursor.fetchall()
                
                if getdata == []:
                    continue

                deleteArray = []
                times = 0
                for ind,i in enumerate(getdata):
                    number = i.getData[1:len(i.getData)-1]
                    print("number", number)
                    deleteArray.append(i)
                    # if string.split("/")[0] == num1 and string.split("/")[1] == num2:
                    #     print(i)
                    #     deleteArray.append(i)
                    print(deleteArray)

                    reportID = i[0]
                    posStart = i[1]
                    posEnd = i[2]
                    
                    times += i[3]
                    num1 = number

                    print("data : ", reportID, posStart, posEnd, times, num1)
                    query = "SELECT * FROM [Vocabulary] where token = ?"
                    args = [token]
                    cursor.execute(query, args)
                    VocabularyRes = cursor.fetchone()
                    tokenID = VocabularyRes.tokenID
                    print("tokenID : ", tokenID)

                    # 只做一次
                    if ind == 0:
                        query = '''delete a output deleted.* from textToken as a inner join reExtraction(?) as b on a.reportID=b.reportID and a.posStart between b.posStart and b.posEnd
                        where a.reportID = ? and b.getData = ?'''
                        args = [string, reportID, value]
                        cursor.execute(query, args)
                        deletedData = cursor.fetchall()
                        print("deletedData : ", deletedData)
                        print("times : ", times, len(deletedData))
                        print("deletedData[ind] : ", deletedData)
                        print("ind : ", ind, len(getdata)-1)
                    #最後一次迴圈看刪除總數
                    if (int(times) != len(deletedData) and ind == len(getdata)-1):
                        raise Exception(f'''查詢textToken數量不等於刪除textToken數量<br>查詢 : {int(times)}<br>刪除 : {len(deletedData)}''')
                    else:
                        print("長度相等")

                    query = '''insert into textToken (reportID, posStart, posEnd, tokenID) output inserted.* values (?, ?, ?, ?)'''
                    args = [reportID, posStart, posEnd, tokenID]
                    cursor.execute(query, args)
                    insertedData = cursor.fetchone()
                    print("insertedData : ", insertedData)

                    if insertedData == None:
                        raise Exception("插入textToken錯誤")
                    
                    group1 = body['group1']
                    print(group1)
                    
                    query = '''insert into extractedValueFromToken (reportID, posStart, REItemID, extractedValue) output inserted.* values (?, ?, ?, ?)'''
                    args = [reportID, posStart, group1, num1]
                    cursor.execute(query, args)
                    insertedData = cursor.fetchone()
                    print("insertedData : ", insertedData)
                    insertcount += 1

        result['status'] = "0"
        result['MSG'] = f"儲存RE成功<br>並已更新{str(len(reportIDArray))}篇文章<br>{reportIDArray}<br>裡面的{insertcount}筆資料"
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        result['ERRMSG'] = str(e)
    
    conn.close()
    return JsonResponse(result)

    
