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
        self.database_name = ""
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "Mock question", "answer": "Mock answer", "difficulty": 1, "category": 1}
        self.search_term = {"search_term": "mock search term"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_retrieve_categories_success(self):
        res = self.client().get('/categories')
        data = json(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_retrieve_categories_with_invalid_method(self):
        res = self.client().post('/categories')
        data = json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_retrieve_questions_success(self):
         res = self.client().get('/questions')
         data = json(res.data)

         self.assertEqual(res.status_code, 200)
         self.assertEqual(data['success'], True)
         self.assertTrue(data['questions'])
         self.assertTrue(data['categories'])
         self.assertEqual(data['current_category'], "All")

    def test_404_retrieve_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={"rating": 1})
        data = json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_delete_question_success(self):
        res = self.client().delete('/questions/1')
        data = json(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(book, None)

   def test_422_delete_question_which_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

   def test_create_question_success(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['create'])

   def test_404_question_creation_not_allowed(self):
        res = self.client().post('/questions/50', json=self.new_question)
        data = json(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

   def test_search_questions(self):
        res = self.client().post('/questions/search', json=self.search_term)
        data = json(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['All'])

   def test_404_question_search_invalid(self):
        res = self.client().post('/questions/search', json={"searchTerm": ""})
        data = json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

   def test_retrieve_questions_by_category_success(self):
        res = self.client().get('/categories/1/questions')
        data = json(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

   def test_404_cannot_retrieve_questions_from_invalid_category(self):
        res = self.client().get('/categories/100000/questions')
        data = json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

   def test_retrieve_quiz_questions(self):
        res = self.client().post('/quizzes',  json={"quiz_category": {"type": "Mock type", "id": 1}, "previous_questions": [1]})
        data = json(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

   def test_404_unable_to_retrieve_quiz_questions(self):
        res = self.client().post('/quizzes',  json={"quiz_category": {"type": "Mock type", "id": 10}, "previous_questions": [1]})
        data = json(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
