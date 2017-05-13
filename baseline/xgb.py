

import xgboost as xgb
import numpy as np
import multiprocessing

from model import *
from parser import *
from recommendation_worker import *
import random

print(" --- Recsys Challenge 2017 Baseline --- ")

N_WORKERS         = 1
USERS_FILE        = "/mnt/hgfs/shared/data/users_2.csv"
ITEMS_FILE        = "/mnt/hgfs/shared/data/items_2.csv"
INTERACTIONS_FILE = "/mnt/hgfs/shared/data/interactions-no-0.csv"
TARGET_USERS      = "/mnt/hgfs/shared/data/targetUsers.csv"
TARGET_ITEMS      = "/mnt/hgfs/shared/data/targetItems.csv"


'''
1) Parse the challenge data, exclude all impressions
   Exclude all impressions
'''
(header_users, users) = select(USERS_FILE, lambda x: True, build_user, lambda x: int(x[0]))
(header_items, items) = select(ITEMS_FILE, lambda x: True, build_item, lambda x: int(x[0]))

builder = InteractionBuilder(users, items)
(header_interactions, interactions) = select(
    INTERACTIONS_FILE,
    lambda x: x[2] != '0',  
    builder.build_interaction,
    lambda x: (int(x[0]), int(x[1])) 
)

'''
Build User-Item Dictionary
'''
user_item_dictionary = {}
for k in interactions:
        if(user_item_dictionary.__contains__(k[0])):
            user_item_dictionary[k[0]].append(interactions[k])
        else:
            user_item_dictionary[k[0]] = [interactions[k]]



'''
2) Build recsys training data
'''
data    = np.array([interactions[key].features() for key in interactions.keys()])
labels  = np.array([interactions[key].label() for key in interactions.keys()])
dataset = xgb.DMatrix(data, label=labels)
dataset.save_binary("recsys2017.buffer")


'''
3) Train XGBoost regression model with maximum tree depth of 2 and 25 trees
'''
evallist = [(dataset, 'train')]
param = {'bst:max_depth': 10, 'bst:eta': 0.1, 'silent': 1, 'objective': 'reg:linear' }
param['nthread']     = 4
param['eval_metric'] = 'rmse'
param['base_score']  = 0.0
num_round            = 25
bst = xgb.train(param, dataset, num_round, evallist)
bst.save_model('recsys2017.model')


'''
3) Load XGBoost regression model
'''
#bst = xgb.Booster({'nthread':4}) #init model
#bst.load_model("recsys2017.model") # load dat

'''
4) Create target sets for items and users
'''
target_users = []
for n, line in enumerate(open(TARGET_USERS)):
   # there is a header in target_users in dataset
    if n == 0:
         continue
    target_users += [int(line.strip())]
target_users = set(target_users)

target_items = []
for line in open(TARGET_ITEMS):
    target_items += [int(line.strip())]


'''
5) Schedule classification
'''

filename = "solution_.csv"
classify_worker(target_items, target_users, items, users, filename, bst, user_item_dictionary)

