# Load module
import json
import pathlib
import textwrap
import regex as re
import torch
import google.generativeai as genai
import tqdm
import sys
import os
import time

# Lấy đường dẫn của thư mục cha chứa main.ipynb
base_dir = os.path.dirname(os.path.abspath('select_model.ipynb'))
# Thêm đường dẫn của thư mục Dataset vào sys.path
sys.path.append(os.path.join(base_dir, '/data/npl/ReasoningCTT/LLM/Dataset'))
# Sau đó, bạn có thể import như bình thường
from dataset import Multiple_Choice_Dataset

def write_json(file_path, result):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file)

def append_to_json(file_path, result):
    with open(file_path, 'a', encoding='utf-8') as file:
        json.dump(result, file)
        file.write('\n')

def prompting(model, qas_dataset:Multiple_Choice_Dataset, file_path):
    results = []
    for id, ques in qas_dataset.questions.items():
        success = False
        retry_count = 0

        input_data = {
            'question': ques.question,
            'options': {
                'A': ques.options[0],
                'B': ques.options[1],
                'C': ques.options[2],
                'D': ques.options[3],
            }
        }
        
        while not success:
            try:
                response = model.generate_content(f'''
                    {input_data}
                    Hãy chọn đáp án đúng, ghi ngắn gọn A, B, C hay D, không cần giải thích.
                ''')
                print(id, response.text)

                result = {
                    'id' : id,
                    'response' : response.text,
                    'correct answer' : ques.correct_answer
                }
                append_to_json(file_path, result )
                results.append(result)
                success = True  
            except Exception as e:
                retry_count += 1
                if(retry_count > 100):
                    return results
                else: 
                    print(f"Lỗi: {e}. Thử lại sau 5 giây.")
                    time.sleep(5)  
        else: continue
    return results

if __name__ == '__main__':

    # gemini model
    GOOGLE_API_KEYS = [
        'AIzaSyDPUvj6wbRbwxjI8_a2lqcf19qI2TOFAmk',
        'AIzaSyA3ltQitqfGSG9IYgssmnbXEMgpHn-uA3E'
    ]
    GOOGLE_API_KEY = "AIzaSyA3ltQitqfGSG9IYgssmnbXEMgpHn-uA3E"
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-002')
    
    device = torch.device("cuda:0")

    # dataset based on subject
    subject = 'S'
    dataset = Multiple_Choice_Dataset('/data/npl/ReasoningCTT/LLM/Dataset/qas.json')
    sub_dataset = dataset.getBaseOnSubject(subject)
    # new_dataset = sub_dataset.getQuestionFromIdToEnd('V11B1200135')

    file_path = '/data/npl/ReasoningCTT/LLM/Gemini/Result/gemini_su_result.json'
    
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write('[\n')

    results = prompting(model, sub_dataset, file_path)

    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(']')
   
