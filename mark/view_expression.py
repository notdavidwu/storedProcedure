from django.shortcuts import render
from django.http import JsonResponse
from django.template import loader
from mark.models import *
from mark.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
import pyodbc
import json
DATABASE_NAME = 'nlpVocabularyLatest' 

@csrf_exempt
def getTag(request):
    cursor = connections[DATABASE_NAME].cursor()
    query = "SELECT [token],[tokenID] FROM [Vocabulary] where tokenType='T' order by tokenID"
    cursor.execute(query,[])
    res = cursor.fetchall()
    token = [row[0] for row in res]
    tokenID = [row[1] for row in res]
    return JsonResponse({'token':token,'tokenID':tokenID})

@csrf_exempt
def getItemDefinition(request):
    server = '172.31.6.22' 
    database = 'nlpVocabularyLatest ' 
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
    database = 'nlpVocabularyLatest ' 
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


        
        query = f'''select  count(distinct a.reportID) as 'numReports', count(*) as 'times', min(a.reportID) as 'exReportID', c.word1, c.word2, c.word3, b.word4, b.word5, b.word6 , a.targetWord1, a.targetWord2, a.targetWord3
							from (
											select a.reportID, a.posStart, b.token as 'targetWord1', c.token as 'targetWord2', d.token as 'targetWord3'
											from (
															select a.reportID, a.posStart, a.tokenID as 'target1', b.tokenID as 'target2', c.tokenID as 'target3'
															from textToken as a inner join textToken as b
																					on a.reportID=b.reportID and b.posStart=(a.posEnd+1) and a.tokenID={IDList[0]} and b.tokenID={IDList[1]}
																			inner join textToken as c
																					on b.reportID=c.reportID and c.posStart=(b.posEnd+1) and c.tokenID={IDList[2]}
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
						group by a.targetWord1, a.targetWord2, a.targetWord3,
											b.word6, b.word5, b.word4, c.word3, c.word2, c.word1
						order by 9,8,7,6,5,4
        '''
        cursor.execute(query,[])
        res = cursor.fetchall()

        print("resssssssssssssssssssssssssssssssssssssss", res[0])
        # reportID = [row.exReport for row in res]
        # numReports = [row.numReports for row in res]
        # times = [row.times for row in res]
        # word1 = [row.word1 for row in res]
        # word2 = [row.word2 for row in res]
        # word3 = [row.word3 for row in res]
        # count4 = [row.count4 for row in res]
        # word4 = [row.word4 for row in res]
        # count5 = [row.count5 for row in res]
        # word5 = [row.word5 for row in res]
        # count6 = [row.count6 for row in res]
        # word6 = [row.word6 for row in res]
        # countTarget = [row.countTarget for row in res]
        # targetWord1 = [row.targetWord1 for row in res]
        # targetWord2 = [row.targetWord2 for row in res]
        # targetWord3 = [row.targetWord3 for row in res]
        # result = {'numReports':numReports,
        #                  'times':times,
        #                  'word1':word1,
        #                  'word2':word2,
        #                  'word3':word3,
        #                  'count4':count4,
        #                  'word4':word4,
        #                  'count5':count5,
        #                  'word5':word5,
        #                  'count6':count6,
        #                  'word6':word6,
        #                  'countTarget':countTarget,
        #                  'targetWord1':targetWord1,
        #                  'targetWord2':targetWord2,
        #                  'targetWord3':targetWord3,
        #                  'reportID':reportID,
        #                  'status':"0",
        #                  }

        reportID = [row.exReportID for row in res]
        numReports = [row.numReports for row in res]
        times = [row.times for row in res]
        word1 = [row.word1 for row in res]
        word2 = [row.word2 for row in res]
        word3 = [row.word3 for row in res]
        word4 = [row.word4 for row in res]
        word5 = [row.word5 for row in res]
        word6 = [row.word6 for row in res]
        targetWord1 = [row.targetWord1 for row in res]
        targetWord2 = [row.targetWord2 for row in res]
        targetWord3 = [row.targetWord3 for row in res]
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
                         'reportID':reportID,
                         'status':"0",
                         }
        
        result[''] = "查詢成功"
        
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        # print("rollbacked, error message : ", e)
        
        result['ERRMSG'] = str(e)
        print("error")

    return JsonResponse(result)


@csrf_exempt
def getStasticTable2(request):
    server = '172.31.6.22' 
    database = 'nlpVocabularyLatest ' 
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


        
        query = f'''select count(distinct a.reportID) as 'numReports', count(*) as 'times', min(a.reportID) as 'exReportID', c.word1, c.word2, c.word3, b.word4, b.word5, b.word6 as 'word6', a.targetWord1, a.targetWord2, a.targetWord3, a.targetWord4, a.targetWord5
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
										) as c on b.reportID=c.reportID and c.posEnd=(b.startT4-1)
						group by a.targetWord1, a.targetWord2, a.targetWord3, a.targetWord4, a.targetWord5,
											b.word6, b.word5, b.word4, c.word3, c.word2, c.word1
						order by 9,8,7,6,5,4
        '''
        cursor.execute(query,[])
        res = cursor.fetchall()
        # print(res)
        # reportID = [row.exReportID for row in res]
        # numReports = [row.numReports for row in res]
        # times = [row.times for row in res]
        # word1 = [row.word1 for row in res]
        # word2 = [row.word2 for row in res]
        # word3 = [row.word3 for row in res]
        # count4 = [row.count4 for row in res]
        # word4 = [row.word4 for row in res]
        # count5 = [row.count5 for row in res]
        # word5 = [row.word5 for row in res]
        # count6 = [row.count6 for row in res]
        # word6 = [row.word6 for row in res]
        # countTarget = [row.countTarget for row in res]
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
        #                  'count4':count4,
        #                  'word4':word4,
        #                  'count5':count5,
        #                  'word5':word5,
        #                  'count6':count6,
        #                  'word6':word6,
        #                  'countTarget':countTarget,
        #                  'targetWord1':targetWord1,
        #                  'targetWord2':targetWord2,
        #                  'targetWord3':targetWord3,
        #                  'targetWord4':targetWord4,
        #                  'targetWord5':targetWord5,
        #                  'reportID':reportID,
        #                  'status':"0",
        #                  }

        
        reportID = [row.exReportID for row in res]
        numReports = [row.numReports for row in res]
        times = [row.times for row in res]
        word1 = [row.word1 for row in res]
        word2 = [row.word2 for row in res]
        word3 = [row.word3 for row in res]
        word4 = [row.word4 for row in res]
        word5 = [row.word5 for row in res]
        word6 = [row.word6 for row in res]
        targetWord1 = [row.targetWord1 for row in res]
        targetWord2 = [row.targetWord2 for row in res]
        targetWord3 = [row.targetWord3 for row in res]
        targetWord4 = [row.targetWord4 for row in res]
        targetWord5 = [row.targetWord5 for row in res]
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
                         'reportID':reportID,
                         'status':"0",
                         }
        
        result['MSG'] = "查詢成功"
        
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        # print("rollbacked, error message : ", e)
        
        result['ERRMSG'] = str(e)
        print("error")

    return JsonResponse(result)
    
