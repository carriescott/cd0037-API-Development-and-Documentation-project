import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    def retrieve_categories():
        try:
            categories = Category.query.all()
            categories_list = {category.id:category.type for category in categories}
        except:
            abort(404)
        return jsonify({
            'success': True,
            'categories': categories_list,
            'total_categories': len(categories)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def retrieve_questions():
        try:
            categories = Category.query.all()
            categories_list = {category.id:category.type for category in categories}
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)
        except:
            abort(404)
        return jsonify({
            'success': True,
            'total_questions': len(questions),
            'questions': current_questions,
            'categories': categories_list,
            'current_category': 'All'
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        print(id)
        try:
            question = Question.query.get(id)
            print(question)

            if question is None:
                abort(422)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })

        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def create_question():

        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        try:
            question = Question(
            question = question,
            answer = answer,
            difficulty = difficulty,
            category = category)

            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
            })

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm')
        formatted_input = '%{0}%'.format(search_term)

        try:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            questions_list = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': questions_list,
                'total_questions': len(questions),
                'current_category': 'All'
            })

        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:id>/questions')
    def retrieve_questions_by_category(id):
        print(id)
        try:
            questions = Question.query.filter(Question.category==id).all()
            print(questions)
            questions_list = [question.format() for question in questions]
            print(questions_list)

            category = Category.query.get(id)

            print(category.type)

            return jsonify({
                'questions': questions_list,
                'total_questions': len(questions),
                'current_category': category.type
            })

        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """


    @app.route('/quizzes', methods=['POST'])
    def retrieve_quiz_questions():
        data = request.get_json()
        quiz_category = data.get('quiz_category', None)
        previous_questions = data.get('previous_questions', None)

        try:
            if quiz_category['id'] == 0:
                quiz_questions = Question.query.all()
            else:
                category = Category.query.filter(Category.id == quiz_category["id"]).one_or_none()
                quiz_questions = Question.query.filter(Question.category == category.id).all()

            possible_questions = []

            for question in quiz_questions:
                if question.id not in previous_questions:
                    possible_questions.append(question)

            if len(possible_questions) != 0:
                selected_question = random.choice(possible_questions)
                return jsonify({
                    'success': True,
                    'question': selected_question.format()
                })
            else:
                abort(422)

        except:
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
                }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
                }), 422

    return app

