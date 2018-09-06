
# coding: utf-8

# In[ ]:


import requests
import json
import pandas as pd
import numpy as np
import urllib
from urllib.parse import urlencode
import time
from random import randint
import hashlib
import collections
import pickle


# In[ ]:


base = "http://codeforces.com/api/"


# In[ ]:


apikey = "cc8887cc1897de6d5a56448ac134d8c7c3a27498 "
secret = "df28d4a475ebbaa1b10a0c9e14acf1d09f96e104"


# In[ ]:


def prepareParams(params, requestMethod):
    params['apikey'] = apikey
    params['time'] = int(time.time())
    
    random_num = randint(100000,999999)
    sortedparams = collections.OrderedDict(sorted(params.items()))
    
    params['apiSig'] = str(random_num) +     hashlib.sha512(str(str(random_num) + "/" + requestMethod + "?" + urlencode(sortedparams)).encode()).hexdigest()
    
    return collections.OrderedDict(sorted(params.items()))


# In[ ]:


users = json.load(open("users.txt","r"))
users['result'] = users['result'][100000:]


# In[ ]:


submissionData = []
count = 100000
for user in users['result']:
    params = {}
    params['handle'] = user['handle']
    method = "user.status"
    retry = 0
    while True:
        try:
            time.sleep(0.08)
            resp = requests.get(base + method + "?", params=prepareParams(params,method))
            submissionData.append((user['handle'],resp.json()['result']))
            count = count + 1
            break
        except KeyboardInterrupt:
            raise
        except:
            retry = retry + 1
            print("retry " + str(count+1))
            if(retry == 10):
                submissionData.append((user['handle'],{}))
                count = count + 1
                break
            continue
            
    if(count % 50 == 0):
        print(count)
    if(count % 5000 == 0):
        print("saved to pickle")
        f = open("submission" + str(count) + ".pkl","wb")
        pickle.dump(submissionData, f , protocol = pickle.HIGHEST_PROTOCOL)
        f.close()
        del submissionData
        submissionData = []


# In[ ]:


print("saved to pickle")
f = open("submission" + str(count) + ".pkl","wb")
pickle.dump(submissionData, f , protocol = pickle.HIGHEST_PROTOCOL)
f.close()
del submissionData
submissionData = []

