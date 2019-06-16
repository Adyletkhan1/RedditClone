import requests
import pytest
from  posts.route import app


class MyTestClass():

    def setUp(self):
        self.app = app.test_client()
        
        self.app.testing = True

   

    def test_home1(self):
        
        res = self.app.get('/')

        
        assert res.status_code == 200

    def test_home2(self):
        
        res = self.app.get('/home')

        
        assert res.status_code == 200

    def test_posts1(self):
        
        res = self.app.get('/history')

        assert res.status_code == 200

    def test_collections(self):
       
        res = self.app.get('/collections')

        assert res.status_code == 200

