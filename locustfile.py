import base64
import string
import random
import json
import requests
 
from locust import HttpLocust, TaskSet, task, seq_task
from random import choice
 
 
class WebTasks(TaskSet):
 
    @seq_task(1)
    def load(self):
        self.client.get("/")

        global username
        username = ""
        for _ in range(10):
            username += str(random.choice(string.ascii_letters))
        c_id = json.loads(self.client.post("/register", json={"username": username, "password": 'password'}).content)['id']
        self.client.post("/cards", json={"longNum":"123123", "expires":"2310", "ccv":"456", "userID": c_id})
        self.client.post("/addresses", json={"street":"123123", "number":"321321", "country":"Korea", "city": "Seongnam-si", "postcode": "123123", "userID": c_id})

        base64_str = base64.encodestring(('%s:%s' % (username,'password')).encode()).decode().replace('\n', '')
        self.client.get("/login", headers={"Authorization":"Basic %s" % base64_str})
        self.client.get("/category.html")

        global item_id
        item_id = choice(self.client.get("/catalogue").json())["id"]
        self.client.get("/detail.html?id={}".format(item_id))
  
        if not self.client.get("/cart").content:
            self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})

        if not self.client.get("/basket.html").content:
            self.client.post("/orders", json={}) 


class Web(HttpLocust):
    task_set = WebTasks
    min_wait = 500
    max_wait = 1000