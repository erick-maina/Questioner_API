"""
This module defines the question model and associated functions
"""
from .base_models import BaseModels


class QuestionModel(BaseModels):
    """
    This class encapsulates the functions of the questions model
    """

    def __init__(self):
        """Initialize the database"""
        super().__init__('questions')

    def create_question(self, user_id, m_id, question):
        """
        Function to create a new question under a particular meetup
        """
        query = """INSERT INTO questions (user_id,meetup_id,title,body)\
        VALUES ('{}','{}','{}','{}') RETURNING user_id,meetup_id,question_id,title,body
        ;""".format(user_id, m_id, question['title'], question['body'])
        self.cur.execute(query)
        self.connect.commit()
        result = self.cur.fetchone()
        return result

    def upvote(self, q_id):
        """Function to upvote a question"""
        self.cur = self.connect.cursor()
        query = """UPDATE questions SET votes = votes + 1 WHERE question_id = {} RETURNING meetup_id,title,body,votes
        ;""".format(q_id)
        self.cur.execute(query)
        self.connect.commit()
        result = self.cur.fetchone()
        return result

    def downvote(self, q_id):
        """Function to downvote a question"""
        self.cur = self.connect.cursor()
        query = """UPDATE questions SET votes = votes - 1 WHERE question_id = {} RETURNING meetup_id,title,body,votes
        ;""".format(q_id)
        self.cur.execute(query)
        self.connect.commit()
        result = self.cur.fetchone()
        return result
