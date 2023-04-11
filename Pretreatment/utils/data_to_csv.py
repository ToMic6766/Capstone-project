import os
import json
import pandas as pd

def counting(path):
    cnt = 0
    data_dir = path

    for path in os.listdir(data_dir):
        if os.path.isfile(os.path.join(data_dir, path)):
            cnt += 1

    #print(f'데이터 개수 = {cnt}')
    return cnt

# purpose data -------------------

target_path = "Pretreatment/training_data/origin/purpose_talk/"
target_path_list = os.listdir(target_path)
target_path_list

total_data = 0
for i in range(len(target_path_list)):
    cnt = counting(target_path+target_path_list[i])
    total_data += cnt
#print(f'총 데이터 개수 = {total_data}')

purpose = []
for i in range(len(target_path_list)):
    files = os.listdir(target_path+target_path_list[i])
    for k in range(len(files)):
        final_path = str(target_path)+str(target_path_list[i])+"/"+str(files[k])
        try:
            target_file = open(f"{final_path}", encoding="UTF-8")
            target_file = json.loads(target_file.read())
            for j in range(len(target_file['info'][0]['annotations']['lines'])):
                purpose.append(target_file['info'][0]['annotations']['lines'][j]['norm_text'][2:])
        except:
            print(f"error! {final_path}")

purpose_df = pd.DataFrame({'text':purpose})

purpose_df.to_csv("Pretreatment/training_data/custom/purpose_talk_data.csv", index=False)


# daily data -------------------
target_path = "Pretreatment/training_data/origin/daily_talk/"
target_path_list = os.listdir(target_path)

total_data = 0
for i in range(len(target_path_list)):
    cnt = counting(target_path+target_path_list[i])
    total_data += cnt
#print(f'총 데이터 개수 = {total_data}')

ex = open(f"Pretreatment/training_data/origin/daily_talk/TL_01. KAKAO/KAKAO_898_15.json", encoding="UTF-8")
ex = json.loads(ex.read())

files = os.listdir(target_path+target_path_list[0])

daily_conversations = []
for i in range(len(target_path_list)):
    files = os.listdir(target_path+target_path_list[i])
    for k in range(len(files)):
        final_path = str(target_path)+str(target_path_list[i])+"/"+str(files[k])
        try:
            target_file = open(f"{final_path}", encoding="UTF-8")
            target_file = json.loads(target_file.read())
            for j in range(len(target_file['info'][0]['annotations']['lines'])):
                daily_conversations.append(target_file['info'][0]['annotations']['lines'][j]['norm_text'])
        except:
            print(f"error! {final_path}")

daily_conversations_df = pd.DataFrame({'text':daily_conversations})

daily_conversations_df.to_csv("Pretreatment/training_data/custom/daily_talk_data.csv", index=False)

#common sense data -------------------
common_sense = open(f"Pretreatment/training_data/origin/ko_wiki_v1_squad.json", encoding="UTF-8")
common_sense = json.loads(common_sense.read())

query = []
answer = []
for i in range(len(common_sense['data'])):
    query.append(common_sense['data'][i]['paragraphs'][0]['qas'][0]['question'])
    answer.append(common_sense['data'][i]['paragraphs'][0]['qas'][0]['answers'][0]['text'])

common_sense_df = pd.DataFrame({'intent':['일반상식']*len(query), 'query':query, 'answer':answer})
common_sense_df.to_csv("Pretreatment/training_data/custom/common_sense_data.csv", index=False)

# m_ratings data -------------------
ratings = pd.read_csv("Pretreatment/training_data/origin/ratings.txt", delimiter='\t')
ratings.to_csv("Pretreatment/training_data/custom/m_rating_data.csv", index=False)