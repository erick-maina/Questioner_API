import json
import unittest
from ... import create_app


class TestQuestioner(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.questions = {"q_id":1,"created_on" : "2000-01-01", "created_by":"1", "meetup":"1",
                 "title":"Posting in Python", "body":"How?", "votes": 3}

    def test_post_comment(self):
        """ Test posting a question."""
        self.client.post('/api/v1/questions', data=json.dumps(self.questions), content_type = 'application/json')
        self.comment = {"q_id":1,"comment" : "Good question"}
        response = self.client.post('/api/v1/comments', data=json.dumps(self.comment), content_type='application/json')
        self.assertEqual(response.status_code, 201)