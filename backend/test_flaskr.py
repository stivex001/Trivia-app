import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('stephen', '0930' 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

        #==== UNITTEST FOR FAILED GET REQUEST ON CATEGORY ======#

    def test_sent_invalid_request(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    #========================================================#
    #========== UNITTEST FOR GET REQUEST ON QUESTIONS=========#

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])

    # ===== UNITTEST FOR GET REQUEST ON QUESTIONS BY CATEGORY ======#

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    #===========================================================#
    #====== UNITTEST FOR FAILED GET REQUEST ON QUESTIONS =======#

    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'rating': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    #======== UNITTEST FOR POST REQUEST ON QUESTION=============#

    def test_add_new_question(self):
        res = self.client().post('/questions', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])

    #==========================================================#
    #=========== UNITTEST FOR DELETE REQUEST ON QUESTION=======#

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_question'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])

    #=============================================================#
    #====== UNITTEST FOR FAILED DELETE REQUEST ON QUESTION =======#

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()