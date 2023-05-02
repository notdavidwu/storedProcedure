from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from django.template import loader
from django.http import HttpResponse
from django.views.generic import ListView,DeleteView

from mark.serializers import TextSerializer 
from mark.models import *
from mark.forms import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import re
import pyodbc
import json
import copy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import sys, os, psutil
from time import process_time
from .view_dictionary import *
from datetime import datetime
import time


@csrf_exempt
def getVocabularyE(request):
    server = '172.31.6.22' 
    database = 'buildVocabulary ' 
    username = 'N824' 
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    query = "SELECT [token],[tokenID] FROM [Vocabulary] where tokenType = 'E' order by tokenID"
    cursor.execute(query,[])
    res = cursor.fetchall()
    token = [row[0] for row in res]
    tokenID = [row[1] for row in res]
    conn.commit()
    conn.close()
    return JsonResponse({'token':token,'tokenID':tokenID})

@csrf_exempt
def backupDB(request):
    server = '172.31.6.22'
    database = 'buildVocabulary '
    username = 'N824'
    password = 'test81218'
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    
    result = {'status':'1'} #預設失敗
    try :
        query = '''
                EXEC msdb.dbo.sp_start_job N'buildVocabulary_backup.backup';
                EXEC msdb.dbo.sp_start_job N'buildVocabulary_backup.backup';
                '''
        
        cursor.execute(query)
        result['status'] = "0"
        result['MSG'] = "Backup completed!"
        conn.commit()
    except Exception as e:
        conn.rollback()
        # print("rollbacked, error message : ", e)
        result['ERRMSG'] = str(e)
    
    conn.close()
    return JsonResponse(result)

@csrf_exempt
def moveRE(request):
    server = '172.31.6.22'
    database = 'buildVocabulary '
    username = 'N824'
    password = 'test81218'
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    
    result = {'status':'1'} #預設失敗
    
    raw = request.body.decode('utf-8')
    msg = ""
    try :
        body = json.loads(raw)
        # -----------------------------------------------------------Vocabulary-----------------------------------------------------------------
        token = body['tokens[]']
        tokenOriginal = []
        tokenIDOriginal = []
        nWordOriginal = []
        tokenTypeOriginal = []
        for ind,i in enumerate(token):
            # print(i)
            query = '''
                    SELECT * FROM [buildVocabulary ].[dbo].[Vocabulary] where token = ?;
                    '''
            args = [str(i)]            
            cursor.execute(query, args)
            VocabularyData = cursor.fetchone()

            tokenOriginal.append(VocabularyData.token)
            tokenIDOriginal.append(VocabularyData.tokenID)
            nWordOriginal.append(VocabularyData.nWord)
            tokenTypeOriginal.append(VocabularyData.tokenType)

            msg += "<br>" + str(ind+1) + ". " + str(i)
        print(tokenOriginal, tokenIDOriginal, nWordOriginal, tokenTypeOriginal)
        # -----------------------------------------------------------Vocabulary-----------------------------------------------------------------



        
        # -----------------------------------------------------------vocabularyRE---------------------------------------------------------------
        REoriginal = []
        REIDoriginal = []
        for i in tokenIDOriginal:
            print("tokenIDOriginal :", i)
            query = '''
                    SELECT * FROM [buildVocabulary ].[dbo].[vocabularyRE] where tokenID = ?;
                    '''
            args = [i]
            cursor.execute(query, args)
            vocabularyREData = cursor.fetchall()
            if (vocabularyREData):
                for j in vocabularyREData:
                    REoriginal.append(j.RE)
                    REIDoriginal.append(j.REID)
        print(REoriginal, REIDoriginal)
        # -----------------------------------------------------------vocabularyRE---------------------------------------------------------------
        
        result['status'] = "0"
        result['MSG'] = str(len(token)) + " Regex and Vocabularies moeved : " + str(msg)
        conn.commit()
    except Exception as e:
        conn.rollback()
        # print("rollbacked, error message : ", e)
        result['ERRMSG'] = str(e)
    
    conn.close()
    return JsonResponse(result)


def REmove(request):
    return render(request, 'mark/REmove.html')