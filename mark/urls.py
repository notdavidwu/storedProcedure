"""regex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mark.views import *
from django.urls import include

app_name = "mark"

from django.views.generic import TemplateView



urlpatterns = [
    path('', Home,name="home"),
    path('TextFormView/', TextFormView, name="TextFormView"),
    path('getVocabulary/', getVocabulary, name="getVocabulary"),
    path('insertVocabulary/', insertVocabulary, name="insertVocabulary"),
    path('inserttokenRE/', inserttokenRE, name="inserttokenRE"),
    path('inserttokenREItem/', inserttokenREItem, name="inserttokenREItem"),
    path('checkName/', checkName, name="checkName"),
    path('checkRE/', checkRE, name="checkRE"),
    path('getVocabularyByType/', getVocabularyByType, name="getVocabularyByType"),
    path('getVocabulary/', getVocabulary, name="getVocabulary"),
    path('getAnalyseText/', getAnalyseText, name="getAnalyseText"),
    path('getReportID/', getReportID, name="getReportID"),
    path('getReportText/', getReportText, name="getReportText"),
    path('getTokenREItemID/', getTokenREItemID, name="getTokenREItemID"),
    path('insertExtractedValueFromToken/', insertExtractedValueFromToken, name="insertExtractedValueFromToken"),
    path('insertVocabulary_U/', insertVocabulary_U, name="insertVocabulary_U"),
    path('getTextToken/', getTextToken, name="getTextToken"),
    path('getToken/', getToken, name="getToken"),
    path('insertTexttoken/', insertTexttoken, name="insertTexttoken"),
    path('getTextToken_3/', getTextToken_3, name="getTextToken_3"),
    path('insertTexttoken_3/', insertTexttoken_3, name="insertTexttoken_3"),
    path('getTokenIDCheckTextToken/', getTokenIDCheckTextToken, name="getTokenIDCheckTextToken"),
    path('getVocabularyByType_Ptable/', getVocabularyByType_Ptable, name="getVocabularyByType_Ptable"),
    path('getNextWord/', getNextWord, name="getNextWord"),
    path('getNextWordReport/', getNextWordReport, name="getNextWordReport"),
    path('getSynTypo/', getSynTypo, name="getSynTypo"),
    path('getReportTextByMergeToken/', getReportTextByMergeToken, name="getReportTextByMergeToken"),
    path('getMergeLog/', getMergeLog, name="getMergeLog"),
    path('twoWord/', twoWord, name="twoWord"),
    path('chineseTwoWord/', chineseTwoWord, name="chineseTwoWord"),
    path('chineseThreeWord/', chineseThreeWord, name="chineseThreeWord"),
    path('getTokenBynWord/', getTokenBynWord, name="getTokenBynWord"),
    path('getReportBetween2Tokens6/', getReportBetween2Tokens6, name="getReportBetween2Tokens6"),
    path('getReportBetween2Tokens6All/', getReportBetween2Tokens6All, name="getReportBetween2Tokens6All"),
    path('getReportBetween2Tokens5/', getReportBetween2Tokens5, name="getReportBetween2Tokens5"),
    path('getReportBetween2Tokens5All/', getReportBetween2Tokens5All, name="getReportBetween2Tokens5All"),
    path('getReportBetween2Tokens4/', getReportBetween2Tokens4, name="getReportBetween2Tokens4"),
    path('getReportBetween2Tokens4All/', getReportBetween2Tokens4All, name="getReportBetween2Tokens4All"),
    path('getReportBetween2Tokens3/', getReportBetween2Tokens3, name="getReportBetween2Tokens3"),
    path('getReportBetween2Tokens3All/', getReportBetween2Tokens3All, name="getReportBetween2Tokens3All"),
    path('fiveWord/', fiveWord, name="fiveWord"),
    path('threeWord/', threeWord, name="threeWord"),
    path('fourWord/', fourWord, name="fourWord"),
    path('getAllWordExsisting/', getAllWordExsisting, name="getAllWordExsisting"),
    
    
    path('Page2/', Page2,name="Page2"),
    path('Merge/', Merge,name="Merge"),
    path('REmove/', REmove,name="REmove"),
    path('static/selectVocabulary/', selectVocabulary.as_view(), name='selectVocabulary'),
    
    path('reportForm/', reportForm,name="reportForm"),
    
    path('worker.js', (TemplateView.as_view(template_name="mark/worker.js", 
    content_type='application/javascript', )), name='worker.js'),
    path('dictionary/', dictionary,name="dictionary"),
    path('getTag/', getTag, name='getTag'),
    path('getVocabularyForDictionary/', getVocabularyForDictionary, name='getVocabularyForDictionary'),
    path('testVocabularyGetReport/', testVocabularyGetReport, name='testVocabularyGetReport'),
    path('getREForTest/', getREForTest, name='getREForTest'),
    path('getAllForms/', getAllForms, name='getAllForms'),
    path('getAllFormProcedures/', getAllFormProcedures, name='getAllFormProcedures'),
    path('getAllFormVocabularies/', getAllFormVocabularies, name='getAllFormVocabularies'),
    path('getVocabularyE/', getVocabularyE, name='getVocabularyE'),
    path('backupDB/', backupDB, name='backupDB'),
    path('moveRE/', moveRE, name='moveRE'),
    path('expression/', expression, name='expression'),
    path('getItemDefinition/', getItemDefinition, name='getItemDefinition'),
    path('getItemByRootID/', getItemByRootID, name='getItemByRootID'),
    path('insertintoItemDefinition/', insertintoItemDefinition, name='insertintoItemDefinition'),
    path('getReportTextByMergeTokenExpression/', getReportTextByMergeTokenExpression, name='getReportTextByMergeTokenExpression'),
    path('getStasticTable/', getStasticTable, name='getStasticTable'),
    path('getReportByReportID/', getReportByReportID, name='getReportByReportID'),
    path('getStasticTable2/', getStasticTable2, name='getStasticTable2'),
    path('getTokenBynumReports/', getTokenBynumReports, name='getTokenBynumReports'),
    path('getFormInfo/', getFormInfo, name='getFormInfo'),
    path('getEToken/', getEToken, name='getEToken'),
    path('checkFormName/', checkFormName, name='checkFormName'),
    path('selectRoot/', selectRoot, name='selectRoot'),
    path('selectInteralNodeofRoot/', selectInteralNodeofRoot, name='selectInteralNodeofRoot'),
    path('selectGroupNodeofRoot/', selectGroupNodeofRoot, name='selectGroupNodeofRoot'),
    path('insertintoItemTrans/', insertintoItemTrans, name='insertintoItemTrans'),
    path('differenceDistance/', differenceDistance, name='differenceDistance'),
    
    path('typo/', typo,name="typo"),
    path('getTypoToken/', getTypoToken,name="getTypoToken"),
    path('insertTypo/', insertTypo,name="insertTypo"),
    path('getCapitalToken/', getCapitalToken,name="getCapitalToken"),
    path('getTypoTokenDistance/', getTypoTokenDistance,name="getTypoTokenDistance"),
]