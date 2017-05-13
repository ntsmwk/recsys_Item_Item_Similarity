'''
Parsing the ACM Recsys Challenge 2017 data into interactions,
items and user models.

by Daniel Kohlsdorf
'''

from model import * 


def is_header(line):
    return "item" in line or "user" in line or "interaction" in line


def process_header(header):
    print(header)
    x = {}
    pos = 0
    for name in header:
        x[name.split(".")[1]] = pos
        pos += 1
    return x

def select(from_file, where, toObject, index):    
    header = None
    data = {}
    i = 0
    for line in open(from_file):
        if is_header(line):
            header = process_header(line.strip().split("\t"))
        else:
            cmp = line.strip().split("\t")
	
            if where(cmp):
                obj = toObject(cmp, header)
                if obj != None:
                    data[index(cmp)] = obj
        i += 1
        if i % 100000 == 0:
            print("... reading line " + str(i) + " from file " + from_file)
    return(header, data)        


def build_user(str_user, names):
    if len(str_user) > 14:
	    return User(
		[int(x) for x in str_user[names["jobroles"]].split(",") if len(x) > 0],
		int(str_user[names["careerlevel"]]),
		int(str_user[names["industryid"]]),
		int(str_user[names["disciplineid"]]),
		str_user[names["country"]],
		str_user[names["region"]],
		int(str_user[names["edudegree"]]),
		int(float(str_user[names["avgemployment"]]))
	    )
    else: 
 	    return User(
		[int(x) for x in str_user[names["jobroles"]].split(",") if len(x) > 0],
		int(str_user[names["careerlevel"]]),
		int(str_user[names["industryid"]]),
		int(str_user[names["disciplineid"]]),
		str_user[names["country"]],
		str_user[names["region"]],
		int(str_user[names["edudegree"]]),
		-3
	    )
    

def build_item(str_item, names):
    if len(str_item) > 14:
	    return Item(
		[int(x) for x in str_item[names["title"]].split(",") if len(x) > 0 and x != '""'],
		int(str_item[names["careerlevel"]]),
		int(str_item[names["industryid"]]),
		int(str_item[names["disciplineid"]]),
		str_item[names["country"]],
		str_item[names["region"]],
		int(str_item[names["employment"]]),
		int(float(str_item[names["avgedudegree"]])),
	    )
    else:
	return Item(
		[int(x) for x in str_item[names["title"]].split(",") if len(x) > 0 and x != '""'],
		int(str_item[names["careerlevel"]]),
		int(str_item[names["industryid"]]),
		int(str_item[names["disciplineid"]]),
		str_item[names["country"]],
		str_item[names["region"]],
		int(str_item[names["employment"]]),
		-3,
	    )


class InteractionBuilder:
    
    def __init__(self, user_dict, item_dict):
        self.user_dict = user_dict
        self.item_dict = item_dict
    
    def build_interaction(self, str_inter, names):
        if int(str_inter[names['item_id']]) in self.item_dict and int(str_inter[names['user_id']]) in self.user_dict:
            return Interaction(
                self.user_dict[int(str_inter[names['user_id']])],
                self.item_dict[int(str_inter[names['item_id']])],
                int(str_inter[names["interaction_type"]])
            )
        else:
            return None


