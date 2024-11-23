# Load module
import json
import pathlib
import textwrap
import regex as re
import torch
import google.generativeai as genai



# def get_context_from_id(sgk, id_qa):
#     subject = id_qa[0]
#     grade = id_qa[1:3]
#     topic_lesson = id_qa[3:6]
#     if topic_lesson[0] == 'B':
#         full_context = ''
#         for topic in sgk[subject][grade].keys():
#             element_in_topic = sgk[subject][grade][topic].keys()
#             if topic_lesson in element_in_topic:
#                 return sgk[subject][grade][topic][topic_lesson]['context']
#             else:
#                 for element in element_in_topic:
#                     if element != 'name':
#                         full_context += sgk[subject][grade][topic][element]['context'] + '. '
#         return full_context
#     else:
#         topic_context = ''
#         for lesson in sgk[subject][grade][topic_lesson].keys():
#             if lesson != 'name':
#                 topic_context += sgk[subject][grade][topic_lesson][lesson]['context'] + '. '
#         return topic_context

def run_model(model, sgk, qas, subject):
    dict_output = {} 
    with torch.no_grad():
        for id_qa in qas.keys():
            question = qas[id_qa]['question']
            
    return dict_output

if __name__ == '__main__':
    
    subject = 'S'
    device = torch.device("cuda:0")

    GOOGLE_API_KEY = "AIzaSyAOvJiDl9H4OR1UNYM6SXgsWkPmv7iubms"
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-1.5-pro-001')



    output_file_name = f'output_{subject}_xlm-r_1.json'
    write_json(output_file_name, dict_output)
