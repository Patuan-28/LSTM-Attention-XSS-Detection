from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from keras.layers import *
from keras.models import *
from keras.layers import Layer
import keras.backend as K
from keras import layers

class attention(Layer):
    def init(self,**kwargs):
        super(attention,self).init(**kwargs)
 
    def build(self,input_shape):
        self.W=self.add_weight(name='attention_weight', shape=(input_shape[-1],1), 
                               initializer='random_normal', trainable=True)
        self.b=self.add_weight(name='attention_bias', shape=(input_shape[1],1), 
                               initializer='zeros', trainable=True)        
        super(attention, self).build(input_shape)
 
    def call(self,x):
        e = K.tanh(K.dot(x,self.W)+self.b)
        e = K.squeeze(e, axis=-1)
        alpha = K.softmax(e)
        alpha = K.expand_dims(alpha, axis=-1)
        context = x * alpha
        context = K.sum(context, axis=1)
        return context

app = FastAPI()

dataset = "datasetClean.csv"
df = pd.read_csv(dataset)
model = load_model("models\lstm_model_attention.h5", custom_objects={"attention": attention})
df_dict = df.to_dict()

class InputData(BaseModel):
    input_data: str

@app.get("/")
def home():
    return df_dict

@app.post("/predict/")
def predict(input_data: InputData):
    inputan_url = input_data.input_data
    dummy_url = [df_dict['Sentence'][4377], df_dict['Sentence'][10089],df_dict['Sentence'][17655],df_dict['Sentence'][12389], inputan_url]

    df_tester = pd.DataFrame(columns=['Sentence', 'Type','contain_<script>','contain_<iframe>','contain_<embed>','contain_<svg>','contain_<audio>','contain_>','contain_%','contain_&',
                                  'contain_#','contain_"">','contain_">','contain_"/>','contain_"%','contain_cookie','contain_alert()','contain_prompt()','contain_document.write()','contain_onerror()','URL_length','URL>75'])

    def insert_zero():
        i=1
        while i <= len(dummy_url):
            url_type = 0
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
        #dataset['contain_<svg>'] = dataset['Sentence'].apply(lambda x: 1 if '<svg' in str(x) else 0)
        dataset['contain_<audio>'] = dataset['Sentence'].apply(lambda x: 1 if '<audio' in str(x) else 0)
        dataset['contain_>'] = dataset['Sentence'].apply(lambda x: 1 if '>' in str(x) else 0)
        dataset['contain_%'] = dataset['Sentence'].apply(lambda x: 1 if '%' in str(x) else 0)
        dataset['contain_&'] = dataset['Sentence'].apply(lambda x: 1 if '&' in str(x) else 0)
        dataset['contain_#'] = dataset['Sentence'].apply(lambda x: 1 if '#' in str(x) else 0)
        dataset['contain_"">'] = dataset['Sentence'].apply(lambda x: 1 if '"">' in str(x) else 0)
        dataset['contain_">'] = dataset['Sentence'].apply(lambda x: 1 if '">' in str(x) else 0)
        dataset['contain_"/>'] = dataset['Sentence'].apply(lambda x: 1 if '"/>' in str(x) else 0)
        #dataset['contain_"%'] = dataset['Sentence'].apply(lambda x: 1 if '"%' in str(x) else 0)
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
    # df_tester
    
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
    return {
        "value" : otd['Type'][4]
    }