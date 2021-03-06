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
        self.db_host = os.environ.get('DB_HOST')
        self.db_user=os.environ.get('DB_USER')
        self.db_password=os.environ.get('DB_PASS')
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.db_user,self.db_password,self.db_host, self.database_name)

        # self.database_path =  "postgresql://{}:{}@{}/{}".format(
        #     "postgres", "123", "localhost:5433", self.database_name
        # )
        setup_db(self.app, self.database_path)

        self.new_question = {
        'question': 'What is the color of the moon?',
        'answer': 'blue',
        'category': 1,
        'difficulty': 1,
        }

  
        self.new_ERROR_question = {
        'question': ' ',
        'answer': ' ',
        'difficulty': 1,
        'category': 1
        
        }
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
    def test_get_paginated_questions(self):
        res=self.client().get('/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))


    def test_404_sent_requesting_beyond_valid_page(self):
        res=self.client().get('/questions?page=1000')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)   
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"resource not found")


    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories'])) 


    def test_404_if_category_not(self):
        res=self.client().get('/categories/140')
        data=json.loads(res.data)  

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"resource not found")    
    

    def test_delete_question(self):
        res=self.client().delete('/questions/6')
        data=json.loads(res.data)
        question= Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],6)
        self.assertTrue(data['total_questions'])



    def test_404_if_question_not_exist(self):
        res=self.client().delete('/questions/1000')
        data= json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
        

    def test_create_question(self):

    
        res=self.client().post('/questions', json=self.new_question)  
        data= json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])
        self.assertTrue((data['total_questions']))
    
    def test_422_create_empty_field(self):

    
        res=self.client().post('/questions', json=self.new_ERROR_question)  
        data= json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"Unprocessable")   



    def test_get_questions_search_with_results(self):
        res = self.client().post("/questions/search", json={"searchTerm": "what"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
       


    def test_get_questions_search_without_results(self):
        res = self.client().post("/questions/search", json={"searchTerm": "winkdbfikrui"})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    def test_get_categories(self):
        res=self.client().get('/categories/5/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['current_category'], 'Entertainment')
        self.assertTrue(len(data['questions']))

    def test_400_if_questions_not_found_by_category(self):
        res=self.client().get('/categories/140/questions')
        data=json.loads(res.data)  

        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"bad request")

    def test_play_quiz_game(self):
        res= self.client().post('/quizzes',
                                      json={'previous_questions': [12, 13],
                                            'quiz_category': {'type': 'Art', 'id': '2'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 2)
        self.assertNotEqual(data['question']['id'], 12)
        self.assertNotEqual(data['question']['id'], 13)

    def test_400_play_quiz_fails(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


        
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()