from django.shortcuts import render
from django.http import JsonResponse
from django.template import loader
from mark.models import *
from mark.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
import pyodbc
import json
DATABASE_NAME = 'buildVocabulary' 

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
    cursor = connections[DATABASE_NAME].cursor()
    query = "SELECT * FROM [itemDefinition] order by itemID"
    cursor.execute(query,[])
    res = cursor.fetchall()
    itemID = [row[0] for row in res]
    rootID = [row[1] for row in res]
    itemName = [row[2] for row in res]
    engName = [row[3] for row in res]
    chtName = [row[4] for row in res]
    return JsonResponse({'itemID':itemID,
                         'rootID':rootID,
                         'itemName':itemName,
                         'engName':engName,
                         'chtName':chtName,
                         })

@csrf_exempt
def getStasticTable(request):
    server = '172.31.6.22' 
    database = 'buildVocabulary ' 
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
            
        print("in")


        
        query = f'''select a.exReport, a.numReports, a.times, b.token as 'word1', c.token as 'word2', d.token as 'word3', 
				sum(times) over (partition by h.tokenID, i.tokenID, j.tokenID, g.tokenID, f.tokenID, e.tokenID order by h.tokenID, i.tokenID, j.tokenID, g.tokenID, f.tokenID, e.tokenID) as 'count4',
						e.token as 'word4', 
				sum(times) over (partition by h.tokenID, i.tokenID, j.tokenID, g.tokenID, f.tokenID order by h.tokenID, i.tokenID, j.tokenID, g.tokenID, f.tokenID) as 'count5',
						f.token as 'word5', 
				sum(times) over (partition by h.tokenID, i.tokenID, j.tokenID, g.tokenID order by h.tokenID, i.tokenID, j.tokenID, g.tokenID) as 'count6',
						g.token as 'word6',						
				sum(times) over (partition by h.tokenID, i.tokenID, j.tokenID order by h.tokenID, i.tokenID, j.tokenID) as 'countTarget',				
				h.token as 'targetWord1', i.token as 'targetWord2', j.token as 'targetWord3'
from (
				select min(a.reportID) as 'exReport', count(distinct a.reportID) as 'numReports', count(*) as 'times', a.targetWord1, a.targetWord2, a.targetWord3, b.tokenID as 'word6', c.tokenID as 'word5', d.tokenID as 'word4', e.tokenID as 'word3', f.tokenID as 'word2', g.tokenID as 'word1'
				from (
								select a.reportID, a.posStart, a.tokenID as 'targetWord1', b.tokenID as 'targetWord2', c.tokenID as 'targetWord3'
								from textToken as a inner join textToken as b 
													on a.reportID=b.reportID and b.posStart=(a.posEnd+1) and a.tokenID={IDList[0]} and b.tokenID={IDList[1]}
											inner join textToken as c
													on b.reportID=c.reportID and c.posStart=(b.posEnd+1) and c.tokenID={IDList[2]}
						)	as a inner join textToken as b
												on a.reportID=b.reportID and b.posEnd=(a.posStart-1)
										inner join textToken as c
												on b.reportID=c.reportID and c.posEnd=(b.posStart-1)
										inner join textToken as d
												on c.reportID=d.reportID and d.posEnd=(c.posStart-1)
										inner join textToken as e
												on d.reportID=e.reportID and e.posEnd=(d.posStart-1)
										inner join textToken as f
												on e.reportID=f.reportID and f.posEnd=(e.posStart-1)
										inner join textToken as g
												on f.reportID=g.reportID and g.posEnd=(f.posStart-1)
				group by a.targetWord1, a.targetWord2, a.targetWord3, b.tokenID, c.tokenID, d.tokenID, e.tokenID, f.tokenID, g.tokenID
		) as a inner join Vocabulary as b
						on a.word1=b.tokenID
					inner join Vocabulary as c
						on a.word2=c.tokenID
					inner join Vocabulary as d
						on a.word3=d.tokenID
					inner join Vocabulary as e
						on a.word4=e.tokenID
						inner join Vocabulary as f
						on a.word5=f.tokenID
					inner join Vocabulary as g
						on a.word6=g.tokenID
					inner join Vocabulary as h
						on a.targetWord1=h.tokenID
					inner join Vocabulary as i
						on a.targetWord2=i.tokenID
					inner join Vocabulary as j
						on a.targetWord3=j.tokenID
order by numReports desc,count6 desc, count5 desc, count4 desc
        '''
        cursor.execute(query,[])
        res = cursor.fetchall()
        # print(res)
        reportID = [row.exReport for row in res]
        numReports = [row.numReports for row in res]
        times = [row.times for row in res]
        word1 = [row.word1 for row in res]
        word2 = [row.word2 for row in res]
        word3 = [row.word3 for row in res]
        count4 = [row.count4 for row in res]
        word4 = [row.word4 for row in res]
        count5 = [row.count5 for row in res]
        word5 = [row.word5 for row in res]
        count6 = [row.count6 for row in res]
        word6 = [row.word6 for row in res]
        countTarget = [row.countTarget for row in res]
        targetWord1 = [row.targetWord1 for row in res]
        targetWord2 = [row.targetWord2 for row in res]
        targetWord3 = [row.targetWord3 for row in res]
        result = {'numReports':numReports,
                         'times':times,
                         'word1':word1,
                         'word2':word2,
                         'word3':word3,
                         'count4':count4,
                         'word4':word4,
                         'count5':count5,
                         'word5':word5,
                         'count6':count6,
                         'word6':word6,
                         'countTarget':countTarget,
                         'targetWord1':targetWord1,
                         'targetWord2':targetWord2,
                         'targetWord3':targetWord3,
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


@csrf_exempt
def getStasticTable2(request):
    server = '172.31.6.22' 
    database = 'buildVocabulary ' 
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


        
        query = f'''select a.exReport, a.numReports, a.times, b.token as 'word1', c.token as 'word2', d.token as 'word3', 
				sum(times) over (partition by h.tokenID, i.tokenID, j.tokenID, g.tokenID, f.tokenID, e.tokenID order by h.tokenID, i.tokenID, j.tokenID, g.tokenID, f.tokenID, e.tokenID) as 'count4',
						e.token as 'word4', 
				sum(times) over (partition by h.tokenID, i.tokenID, j.tokenID, g.tokenID, f.tokenID order by h.tokenID, i.tokenID, j.tokenID, g.tokenID, f.tokenID) as 'count5',
						f.token as 'word5', 
				sum(times) over (partition by h.tokenID, i.tokenID, j.tokenID, g.tokenID order by h.tokenID, i.tokenID, j.tokenID, g.tokenID) as 'count6',
						g.token as 'word6',						
				sum(times) over (partition by h.tokenID, i.tokenID, j.tokenID order by h.tokenID, i.tokenID, j.tokenID) as 'countTarget',				
				h.token as 'targetWord1', i.token as 'targetWord2', j.token as 'targetWord3', k.token as 'targetWord4', l.token as 'targetWord5'
from (
				select min(a.reportID) as 'exReport', count(distinct a.reportID) as 'numReports', count(*) as 'times', a.targetWord1, a.targetWord2, a.targetWord3, a.targetWord4, a.targetWord5, b.tokenID as 'word6', c.tokenID as 'word5', d.tokenID as 'word4', e.tokenID as 'word3', f.tokenID as 'word2', g.tokenID as 'word1'
				from (
								select a.reportID, a.posStart, a.tokenID as 'targetWord1', b.tokenID as 'targetWord2', c.tokenID as 'targetWord3', d.tokenID as 'targetWord4', e.tokenID as 'targetWord5'
								from textToken as a inner join textToken as b 
													on a.reportID=b.reportID and b.posStart=(a.posEnd+1) and a.tokenID={IDList[0]} and b.tokenID={IDList[1]}
											inner join textToken as c
													on b.reportID=c.reportID and c.posStart=(b.posEnd+1) and c.tokenID={IDList[2]}
                                            inner join textToken as d
													on d.reportID=c.reportID and d.posStart=(c.posEnd+1) and d.tokenID={IDList[3]}
                                            inner join textToken as e
													on e.reportID=d.reportID and e.posStart=(d.posEnd+1) and e.tokenID={IDList[4]}
						)	as a inner join textToken as b
												on a.reportID=b.reportID and b.posEnd=(a.posStart-1)
										inner join textToken as c
												on b.reportID=c.reportID and c.posEnd=(b.posStart-1)
										inner join textToken as d
												on c.reportID=d.reportID and d.posEnd=(c.posStart-1)
										inner join textToken as e
												on d.reportID=e.reportID and e.posEnd=(d.posStart-1)
										inner join textToken as f
												on e.reportID=f.reportID and f.posEnd=(e.posStart-1)
										inner join textToken as g
												on f.reportID=g.reportID and g.posEnd=(f.posStart-1)
				group by a.targetWord1, a.targetWord2, a.targetWord3, a.targetWord4, a.targetWord5, b.tokenID, c.tokenID, d.tokenID, e.tokenID, f.tokenID, g.tokenID
		) as a inner join Vocabulary as b
						on a.word1=b.tokenID
					inner join Vocabulary as c
						on a.word2=c.tokenID
					inner join Vocabulary as d
						on a.word3=d.tokenID
					inner join Vocabulary as e
						on a.word4=e.tokenID
						inner join Vocabulary as f
						on a.word5=f.tokenID
					inner join Vocabulary as g
						on a.word6=g.tokenID
					inner join Vocabulary as h
						on a.targetWord1=h.tokenID
					inner join Vocabulary as i
						on a.targetWord2=i.tokenID
					inner join Vocabulary as j
						on a.targetWord3=j.tokenID
					inner join Vocabulary as k
						on a.targetWord4=k.tokenID
					inner join Vocabulary as l
						on a.targetWord5=l.tokenID
order by numReports desc,count6 desc, count5 desc, count4 desc
        '''
        cursor.execute(query,[])
        res = cursor.fetchall()
        # print(res)
        reportID = [row.exReport for row in res]
        numReports = [row.numReports for row in res]
        times = [row.times for row in res]
        word1 = [row.word1 for row in res]
        word2 = [row.word2 for row in res]
        word3 = [row.word3 for row in res]
        count4 = [row.count4 for row in res]
        word4 = [row.word4 for row in res]
        count5 = [row.count5 for row in res]
        word5 = [row.word5 for row in res]
        count6 = [row.count6 for row in res]
        word6 = [row.word6 for row in res]
        countTarget = [row.countTarget for row in res]
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
                         'count4':count4,
                         'word4':word4,
                         'count5':count5,
                         'word5':word5,
                         'count6':count6,
                         'word6':word6,
                         'countTarget':countTarget,
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
    
