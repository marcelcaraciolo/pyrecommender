# -*- coding: utf-8 -*-
from apontador import ApontadorAPI
import Queue
import threading
import pickle
import time
import simplejson


#Simple Crawler of Places at Apontador


#CONSUMER_KEY = "KpsWD7ynRUXINRFkml8Q-xIUA5LT_fY8OT5h1VZr0Uc~"
#CONSUMER_SECRET = "68vdw3xwgy-eM0iRDlMLFF418IQ~" 
#OAUTH_TOKEN = '9153904622-KpsWD7ynRUV_0-8wQQnXgBZZ9XHYj__xfMhJ3aexK9HVyxdBcXZa4A~~'
#OAUTH_TOKEN_SECRET = 'jqgnH6aV6-VQKOQyiLIu_-0ZQIQ~'
#USERID = '9153904622'

api = ApontadorAPI(consumer_key = CONSUMER_KEY,
                   consumer_secret = CONSUMER_SECRET,
                   oauth_token = OAUTH_TOKEN,
                   oauth_token_secret = OAUTH_TOKEN_SECRET)

output_file = open('dataset.txt', 'a')

class ApontadorExtractor(threading.Thread):
    def __init__(self,out_queue):
        threading.Thread.__init__(self)
        self.out_queue = out_queue
    
    def extractReviews(self, reviewsLimit=200):
        page = 1
        reviews_list = []
        
        reviewsFlag = True
        
        while True:
            tempList = []
            place = self.out_queue.get()

            page = 1
            reviews_list = []

            reviewsFlag = True
    
            while reviewsFlag:          
                for i in range(5):
                    try:
                        response = api.get_place_reviews(placeid= place[0], page=page, type="json")
                        response = simplejson.loads(response)
                        break
                    except:
                        print 'FAILED at page %d' % page
                    
                    time.sleep(4)
            
                reviews = response['place']['reviews']
                if len(reviews) > 0 and len(reviews_list) < reviewsLimit:
                    tempList = [(review['review']['place']['id'], int(review['review']['rating']), review['review']['created']['user']['name'], review['review']['created']['user']['id'])  \
                                    for review in reviews]
                    reviews_list.extend(tempList)
                    if len(reviews_list) > reviewsLimit:
                        reviewsFlag = False
                    page+=1
                    for place_id,rating,username,user_id in tempList:
                        output_file.write('%s,%s,%d\n'  % (user_id,place_id,rating)) 
                else:
                    reviewsFlag = False
            
            self.out_queue.task_done()
            
    
    def run(self):
        self.extractReviews()
        output_file.close()
          


class ApontadorCollector(threading.Thread):
    def __init__(self,queue,out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
    
    def getPlaces(self,category,rating,pageLimit=200,placesLimit=200,order='descending'):
        page = 1
        places_list = []
        
        statusFlag = True
        
        while statusFlag: 
            tempList = []
            for i in range(2):
                try:
                    response = api.search_places_by_address(state="SP", city="Sao Paulo", type="json", rating=str(rating), limit=pageLimit,page=page,category_id=category)
                    response = simplejson.loads(response)
                    break
                except:
                    print 'FAILED at page %d' % page
                    statusFlag = False
                    break
            
                time.sleep(4)
            
            places = response['search']['places']
            if len(places) > 0 and len(places_list) < placesLimit:
                tempList = [(place['place']['id'], place['place']['name'])  for place in places if int(place['place']['review_count']) > 0]
                places_list.extend(tempList)
                if len(places_list) > placesLimit:
                    statusFlag = False
                page+=1
                for place in tempList:
                    print place
                    self.out_queue.put(place)
            else:
                statusFlag = False              
                
    
    def run(self):
        self.getPlaces(category=63,rating=1)
        self.getPlaces(category=63,rating=2)
        self.getPlaces(category=63,rating=3)
        self.getPlaces(category=63,rating=4)
        self.getPlaces(category=63,rating=5)

        self.getPlaces(category=17,rating=1)
        self.getPlaces(category=17,rating=2)
        self.getPlaces(category=17,rating=3)
        self.getPlaces(category=17,rating=4)
        self.getPlaces(category=17,rating=5)


queue = Queue.Queue()
out_queue = Queue.Queue()

ac = ApontadorCollector(queue,out_queue)
ac.run()


ae = ApontadorExtractor(out_queue)
ae.run()


