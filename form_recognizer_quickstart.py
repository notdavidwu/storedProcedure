

# from azure.core.credentials import AzureKeyCredential
# from azure.ai.formrecognizer import DocumentAnalysisClient
# from azure.ai.formrecognizer import FormRecognizerClient
# import json

# """
# Remember to remove the key from your code when you're done, and never post it publicly. For production, use
# secure methods to store and access your credentials. For more information, see 
# https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
# """
# endpoint = "https://csh-ocr.cognitiveservices.azure.com/"
# key = "b9917f1f388b40fc8e05115b5178d8aa"

# # sample document
# # formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"
# formUrl = "D:/scan/20230512_GCP教育訓練證明切結害.pdf"

# # document_analysis_client = DocumentAnalysisClient(
# #     endpoint=endpoint, credential=AzureKeyCredential(key)
# # )
    
# # poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-layout", formUrl)
# # result = poller.result()

# form_recognizer_client = FormRecognizerClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# filePath = formUrl

# f = open(filePath,'rb').read()

# result = form_recognizer_client.begin_recognize_content(f).result()
# # print(result)
# for page in result:
#     print("Page number:", page.page_number)

#     # Print the recognized lines of text
#     for line in page.lines:
#         print("Line:", line.text)

#     # Print the bounding boxes of words
#     # for line in page.lines:
#     #     for word in line.words:
#     #         print("Word:", word.text)
#             # print("Bounding Box:", word.bounding_box)

#     # Print the tables, if any
#     # for table in page.tables:
#     #     print("Table:")
#     #     for cell in table.cells:
#     #         print("Cell Text:", cell.text)
#     #         print("Bounding Box:", cell.bounding_box)
# # for idx, style in enumerate(result.styles):
# #     print(
# #         "Document contains {} content".format(
# #          "handwritten" if style.is_handwritten else "no handwritten"
# #         )
# #     )

# # for page in result.pages:
# #     for line_idx, line in enumerate(page.lines):
# #         print(
# #          "...Line # {} has text content '{}'".format(
# #         line_idx,
# #         line.content.encode("utf-8")
# #         )
# #     )

# #     for selection_mark in page.selection_marks:
# #         print(
# #          "...Selection mark is '{}' and has a confidence of {}".format(
# #          selection_mark.state,
# #          selection_mark.confidence
# #          )
# #     )

# # for table_idx, table in enumerate(result.tables):
# #     print(
# #         "Table # {} has {} rows and {} columns".format(
# #         table_idx, table.row_count, table.column_count
# #         )
# #     )
        
# #     for cell in table.cells:
# #         print(
# #             "...Cell[{}][{}] has content '{}'".format(
# #             cell.row_index,
# #             cell.column_index,
# #             cell.content.encode("utf-8"),
# #             )
# #         )
# # print(result)

# # for i in result:
# #     print(i)
# # d = [page.to_dict() for page in result]
# # json_string = json.dumps(d)
# # print(json_string)
# print("----------------------------------------")



from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import os

endpoint = "https://csh-ocr.cognitiveservices.azure.com/"
key = "b9917f1f388b40fc8e05115b5178d8aa"
formUrl = "D:/scan/test1.png"
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)
with open(formUrl, "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout", document=f, locale="zh-Hant"
    )
# with open(formUrl, "rb") as f:
#     poller = document_analysis_client.begin_analyze_document(
#         "prebuilt-document", document=f
#     )
invoices = poller.result()
# print(invoices.lines)
pages = invoices.pages

# Iterate over the pages
for page in pages:
    # Accessing the lines on each page
    lines = page.lines
    marks = page.selection_marks
    
    for selection_mark in marks:
            print(selection_mark.state)
            # print(
            #     "...Selection mark is '{}' within bounding box '{}' and has a confidence of {}".format(
            #         selection_mark.state,
            #         # selection_mark.polygon,
            #         # selection_mark.confidence,
            #     )
            # )
    # Iterate over the lines
    # for line in lines:
    #     print(line.content)

