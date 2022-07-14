import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    formatted_question = questions[start:end]
    return formatted_question


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    """
    After_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    """
    Endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:

            categories = Category.query.order_by(Category.id).all()
            formatted_categories = [categorie.format() for categorie in categories]

            return jsonify({
                'success': True,
                'categories': {category.id: category.type for category in categories},
                'total_categories': len(formatted_categories)
            })
        except:
             abort(404)   

    """
    @TODO:
    This endpoint  handles GET requests for questions,
    including pagination (every 10 questions).
    This endpoint returns a list of questions,
    number of total questions, current category, categories.

    """
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()

        categories = Category.query.order_by(Category.type).all()
        current_question = paginate_questions(request, questions)
        if len(current_question) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(questions),
            'current_category': None,
            'categories': {category.id: category.type for category in categories},

        })

    """"
  Endpoint to DELETE question using a question ID.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'total_questions': len(Question.query.all())
            })
        except BaseException:
            abort(404)

    """"
    Endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    """

    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        new_question = body.get("question", ' ')
        new_answer_text = body.get("answer", ' ')
        new_category = body.get("category", ' ')
        new_difficulty_score = body.get("difficulty", ' ')
        try:
            if ((new_question == ' ') or (new_answer_text == ' ')
                    or (new_difficulty_score == ' ') or (new_category == ' ')):
                abort(422)
            else:
                question = Question(
                    question=new_question,
                    answer=new_answer_text,
                    category=new_category,
                    difficulty=new_difficulty_score)

                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_question = paginate_questions(request, selection)

                return jsonify({
                    "success": True,
                    "created": question.id,
                    "total_questions": len(Question.query.all())
                })
        except BaseException:
            abort(422)
    """

   Endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    """

    @app.route("/questions/search", methods=['POST'])
    def search_question():
        body = request.get_json()
        search_term = body['searchTerm']
        try:
            selection = Question.query.filter(
                Question.question.ilike("%" + search_term + "%")
            ).all()
            current_question = paginate_questions(request, selection)
            if len(current_question) == 0:
                abort(400)

            return jsonify({
                "success": True,
                "questions": current_question,
                "total_questions": len(selection)
            })
        except BaseException:
            abort(404)

    """
      GET endpoint to get questions based on category.

    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category_id(category_id):
        categories = Category.query.get(category_id)
        try:
            questions = Question.query.filter_by(
                category=str(category_id)).all()

            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'current_category': categories.type,
                'total_questions': len(questions)

            })
        except BaseException:
            abort(400)

    """
      POST endpoint to get questions to play the quiz.
    """
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')

        category_id = quiz_category['id']
        try:
            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(400)
                # this means no category was selected so diplay all questions
            if (category_id == 0):
                questions = Question.query.all()
                formatted_question = [question.format(
                ) for question in questions if question.id not in previous_questions]
                random_question = random.sample(
                    formatted_question, len(formatted_question))

                if len(random_question) > 0:
                    question = random_question[0]
                else:
                    question = None
            else:
                # this means a category was selected so diplay  questions in
                # category selected
                questions = Question.query.filter_by(
                    category=category_id).all()
                formatted_question = [question.format(
                ) for question in questions if question.id not in previous_questions]
                random_question = random.sample(
                    formatted_question, len(formatted_question))

                if len(random_question) > 0:
                    question = random_question[0]
                else:
                    question = None

            return jsonify({
                'success': True,
                'question': question,
            }), 200

        except Exception as e:
            print(e)
            abort(400)

    """
     Error handlers for all expected errors
    including 404 , 422 and 400.
    """
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"}), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"}), 422

    return app
