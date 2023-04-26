from django.shortcuts import render
from django.http import JsonResponse
from django.template import loader
from mark.models import *
from mark.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
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


    
