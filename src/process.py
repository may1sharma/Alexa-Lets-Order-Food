import pandas as pd
import graphlab as gl
import pickle
import numpy as np
import bottlenose
from bs4 import BeautifulSoup
from time import sleep
from collections import defaultdict
# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.cluster import KMeans
# from collections import defaultdict
# from amazonproduct import API
class Data():
    def __init__(self):
        print ("Init")
        # self.items = gl.SFrame.read_csv('data/Reviews.csv')
        # self.items.show()
        # self.training_data, self.test_data = self.items.random_split(0.8, seed=0)
        # model = gl.recommender.item_similarity_recommender.create(training_data, 'UserId', 'ProductId')
        # model.save('item-model1')
        # model = gl.load_model("item-model1")
        # pred = model.predict(validation_data)
        # results = model.evaluate(validation_data)
        # print (results)
        # view = model.views.overview(validation_set=test_data )
        # view.show()
        # gl.evaluation.rmse(self.validation_data, recs)
        # view =  model.views.overview(validation_set=self.validation_data)
        # view.show()

    def createMF(self):
        mf = gl.recommender.factorization_recommender.create(self.training_data, user_id = 'UserId', item_id = 'ProductId',
                                                             target = 'Score', verbose=True)
        mf.save('factor-model')

    def getRecommendation(self, user_id, topk):
        model = gl.load_model('factor-model')
        results = model.recommend(users=user_id,k=topk)
        return results

    def queryAmazon(self, prodList,rgp=''):
        amazon = bottlenose.Amazon('AKIAITX2CCN72YWYELRQ', 'kLLl52gmWgKTNDdbir8EnY6ODwjLK5PlCqMs4yRI', 'ojharash-20')
        itemdict = []
        for item in prodList:
            try:
                response = amazon.ItemLookup(ItemId=item, ResponseGroup=rgp)
                soup = BeautifulSoup(response,"xml")
                if len(rgp) != 0:
                    value = soup.LargeImage.URL.string
                else:
                    value = soup.ItemAttributes.Title.string
            except:
                value = ""
                pass
            itemdict.append(value)
        return itemdict

# def save_obj(self,name ):
#     with open('data/'+ name + '.pkl', 'wb') as f:
#         pickle.dump(self.modelS, f)
#
# def load_obj(name):
#     f = open('data/' + name + '.pkl', 'rb')
#     return pickle.load(f)
#
# def findRecommendation(obj,validation_data):
#     print recs[:4]
#     view = obj.views.overview(validation_set=validation_data)
#     view.show()


# d= Data()
# # d.createMF()
# # d.loadMF()
# # findRecommendation(load_obj('item-model'),)
# #
# reco = d.getRecommendation(['ABXLMWJIXXAIN'],10)
# pn = d.queryAmazon(reco['ProductId'])
# pn = [x.encode('UTF8') for x in pn]
# reco.add_column(gl.SArray(pn), name='ProductName')
# rn = d.queryAmazon(reco['ProductId'],'Images')
# rn = [x.encode('UTF8') for x in rn]
# reco.add_column(gl.SArray(rn), name='ProductURL')
#
# reco = reco.pack_columns(columns=['score','rank','ProductName','ProductURL'], new_column_name='Details')
# df = reco.to_dataframe().set_index('ProductId')
# result = df.to_dict(orient='dict')['Details']
# print (result)