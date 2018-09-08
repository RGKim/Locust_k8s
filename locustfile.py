import base64
 
from locust import HttpLocust, TaskSet, task
from random import randint, choice
 
 
class WebTasks(TaskSet):
 
    @task
    def load(self):
        base64_str = base64.encodestring(('%s:%s' % ('user','password')).encode()).decode().replace('\n', '')
        catalogue = self.client.get("/catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]
 
        self.client.get("/")
        self.client.get("/login", headers={"Authorization":"Basic %s" % base64_str})
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.get("/basket.html")
        self.client.post("/orders")
 
 
class Web(HttpLocust):
    task_set = WebTasks