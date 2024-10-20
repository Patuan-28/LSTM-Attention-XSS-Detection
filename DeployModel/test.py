import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
dataset = "datasetClean.csv"
model = load_model("models\lstm_model.h5")

df = pd.read_csv(dataset, delimiter=",")
# df_dict = {
#     "Sentence":df.iloc[0,0],
#     "Type":df.iloc[0,1]
#     }
df_dict = df.to_dict()


#tester
inputan_url = "https://stackoverflow.com/questions/57664997/how-to-return-400-bad-request-on-flask"
dummy_url = [df_dict['Sentence'][4377], df_dict['Sentence'][10089],df_dict['Sentence'][17655],df_dict['Sentence'][12389], inputan_url]

df_tester = pd.DataFrame(columns=['Sentence', 'Type','contain_<script>','contain_<iframe>','contain_<embed>','contain_<svg>','contain_<audio>','contain_>','contain_%','contain_&',
                                  'contain_#','contain_"">','contain_">','contain_"/>','contain_"%','contain_cookie','contain_alert()','contain_prompt()','contain_document.write()','contain_onerror()','URL_length','URL>75'])

# Creating the Second Dataframe using dictionary
def insert_zero():
  i=1
  while i <= len(dummy_url):
    url_type = 0
    # print(url_type)
    i+=1
    return url_type

df2 = pd.DataFrame({"Sentence":dummy_url,
                    "Type":insert_zero()}
                   )
df_tester = df_tester.append(df2)

def feature_checking(dataset):
  dataset['contain_<script>'] = dataset['Sentence'].apply(lambda x: 1 if '<script' in str(x) else 0)
  dataset['contain_<iframe>'] = dataset['Sentence'].apply(lambda x: 1 if '<iframe' in str(x) else 0)
  dataset['contain_<embed>'] = dataset['Sentence'].apply(lambda x: 1 if '<embed' in str(x) else 0)
  dataset['contain_<svg>'] = dataset['Sentence'].apply(lambda x: 1 if '<svg' in str(x) else 0)
  dataset['contain_<audio>'] = dataset['Sentence'].apply(lambda x: 1 if '<audio' in str(x) else 0)
  dataset['contain_>'] = dataset['Sentence'].apply(lambda x: 1 if '>' in str(x) else 0)
  dataset['contain_%'] = dataset['Sentence'].apply(lambda x: 1 if '%' in str(x) else 0)
  dataset['contain_&'] = dataset['Sentence'].apply(lambda x: 1 if '&' in str(x) else 0)
  dataset['contain_#'] = dataset['Sentence'].apply(lambda x: 1 if '#' in str(x) else 0)
  dataset['contain_"">'] = dataset['Sentence'].apply(lambda x: 1 if '"">' in str(x) else 0)
  dataset['contain_">'] = dataset['Sentence'].apply(lambda x: 1 if '">' in str(x) else 0)
  dataset['contain_"/>'] = dataset['Sentence'].apply(lambda x: 1 if '"/>' in str(x) else 0)
  dataset['contain_"%'] = dataset['Sentence'].apply(lambda x: 1 if '"%' in str(x) else 0)
  dataset['contain_cookie'] = dataset['Sentence'].apply(lambda x: 1 if 'document.cookie' in str(x) else 0)
  dataset['contain_alert()'] = dataset['Sentence'].apply(lambda x: 1 if 'alert(' in str(x) else 0)
  dataset['contain_prompt()'] = dataset['Sentence'].apply(lambda x: 1 if 'prompt(' in str(x) else 0)
  dataset['contain_document.write()'] = dataset['Sentence'].apply(lambda x: 1 if 'document.write(' in str(x) else 0)
  dataset['contain_onerror()'] = dataset['Sentence'].apply(lambda x: 1 if 'onerror(' in str(x) else 0)
  
def url_length(string):
  return len(string.split())

df_tester['URL_length'] = df_tester['Sentence'].apply(url_length)

def label(x):
  if x['URL_length'] > 75:
    return 1
  else:
    return 0

df_tester['URL>75'] = df_tester.apply(lambda x:label(x), axis=1)
feature_checking(df_tester)


test_predict_datas = []
for i in df_tester.index:
  sum_test = df_tester.iloc[i,2:22].sum().sum()
  if sum_test > 1 :
    res=1
    test_predict_datas.append(res)
  else:
    res=0
    test_predict_datas.append(res)

df_test_predict =  pd.DataFrame(columns=["Type"])
df2 = pd.DataFrame({"Type":test_predict_datas})
df_test_predict = df_test_predict.append(df2)

series_test_predict = pd.Series(np.array(test_predict_datas))
prediction = model.predict(series_test_predict)
list(prediction[0:9])

list_pred = []
i=0
while i < len(prediction):
  # print(prediction[i])
  df_tester.loc[i,'Type'] = prediction[i]
  i+=1
df_tester

list_pred = []
i=0
while i < len(df_tester.index):
  if df_tester.loc[i,'Type'] < 0.5:
    df_tester.loc[i,'Type'] = 'Benign'
  else:
   df_tester.loc[i,'Type'] = 'Malicious'
  i+=1


output_tester_dict = df_tester.to_dict()
otd = output_tester_dict
# print(otd)
output_dict = {
        "Sentence" : otd['Sentence'][4], 
        "Type" : otd['Type'][4]
        }

print(output_dict)