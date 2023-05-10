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
def getTypoToken(request):
    server = '172.31.6.22' 
    database = 'nlpVocabularyLatest ' 
    username = 'N824' 
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    result = {'status': "1"}
    
    # raw = request.body.decode('utf-8')
    
    try:        
        # body = json.loads(raw)
        query = '''select a.tokenID as 'tokenID1', a.token as 'token1', b.tokenID as 'tokenID2', b.token as 'token2'
            from (
            select tokenID, token
            from Vocabulary
            where token=LOWER(token)
            ) as a inner join
            (
            select tokenID, token
            from Vocabulary
            where token<>LOWER(token)
            ) as b on a.token=LOWER(b.token)
            order by tokenID1'''
        cursor.execute(query)
        res = cursor.fetchall()
        # print(res)
        tokenID1 = [row.tokenID1 for row in res]
        token1 = [row.token1 for row in res]
        tokenID2 = [row.tokenID2 for row in res]
        token2 = [row.token2 for row in res]

        result['status'] = "0"
        
        result['tokenID1'] = tokenID1
        result['token1'] = token1
        result['tokenID2'] = tokenID2
        result['token2'] = token2
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        result['ERRMSG'] = str(e)
    # print(result)
    
    conn.close()
    
    return JsonResponse(result)