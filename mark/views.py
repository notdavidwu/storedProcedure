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

import time

    # queryset = Text.objects.all()
    # serializer_class = TextSerializer
    # def get(self, request, *args, **krgs):
    #     Texts = self.get_queryset()
    #     serializer = self.serializer_class(Texts, many=True)
    #     data = serializer.data
    #     return JsonResponse(data, safe=False)
    # def post(self, request, *args, **krgs):
    #     data = request.data
    #     try:
    #         serializer = self.serializer_class(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         with transaction.atomic():
    #             serializer.save()
    #         data = serializer.data
    #     except Exception as e:
    #         data = {'error': str(e)}
    #     return JsonResponse(data)
    
    #沒用到
def TextView(request):
    result = {'status':'1'}#預設失敗
    if request.method == 'GET':
        a = Text.objects.all()
        result = {'status':'0'}#成功
        result['text_input'] = []
        for item in a:
            record = {}
            record['id'] = item.id
            record['regexText'] = item.regexText
            record['inputText'] = item.inputText
            result['text_input'].append(record)
    # return JsonResponse(result)
    template = loader.get_template('index.html')
    # return HttpResponse(template.render()) #回傳template
    return render(request, 'index.html')

    #沒用到
@csrf_exempt
def TextFormView(request):
    if  request.method == 'POST':
        form = TextModelForm(request.POST) #拿到POST過來的資料並填入form
        result = {'status':'1'} #預設失敗
        # # # # # print(request.POST)
        if form.is_valid(): #檢查forms.py中的格式
            # # # # # print("form is valid")            
            data = form.cleaned_data #接form裡面丟出來的資料
            # # # # # # print(data)
            FormRegexText = form.cleaned_data['regexText'] #依標籤解析出資料
            FormInputText = form.cleaned_data['inputText'] #依標籤解析出資料
            # # # # # # print("User is :", request.user)
            # # # # # # print("regexText is :",FormRegexText)
            # # # # # # print("inputText is :",FormInputText)
            # if FormInputText != None and FormRegexText != None:
            #     text123 = Text.objects.create(author=request.user) #建立新表單
            #     text123.author = request.user
            #     text123.regexText = FormRegexText #將解析完的資料丟到物件內
            #     text123.inputText = FormInputText #將解析完的資料丟到物件內
            #     result = {'status':'0'}
            #     text123.save() #存檔
            # # # # # # print(result)
        else:
            pass
            # # # # # print("form is NOT valid.")
    
    
    
        
        
    return JsonResponse(result)

    #取得Vocabulary所有token並回傳
@csrf_exempt
def getVocabulary(request):
    if request.method == 'GET':
        #測試拉資料
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        result = cursor.execute("select * from [nlpVocabularyLatest  ].[dbo].[Vocabulary] where tokenType != 'U' ")
        patient = cursor.fetchall()
        result = {}
        result['data'] = []
        for item in patient:
            record = {}
            record['token'] = item.token
            result['data'].append(record)
        
        conn.commit()
        conn.close()
    return JsonResponse(result)

    #取得Vocabulary所有token用tokenType篩選並回傳
@csrf_exempt
def getVocabularyByType(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        if request.GET['tokenType'] == 'U':
            query = 'select * from [nlpVocabularyLatest  ].[dbo].[Vocabulary] where (tokenType = ? and tokenID <= 152 and tokenID != 151) order by tokenID DESC;'
        elif request.GET['tokenType'] == 'P':
            query = 'select * from [nlpVocabularyLatest  ].[dbo].[Vocabulary] where tokenType = ? or tokenType != \'U\';'
        else:
            query = 'select * from [nlpVocabularyLatest  ].[dbo].[Vocabulary] where tokenType = ? ;'
        args = [request.GET['tokenType']]
        # # # # # print(args)
        cursor.execute(query, args)
        tokenID = cursor.fetchall()
        ## # # # # print(tokenID[0])
        result['status'] = '0'            
        result['data'] = []
        for i in tokenID:
            record = {}
            record['token'] = i.token 
            record['tokenType'] = i.tokenType     
            ## # # # # print("token: " + str(i.token))
            result['data'].append(record)
    
        conn.commit()
        conn.close()
    return JsonResponse(result)
@csrf_exempt
def getVocabularyByType_Ptable(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        # query = '''    SELECT * FROM(
                # SELECT a.*, b.token, b.tokenType, ROW_NUMBER() OVER (PARTITION BY a.tokenID ORDER BY posStart, reportID) AS rowID2
                # --a.reportID, a.tokenID, b.token, a.posStart, a.posEnd
                # FROM (
                #  SELECT *, ROW_NUMBER() OVER (PARTITION BY reportID, tokenID ORDER BY posStart, reportID) AS rowID
                #  FROM textToken
                # ) AS a
                #  inner join Vocabulary AS b ON (a.tokenID = b.tokenID) and ( b.tokenType != 'C' and b.tokenType != 'G' and b.tokenType != 'S') and b.token != '[NUM]' and b.token != '[SPACE]' and b.token != '[EOL]'
                # ) AS res
                # WHERE res.rowID=1 and res.rowID2=1
                # ORDER BY  tokenID, posStart,reportID
                # '''
        # # # # print(args)
        # cursor.execute(query)
        # tokenID = cursor.fetchall()
        # result['data'] = []
            # 
        # for ind,i in enumerate(tokenID):
            # # # # print("i[0] : ",i[0])
            # # # # print("i : ", i)
            # if i[1]>0 and i[2]>0 and (i[6] == 'E' or i[6] == 'C' or i[6] == 'G' or i[6] == 'T'):
                # result['data'].append({
                    # 'No': ind+1,
                    # 'ProperNoun': i[5],
                    # 'tokenType': i[6],
                    # 'NewRE': '<button onclick="changeSrc()" class="btn btn-secondary">NewRE</button>',
                    # 'UnMerge':'<button onclick="UnMerge()" class="btn btn-danger">UnMerge</button>',
                # })
            # else:
                # result['data'].append({
                    # 'No': ind+1,
                    # 'ProperNoun': i[5],
                    # 'tokenType': i[6],
                    # 'NewRE': '',
                    # 'UnMerge':'',
                # })

        query = '''    SELECT * FROM Vocabulary where tokenType in ('C', 'P', 'G', 'T', 'E');
                '''
        # # # # # print(args)
        cursor.execute(query)
        tokenID = cursor.fetchall()
        result['data'] = []
            
        for ind,i in enumerate(tokenID):
            # # # # # print("i[0] : ",i[0])
            # # # # # print("i : ", i)
            if i[3] == 'E' or i[3] == 'C' or i[3] == 'G' or i[3] == 'T' or i[3] == 'P':
                result['data'].append({
                    'No': ind+1,
                    'ProperNoun': i[0],
                    'tokenType': i[3],
                    'NewRE': '<button onclick="changeSrc()" class="btn btn-secondary btn_view" tokenID="' + str(i.tokenID) + '">NewRE</button>',
                    'UnMerge':'<button onclick="UnMerge()" class="btn btn-danger btn_view">UnMerge</button>',
                })
            else:
                result['data'].append({
                    'No': ind+1,
                    'ProperNoun': i[0],
                    'tokenType': i[3],
                    'NewRE': '',
                    'UnMerge':'',
                })
    
        conn.commit()
        conn.close()
    return JsonResponse(result)

    #新增至Vocabulary並回傳新增的tokenID
@csrf_exempt
def insertVocabulary(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #result = cursor.execute("select * from Vocabulary")
        #取得post資料
        result['data'] = []
        record = {}
        record['token'] = request.POST.get('token')
        record['nWord'] = request.POST.get('nWord')
        record['tokenType'] = request.POST.get('tokenType')


        query = 'select * from [nlpVocabularyLatest  ].[dbo].[Vocabulary] where token = ? and nWord = ?;'
        args = [request.POST.get('token'),int(request.POST.get('nWord'))]
        cursor.execute(query, args)
        tokenID_original = cursor.fetchone()
        # # # # print("tokenID_original : ", tokenID_original)

        
        if tokenID_original == None and request.POST.get('tokenType'):

        #插入資料表
            query = 'INSERT into [nlpVocabularyLatest  ].[dbo].[Vocabulary] (token,nWord,tokenType) OUTPUT [INSERTED].tokenID,[INSERTED].token,[INSERTED].tokenType VALUES (?, ?, ?);'
            args = [request.POST.get('token'),int(request.POST.get('nWord')),request.POST.get('tokenType')]
            # # # # # print(args)
            cursor.execute(query, args)
            tokenID = cursor.fetchall()
            # # # # print(tokenID[0][0], tokenID[0][1], tokenID[0][2])
            if tokenID != []:
                result['status'] = '0'
                record['tokenID'] = tokenID[0][0]
                record['token'] = tokenID[0][1]
                record['tokenType'] = tokenID[0][2]
                result['data'].append(record)

        elif tokenID_original != None:
            # # # # # print("tokenID_original : ", tokenID_original)
            result['status'] = 'already_exist'
            record['tokenID'] = tokenID_original[2]
            record['token'] = tokenID_original[0]
            record['tokenType'] = tokenID_original[3]
            result['data'].append(record)

        # # # # # # print("data saved(Vocabulary)")
        conn.commit()
        conn.close()
            
    return JsonResponse(result)

    #新增至Vocabulary並回傳新增的tokenID
@csrf_exempt
def insertVocabulary_U(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #result = cursor.execute("select * from Vocabulary")
        #取得post資料
        result['data'] = []
        # record = {}
        # record['token'] = request.POST.get('token')
        # record['nWord'] = request.POST.get('nWord')
        # record['tokenType'] = request.POST.get('tokenType')
        token = request.POST.getlist('token[]')
        nWord = request.POST.getlist('nWord[]')
        tokenType = request.POST.getlist('tokenType[]')
        # # # # # print("token : ", len(token))
        # # # # # print("nWord : ", len(nWord))
        # # # # # print("tokenType : ", len(tokenType))
        tokenID = []
        args = []
        # for i in range(len(token)):
        #     args.append({"token": token[i], "nWord":nWord[i], "tokenType":tokenType[i], })


        #     # args = [Token,nWord[i],tokenType[i]]
        # query = 'EXEC insertVocabulary_POST @array = ?;'
        # args = json.dumps(args)
        # # # # # print(args)
        # cursor.execute(query, args)
        # newtoken = cursor.fetchall()
        # # # # print(" newtoken : ", newtoken)


        for i in range(len(token)):
            Token = token[i]
            # # # # # print("Token : ", Token)
            #先查詢
            query = 'select * from [nlpVocabularyLatest  ].[dbo].[Vocabulary] where token = ?;'
            args = [Token]
            cursor.execute(query, args)
            old_tokenID = cursor.fetchone()
            # # # # # # print("old_tokenID", old_tokenID)
            # # # # # # print("i : ", i)
            # 不存在插入
            if old_tokenID == None:
                # # # # # # print("i : ", i)
                query = 'INSERT into Vocabulary (token,nWord,tokenType) OUTPUT [INSERTED].tokenID VALUES (?, ?, ?);'
                args = [Token,nWord[i],tokenType[i]]
                # # # # # # print("args : ", args)
                cursor.execute(query, args)
                newtoken = cursor.fetchone()
                # 沒找到存現在的tokenID
                tokenID.append(newtoken.tokenID)
            else:
                # 有找到存舊的tokenID
                tokenID.append(old_tokenID.tokenID)
        # # # # print("ID : ", tokenID)

        
        result['status'] = '0'
        # record['tokenID'] = tokenID[0][0]

        # for i in newtoken:
        #     # # # print("i : ", i[0])
        #     # tokenID.append(i[0])
        #     result['data'].append(i[0])
        # # # # print("result : ", result)

        # # # # # # print("data saved(Vocabulary)")
        # # # # # print(result)

        for i in tokenID:
            result['data'].append(i)
        # # print(result)
            
        conn.commit()
        conn.close()            
    return JsonResponse(result)

    
@csrf_exempt
def getTextToken(request):
    #取得
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        filter_times = int(request.GET['filter_times'])
        if filter_times == 0:
            filter_times = 1
        query = '''
                EXEC two_word @filter_times = ?, @space = 44867;
                '''
        args = [filter_times]
        cursor.execute(query, args)
        textTokenData = cursor.fetchall()
        # # print("textTokenData : ", textTokenData)
        result['data'] = []
        # # # # # # print(textTokenData[0][0])
        record = {}
        RE = re.compile(r'([^\u4e00-\u9fa50-9a-zA-Z]{1})')
        RE1 = re.compile(r'([^\u4e00-\u9fa50-9a-zA-Z\(\)\:\[\]\{\}\-\/\.\,\+\<\>\~\!\@\#\$\%\^\&\*\_\=\;\'\"\?\`\【\】]{1})')
        number = 1
        for ind,i in enumerate(textTokenData):
            # # print("textTokenData : ", i)

            if request.GET['NoSign'] == 'NS':
                first = RE.findall(i[0])
                second = RE.findall(i[1])
                # # # # # print("first : ", first)
                # # # # # print("second : ", first)
                if first == [] and second == [] :
                    result['data'].append({
                        'No': '<button  onclick="searchReportText()" class="btn btn-secondary" name="'+ str(i[6]) +'" >' + str(number) + '</button>',
                        'First': i[0],
                        'Second': i[1],
                        'Times': i[5],
                        'Mergecheck':'<button onclick="merge()" class="btn btn-info" name="'+ str(i[4]) +'" >Merge</button>',
                    })
                    number += 1
                    
            else:                   
                # first = RE1.findall(i[0])
                # second = RE1.findall(i[1])
                # # # # # print("first : ", first)
                # # # # # print("second : ", first)
                # if (first == [] and second == []) or i[0] == '[NUM]' or i[1] == '[NUM]':
                result['data'].append({
                        'No': '<button  onclick="searchReportText()" class="btn btn-secondary" name="'+ str(i[6]) +'" >' + str(number) + '</button>',
                        'First': i[0],
                        'Second': i[1],
                        'Times': i[5],
                        'Mergecheck':'<button onclick="merge()" class="btn btn-info" name="'+ str(i[4]) +'" >Merge</button>',
                    })
                number += 1 

        conn.commit()
        conn.close()
        # # # # print("STATIC_ROOT : ", settings.STATIC_ROOT)

    #插入U資料
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # # # # # # print(request.POST)
        reportID = request.POST.getlist('reportID[]')
        posStart = request.POST.getlist('posStart[]')
        posEnd = request.POST.getlist('posEnd[]')
        tokenID = request.POST.getlist('tokenID[]')
        # # # print("tokenID :", tokenID)
        # tokenID = tokenID.split(",")
        # # # # print(len(reportID), len(posStart), len(posEnd), len(tokenID))
        # # # # # # print(  type(reportID), type(posStart), type(posEnd), type(tokenID))
        # # # # # # print("tokenID : ", tokenID.split(","))
        for i in range(len(reportID)):
            result['status'] = '0'
            # # # # # print(int(reportID[i]))
            # # # # # print(posStart[i])
            # # # # # print(posEnd[i])
            # # # # # print(int(tokenID[i]))
            # # # # # print( reportID[i], posStart[i], posEnd[i], tokenID[i])
            #插入資料表
            query = 'INSERT into [nlpVocabularyLatest  ].[dbo].[textToken] (reportID, posStart, posEnd, tokenID) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
            args = [int(reportID[i]), posStart[i], posEnd[i], int(tokenID[i])]
            # # # # # # print("args : ", args)
            cursor.execute(query, args)

        conn.commit()
        conn.close()

    #把posStart posEnd *(-1)
    if request.method == 'PATCH':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # # # # # print(body)
        # # # # # # print( body['reportID1'])

        tokenID1 = body['tokenID1']
        tokenID2 = body['tokenID2']
        tokenID3 = body['tokenID3']
        jump = body['jump']

        
        # # # print("tokenID :", tokenID1, tokenID2, tokenID3)


        

        if jump == "0":  
            query = '''
                EXEC [getTextToken_PATCH] @tokenID1=?, @tokenID2=?, @tokenID3=?, @block='A'
                '''
            args = [tokenID1, tokenID2, tokenID3]
            cursor.execute(query, args)
            changed_texttoken1 = cursor.fetchall()
            # # # # # # print("changed_texttoken first : ", changed_texttoken1)

            query = '''
                    EXEC [getTextToken_PATCH] @tokenID1=?, @tokenID2=?, @tokenID3=?, @block='B'
                    '''
            args = [tokenID1, tokenID2, tokenID3]
            cursor.execute(query, args)
            changed_texttoken2 = cursor.fetchall()
            # # # # # # print("changed_texttoken second: ", changed_texttoken2)
            # 
            #   
        else:
            # # print("it's jump PATCH")
            query = '''
                EXEC [getTextToken_PATCH] @tokenID1=?, @tokenID2=?, @tokenID3=?, @block='C'
                '''
            args = [tokenID1, tokenID2, tokenID3]
            cursor.execute(query, args)
            # changed_texttoken1 = cursor.fetchall()
            # # # print("changed_texttoken first : ", changed_texttoken1)

            query = '''
                    EXEC [getTextToken_PATCH] @tokenID1=?, @tokenID2=?, @tokenID3=?, @block='D'
                    '''
            args = [tokenID1, tokenID2, tokenID3]
            cursor.execute(query, args)
            # changed_texttoken2 = cursor.fetchall()
            # # # print("changed_texttoken second: ", changed_texttoken2)

            query = '''
                    EXEC [getTextToken_PATCH] @tokenID1=?, @tokenID2=?, @tokenID3=?, @block='E'
                    '''
            args = [tokenID1, tokenID2, tokenID3]
            cursor.execute(query, args)
            # changed_texttoken2 = cursor.fetchall()
            # # # print("changed_texttoken second: ", changed_texttoken2)



        
        result = {'status':'0'} #成功
        result['data'] = []
        record = {}

        # for i in changed_texttoken1:
            # # # # print(i)
            # record['reportID'] = i[0]
            # record['posStart'] = i[1]
            # record['posEnd'] = i[2]
            # record['tokenID'] = i[3]
            # result['data'].append(copy.deepcopy(record))
# 
        # for i in changed_texttoken2:
            # # # # print(i)
            # record['reportID'] = i[0]
            # record['posStart'] = i[1]
            # record['posEnd'] = i[2]
            # record['tokenID'] = i[3]
            # result['data'].append(copy.deepcopy(record))

        

        conn.commit()
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def getTextToken_3(request):
    #取得
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        
        filter_times = int(request.GET['filter_times'])
        if filter_times == 0:
            filter_times = 1

        query = '''
                EXEC three_word @filter_times = ?;
                ''' 
        args = [filter_times]
        cursor.execute(query, args)
        textTokenData = cursor.fetchall()
        # # # # print("textTokenData : ", textTokenData)
        result['data'] = []
        # # # # # # print(textTokenData[0][0])
        record = {}

        RE = re.compile(r'([^\u4e00-\u9fa50-9a-zA-Z \n]{1})') 
        RE1 = re.compile(r'([^\u4e00-\u9fa50-9a-zA-Z\(\)\:\[\]\{\}\-\/\.\,\+\<\>\~\!\@\#\$\%\^\&\*\_\=\;\'\"\?\`\【\】]{1})')
        number = 1
        for ind,i in enumerate(textTokenData):
            # # # # # print(i)

            if request.GET['NoSign'] == 'NS':
                first = RE.findall(i[0])
                second = RE.findall(i[1])
                third = RE.findall(i[2])
                if first == [] and second == [] and third == [] :
                    result['data'].append({
                        'No': '<button  onclick="searchReportText()" class="btn btn-secondary">' + str(number) + '</button>',
                        'First': i[0],
                        'Second': i[1],
                        'Third': i[2],
                        'Times': i[3],
                        'Mergecheck':'<button onclick="merge_3()" class="btn btn-info">Merge</button>',
                    })
                    number += 1
                    
            else:
                # first = RE1.findall(i[0])
                # second = RE1.findall(i[1])
                # third = RE.findall(i[2])
                # # # # # # print("first : ", first)
                # # # # # # print("second : ", first)
                # if (first == [] and second == [] and third == []) or i[0] == '[NUM]' or i[1] == '[NUM]' or i[2] == '[NUM]':
                result['data'].append({
                        'No': '<button  onclick="searchReportText()" class="btn btn-secondary">' + str(number) + '</button>',
                        'First': i[0],
                        'Second': i[1],
                        'Third': i[2],
                        'Times': i[3],
                        'Mergecheck':'<button onclick="merge_3()" class="btn btn-info">Merge</button>',
                    })
                number += 1

        conn.commit()
        conn.close()


    #把posStart posEnd *(-1)
    if request.method == 'PATCH':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # # # # # print(body)
        # # # # # # print( body['reportID1'])

        tokenID1 = body['tokenID1']
        tokenID2 = body['tokenID2']
        tokenID3 = body['tokenID3']

        
        # # # # # print(tokenID1, tokenID2, tokenID3)


        query = '''
                EXEC [getTextToken_3_PATCH] @tokenID1=?, @tokenID2=?,@tokenID3=?,@block='A'
                '''
        args = [tokenID1, tokenID2, tokenID3]
        cursor.execute(query, args)
        changed_texttoken1 = cursor.fetchall()
        # # # # # print("changed_texttoken first : ", changed_texttoken1)

        


        query = '''
                EXEC [getTextToken_3_PATCH] @tokenID1=?, @tokenID2=?,@tokenID3=?,@block='B'
                '''
        args = [tokenID1, tokenID2, tokenID3]
        cursor.execute(query, args)
        changed_texttoken2 = cursor.fetchall()
        # # # # # print("changed_texttoken second: ", changed_texttoken2)



        query = '''
                EXEC [getTextToken_3_PATCH] @tokenID1=?, @tokenID2=?,@tokenID3=?,@block='C'
                '''
        args = [tokenID1, tokenID2, tokenID3]
        cursor.execute(query, args)
        changed_texttoken3 = cursor.fetchall()
        # # # # # print("changed_texttoken Third: ", changed_texttoken3)

        # # # # # print("length of all data : ",  len(changed_texttoken1) + len(changed_texttoken2) + len(changed_texttoken3))



        
        result = {'status':'0'} #成功
        result['data'] = []
        record = {}

        for i in changed_texttoken1:
            # # # # # print(i)
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[2]
            record['tokenID'] = i[3]
            result['data'].append(copy.deepcopy(record))

        for i in changed_texttoken2:
            # # # # # print(i)
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[2]
            record['tokenID'] = i[3]
            result['data'].append(copy.deepcopy(record))

        for i in changed_texttoken3:
            # # # # # print(i)
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[2]
            record['tokenID'] = i[3]
            result['data'].append(copy.deepcopy(record))

        

        conn.commit()
        conn.close()
    return JsonResponse(result)
    


@csrf_exempt
def insertTexttoken(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()        

        tokenID1 = request.GET['tokenID1']
        tokenID2 = request.GET['tokenID2']
        # # # print("token : ", tokenID1, tokenID2, tokenID3)
        query = '''
                EXEC insertTexttoken_GET @tokenID1=? , @tokenID2=?, @tokenID3=?;
                '''
        args = [tokenID1, tokenID2 ]
        cursor.execute(query, args)
        position = cursor.fetchall()
        result['data'] = []
        record = {}
        for i in position:
            # # print( "reportID = ", i[0], "position from ", i[1], " to ", i[6])
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[6]
            result['data'].append(copy.deepcopy(record))
        # # # # # print(result)

        result['status'] = '0'
        conn.commit()
        conn.close()



    #插入新的textToken資料([1,1] + [2,2] = [1,2])
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        data = json.loads(request.body)
        # # # # # print("positionArray : ", data.get('positionArray[]'))
        # # # # # print("newTokenID : ", data.get('newTokenID'))

        positionArray = data.get('positionArray[]')
        newTokenID = data.get('newTokenID')
        args = []
        for i in positionArray:
            args.append({"reportID":i['reportID'], "posStart":i['posStart'], "posEnd":i['posEnd'], "newTokenID":newTokenID})           
        query = '''
            EXEC insertTexttoken_POST @array=?
        '''
        jsonArgs = json.dumps(args)
        cursor.execute(query, jsonArgs)
        
        result['status'] = '0'

        conn.commit()
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def insertTexttoken_3(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()        

        tokenID1 = request.GET['tokenID1']
        tokenID2 = request.GET['tokenID2']
        tokenID3 = request.GET['tokenID3']

        query = '''
                EXEC insertTexttoken3_GET @tokenID1=? , @tokenID2=? , @tokenID3=?
                '''
        args = [tokenID1, tokenID2, tokenID3]
        cursor.execute(query, args)
        position = cursor.fetchall()
        result['data'] = []
        record = {}
        for i in position:
            # # # # # print( "reportID = ", i[0], "position from ", i[1], " to ", i[10])
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[10]
            result['data'].append(copy.deepcopy(record))
        # # # # # print(result)

        result['status'] = '0'
        conn.commit()
        conn.close()



    #插入新的textToken資料([1,1] + [2,2] = [1,2])
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        data = json.loads(request.body)
        # # # # # print("positionArray : ", data.get('positionArray[]'))
        # # # # # print("newTokenID : ", data.get('newTokenID'))

        positionArray = data.get('positionArray[]')
        newTokenID = data.get('newTokenID')
        # # # # print(newTokenID)
        args = []
        for i in positionArray:
            args.append({"reportID":i['reportID'], "posStart":i['posStart'], "posEnd":i['posEnd'], "newTokenID":newTokenID})           
        query = '''
            EXEC insertTexttoken_POST @array=?
        '''
        jsonArgs = json.dumps(args)
        cursor.execute(query, jsonArgs)

        result['status'] = '0'

        conn.commit()
        conn.close()
    return JsonResponse(result)



    #新增至tokenRE並回傳tokenID.RE.tokenREID
@csrf_exempt
def inserttokenRE(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #result = cursor.execute("select * from [nlpVocabularyLatest  ].[dbo].[Vocabulary]")
        #取得post資料
        result['data'] = []
        record = {}
        record['tokenID'] = request.POST.get('tokenID')
        record['RE'] = request.POST.get('RE')


        query = 'select * from [nlpVocabularyLatest  ].[dbo].[vocabularyRE] where tokenID = ? and RE = ?;'
        args = [int(request.POST.get('tokenID')), request.POST.get('RE') ]
        cursor.execute(query, args)
        tokenREID_original = cursor.fetchall()
        # # # # # print("tokenREID_original : ", tokenREID_original)
        if tokenREID_original == []:
            #插入資料表
            query = 'INSERT into [nlpVocabularyLatest  ].[dbo].[vocabularyRE] (tokenID, RE) OUTPUT [INSERTED].REID VALUES (?, ?);'
            args = [int(request.POST.get('tokenID')), request.POST.get('RE') ]
            # # # # # print(args)
            cursor.execute(query, args)
            tokenREID = cursor.fetchall()
            # # # # # print(tokenREID[0])
            result['status'] = '0'
            record['tokenREID'] = tokenREID[0][0]            
            result['data'].append(record)
            # # # # # print("data saved(tokenRE)")
        else:
            result['status'] = 'already_exist'
    
        conn.commit()
        conn.close()

    return JsonResponse(result)

    #新增至tokenREItem並回傳tokenREID.serialNo.itemName.tokenREItemID
@csrf_exempt
def inserttokenREItem(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #result = cursor.execute("select * from Vocabulary")
        #取得post資料
        result['data'] = []
        record = {}
        record['tokenREID'] = request.POST.get('tokenREID')
        record['serialNo'] = request.POST.get('serialNo')
        record['itemName'] = request.POST.get('itemName')

        
        query = 'select * from [itemDefinition] where itemName = ?;'
        args = [request.POST.get('itemName')]
        cursor.execute(query, args)
        itemDefinition = cursor.fetchone()
        # # print("itemID : ", itemDefinition)
        if itemDefinition == None:            
            query = 'insert into [itemDefinition] (itemName) output [INSERTED].itemID values(?);'
            args = [request.POST.get('itemName')]
            cursor.execute(query, args)
            itemDefinition = cursor.fetchone()            
            # # print("inserted itemID : ", itemDefinition.itemID)#itemID[0]
        # else:
            # print("original itemID : ", itemDefinition.itemID)
        #插入資料表
        query = 'INSERT into [REItem] (REID, seqNo, itemID) OUTPUT [INSERTED].REItemID VALUES (?, ?, ?);'
        args = [int(request.POST.get('tokenREID')), request.POST.get('serialNo'), itemDefinition.itemID ]
        # # # # # print(args)
        cursor.execute(query, args)
        tokenREItemID = cursor.fetchone()
        # # # # # print(tokenREItemID[0])
        result['status'] = '0'
        record['tokenREItemID'] = tokenREItemID.REItemID
        result['data'].append(record)
        # # # # print("data saved(tokenREItem)")
        # # print(result)
        conn.commit()
        conn.close()


    return JsonResponse(result)

    #檢查傳入的token存不存在Vocabulary
@csrf_exempt
def checkName(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        Token = request.GET.getlist('Name[]')
        tokenID = []
        tokenType = []
        # # # # print("Token : ", Token)

        for i in range(len(Token)):
            query = 'SELECT * FROM [nlpVocabularyLatest  ].[dbo].[Vocabulary] WHERE token = ?;'
            args = [Token[i]]
            cursor.execute(query, args)
            token = cursor.fetchone()
            # # # # print("token : ", token)
            if token:
                tokenID.append(token.tokenID)
                if token.token == '[NUM]':
                    tokenType.append('U')
                else:                    
                    tokenType.append(token.tokenType)
                
                result['status'] = '0'
                result['tokenID'] = tokenID
                result['tokenType'] = tokenType
        # # # print(token)
        # # # # # # print(tokenType)
# 
        # # 有找到
        # if token:
        #     result['status'] = '0'
        #     result['tokenID'] = tokenID
        #     result['tokenType'] = tokenType
        
        # # # print("result : ", result)
        conn.commit()
        conn.close()
    return JsonResponse(result)

#找RE
@csrf_exempt
def checkRE(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        TokenID = request.GET.getlist('tokenID[]')
        RE = []
        TokenREID = []

        for i in range(len(TokenID)):
            query = 'SELECT * FROM [nlpVocabularyLatest  ].[dbo].[tokenRE] WHERE tokenID = ?;'
            args = [TokenID[i]]
            # # # # # # print(args)
            ## # # # # print(query)
            cursor.execute(query, args)
            tokenREID = cursor.fetchone()
            if tokenREID:
                RE.append(tokenREID.RE)
                TokenREID.append(tokenREID.tokenREID)
        # # # # # print("RE : ", RE)
        # # # # # print("TokenREID : ", TokenREID)

        #有找到
        if tokenREID != None:
            result['status'] = '0'
            result['RE'] = RE
            result['tokenREID'] = TokenREID
        
        conn.commit()
        conn.close()            
    return JsonResponse(result)

    #取得點選ID的reportText
@csrf_exempt
def getAnalyseText(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = 'SELECT * FROM [nlpVocabularyLatest  ].[dbo].[analyseText];'
        cursor.execute(query)
        reportText = cursor.fetchall()

        #有找到
        if reportText != None:
            result['status'] = '0'
            result['data'] = []
            for item in reportText:
                record = {}
                record['reportText'] = item.reportText
                result['data'].append(record)
        #     # # # # # print(token[0])
        conn.commit()
        conn.close()
        
    return JsonResponse(result)

    #讀取所有reportID
@csrf_exempt
def getReportID(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        # query = 'SELECT * FROM [nlpVocabularyLatest ].[dbo].[analyseText] where reportID = 10002;'
        # query = 'SELECT * FROM analyseText;'
        query = 'SELECT * FROM [nlpVocabularyLatest ].[dbo].[analyseText] where reportID >= ? and reportID <= ?'
        args = [request.GET['reportID1'], request.GET['reportID2']]
        
        cursor.execute(query, args)
        reportID = cursor.fetchall()
        # # # # # # print(reportID)

        #有找到
        if reportID != None:
            result['status'] = '0'
            result['data'] = []
            record = {}
            for item in reportID:
                if item.analysed == 0:
                    record[str(item.reportID)] = item.reportText
                else:
                    record[str(item.reportID)] = item.residualText
            result['data'].append(record)
        #     # # # # # print(token[0])
        # # # # # print(result)
        
        conn.commit()
        conn.close()
    return JsonResponse(result)

    #用reportID讀取reportText
@csrf_exempt
def getReportText(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = 'SELECT * FROM [nlpVocabularyLatest  ].[dbo].[analyseText] where reportID = ?;'
        args = [request.GET['reportID']]
        cursor.execute(query, args)
        reportID = cursor.fetchone()

        #有找到
        if reportID != None:
            ## # # # # print(reportID.reportText)
            result['status'] = '0'
            result['reportText'] = []
            # result['reportText'].append(reportID.reportText)
            if reportID.analysed == 0:
                result['reportText'].append(reportID.reportText)
            else:
                result['reportText'].append(reportID.residualText)

        
        conn.commit()
        conn.close()

    if request.method == 'PATCH':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # # # # # # print("patch in")
        #更新資料表
        query = 'update [nlpVocabularyLatest  ].[dbo].[analyseText]  set analysed = ?, residualText = ? output INSERTED.reportID,INSERTED.reportText,INSERTED.residualText where reportID = ?;'
        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # # # # # # print('data : ' + data.getlist['residualText'])
        # # # # # print( body['reportID'])
        
        args = [1, body['residualText'], body['reportID']]
        cursor.execute(query, args)
        reportID = cursor.fetchone()

        
        # Get a list of all running processes
        processes = psutil.process_iter()

        # Filter the list to include only cmd.exe processes
        cmd_processes = [p for p in processes if p.name() == 'cmd.exe']

        # Get the number of cmd.exe processes
        num_cmd_processes = len(cmd_processes)

        # # print(f"There are {num_cmd_processes} cmd.exe processes running.")

            
        # # # print(args)
        # # # print(reportID)

        # Close the pipe\

        #有找到
        if reportID != None:
            ## # # # # print(reportID.reportText)
            result['status'] = '0'
            result['reportText'] = reportID[0]
        conn.commit()
        conn.close()

    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # # # # # # print(request.POST)
        reportID = request.POST.getlist('reportID[]')
        posStart = request.POST.getlist('posStart[]')
        posEnd = request.POST.getlist('posEnd[]')
        token = request.POST.getlist('token[]')
        # # # # # # print(len(reportID), len(posStart), len(posEnd), len(tokenID))
        # # # # # # print(reportID, posStart, posEnd, tokenID)
        for i in range(len(reportID)):
            # # # # # # print(reportID[i], posStart[i], posEnd[i], tokenID[i])
            query = "select * from [nlpVocabularyLatest  ].[dbo].[Vocabulary] where token = ?"
            args = [token[i]]
            cursor.execute(query, args)
            id = cursor.fetchone()
            
            result['status'] = '0'
            if id.tokenType == 'U':
                result = {'status':'U'}
            #插入資料表
            query = 'INSERT into [nlpVocabularyLatest  ].[dbo].[textToken] (reportID, posStart, posEnd, tokenID) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
            args = [reportID[i], posStart[i], posEnd[i], id.tokenID]
            # # # # # # print("args : ", args)
            cursor.execute(query, args)

        conn.commit()
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def getTokenREItemID(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        data = []
        #取締一個取成功
        if request.is_ajax():
            # # # # # # print('Raw Data: "%s"' % request.body)
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            for i in body:
                data.append(i)
            # # # # # # print("data : ", data)
            # content = body[0]
            # # # # # # print('Data: "%s"' % content['year'])
        tokenIDArray = []
        tokentypeArray = []
        tokenREIDArray = []
        tokenREItemIDArray = []
                                        
        temp = []
        
        for i in range(len(data)):
            temp.clear()
            # # # # # # print("data[i] : ", data[i])
            if data[i]['tokenID']:
                #查詢tokenType
                query = 'SELECT * FROM [nlpVocabularyLatest  ].[dbo].[Vocabulary] where tokenID = ?;'
                args = [data[i]['tokenID']]
                cursor.execute(query, args)
                tokenType = cursor.fetchone()
                # # # # # # print("tokenType ", tokenID.tokenType)
                if tokenType:
                    tokenIDArray.append(tokenType.tokenID)
                    tokentypeArray.append(tokenType.tokenType)

                if tokenType.tokenType != 'T' or tokenType.tokenType != 'U':
                    #查詢tokenREID
                    # # # # # print("tokentype is not T or U")
                    query = 'SELECT * FROM [nlpVocabularyLatest  ].[dbo].[tokenRE] where tokenID = ?;'
                    args = [data[i]['tokenID']]
                    cursor.execute(query, args)
                    tokenREID = cursor.fetchone()
                    if tokenREID:
                        tokenREIDArray.append(tokenREID.tokenREID)
                    # # # # # print("data[i].keys()", data[i].keys())
                    for j in range(len(list(data[i].keys()))):
                        if tokenType.tokenType != 'T' or tokenType.tokenType != 'U':
                            # # # # # # print(j)
                            #查詢tokenREItemID
                            query = 'SELECT * FROM [nlpVocabularyLatest ].[dbo].[tokenREItem] where tokenREID = ? and itemName = ?;'
                            args = [tokenREID.tokenREID, list(data[i].keys())[j]]
                            cursor.execute(query, args)
                            tokenREItemID = cursor.fetchone()
                        if tokenREItemID:
                            temp.append(tokenREItemID.tokenREItemID)
                            # # # # # print("temp : ", temp)
                        # # # # # print("j : ", j)
                        # # # # # print("len : ", len(list(data[i].keys()))-1)
                        if len(list(data[i].keys()))-1 == j:
                            tokenREItemIDArray.append(copy.deepcopy(temp))
                            # # # # # print("tokenREItemIDArray : ", tokenREItemIDArray)

        record = {}
        result['data'] = []
        record['tokenID'] = tokenIDArray
        record['tokenREID'] = tokenREIDArray
        record['tokenType'] = tokentypeArray
        record['tokenREItemID'] = tokenREItemIDArray
        result['data'].append(record)
        # # # # # # print(result)
        conn.commit()
        conn.close()
        result['status'] = '0'
    return JsonResponse(result)

@csrf_exempt
def insertExtractedValueFromToken(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # # # # # # print("request: ", request.POST.getlist('tokenID[]'))

        #取得post資料
        reportID = request.POST.getlist('reportID[]')
        posStart = request.POST.getlist('posStart[]')
        tokenREItemID = request.POST.getlist('tokenREItemID[]')
        tokenType = request.POST.getlist('tokenType[]')
        Value = request.POST.getlist('Value[]')
        # # # # # print("reportID: ", request.POST.getlist('reportID[]'))
        # # # # # print("posStart: ", request.POST.getlist('posStart[]'))
        # # # # # print("tokenREItemID: ", request.POST.getlist('tokenREItemID[]'))
        # # # # # print("tokenType: ", request.POST.getlist('tokenType[]'))
        # # # # # print("Value: ", request.POST.getlist('Value[]'))

        # 處理tokenREItemID二維陣列(用逗號分開轉int)
        for i in range(len(tokenREItemID)):
            tokenREItemID[i] = tokenREItemID[i].split(',')
            for j in range(len(tokenREItemID[i])):
                tokenREItemID[i][j] = int(tokenREItemID[i][j])
        # # # # # # print("tokenREItemID: ", tokenREItemID)

        # 處理Value二維陣列(用逗號分開)
        for i in range(len(Value)):
            Value[i] = Value[i].split(',')
        # # # # # print("Value: ", len(Value))
        # # # # # print("Value: ", Value)
        
        # # # # # # print("tokenREItemID: ", len(tokenREItemID))
        tokenREItemIDIndex = 0
        #插入資料表()
        for i in range(len(reportID)):
            # # # # # # print("i : ", i)
            if tokenType[i]  != 'T' or tokenType[i]  != 'U':
                # # # # # print("TU")
                for j in range(len(tokenREItemID[tokenREItemIDIndex])):
                    # # # # # # print("j : ", j)
                    # # # # # # print(tokenType[i])
                    # # # # # # print(reportID[i], posStart[i], tokenREItemID[i][j], Value[i][j])
                    query = 'INSERT into [nlpVocabularyLatest  ].[dbo].[extractedValueFromToken] (reportID, posStart, tokenREItemID, extractedValue) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
                    Value[tokenREItemIDIndex][j] = Value[tokenREItemIDIndex][j].replace("|", ",")
                    args = [reportID[i], posStart[i], tokenREItemID[tokenREItemIDIndex][j], Value[tokenREItemIDIndex][j]]
                    # # # # # print(args)
                    cursor.execute(query, args)
                tokenREItemIDIndex += 1

        conn.commit()
        conn.close()
        result['status'] = '0'
        # # # # # # print(result)
    return JsonResponse(result)


@csrf_exempt
def getToken(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # # # # # # print("request: ", request.POST.getlist('tokenID[]'))

        #取得資料
        tokenID1 = request.POST.getlist('tokenID1[]')
        tokenID2 = request.POST.getlist('tokenID2[]')
        # # # # # # print(tokenID1)        
        # # # # # # print(tokenID2)
        token1 = []
        token2 = []
        for i in tokenID1:
            # # # # # # print(i)
            query = 'select * from [nlpVocabularyLatest  ].[dbo].[Vocabulary] where tokenID = ?;'
            args = [i]
            cursor.execute(query, args)
            token = cursor.fetchone()
            # # # # # # print(token.token)
            token1.append(token.token)

        for i in tokenID2:
            # # # # # # print(i)
            query = 'select * from [nlpVocabularyLatest  ].[dbo].[Vocabulary] where tokenID = ?;'
            args = [i]
            cursor.execute(query, args)
            token = cursor.fetchone()
            # # # # # # print(token.token)
            token2.append(token.token)

        # # # # # # print(token1)
        # # # # # # print(token2)
        result['data'] = []
        record = {}
        record['token1'] = token1
        record['token2'] = token2
        result['data'].append(record)
        conn.commit()
        conn.close()
        result['status'] = '0'
        # # # # # # print(result)
    return JsonResponse(result)

        #讀取tokenID再檢查textToken是否為正值
@csrf_exempt
def getTokenIDCheckTextToken(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        token = request.POST.getlist('token[]')
        # # # # # # print(token)

        PNarray = []
        for i, t in enumerate(token):
            pn = 0
            # # # # # print("Index:", i, "Token:", t)
            query = 'SELECT * FROM [nlpVocabularyLatest  ].[dbo].[Vocabulary] where token = ?;'
            args = [t]
            # # # # # # print(i)

            
            cursor.execute(query, args)
            tokenID = cursor.fetchone()

            # 有找到
            if tokenID != None:
                # # # # # # print(tokenID.tokenID)
                
                query = 'SELECT * FROM [nlpVocabularyLatest  ].[dbo].[textToken] where tokenID = ?;'
                args = [tokenID.tokenID]

                cursor.execute(query, args)
                textTokenData = cursor.fetchall()

                if textTokenData != []:
                    # # # # # # print(textTokenData)
                    result['status'] = '0'
                    for jcount, j in enumerate(textTokenData) :
                        result['status'] = '0'
                        if (j[1] > 0 and j[2] > 0) == False:
                            # # # # # print("negative")
                            PNarray.append(1)
                            pn = 1      
                            break
                        # # # # # print("jcount :", jcount, " len : ", len(textTokenData))
                        if jcount == len(textTokenData)-1 and pn == 0:
                            PNarray.append(0)
                else:
                    pn = 0      
                    PNarray.append(2)
        
        result['data'] = PNarray
        # # # # # # print("PNarray : ", PNarray)
        conn.commit()
        conn.close()
    return JsonResponse(result)



@csrf_exempt
def getNextWord(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        num = int(request.GET['word'])
        firstToken = request.GET['firstToken']
        # # # # # print(firstToken)
        # # # # # # print(token)

        token = ''
        mergetoken = ''
        innerjoinpos = ''
        innerjointoken = ''
        groupby = ''
        #如果>=3就遞迴增加
        if num >= 3:
            for i in range(num-2):
                token += f', c{i+5}.token as token{i+5}'
                mergetoken += f' + c{i+5}.token'
                if i == 0:
                    innerjoinpos += f' inner join [nlpVocabularyLatest  ].[dbo].[textToken] as b{i+4} on a1.reportID = b{i+4}.reportID and (a1.posEnd + 1) = b{i+4}.posStart and a1.posStart > 0 and b{i+4}.posStart > 0'
                else:
                    innerjoinpos += f' inner join [nlpVocabularyLatest  ].[dbo].[textToken] as b{i+4} on a1.reportID = b{i+4}.reportID and (b{i+3}.posEnd + 1) = b{i+4}.posStart and b{i+3}.posStart > 0 and b{i+4}.posStart > 0'

                innerjointoken += f' inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as c{i+5} on b{i+4}.tokenID = c{i+5}.tokenID'
                groupby += f' , c{i+5}.token'
                text = innerjoinpos
        #如果<3就固定抓三個字
        else:
            token = f''' , a5.token as token3'''
            mergetoken = f''' + a5.token'''
            innerjoinpos = f''' inner join [nlpVocabularyLatest  ].[dbo].[textToken] as a4 on a1.reportID = a4.reportID and (a1.posEnd + 1) = a4.posStart and a1.posStart > 0 and a4.posStart > 0'''
            innerjointoken = f''' inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a5 on a4.tokenID = a5.tokenID'''
            groupby = f''' , a5.token'''
            text = innerjoinpos

        query = f'''
                select textTokenData.* from (
                '''
        query +=f'''
                 select a2.token as token1, a3.token as token2
                '''
        # query +=f''' , a{num+2}.token as token{num}'''
        query += token

        query +=f''' , COUNT(*) as times, a2.token + a3.token'''

        # query +=f''' + a{num+2}.token'''
        query += mergetoken

        query +=f''' as mergeToken
                from [nlpVocabularyLatest  ].[dbo].[textToken] as a0
                inner join [nlpVocabularyLatest  ].[dbo].[textToken] as a1 on a0.reportID = a1.reportID and (a0.posEnd + 1) = a1.posStart and a0.posStart > 0 and a1.posStart > 0
                '''
        # query +=f''' inner join [nlpVocabularyLatest  ].[dbo].[textToken] as a4 on a1.reportID = a{num+1}.reportID and (a1.posEnd + 1) = a{num+1}.posStart and a1.posStart > 0 and a{num+1}.posStart > 0'''
        query += innerjoinpos
        # 找第一個字
        if firstToken != "":
            query +=f''' inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a2 on a0.tokenID = a2.tokenID and a2.token = '{firstToken}'
                    inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a3 on a1.tokenID = a3.tokenID
                    '''
        else:
            query +=f''' inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a2 on a0.tokenID = a2.tokenID
                    inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a3 on a1.tokenID = a3.tokenID
                    '''
        # query +=f''' inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a{num+2} on a{num+1}.tokenID = a{num+2}.tokenID'''
        query += innerjointoken
        query +=f''' group by a2.token, a3.token
                '''
        # query +=f''' , a{num+2}.token'''
        query += groupby
        
        query +=f'''
                ) as textTokenData
                left join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as word on textTokenData.mergeToken = word.token
                where word.tokenID is null
                order by times desc;
                '''
        # # # # print("query : ", query)
        # # # # # print("text : ", text)
        
        
        cursor.execute(query)
        texttoken = cursor.fetchall()
        # # # print("texttoken : ", texttoken)
        # for i in texttoken:
        #     # if i[0] == '[NUM]':
        #     # # # # print("texttoken : ", i)
        result['data'] = []
        record = {}
        if texttoken != []:
            record['reportID'] = texttoken[0][num + 1]

            for ind,i in enumerate(texttoken):
                # # # # # print("i[0] : ",i[0])
                dataDict = {}
                if num >= 3:
                    # # # # # print("i[ind] : ", type(i))
                    if type(i) != int:
                        for index,j in enumerate(i):
                            # # # # # print("j : ", j)
                            # # # # # print("i[index] : ", i[index])
                            dataDict[str(index + 1)] = j
                    dataDict["No"] = ind+1
                    dataDict["times"] = i[len(i)-2]
                    # # # # print("dataDict : ", dataDict)
                    result['data'].append(dataDict)
                else:
                    # # # # print(i[len(i)-2])
                    result['data'].append({
                        'No': ind+1,
                        '1': i[0],
                        '2': i[1],
                        '3': i[2],
                        'times': i[len(i)-2],
                    })

        # # # # # print("PNarray : ", PNarray)
        # # print("result['data'] : ", result['data'])
        conn.commit()
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def getNextWordReport(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        num = int(request.GET['word'])
        firstToken = request.GET['firstToken']
        # # # # print(firstToken)
        # # # # # # print(token)

        token = ''
        mergetoken = ''
        innerjoinpos = ''
        innerjointoken = ''
        groupby = ''
        #如果>=3就遞迴增加
        if num >= 3:
            for i in range(num-2):
                token += f', c{i+5}.token as token{i+5}'
                mergetoken += f' + c{i+5}.token'
                if i == 0:
                    innerjoinpos += f' inner join [nlpVocabularyLatest  ].[dbo].[textToken] as b{i+4} on a1.reportID = b{i+4}.reportID and (a1.posEnd + 1) = b{i+4}.posStart and a1.posStart > 0 and b{i+4}.posStart > 0'
                else:
                    innerjoinpos += f' inner join [nlpVocabularyLatest  ].[dbo].[textToken] as b{i+4} on a1.reportID = b{i+4}.reportID and (b{i+3}.posEnd + 1) = b{i+4}.posStart and b{i+3}.posStart > 0 and b{i+4}.posStart > 0'

                innerjointoken += f' inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as c{i+5} on b{i+4}.tokenID = c{i+5}.tokenID'
                groupby += f' , c{i+5}.token'
                text = innerjoinpos
        #如果<3就固定抓三個字
        else:
            token = f''' , a5.token as token3'''
            mergetoken = f''' + a5.token'''
            innerjoinpos = f''' inner join [nlpVocabularyLatest  ].[dbo].[textToken] as a4 on a1.reportID = a4.reportID and (a1.posEnd + 1) = a4.posStart and a1.posStart > 0 and a4.posStart > 0'''
            innerjointoken = f''' inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a5 on a4.tokenID = a5.tokenID'''
            groupby = f''' , a5.token'''
            text = innerjoinpos

        query = f'''
                select textTokenData.* from (
                '''
        query +=f'''
                 select a2.token as token1, a3.token as token2
                '''
        # query +=f''' , a{num+2}.token as token{num}'''
        query += token

        query +=f''' , COUNT(*) as times, a2.token + a3.token'''

        # query +=f''' + a{num+2}.token'''
        query += mergetoken

        query +=f''' as mergeToken
                from [nlpVocabularyLatest  ].[dbo].[textToken] as a0
                inner join [nlpVocabularyLatest  ].[dbo].[textToken] as a1 on a0.reportID = a1.reportID and (a0.posEnd + 1) = a1.posStart and a0.posStart > 0 and a1.posStart > 0
                '''
        # query +=f''' inner join [nlpVocabularyLatest  ].[dbo].[textToken] as a4 on a1.reportID = a{num+1}.reportID and (a1.posEnd + 1) = a{num+1}.posStart and a1.posStart > 0 and a{num+1}.posStart > 0'''
        query += innerjoinpos
        # 找第一個字
        if firstToken != "":
            query +=f''' inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a2 on a0.tokenID = a2.tokenID and a2.token = '{firstToken}' and a2.tokenType != 'E'
                    inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a3 on a1.tokenID = a3.tokenID
                    '''
        else:
            query +=f''' inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a2 on a0.tokenID = a2.tokenID
                    inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a3 on a1.tokenID = a3.tokenID
                    '''
        # query +=f''' inner join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as a{num+2} on a{num+1}.tokenID = a{num+2}.tokenID'''
        query += innerjointoken
        query +=f''' group by a2.token, a3.token
                '''
        # query +=f''' , a{num+2}.token'''
        query += groupby
        
        query +=f'''
                ) as textTokenData
                left join [nlpVocabularyLatest  ].[dbo].[Vocabulary] as word on textTokenData.mergeToken = word.token
                where word.tokenID is null
                order by times desc;
                '''
        # # # # print("query : ", query)
        # # # # print("text : ", text)
        
        
        cursor.execute(query)
        texttoken = cursor.fetchall()
        # # # # print("texttoken : ", texttoken)
        # for i in texttoken:
        #     # if i[0] == '[NUM]':
        #     # # # # print("texttoken : ", i)
        result['data'] = []
        record = {}
        if texttoken != []:
            record['reportID'] = texttoken[0][num + 1]

            for ind,i in enumerate(texttoken):
                # # # # # print("i[0] : ",i[0])
                dataDict = {}
                if num >= 3:
                    # # # # # print("i[ind] : ", type(i))
                    if type(i) != int:
                        for index,j in enumerate(i):
                            # # # # # print("j : ", j)
                            # # # # # print("i[index] : ", i[index])
                            dataDict[str(index + 1)] = j
                    dataDict["No"] = ind+1
                    dataDict["times"] = i[len(i)-2]
                    # # # # # print("dataDict : ", dataDict)
                    result['data'].append(dataDict)
                else:
                    # # # # print(i[len(i)-2])
                    result['data'].append({
                        'No': ind+1,
                        '1': i[0],
                        '2': i[1],
                        '3': i[2],
                        'times': i[len(i)-2],
                    })

        # # # # # print("PNarray : ", PNarray)
        conn.commit()
        conn.close()
    return JsonResponse(result)


@csrf_exempt
def getSynTypo(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes; as_dict=True;')
        cursor = conn.cursor()
        #插入資料表
        # query = 'SELECT * FROM [nlpVocabularyLatest  ].[dbo].[Vocabulary] where tokenType = ?;'
        # args = [request.GET['tokenType']]
        # cursor.execute(query, args)
        query = "SELECT * FROM [nlpVocabularyLatest  ].[dbo].[Vocabulary] where tokenType != \'U\' and token != '[NUM]' ;"
        cursor.execute(query)
        Vocabulary = cursor.fetchall()
        # # # # # print("Vocabulary : ", Vocabulary)
        


        
        result['data'] = []
        record = {}
        for i in Vocabulary:
            record['token'] = i[0]
            record['nWord'] = i[1]
            record['tokenID'] = i[2]
            record['tokenType'] = i[3]
            result['data'].append(copy.deepcopy(record))
        result['status'] = '0'
        conn.commit()
        conn.close()
    return JsonResponse(result)


@csrf_exempt
def getReportTextByMergeToken(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes; as_dict=True;')
        cursor = conn.cursor()
        words = request.GET['words']
        mergetoken = request.GET['mergeToken']
        # # # # print(type(words))
        # # # # print(mergetoken)
        if words == "2":
            query = "EXEC [countMergeToken_GET] @mergeToken = ?;"
        else:
            query = "EXEC [countMergeToken3_GET] @mergeToken = ?;"
        args = [mergetoken]

        cursor.execute(query, args)
        Text = cursor.fetchall()
        # # # # print("Text : ", Text)
        


        
        result['data'] = []
        record = {}
        for i in Text:
            if words == "2":
                record['reportID'] = i[4]
                record['reportText'] = i[5]
            else:
                record['reportID'] = i[5]
                record['reportText'] = i[6]
            result['data'].append(copy.deepcopy(record))
        result['status'] = '0'
        conn.commit()
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def getMergeLog(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes; as_dict=True;')
        cursor = conn.cursor()
        twoOrThree = request.POST.get('twoOrThree')
        # # print("twoOrThree : ", twoOrThree)
        if twoOrThree == "2":
            token1 = request.POST.get('token1')
            token2 = request.POST.get('token2')            
            mergedToken = request.POST.get('mergedToken')

            # # print("token1 : ", token1)
            # # print("token2 : ", token2)
            # # print("mergedToken : ", mergedToken)

            query = "EXEC [insertMergeLog_POST] @mergedToken = ?, @token1 = ?, @token2 = ?, @token3 = ?;"
            args = [mergedToken, token1, token2, None]
            # # print("args : ", args)

            cursor.execute(query, args)
            rec = cursor.fetchall()
            # # print("rec : ", rec)        
            
            result['status'] = '0'
        elif twoOrThree == "3":
            token1 = request.POST.get('token1')
            token2 = request.POST.get('token2')       
            token3 = request.POST.get('token3')
            mergedToken = request.POST.get('mergedToken')

            query = "EXEC [insertMergeLog_POST] @mergedToken = ?, @token1 = ?, @token2 = ?, @token3 = ?;"
            args = [mergedToken, token1, token2, token3]

            cursor.execute(query, args)
            rec = cursor.fetchall()
            # # print("rec : ", rec)
            result['status'] = '0'
        # # # # print("Text : ", Text)
        


        
        conn.commit()
        conn.close()
    return JsonResponse(result)







@csrf_exempt
def chineseTwoWord(request):
    #取得
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        filter_times = int(request.GET['filter_times'])
        if filter_times == 0:
            filter_times = 1
        query = '''
                EXEC cTwoCounting @LB = ?;
                '''
        args = [filter_times]
        cursor.execute(query, args)
        textTokenData = cursor.fetchall()
        # # # # print("textTokenData : ", textTokenData)
        result['data'] = []
        # # # # # # print(textTokenData[0][0])
        record = {}
        number = 1
        for ind,i in enumerate(textTokenData):
            # # # print("textTokenData : ", i)
            result['data'].append({
                'No': '<button  onclick="searchReportText()" class="btn btn-secondary" name="'+ i.mergeWord +'" >' + str(number) + '</button>',
                'First': i.token1,
                'Second': i.token2,
                'Times': i.times,
                'Mergecheck':'<button onclick="allInOne()" class="btn btn-info" mergeToken="'+ i.mergeWord +'" mergeNWord="'+ str(i.mergeNWord) +'">Merge</button>',
            })
            number += 1
                    
           

        conn.commit()
        conn.close()    
    return JsonResponse(result)

@csrf_exempt
def chineseThreeWord(request):
    #取得
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        
        filter_times = int(request.GET['filter_times'])
        if filter_times == 0:
            filter_times = 1
        
        if request.GET['English'] == 'English':
            query = '''
                    EXEC [gThreeCounting] @LB = ?;
                    ''' 

        else:
            query = '''
                    EXEC [cThreeCounting] @LB = ?;
                    ''' 
        args = [filter_times]
        cursor.execute(query, args)
        textTokenData = cursor.fetchall()
        # # # # print("textTokenData : ", textTokenData)
        result['data'] = []
        # # # # # # print(textTokenData[0][0])
        record = {}
        number = 1
        for ind,i in enumerate(textTokenData):

            result['data'].append({
                'No': '<button  onclick="searchReportText()" class="btn btn-secondary" name="'+ i.mergeWord +'">' + str(number) + '</button>',
                'First': i.token1,
                'Second': i.token2,
                'Third': i.token3,
                'Times': i.times,
                'Mergecheck':'<button onclick="merge_3()" class="btn btn-info" mergeToken="'+ i.mergeWord +'" mergeNWord="'+ str(i.mergeNWord) +'">Merge</button>',
            })
            number += 1

        conn.commit()
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def getTokenBynWord(request):
    #取得
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        
        start = process_time()  
        # ------------------------------------------------------- 抓token--------------------------------------------------------------------
        query = '''
                SELECT * FROM [nlpVocabularyLatest ].[dbo].[Vocabulary]
                where tokenType in ('C', 'G', 'S') and token not in ('Undefined_Chinese', 'Undefined_English', 'Undefined_Sign')
                order by nWord desc
                ''' 
        cursor.execute(query)
        Vocabulary = cursor.fetchall()
        # # print("Vocabulary : ", Vocabulary)
        # -----------------------------------------------------------------------------------------------------------------------------------

        
        # ------------------------------------------------------- 處理報告殘文--------------------------------------------------------------------
        query = '''
                SELECT top(10000) * FROM [nlpVocabularyLatest ].[dbo].[analyseText]
                ''' 
        cursor.execute(query)
        text = cursor.fetchall()
        
        for j in text:
            query = j.reportText
            restartPos = 0
            for ind,i in enumerate(Vocabulary):
                # # # print(i, ind)
                
                word = i.token
                startPos = query.find(word, restartPos)
                endPos = startPos + len(word)
                if startPos >= 0 and endPos >= 0:
                    # # # print("token : ", i.token, i.tokenType)
                    # # # print("startPos : ", startPos)
                    # # # print("endPos : ", endPos)
                    # # # print("length : ", len(word), "\n")

                    if i.tokenType == "G" and startPos-1 > 0 and endPos + 1 < len(query):
                        # # # print("alpha : ", query[startPos-1], query[startPos-1].isalpha())

                        if (query[startPos-1].isalpha() == False) and (query[endPos+1].isalpha() == False):
                            replacement = ' ' * len(word)
                            query = query[:startPos] + replacement + query[endPos:]
                            # # # print("query : ", query)
                        else:
                            restartPos = endPos
                            # # # print("restartPos changed : ", restartPos)
                    else:
                        replacement = ' ' * len(word)
                        query = query[:startPos] + replacement + query[endPos:]
                        # # # print("query : ", query)
                    # # # print("query : ", query)

        
        
        end = process_time()  
        # # print("time : ", end - start)
        # cursor.execute(query)
        # Vocabulary = cursor.fetchall()
        # # # print("Vocabulary : ", Vocabulary)
        # -----------------------------------------------------------------------------------------------------------------------------------
        conn.commit()
        conn.close()
    return JsonResponse(result)


@csrf_exempt
def getReportBetween2Tokens6(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # # # # # print(body)
        # # # # # # print( body['reportID1'])

        firstTokenID = body['firstTokenID']
        secondTokenID = body['secondTokenID']
        tokens = body['tokens[]']
        # # # print(firstTokenID, secondTokenID, tokens)
        string = ""
        for i in tokens:
            string += str(i) + " "
        string = string[0:len(string)-1] 
        # # print("string : ", string)
        
        tokenTypes = body['tokenTypes[]']
        # # # print(firstTokenID, secondTokenID, tokens)
        Types = ""
        for i in tokenTypes:
            Types += i + ","
        Types = Types[0:len(Types)-1] 
        # # # print("string : ", string)
        
        query = '''
                select * from [summary_6f](?,?,?) order by 1 desc
                ''' 
        args = [firstTokenID, secondTokenID, string]
        # print(Types)
        # print(args)
        cursor.execute(query, args)
        datatoken = cursor.fetchall()
        # print(datatoken)
        result['data'] = []
        number = 1
        for ind,i in enumerate(datatoken):
            # # # print(i)
            token1 = i.token1 if i.token1 != ' ' else '[SPACE]'
            token2 = i.token2 if i.token2 != ' ' else '[SPACE]'
            token3 = i.token3 if i.token3 != ' ' else '[SPACE]'
            token4 = i.token4 if i.token4 != ' ' else '[SPACE]'
            token5 = i.token5 if i.token5 != ' ' else '[SPACE]'
            token6 = i.token6 if i.token6 != ' ' else '[SPACE]'
            mergeToken2 = i.token1 + i.token2
            mergeToken3 = i.token1 + i.token2 + i.token3
            mergeToken4 = i.token1 + i.token2 + i.token3 + i.token4
            mergeToken5 = i.token1 + i.token2 + i.token3 + i.token4 + i.token5
            result['data'].append({
                'No': '<div >' + str(number) + '</div>',
                'Token1': token1,
                'Token2': token2,
                'Token3': token3,
                'Token4': token4,
                'Token5': token5,
                'Token6': token6,
                'NumReports': i.numReports,
                'Times': i.times,
                'Mergecheck':'<button onclick="allInOneTwoThreeFiveWord()" class="btn btn-info btn_view" ' + 
                'mergeToken2="'+ mergeToken2 +
                '" mergeToken3="'+ mergeToken3 + 
                '" mergeToken4="'+ mergeToken4 + 
                '" mergeToken5="'+ mergeToken5 + 
                '" mergeNWord2="'+ str(i.nWord2) +
                '" mergeNWord3="'+ str(i.nWord3) +
                '" mergeNWord4="'+ str(i.nWord4) +
                '" mergeNWord5="'+ str(i.nWord5) +
                '">Merge</button>',
                'Type': i.tokenType,
            })
            number += 1
        
        conn.commit()
        conn.close()
        
        end = time.time()
        # print("start - end = ",  end - start)
    return JsonResponse(result)


@csrf_exempt
def getReportBetween2Tokens6All(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        
        query = '''
                select * from summary_6() order by 1 desc
                ''' 
        cursor.execute(query)
        datatoken = cursor.fetchall()
        # print(datatoken)
        result['data'] = []
        number = 1
        for ind,i in enumerate(datatoken):
            # # # print(i)
            token1 = i.token1 if i.token1 != ' ' else '[SPACE]'
            token2 = i.token2 if i.token2 != ' ' else '[SPACE]'
            token3 = i.token3 if i.token3 != ' ' else '[SPACE]'
            token4 = i.token4 if i.token4 != ' ' else '[SPACE]'
            token5 = i.token5 if i.token5 != ' ' else '[SPACE]'
            token6 = i.token6 if i.token6 != ' ' else '[SPACE]'
            mergeToken2 = i.token1 + i.token2
            mergeToken3 = i.token1 + i.token2 + i.token3
            mergeToken4 = i.token1 + i.token2 + i.token3 + i.token4
            mergeToken5 = i.token1 + i.token2 + i.token3 + i.token4 + i.token5
            result['data'].append({
                'No': '<div >' + str(number) + '</div>',
                'Token1': token1,
                'Token2': token2,
                'Token3': token3,
                'Token4': token4,
                'Token5': token5,
                'Token6': token6,
                'NumReports': i.numReports,
                'Times': i.times,
                'Mergecheck':'<button onclick="allInOneTwoThreeFiveWord()" class="btn btn-info btn_view" ' + 
                'mergeToken2="'+ mergeToken2 +
                '" mergeToken3="'+ mergeToken3 + 
                '" mergeToken4="'+ mergeToken4 + 
                '" mergeToken5="'+ mergeToken5 + 
                '" mergeNWord2="'+ str(i.nWord2) +
                '" mergeNWord3="'+ str(i.nWord3) +
                '" mergeNWord4="'+ str(i.nWord4) +
                '" mergeNWord5="'+ str(i.nWord5) +
                '">Merge</button>',
                'Type': i.tokenType,
            })
            number += 1
        
        conn.commit()
        conn.close()
        
        end = time.time()
        # print("start - end = ",  end - start)
    return JsonResponse(result)


@csrf_exempt
def getReportBetween2Tokens5(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # # # # # print(body)
        # # # # # # print( body['reportID1'])

        firstTokenID = body['firstTokenID']
        secondTokenID = body['secondTokenID']
        tokens = body['tokens[]']
        # # # print(firstTokenID, secondTokenID, tokens)
        string = ""
        for i in tokens:
            string += str(i) + " "
        string = string[0:len(string)-1] 
        # # print("string : ", string)
        
        tokenTypes = body['tokenTypes[]']
        # # # print(firstTokenID, secondTokenID, tokens)
        Types = ""
        for i in tokenTypes:
            Types += i + ","
        Types = Types[0:len(Types)-1] 
        # # # print("string : ", string)
        
        query = '''
                select * from [summary_5f](?,?,?) order by 1 desc
                ''' 
        args = [firstTokenID, secondTokenID, string]
        # print(Types)
        # print(args)
        cursor.execute(query, args)
        datatoken = cursor.fetchall()
        # print(datatoken)
        result['data'] = []
        number = 1
        for ind,i in enumerate(datatoken):
            # # # print(i)
            token1 = i.token1 if i.token1 != ' ' else '[SPACE]'
            token2 = i.token2 if i.token2 != ' ' else '[SPACE]'
            token3 = i.token3 if i.token3 != ' ' else '[SPACE]'
            token4 = i.token4 if i.token4 != ' ' else '[SPACE]'
            token5 = i.token5 if i.token5 != ' ' else '[SPACE]'
            mergeToken2 = i.token1 + i.token2
            mergeToken3 = i.token1 + i.token2 + i.token3
            mergeToken4 = i.token1 + i.token2 + i.token3 + i.token4
            result['data'].append({
                'No': '<div >' + str(number) + '</div>',
                'Token1': token1,
                'Token2': token2,
                'Token3': token3,
                'Token4': token4,
                'Token5': token5,
                'NumReports': i.numReports,
                'Times': i.times,
                'Mergecheck':'<button onclick="allInOneTwoThreeFiveWord()" class="btn btn-info btn_view" ' + 
                'mergeToken2="'+ mergeToken2 +
                '" mergeToken3="'+ mergeToken3 + 
                '" mergeToken4="'+ mergeToken4 + 
                '" mergeNWord2="'+ str(i.nWord2) +
                '" mergeNWord3="'+ str(i.nWord3) +
                '" mergeNWord4="'+ str(i.nWord4) +
                '">Merge</button>',
                'Type': i.tokenType,
            })
            number += 1
        
        conn.commit()
        conn.close()
        
        end = time.time()
        # print("start - end = ",  end - start)
    return JsonResponse(result)


@csrf_exempt
def getReportBetween2Tokens5All(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        query = '''
                select * from summary_5() order by 1 desc
                ''' 
        cursor.execute(query)
        datatoken = cursor.fetchall()
        # print(datatoken)
        result['data'] = []
        number = 1
        for ind,i in enumerate(datatoken):
            # # # print(i)
            token1 = i.token1 if i.token1 != ' ' else '[SPACE]'
            token2 = i.token2 if i.token2 != ' ' else '[SPACE]'
            token3 = i.token3 if i.token3 != ' ' else '[SPACE]'
            token4 = i.token4 if i.token4 != ' ' else '[SPACE]'
            token5 = i.token5 if i.token5 != ' ' else '[SPACE]'
            mergeToken2 = i.token1 + i.token2
            mergeToken3 = i.token1 + i.token2 + i.token3
            mergeToken4 = i.token1 + i.token2 + i.token3 + i.token4
            result['data'].append({
                'No': '<div >' + str(number) + '</div>',
                'Token1': token1,
                'Token2': token2,
                'Token3': token3,
                'Token4': token4,
                'Token5': token5,
                'NumReports': i.numReports,
                'Times': i.times,
                'Mergecheck':'<button onclick="allInOneTwoThreeFiveWord()" class="btn btn-info btn_view" ' + 
                'mergeToken2="'+ mergeToken2 +
                '" mergeToken3="'+ mergeToken3 + 
                '" mergeToken4="'+ mergeToken4 + 
                '" mergeNWord2="'+ str(i.nWord2) +
                '" mergeNWord3="'+ str(i.nWord3) +
                '" mergeNWord4="'+ str(i.nWord4) +
                '">Merge</button>',
                'Type': i.tokenType,
            })
            number += 1
        
        conn.commit()
        conn.close()
        
        end = time.time()
        # print("start - end = ",  end - start)
    return JsonResponse(result)


@csrf_exempt
def getReportBetween2Tokens4(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # # # # # print(body)
        # # # # # # print( body['reportID1'])

        firstTokenID = body['firstTokenID']
        secondTokenID = body['secondTokenID']
        tokens = body['tokens[]']
        # # # print(firstTokenID, secondTokenID, tokens)
        string = ""
        for i in tokens:
            string += str(i) + " "
        string = string[0:len(string)-1] 
        # # print("string : ", string)
        
        tokenTypes = body['tokenTypes[]']
        # # # print(firstTokenID, secondTokenID, tokens)
        Types = ""
        for i in tokenTypes:
            Types += i + ","
        Types = Types[0:len(Types)-1] 
        # # # print("string : ", string)
        
        query = '''
                select * from [summary_4f](?,?,?) order by 1 desc
                ''' 
        args = [firstTokenID, secondTokenID, string]
        # print(Types)
        # print(args)
        cursor.execute(query, args)
        datatoken = cursor.fetchall()
        # print(datatoken)
        result['data'] = []
        number = 1
        for ind,i in enumerate(datatoken):
            # # # print(i)
            token1 = i.token1 if i.token1 != ' ' else '[SPACE]'
            token2 = i.token2 if i.token2 != ' ' else '[SPACE]'
            token3 = i.token3 if i.token3 != ' ' else '[SPACE]'
            token4 = i.token4 if i.token4 != ' ' else '[SPACE]'
            mergeToken2 = i.token1 + i.token2
            mergeToken3 = i.token1 + i.token2 + i.token3
            result['data'].append({
                'No': '<div >' + str(number) + '</div>',
                'Token1': token1,
                'Token2': token2,
                'Token3': token3,
                'Token4': token4,
                'NumReports': i.numReports,
                'Times': i.times,
                'Mergecheck':'<button onclick="allInOneTwoThreeFiveWord()" class="btn btn-info btn_view" ' + 
                'mergeToken2="'+ mergeToken2 +
                '" mergeToken3="'+ mergeToken3 + 
                '" mergeNWord2="'+ str(i.nWord2) +
                '" mergeNWord3="'+ str(i.nWord3) +
                '">Merge</button>',
                'Type': i.tokenType,
            })
            number += 1
        
        conn.commit()
        conn.close()
        
        end = time.time()
        # print("start - end = ",  end - start)
    return JsonResponse(result)


@csrf_exempt
def getReportBetween2Tokens4All(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        query = '''
                select * from [summary_4]() order by 1 desc
                ''' 
        cursor.execute(query)
        datatoken = cursor.fetchall()
        # print(datatoken)
        result['data'] = []
        number = 1
        for ind,i in enumerate(datatoken):
            # # # print(i)
            token1 = i.token1 if i.token1 != ' ' else '[SPACE]'
            token2 = i.token2 if i.token2 != ' ' else '[SPACE]'
            token3 = i.token3 if i.token3 != ' ' else '[SPACE]'
            token4 = i.token4 if i.token4 != ' ' else '[SPACE]'
            mergeToken2 = i.token1 + i.token2
            mergeToken3 = i.token1 + i.token2 + i.token3
            result['data'].append({
                'No': '<div >' + str(number) + '</div>',
                'Token1': token1,
                'Token2': token2,
                'Token3': token3,
                'Token4': token4,
                'NumReports': i.numReports,
                'Times': i.times,
                'Mergecheck':'<button onclick="allInOneTwoThreeFiveWord()" class="btn btn-info btn_view" ' + 
                'mergeToken2="'+ mergeToken2 +
                '" mergeToken3="'+ mergeToken3 + 
                '" mergeNWord2="'+ str(i.nWord2) +
                '" mergeNWord3="'+ str(i.nWord3) +
                '">Merge</button>',
                'Type': i.tokenType,
            })
            number += 1
        
        conn.commit()
        conn.close()
        
        end = time.time()
        # print("start - end = ",  end - start)
    return JsonResponse(result)


@csrf_exempt
def getReportBetween2Tokens3(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # # # # # print(body)
        # # # # # # print( body['reportID1'])

        firstTokenID = body['firstTokenID']
        secondTokenID = body['secondTokenID']
        tokens = body['tokens[]']
        # # # print(firstTokenID, secondTokenID, tokens)
        string = ""
        for i in tokens:
            string += str(i) + " "
        string = string[0:len(string)-1] 
        # # print("string : ", string)
        
        tokenTypes = body['tokenTypes[]']
        # # # print(firstTokenID, secondTokenID, tokens)
        Types = ""
        for i in tokenTypes:
            Types += i + ","
        Types = Types[0:len(Types)-1] 
        # # # print("string : ", string)
        
        query = '''
                select * from [summary_3f](?,?,?) order by 1 desc
                ''' 
        args = [firstTokenID, secondTokenID, string]
        # print(Types)
        # print(args)
        cursor.execute(query, args)
        datatoken = cursor.fetchall()
        # print(datatoken)
        result['data'] = []
        number = 1
        for ind,i in enumerate(datatoken):
            # # # print(i)
            token1 = i.token1 if i.token1 != ' ' else '[SPACE]'
            token2 = i.token2 if i.token2 != ' ' else '[SPACE]'
            token3 = i.token3 if i.token3 != ' ' else '[SPACE]'
            mergeToken2 = i.token1 + i.token2
            mergeToken3 = i.token1 + i.token2 + i.token3
            result['data'].append({
                'No': '<div >' + str(number) + '</div>',
                'Token1': token1,
                'Token2': token2,
                'Token3': token3,
                'NumReports': i.numReports,
                'Times': i.times,
                'Mergecheck':'<button onclick="allInOneTwoThreeFiveWord()" class="btn btn-info btn_view" ' + 
                'mergeToken2="'+ mergeToken2 +
                '" mergeNWord2="'+ str(i.nWord2) +
                '">Merge</button>',
                'Type': i.tokenType,
            })
            number += 1
        
        conn.commit()
        conn.close()
        
        end = time.time()
        # print("start - end = ",  end - start)
    return JsonResponse(result)


@csrf_exempt
def getReportBetween2Tokens3All(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        query = '''
                select * from [summary_3]() order by 1 desc
                ''' 
        cursor.execute(query)
        datatoken = cursor.fetchall()
        # print(datatoken)
        result['data'] = []
        number = 1
        for ind,i in enumerate(datatoken):
            # # # print(i)
            token1 = i.token1 if i.token1 != ' ' else '[SPACE]'
            token2 = i.token2 if i.token2 != ' ' else '[SPACE]'
            token3 = i.token3 if i.token3 != ' ' else '[SPACE]'
            mergeToken2 = i.token1 + i.token2
            mergeToken3 = i.token1 + i.token2 + i.token3
            result['data'].append({
                'No': '<div >' + str(number) + '</div>',
                'Token1': token1,
                'Token2': token2,
                'Token3': token3,
                'NumReports': i.numReports,
                'Times': i.times,
                'Mergecheck':'<button onclick="allInOneTwoThreeFiveWord()" class="btn btn-info btn_view" ' + 
                'mergeToken2="'+ mergeToken2 +
                '" mergeNWord2="'+ str(i.nWord2) +
                '">Merge</button>',
                'Type': i.tokenType,
            })
            number += 1
        
        conn.commit()
        conn.close()
        
        end = time.time()
        # print("start - end = ",  end - start)
    return JsonResponse(result)


@csrf_exempt
def fiveWord(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes; as_dict=True;')
        cursor = conn.cursor()
        block = 0
        try:
            token1 = request.POST.get('token1')
            token2 = request.POST.get('token2')
            token3 = request.POST.get('token3')
            token4 = request.POST.get('token4')
            token5 = request.POST.get('token5')
            if token1 == None or token2 == None or token3 == None or token4 == None or token5 == None:
                raise Exception("token None")
            # ------------------------------------------------------- 抓舊字tokenID---------------------------------------------------------------
            # # print("token1 : ", token1)
            # # print("token2 : ", token2)
            # # print("token3 : ", token3)
            # # print("token4 : ", token4)
            # # print("token5 : ", token5)
            token = [token1, token2, token3, token4, token5]
            tokenIDArray = []
            for i in token:
                query = "select tokenID from Vocabulary where token = ?;"
                args = [i]
                tokenID = cursor.execute(query, args).fetchone()
                # # print("tokenID : ", tokenID)
                tokenIDArray.append(tokenID.tokenID)
            # # print("tokenIDArray : ", tokenIDArray)
            # tokenIDArray.append(tokenID.tokenID)
            tokenID1 = tokenIDArray[0]
            tokenID2 = tokenIDArray[1]
            tokenID3 = tokenIDArray[2]
            tokenID4 = tokenIDArray[3]
            tokenID5 = tokenIDArray[4]

            if tokenID1 == None or tokenID2 == None or tokenID3 == None or tokenID4 == None or tokenID5 == None:
                raise Exception("tokenID None")
            
            # # print(tokenID1, tokenID2)
            # ------------------------------------------------------------------------------------------------------------------------------------
            
            block = 1


            # ------------------------------------------------------- 抓原本的位置-----------------------------------------------------------------
            query = "EXEC [fiveWord] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?, @tokenID5 = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4, tokenID5]

            cursor.execute(query, args)
            fiveWordRes = cursor.fetchall()
            # # # print("twoWordNoJumpRes : ", twoWordNoJumpRes)
            
            if fiveWordRes == None :
                raise Exception("twoWordNoJumpRes None")
            
            mergeToken = request.POST.get('mergeToken')
            if mergeToken == None :
                raise Exception("mergeToken None")
            
            argsForinsertTextToken = []
            for i,ind in enumerate(fiveWordRes):
                # 取得資料
                # # # print("reportID :", ind[0], "|posStart :", ind[1], "|posEnd :", ind[2], "|mergeToken : ", mergeToken)
            #     args = []
            #     args.append({"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":newTokenID})
                data = {"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":mergeToken}
                argsForinsertTextToken.append(copy.deepcopy(data))
            # # # print("argsForinsertTextToken : ", argsForinsertTextToken)

            #------------------------------------------------------------------------------------------------------------------------------------    
            

            
            block = 2
            
            # ------------------------------------------------------- *(-1)-----------------------------------------------------------------------
            query = "EXEC [fiveWord*-1] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?, @tokenID5 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4, tokenID5, 'A']
            timesMinusOneA = cursor.execute(query, args)
            # # # print("timesMinusOneA : ", len(timesMinusOneA))

            
            
            query = "EXEC [fiveWord*-1] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?, @tokenID5 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4, tokenID5, 'B']
            timesMinusOneB = cursor.execute(query, args)
            query = "EXEC [fiveWord*-1] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?, @tokenID5 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4, tokenID5, 'C']
            timesMinusOneB = cursor.execute(query, args)
            query = "EXEC [fiveWord*-1] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?, @tokenID5 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4, tokenID5, 'D']
            timesMinusOneB = cursor.execute(query, args)
            query = "EXEC [fiveWord*-1] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?, @tokenID5 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4, tokenID5, 'E']
            timesMinusOneB = cursor.execute(query, args)
            # # # print("timesMinusOneB : ", len(timesMinusOneB))
            # ------------------------------------------------------------------------------------------------------------------------------------

            
            block = 3
            
            # ------------------------------------------------------- 插入新字---------------------------------------------------------------------           
            TokenType = request.POST.get('TokenType')
            # # print("TokenType : ", TokenType)
            query = "select token, tokenID from Vocabulary where token = ?;"
            args = [mergeToken]
            selectMergeToken = cursor.execute(query, args).fetchone()
            # # print("selectMergeToken : ", selectMergeToken)        
            nWord = request.POST.get('nWord')
            if selectMergeToken == None:
                query = "insert into Vocabulary (token, nWord, tokenType) output [inserted].tokenID values(?, ?, ?);"
                args = [mergeToken, nWord, TokenType]
                inertMergeToken = cursor.execute(query, args).fetchone()
                # # print("inertMergeToken : ", inertMergeToken.tokenID)
                newTokenID = inertMergeToken.tokenID
            else:
                newTokenID = selectMergeToken.tokenID
            # # print("newTokenID : ", newTokenID)
            # ------------------------------------------------------------------------------------------------------------------------------------

            
            block = 4
            
            # ------------------------------------------------------- 插入新textToken--------------------------------------------------------------
            
            args = []
            for i,ind in enumerate(fiveWordRes):
                # 取得資料
                # # # print("reportID :", ind[0], "|posStart :", ind[1], "|posEnd :", ind[2], "|mergeToken : ", mergeToken)
                args.append({"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":newTokenID})
                

            # # print(args)
            query = ' EXEC insertTexttoken_POST @array = ?;'
            args = json.dumps(args)
            selectMergeToken = cursor.execute(query, args)
            # ------------------------------------------------------------------------------------------------------------------------------------
            result['status'] = '0'
            # # # # print("Text : ", Text)
            


            
            # block = 5
            
            conn.commit()
            # # print("committed")
        except Exception as e:
            conn.rollback()
            # # print("rollbacked, error message : ", e, " block : ", block)
            result['ERRMSG'] = str(e)
        conn.close()
        # # print(result)
    return JsonResponse(result)


@csrf_exempt
def fourWord(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes; as_dict=True;')
        cursor = conn.cursor()
        block = 0
        try:
            token1 = request.POST.get('token1')
            token2 = request.POST.get('token2')
            token3 = request.POST.get('token3')
            token4 = request.POST.get('token4')
            if token1 == None or token2 == None or token3 == None or token4 == None:
                raise Exception("token None")
            # ------------------------------------------------------- 抓舊字tokenID---------------------------------------------------------------
            # # print("token1 : ", token1)
            # # print("token2 : ", token2)
            # # print("token3 : ", token3)
            # # print("token4 : ", token4)
            token = [token1, token2, token3, token4]
            tokenIDArray = []
            for i in token:
                query = "select tokenID from Vocabulary where token = ?;"
                args = [i]
                tokenID = cursor.execute(query, args).fetchone()
                # # print("tokenID : ", tokenID)
                tokenIDArray.append(tokenID.tokenID)
            # # print("tokenIDArray : ", tokenIDArray)
            # tokenIDArray.append(tokenID.tokenID)
            tokenID1 = tokenIDArray[0]
            tokenID2 = tokenIDArray[1]
            tokenID3 = tokenIDArray[2]
            tokenID4 = tokenIDArray[3]

            if tokenID1 == None or tokenID2 == None or tokenID3 == None or tokenID4 == None:
                raise Exception("tokenID None")
            
            # # print(tokenID1, tokenID2)
            # ------------------------------------------------------------------------------------------------------------------------------------
            
            block = 1


            # ------------------------------------------------------- 抓原本的位置-----------------------------------------------------------------
            query = "EXEC [fourWord] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4]

            cursor.execute(query, args)
            fourWordRes = cursor.fetchall()
            # # # print("twoWordNoJumpRes : ", twoWordNoJumpRes)
            
            if fourWordRes == None :
                raise Exception("twoWordNoJumpRes None")
            
            mergeToken = request.POST.get('mergeToken')
            if mergeToken == None :
                raise Exception("mergeToken None")
            
            argsForinsertTextToken = []
            for i,ind in enumerate(fourWordRes):
                # 取得資料
                # # # print("reportID :", ind[0], "|posStart :", ind[1], "|posEnd :", ind[2], "|mergeToken : ", mergeToken)
            #     args = []
            #     args.append({"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":newTokenID})
                data = {"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":mergeToken}
                argsForinsertTextToken.append(copy.deepcopy(data))
            # # # print("argsForinsertTextToken : ", argsForinsertTextToken)

            #------------------------------------------------------------------------------------------------------------------------------------    
            

            
            block = 2
            
            # ------------------------------------------------------- *(-1)-----------------------------------------------------------------------
            query = "EXEC [fourWord*-1] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4, 'A']
            timesMinusOneA = cursor.execute(query, args)
            # # # print("timesMinusOneA : ", len(timesMinusOneA))

            
            
            query = "EXEC [fourWord*-1] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4, 'B']
            timesMinusOneB = cursor.execute(query, args)
            query = "EXEC [fourWord*-1] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4, 'C']
            timesMinusOneB = cursor.execute(query, args)
            query = "EXEC [fourWord*-1] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @tokenID4 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, tokenID4, 'D']
            timesMinusOneB = cursor.execute(query, args)
            # # # print("timesMinusOneB : ", len(timesMinusOneB))
            # ------------------------------------------------------------------------------------------------------------------------------------

            
            block = 3
            
            # ------------------------------------------------------- 插入新字---------------------------------------------------------------------           
            TokenType = request.POST.get('TokenType')
            # # print("TokenType : ", TokenType)
            query = "select token, tokenID from Vocabulary where token = ?;"
            args = [mergeToken]
            selectMergeToken = cursor.execute(query, args).fetchone()
            # # print("selectMergeToken : ", selectMergeToken)        
            nWord = request.POST.get('nWord')
            if selectMergeToken == None:
                query = "insert into Vocabulary (token, nWord, tokenType) output [inserted].tokenID values(?, ?, ?);"
                args = [mergeToken, nWord, TokenType]
                inertMergeToken = cursor.execute(query, args).fetchone()
                # # print("inertMergeToken : ", inertMergeToken.tokenID)
                newTokenID = inertMergeToken.tokenID
            else:
                newTokenID = selectMergeToken.tokenID
            # # print("newTokenID : ", newTokenID)
            # ------------------------------------------------------------------------------------------------------------------------------------

            
            block = 4
            
            # ------------------------------------------------------- 插入新textToken--------------------------------------------------------------
            
            args = []
            for i,ind in enumerate(fourWordRes):
                # 取得資料
                # # # print("reportID :", ind[0], "|posStart :", ind[1], "|posEnd :", ind[2], "|mergeToken : ", mergeToken)
                args.append({"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":newTokenID})
                

            # # print(args)
            query = ' EXEC insertTexttoken_POST @array = ?;'
            args = json.dumps(args)
            selectMergeToken = cursor.execute(query, args)
            # ------------------------------------------------------------------------------------------------------------------------------------
            result['status'] = '0'
            # # # # print("Text : ", Text)
            


            
            # block = 5
            
            conn.commit()
            # # print("committed")
        except Exception as e:
            conn.rollback()
            # # print("rollbacked, error message : ", e, " block : ", block)
            result['ERRMSG'] = str(e)
        conn.close()
        # # print(result)
    return JsonResponse(result)


@csrf_exempt
def threeWord(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes; as_dict=True;')
        cursor = conn.cursor()
        block = 0
        try:
            token1 = request.POST.get('token1')
            token2 = request.POST.get('token2')
            token3 = request.POST.get('token3')
            if token1 == None or token2 == None or token3 == None:
                raise Exception("token None")
            # ------------------------------------------------------- 抓舊字tokenID---------------------------------------------------------------
            # # print("token1 : ", token1)
            # # print("token2 : ", token2)
            # # print("token3 : ", token3)
            token = [token1, token2, token3]
            tokenIDArray = []
            for i in token:
                query = "select tokenID from Vocabulary where token = ?;"
                args = [i]
                tokenID = cursor.execute(query, args).fetchone()
                tokenIDArray.append(tokenID.tokenID)
            # # print("tokenID : ", tokenIDArray)
            # tokenIDArray.append(tokenID.tokenID)
            tokenID1 = tokenIDArray[0]
            tokenID2 = tokenIDArray[1]
            tokenID3 = tokenIDArray[2]

            if tokenID1 == None or tokenID2 == None or tokenID3 == None:
                raise Exception("tokenID None")
            
            # # print(tokenID1, tokenID2)
            # ------------------------------------------------------------------------------------------------------------------------------------
            
            block = 1


            # ------------------------------------------------------- 抓原本的位置-----------------------------------------------------------------
            query = "EXEC [threeWord] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?;"
            args = [tokenID1, tokenID2, tokenID3]

            cursor.execute(query, args)
            threeWordRes = cursor.fetchall()
            # # # print("twoWordNoJumpRes : ", twoWordNoJumpRes)
            
            if threeWordRes == None :
                raise Exception("threeWordRes None")
            
            mergeToken = request.POST.get('mergeToken')
            if mergeToken == None :
                raise Exception("mergeToken None")
            
            argsForinsertTextToken = []
            for i,ind in enumerate(threeWordRes):
                # 取得資料
                # # # print("reportID :", ind[0], "|posStart :", ind[1], "|posEnd :", ind[2], "|mergeToken : ", mergeToken)
            #     args = []
            #     args.append({"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":newTokenID})
                data = {"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":mergeToken}
                argsForinsertTextToken.append(copy.deepcopy(data))
            # # # print("argsForinsertTextToken : ", argsForinsertTextToken)

            #------------------------------------------------------------------------------------------------------------------------------------    
            

            
            block = 2
            
            # ------------------------------------------------------- *(-1)-----------------------------------------------------------------------
            query = "EXEC [getTextToken_3_PATCH] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, 'A']
            timesMinusOneA = cursor.execute(query, args)
            # # # print("timesMinusOneA : ", len(timesMinusOneA))

            
            
            query = "EXEC [getTextToken_3_PATCH] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, 'B']
            timesMinusOneB = cursor.execute(query, args)
            query = "EXEC [getTextToken_3_PATCH] @tokenID1 = ?, @tokenID2 = ?, @tokenID3 = ?, @block = ?;"
            args = [tokenID1, tokenID2, tokenID3, 'C']
            timesMinusOneB = cursor.execute(query, args)
            # # # print("timesMinusOneB : ", len(timesMinusOneB))
            # ------------------------------------------------------------------------------------------------------------------------------------

            
            block = 3
            
            # ------------------------------------------------------- 插入新字---------------------------------------------------------------------           
            TokenType = request.POST.get('TokenType')
            # # print("TokenType : ", TokenType)
            query = "select token, tokenID from Vocabulary where token = ?;"
            args = [mergeToken]
            selectMergeToken = cursor.execute(query, args).fetchone()
            # # print("selectMergeToken : ", selectMergeToken)
            nWord = request.POST.get('nWord')
            if selectMergeToken == None:
                query = "insert into Vocabulary (token, nWord, tokenType) output [inserted].tokenID values(?, ?, ?);"
                args = [mergeToken, nWord, TokenType]
                inertMergeToken = cursor.execute(query, args).fetchone()
                # # print("inertMergeToken : ", inertMergeToken.tokenID)
                newTokenID = inertMergeToken.tokenID
            else:
                newTokenID = selectMergeToken.tokenID
            # # print("newTokenID : ", newTokenID)
            # ------------------------------------------------------------------------------------------------------------------------------------

            
            block = 4
            
            # ------------------------------------------------------- 插入新textToken--------------------------------------------------------------
            
            args = []
            for i,ind in enumerate(threeWordRes):
                # 取得資料
                # # # print("reportID :", ind[0], "|posStart :", ind[1], "|posEnd :", ind[2], "|mergeToken : ", mergeToken)
                args.append({"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":newTokenID})
                

            # # print(args)
            query = ' EXEC insertTexttoken_POST @array = ?;'
            args = json.dumps(args)
            selectMergeToken = cursor.execute(query, args)
            # ------------------------------------------------------------------------------------------------------------------------------------
            result['status'] = '0'
            # # # # print("Text : ", Text)
            


            
            # block = 5
            
            conn.commit()
            # # print("committed")
        except Exception as e:
            conn.rollback()
            # # print("rollbacked, error message : ", e, " block : ", block)
            result['ERRMSG'] = str(e)
        conn.close()
        # # print(result)
    return JsonResponse(result)


@csrf_exempt
def twoWord(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes; as_dict=True;')
        cursor = conn.cursor()
        token1 = request.POST.get('token1')
        token2 = request.POST.get('token2')

        block = 0
        
        try:
            # ------------------------------------------------------- 抓舊字tokenID---------------------------------------------------------------
            # # print("token1 : ", token1)
            # # print("token2 : ", token2)
            
            if token1 == None or token2 == None:
                raise Exception("token None")
            token = [token1, token2]
            tokenIDArray = []
            for i in token:
                query = "select tokenID from Vocabulary where token = ?;"
                args = [i]
                tokenID = cursor.execute(query, args).fetchone()
                tokenIDArray.append(tokenID.tokenID)
            tokenID1 = tokenIDArray[0]
            tokenID2 = tokenIDArray[1]
            

            if tokenID1 == None or tokenID2 == None:
                raise Exception("tokenID None")

            # # print(tokenID1, tokenID2)
            # ------------------------------------------------------------------------------------------------------------------------------------
            block = 1



            # ------------------------------------------------------- 抓原本的位置-----------------------------------------------------------------
            query = "EXEC [twoWordNoJump] @tokenID1 = ?, @tokenID2 = ?;"
            args = [tokenID1, tokenID2]
            # # print("twoWordNoJump : ", args)

            cursor.execute(query, args)
            twoWordNoJumpRes = cursor.fetchall()
            
            
            if twoWordNoJumpRes == None :
                raise Exception("twoWordNoJumpRes None")
            # # # print("twoWordNoJumpRes : ", twoWordNoJumpRes)
            mergeToken = request.POST.get('mergeToken')
            if mergeToken == None :
                raise Exception("mergeToken None")
            
            argsForinsertTextToken = []
            for i,ind in enumerate(twoWordNoJumpRes):
                # 取得資料
                # # # print("reportID :", ind[0], "|posStart :", ind[1], "|posEnd :", ind[2], "|mergeToken : ", mergeToken)
            #     args = []
            #     args.append({"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":newTokenID})
                data = {"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":mergeToken}
                argsForinsertTextToken.append(copy.deepcopy(data))

            # ------------------------------------------------------------------------------------------------------------------------------------  
            block = 2  
            # 


            
            # ------------------------------------------------------- *(-1)-----------------------------------------------------------------------
            query = "EXEC [twoWordNoJump*-1] @tokenID1 = ?, @tokenID2 = ?, @block = ?;"
            args = [tokenID1, tokenID2, 'A']
            timesMinusOneA = cursor.execute(query, args).fetchall()
            # # print("timesMinusOneA : ", len(timesMinusOneA))

            
            
            query = "EXEC [twoWordNoJump*-1] @tokenID1 = ?, @tokenID2 = ?, @block = ?;"
            args = [tokenID1, tokenID2, 'B']
            timesMinusOneB = cursor.execute(query, args).fetchall()
            # # print("timesMinusOneB : ", len(timesMinusOneB))
            # ------------------------------------------------------------------------------------------------------------------------------------
            block = 3


            
            # ------------------------------------------------------- 插入新字---------------------------------------------------------------------        
            TokenType = request.POST.get('TokenType')
            query = "select token, tokenID from Vocabulary where token = ?;"
            args = [mergeToken]
            selectMergeToken = cursor.execute(query, args).fetchone()
            # # print("selectMergeToken : ", selectMergeToken)        
            nWord = request.POST.get('nWord')
            if selectMergeToken == None:
                query = "insert into Vocabulary (token, nWord, tokenType) output [inserted].tokenID values(?, ?, ?);"
                args = [mergeToken, nWord, TokenType]
                inertMergeToken = cursor.execute(query, args).fetchone()
                # # print("inertMergeToken : ", inertMergeToken.tokenID)
                newTokenID = inertMergeToken.tokenID
            else:
                newTokenID = selectMergeToken.tokenID
            # # print("newTokenID : ", newTokenID)
            # ------------------------------------------------------------------------------------------------------------------------------------
            block = 4

            
            
            # ------------------------------------------------------- 插入新textToken--------------------------------------------------------------
            
            args = []
            for i,ind in enumerate(twoWordNoJumpRes):
                # 取得資料
                # # # print("reportID :", ind[0], "|posStart :", ind[1], "|posEnd :", ind[2], "|mergeToken : ", mergeToken)
                args.append({"reportID":ind[0], "posStart":ind[1], "posEnd":ind[2], "newTokenID":newTokenID})
                

            # # print(args)
            query = ' EXEC insertTexttoken_POST @array = ?;'
            args = json.dumps(args)
            selectMergeToken = cursor.execute(query, args)
            # ------------------------------------------------------------------------------------------------------------------------------------
            block = 5
            conn.commit()
            result['status'] = '0'
        
        except Exception as e:
            conn.rollback()
            # # print("rollbacked, error message : ", e, " block : ", block)
            result['ERRMSG'] = str(e)
        # # # # print("Text : ", Text)
        


        
        conn.close()
    return JsonResponse(result)


@csrf_exempt
def getAllWordExsisting(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes; as_dict=True;')
        cursor = conn.cursor()
        
        raw = request.body.decode('utf-8')
        try:
            
            body = json.loads(raw)
            # # # # # print(body)
            # # # # # # print( body['reportID1'])

            reportFormID = body['reportFormID']

            query = '''SELECT * FROM [nlpVocabularyLatest ].[dbo].[reportFormVocabulary] as a 
            right join [nlpVocabularyLatest ].[dbo].[Vocabulary] as b 
            on a.tokenID = b.tokenID and a.reportFormID = ?
            '''
            args = [reportFormID]

            cursor.execute(query, args)
            select = cursor.fetchall()
            # # print(select)
            conn.commit()
            result['status'] = '0'
            token = []
            tokenID = []
            selected = []
            for i in select :
                if (i.reportFormID != reportFormID and i.reportFormID == None):
                    selected.append('Y')
                else:
                    selected.append('N')                
                token.append(i.token)
                tokenID.append(i.tokenID)

            result['token'] = token
            result['tokenID'] = tokenID
            result['selected'] = selected

            
            query = "select tokenID, token from Vocabulary;"

            cursor.execute(query)
            select = cursor.fetchall()

        
        except Exception as e:
            conn.rollback()
            # print("rollbacked, error message : ", e)
            result['ERRMSG'] = str(e)
        


        # # print(result)
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def testVocabularyGetReport(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        try :
            body = json.loads(raw)
            # # # # # print(body)
            # # # # # # print( body['reportID1'])

            firstTokenID = body['firstTokenID']
            secondTokenID = body['secondTokenID']
            tokens = body['tokens[]']
            # # # print(firstTokenID, secondTokenID, tokens)
            string = ""
            for i in tokens:
                string += str(i) + " "
            string = string[0:len(string)-1] 
            # # print("string : ", string)
            
            # # # print("string : ", string)
            
            query = '''
                    EXEC [testVocabulary] @firstTokenID = ?, @secondTokenID = ?, @tokens = ?;
                    ''' 
            args = [firstTokenID, secondTokenID, string]
            cursor.execute(query, args)
            datatoken = cursor.fetchone()

            # # print(datatoken)
            result['reportID'] = [datatoken.reportID]
            result['reportText'] = [datatoken.reportText]

            if result['reportText'] == []:
                raise Exception("No Report Found!!")
            # print(result)
            result['status'] = "0"
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            # print("rollbacked, error message : ", e)
            result['ERRMSG'] = str(e)

        conn.close()
        
        end = time.time()
        # print("start - end = ",  end - start)
    return JsonResponse(result)

@csrf_exempt
def getREForTest(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        try :
            body = json.loads(raw)
            token = body['token[]']
            reportFormID = body['reportFormID']
            # print("token : ", token)
            # print("reportFormID : ", reportFormID)
            tokenString = ""
            for i in token:
                tokenString += i + " "
            # print("tokenString : ", tokenString)
            
            if reportFormID == None or token == None:
                raise Exception("reportFormID or token None")
            
            query = '''
                    SELECT * FROM Vocabulary as a
                    left join vocabularyRE as b on a.tokenID = b.tokenID
                    left join [reportFormVocabulary] as c on a.tokenID = c.tokenID
                    where a.tokenID in (SELECT convert(int, value) FROM STRING_SPLIT(?, ' ')) and c.reportFormID = ? 
                    or a.tokenID in (SELECT convert(int, value) FROM STRING_SPLIT(?, ' ')) and c.reportFormID is Null
                    order by a.tokenID
                    ''' 
            args = [tokenString, reportFormID, tokenString]
            cursor.execute(query, args)
            data = cursor.fetchall()
            # # print("data : ", data)
            if data == []:
                raise Exception("No Vocabularies found")
            REarray = []
            existArray = []
            for i in data:
                # print(i, i.RE)
                if i.RE == None:
                    REarray.append(i.token)
                else:
                    REarray.append(i.RE)
                if i.reportFormID == None:
                    existArray.append('N')
                else:
                    existArray.append('Y')

            # # print(datatoken)
            result['REarray'] = REarray
            result['existArray'] = existArray
            result['status'] = "0"
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            # print("rollbacked, error message : ", e)
            result['ERRMSG'] = str(e)

        conn.close()
        
        end = time.time()
        # # print("start - end = ",  end - start)
    return JsonResponse(result)

@csrf_exempt
def getAllForms(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        try :
            query = '''
                    SELECT * FROM [reportForm]; 
                    ''' 
            cursor.execute(query)
            data = cursor.fetchall()
            # print(data)
            reportFormID = []
            reportFormName = []
            for i in data:
                reportFormID.append(i.reportFormID)
            # # print(datatoken)
                reportFormName.append(str(i.reportFormName))
            result['reportFormID'] = reportFormID
            result['reportFormName'] = reportFormName
            result['status'] = "0"
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            # print("rollbacked, error message : ", e)
            result['ERRMSG'] = str(e)

        conn.close()
        
        end = time.time()
        # # print("start - end = ",  end - start)
    return JsonResponse(result)

@csrf_exempt
def getAllFormProcedures(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        try :
            # print("in")
            body = json.loads(raw)
            reportFormID = body['reportFormID']
            query = '''
                    SELECT * FROM [reportFormProcedure] where reportFormID = ?; 
                    ''' 
            args = [reportFormID]
            cursor.execute(query, args)
            data = cursor.fetchall()
            # print(data)
            procedureName = []
            procedureID = []
            for i in data:
                procedureName.append(i.procedureName)
                procedureID.append(i.procedureID)
            result['procedureName'] = procedureName
            result['procedureID'] = procedureID
            result['status'] = "0"
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            # print("rollbacked, error message : ", e)
            result['ERRMSG'] = str(e)

        conn.close()
        
        end = time.time()
        # # print("start - end = ",  end - start)
    return JsonResponse(result)

@csrf_exempt
def getAllFormVocabularies(request):
    #取得
    if request.method == 'POST':
        
        start = time.time()
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'nlpVocabularyLatest ' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        try :
            # print("in")
            body = json.loads(raw)
            reportFormID = body['reportFormID']
            procedureID = body['procedureID']
            # print(reportFormID, procedureID)
            query = '''
                    SELECT * FROM [reportFormVocabulary]
                    where reportFormID = ? and [procedureID] = ?; 
                    ''' 
            args = [reportFormID, procedureID]
            cursor.execute(query, args)
            data = cursor.fetchall()
            # print(data)
            reportItem = []
            tokenID = []
            for i in data:
                reportItem.append(i.reportItem)
                tokenID.append(i.tokenID)
            result['reportItem'] = reportItem
            result['tokenID'] = tokenID
            result['status'] = "0"
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            # print("rollbacked, error message : ", e)
            result['ERRMSG'] = str(e)

        conn.close()
        
        end = time.time()
        # # print("start - end = ",  end - start)
    return JsonResponse(result)





import django.forms
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.db import connections

def Home(request):
    return render(request, 'mark/base.html')

# class Home(ListView):
#     model = Text
#     template_name = 'base.html'

def Merge(request):
    return render(request, 'mark/merge.html')


def Page2(request):
    return render(request, 'mark/page2.html')
# class Page2(ListView):
#     model = Text
#     template_name = 'Page2.html'

# class Merge(ListView):
#     model = Text
#     template_name = 'merge.html'


def dictionary(request):
    return render(request, 'mark/dictionary.html')


def reportForm(request):
    return render(request, 'mark/reportForm.html')
    
class selectVocabulary(ListView):
    model = Text
    template_name = 'selectVocabulary.js'



    



    
