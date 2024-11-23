import json
import torch
from torch.utils.data import Dataset, DataLoader

class Question:
    def __init__(self, question, options, correct_ans):
        self.question = question
        self.options = options
        self.correct_answer = correct_ans

class Multiple_Choice_Dataset(Dataset):
    def __init__(self, qas_json_file=None, qas_dict=None):
        self.questions = dict()
        if qas_json_file:
            self.loadDatasetFromFile(qas_json_file)
        elif qas_dict:
            self.loadDatasetFromDict(qas_dict)

    # super().__init__()
    def loadDatasetFromDict(self, qas_dict):
        self.questions.clear()
        self._loadData(qas_dict)

    def loadDatasetFromFile(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        self._loadData(data)
    
    def _loadData(self, data):
        for id, question_data in data.items():
            question = question_data['question']
            answer_options = question_data['answer_options']
            correct_answer = question_data['correct_answer']

            self.questions[id] = Question(question, answer_options, correct_answer)

    def getQuestionById(self, id):
        return self.questions[id]
    
    def getQuestionFromIdToEnd(self, curr_id):
        unprompt_ques = {id: question for id, question in self.questions.items() if id[-3:] > curr_id[-3:]}
        new_dataset = Multiple_Choice_Dataset()
        new_dataset.questions = unprompt_ques
        return new_dataset

    def getNumQues(self):
        return len(self.questions)
    
    def getBaseOnSubject(self, subject):
        sub_ques = {id: question for id, question in self.questions.items() if id[0] == subject}
        new_dataset = Multiple_Choice_Dataset()
        new_dataset.questions = sub_ques
        return new_dataset


        