from django.shortcuts import render
from django.http import JsonResponse
from django.template import loader
from mark.models import *
from mark.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
import pyodbc
import json
import Levenshtein
DATABASE_NAME = 'nlpVocabularyLatest' 

@csrf_exempt
def getCapitalToken(request):
    server = '172.31.6.22' 
    database = 'nlpVocabularyLatest' 
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
        result['data'] = []
        for i in res:
            # print(i)
            result['data'].append({
                'tokenID1': i.tokenID1,
                'token1': i.token1,
                'tokenID2': i.tokenID2,
                'token2': i.token2,
            })
        # tokenID1 = [row.tokenID1 for row in res]
        # token1 = [row.token1 for row in res]
        # tokenID2 = [row.tokenID2 for row in res]
        # token2 = [row.token2 for row in res]

        result['status'] = "0"
        
        # result['tokenID1'] = tokenID1
        # result['token1'] = token1
        # result['tokenID2'] = tokenID2
        # result['token2'] = token2
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        result['ERRMSG'] = str(e)
    # print(result)
    
    conn.close()
    
    return JsonResponse(result)

@csrf_exempt
def getTypoToken(request):
    server = '172.31.6.22' 
    database = 'nlpVocabularyLatest' 
    username = 'N824'
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    result = {'status': "1"}    
    # raw = request.body.decode('utf-8')
    
    try:        
        # body = json.loads(raw)
        query = '''select a.token, count(*) as 'times' from Vocabulary as a 
        inner join textToken as b 
        on a.tokenID = b.tokenID 
        where tokenType = 'G'
        group by a.token
        order by times '''
        cursor.execute(query)
        res = cursor.fetchall()
        # print(res[0])
        # tokenID1 = [row.tokenID for row in res]
        # token1 = [row.token for row in res]

        result['status'] = "0"
        
        # result['tokenID'] = tokenID1
        # result['token'] = token1
        result['data'] = []
        for i in res:
            # print(i)
            result['data'].append({
                'token': i[0],
                'times': i[1],
            })
        conn.commit()
        print(result['data'])
    except Exception as e:
        conn.rollback()
        result['ERRMSG'] = str(e)
    # print(result)
    
    conn.close()
    
    return JsonResponse(result)

def order_words_by_edit_distance(word_list, search_str):
    # Calculate edit distance between search string and each word in the list
    distances = [(word, Levenshtein.distance(search_str, word)) for word in word_list]
    # Sort the list of words by their edit distance from the search string
    sorted_words = sorted(distances, key=lambda x: x[1])
    # Return only the words (not the distances)
    return [word[0] for word in sorted_words]

@csrf_exempt
def getTypoTokenDistance(request):
    server = '172.31.6.22' 
    database = 'nlpVocabularyLatest' 
    username = 'N824'
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    result = {'status': "1"}    
    raw = request.body.decode('utf-8')
    
    try:        
        body = json.loads(raw)        
        token = body['token']

        query = '''select * from Vocabulary where token = ?'''
        args = [token]
        cursor.execute(query, args)
        res = cursor.fetchone()
        tokenType = res.tokenType
        number = 1
        query = '''select * from Vocabulary where tokenType = ?'''
        args = [tokenType]
        cursor.execute(query, args)
        res = cursor.fetchall()
        # print(res)
        Array = []
        for i in res:
            # dis = edit_distance(i.token, token)
            # if dis <= number and i.token != token:
            #     Array.append(i.token)
            
            if i.token != token:
                Array.append(i.token)

        sorted_words = order_words_by_edit_distance(Array, token)
        print(len(sorted_words))
        top_100 = sorted_words[:100]
        tempArray = []
        for i in top_100:
            query = '''select   b.reportID, a.token from Vocabulary  as a
            left join textToken as b 
            on a.tokenID = b.tokenID

            where a.tokenType = 'G' and a.token = ?
            group by b.reportID, a.token'''
            args = [i]
            cursor.execute(query, args)
            temp = cursor.fetchone()
            tempArray.append(temp.reportID)
            # print("temp : ", temp)
        print("tempArray : ", tempArray)
        # query = "SELECT top(1) * FROM textToken WHERE tokenID = {}".format(" OR tokenID = ".join(['?' for i in range(len(sorted_words))]))
        print(query)

        # print(sorted_words)
        # print(Array)
        result['status'] = "0"
        
        result['token'] = top_100
        result['reportID'] = tempArray
        # result['token'] = token1
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        result['ERRMSG'] = str(e)
    # print(result)
    
    conn.close()
    
    return JsonResponse(result)

def edit_distance(s1, s2):
    """
    Computes the Levenshtein distance between two strings.

    Parameters:
    s1 (str): First string
    s2 (str): Second string

    Returns:
    int: The Levenshtein distance between s1 and s2
    """
    # Create a matrix to hold the edit distances
    m = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    # Fill in the first row and column of the matrix
    for i in range(len(s1) + 1):
        m[i][0] = i
    for j in range(len(s2) + 1):
        m[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            m[i][j] = min(m[i - 1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1] + cost)

    # Return the bottom-right element of the matrix
    return m[-1][-1]

@csrf_exempt
def insertTypo(request):
    server = '172.31.6.22' 
    database = 'nlpVocabularyLatest' 
    username = 'N824'
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    result = {'status': "1"}
    
    raw = request.body.decode('utf-8')
    
    try:
        body = json.loads(raw)
        insertType = body['insertType']
        if insertType == "captalization":
            correctWord = body['correctWord']
            wrongWord = body['wrongWord']
            # print("correctWord : ", correctWord)
            # print("wrongWord : ", wrongWord)
            # html = ""
            html = '''<table class='table'>
                    <thead class="thead-dark">
                        <tr>
                            <th class="header" scope="col" style = "width : 100px;">大小不同字</th>
                            <th class="header" scope="col" style = "width : 100px;">調整為正確字</th>
                        </tr>
                    </thead>
                    <tbody>'''
            for correct, wrong in zip(correctWord, wrongWord):
                print(correct, wrong)
                query = '''select * from Vocabulary where token = ?'''
                args = [correct]
                cursor.execute(query, args)
                correctTokenID = cursor.fetchone().tokenID
                
                query = '''select * from Vocabulary where token = ?'''
                args = [wrong]
                cursor.execute(query, args)
                wrongTokenID = cursor.fetchone().tokenID

                print(correctTokenID, wrongTokenID)

                if (correctTokenID == None or wrongTokenID == None):
                    raise Exception("單字不存在")
                
                query = '''update Vocabulary set prototype = ?, capitalization = ? OUTPUT inserted.* where token = ? '''
                args = [correct, "1", wrong]
                cursor.execute(query, args)
                changedToken = cursor.fetchone()
                print("changedToken : ", changedToken)
                html += '''<tr>'''
                html += '''<td>'''
                html += changedToken.token
                html += '''</td>'''
                html += '''<td>'''
                html += changedToken.prototype
                html += '''</td>'''
                html += '''</tr>'''
            html += '''
                </tbody>
            </table>''' 
                # html += "[" + changedToken.token + ", " + changedToken.prototype + "]<br>"
            result['MSG'] = "已完成更新<br>" + html
        elif insertType == "typo":
            print("typo")
            
            correctWord = body['correctWord']
            wrongWord = body['wrongWord']
            print("correctWord : ", correctWord)
            print("wrongWord : ", wrongWord)

            query = '''select * from Vocabulary where token = ?'''
            args = [correctWord]
            cursor.execute(query, args)
            correctTokenID = cursor.fetchone().tokenID
            if correctTokenID == None:
                raise Exception("正確字不存在")
            # html = ""
            html = '''<table class='table'>
                    <thead class="thead-dark">
                        <tr>
                            <th class="header" scope="col" style = "width : 100px;">錯別字</th>
                            <th class="header" scope="col" style = "width : 100px;">調整為正確字</th>
                        </tr>
                    </thead>
                    <tbody>'''
            for i in wrongWord:
                query = '''select * from Vocabulary where token = ?'''
                args = [i]
                cursor.execute(query, args)
                wrongTokenID = cursor.fetchone().tokenID
                if wrongTokenID == None:
                    raise Exception("錯誤字不存在")
                
                query = '''update Vocabulary set prototype = ?, typo = ? OUTPUT inserted.* where token = ? '''
                args = [correctWord, "1", i]
                cursor.execute(query, args)
                changedToken = cursor.fetchone()
                print("changedToken : ", changedToken)
                # html += "錯別字 : " + changedToken.token + ", 調整為 : " + changedToken.prototype + "<br>"
                
                html += '''<tr>'''
                html += '''<td>'''
                html += changedToken.token
                html += '''</td>'''
                html += '''<td>'''
                html += changedToken.prototype
                html += '''</td>'''
                html += '''</tr>'''
            html += '''
                </tbody>
            </table>''' 
            result['MSG'] = "已完成更新<br>" + html
        elif insertType == "stop":
            print("stop")
            
            stopWord = body['stopWord']
            print("stopWord : ", stopWord)
            
            
            html = '''<table class='table'>
                    <thead class="thead-dark">
                        <tr>
                            <th class="header" scope="col" style = "width : 100px;">不統計字</th>
                        </tr>
                    </thead>
                    <tbody>'''
            for i in stopWord:
                query = '''select * from Vocabulary where token = ?'''
                args = [i]
                cursor.execute(query, args)
                correctTokenID = cursor.fetchone().tokenID
                if correctTokenID == None:
                    raise Exception(f"單字不存在 : {i}")
                
                query = '''update Vocabulary set prototype = ?, stopWord = ? OUTPUT inserted.* where token = ? '''
                args = [correctWord, "1", i]
                cursor.execute(query, args)
                changedToken = cursor.fetchone()
                print("changedToken : ", changedToken)
                # html += "錯別字 : " + changedToken.token + ", 調整為 : " + changedToken.prototype + "<br>"
                
                html += '''<tr>'''
                html += '''<td>'''
                html += changedToken.token
                html += '''</td>'''
                html += '''</tr>'''
            html += '''
                </tbody>
            </table>''' 
            result['MSG'] = "已完成更新<br>" + html
    
        result['status'] = "0"
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        result['ERRMSG'] = str(e)
    # print(result)
    
    conn.close()
    
    return JsonResponse(result)



@csrf_exempt
def selectReportByReportID(request):
    server = '172.31.6.22' 
    database = 'nlpVocabularyLatest' 
    username = 'N824'
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    result = {'status': "1"}    
    raw = request.body.decode('utf-8')
    
    try:        
        body = json.loads(raw)        
        reportID = body['reportID']

        query = '''select * from analyseText where reportID = ?'''
        args = [reportID]
        cursor.execute(query, args)
        res = cursor.fetchone()
        result['status'] = "0"
        
        result['reportText'] = res.reportText
        # result['token'] = token1
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        result['ERRMSG'] = str(e)
    # print(result)
    
    conn.close()
    
    return JsonResponse(result)

@csrf_exempt
def getStopToken(request):
    server = '172.31.6.22' 
    database = 'nlpVocabularyLatest' 
    username = 'N824'
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    result = {'status': "1"}    
    # raw = request.body.decode('utf-8')
    
    try:        
        # body = json.loads(raw)
        query = '''select TOP 1000 token, COUNT(*) AS frequency, count(distinct a.reportID) as numReports
                FROM textToken as a
                inner join Vocabulary as b ON a.tokenID = b.tokenID
                where b.tokenType = 'G'
                group by a.tokenID, b.token
                order by frequency desc; '''
        cursor.execute(query)
        res = cursor.fetchall()
        # print(res[0])
        # tokenID1 = [row.tokenID for row in res]
        # token1 = [row.token for row in res]

        result['status'] = "0"
        
        # result['tokenID'] = tokenID1
        # result['token'] = token1
        result['data'] = []
        for i in res:
            # print(i)
            result['data'].append({
                'token': i.token,
                'frequency': i.frequency,
                'numReports': i.numReports,
            })
        conn.commit()
        print(result['data'])
    except Exception as e:
        conn.rollback()
        result['ERRMSG'] = str(e)
    # print(result)
    
    conn.close()
    
    return JsonResponse(result)