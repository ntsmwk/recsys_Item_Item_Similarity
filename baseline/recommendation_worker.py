'''
Build recommendations based on trained XGBoost model

by Daniel Kohlsdorf
'''

from model import *
import xgboost as xgb
import numpy as np

TH = 0.8

def classify_worker(item_ids, target_users, items, users, output_file, model, user_item_dictionary):
    with open(output_file, 'w') as fp:
        pos = 0
        average_score = 0.0
        num_evaluated = 0.0
        for i in item_ids:
            data = []        
            ids  = []
            THRESHOLD = 10
            users_score = {}
            #print("new item started\n")
            for u in target_users:
                users_score[u] = 0
                if(user_item_dictionary.__contains__(u) and items.__contains__(u)):
                    for k in user_item_dictionary.get(u):
                        if(k.interaction_type != 4):
                            score = k.item.compare(items[i])
                            if(k.interaction_type == 2 or k.interaction_type == 3):
                                score *= 5
                            elif(k.interaction_type == 5):
                                score *= 20
                            if(score > THRESHOLD and users_score[u] < score ):
                                users_score[u] = score

            sortedList = sorted(users_score, key=lambda x: users_score[x], reverse=True)
            if len(sortedList) > 0:
                item_id = str(i) + "\t"
                fp.write(item_id)

                list_len = len(sortedList)
                if(len(sortedList) > 100):
                    list_len = 99
                for j in range(0, list_len-1):
                    user_id = str(sortedList[j]) + ","
                    fp.write(user_id)
                user_id = str(sortedList[-1]) + "\n"
                fp.write(user_id)
                fp.flush()

            if pos % 100 == 0:
                try:
                    score = str(average_score / num_evaluated)
                except ZeroDivisionError:
                    score = 0
                percentageDown = str(pos / float(len(item_ids)))
                print(percentageDown)
            pos += 1

            '''
            # build all (user, item) pair features based for this item
            for u in target_users:
                x = Interaction(users[u], items[i], -1)
                if x.title_match() > 0:
                    f = x.features()
                    data += [f]
                    ids  += [u]


            if len(data) > 0:
                # predictions from XGBoost
                dtest = xgb.DMatrix(np.array(data))
                ypred = model.predict(dtest)

                # compute average score
                average_score += sum(ypred)
                num_evaluated += float(len(ypred))

                # use all items with a score above the given threshold and sort the result
                user_ids = sorted(
                    [
                        (ids_j, ypred_j) for ypred_j, ids_j in zip(ypred, ids) if ypred_j > TH
                    ],
                    key = lambda x: -x[1]
                )[0:99]

                # write the results to file
                if len(user_ids) > 0:
                    item_id = str(i) + "\t"
                    fp.write(item_id)
                    for j in range(0, len(user_ids)):
                        user_id = str(user_ids[j][0]) + ","
                        fp.write(user_id)
                    user_id = str(user_ids[-1][0]) + "\n"
                    fp.flush()

            # Every 100 iterations print some stats
            if pos % 100 == 0:
                try:
                    score = str(average_score / num_evaluated)
                except ZeroDivisionError:
                    score = 0
                percentageDown = str(pos / float(len(item_ids)))
                print(percentageDown)
            pos += 1

            '''
