# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python
   for your platform in the
   [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment
   whenever using Python for projects. This keeps your dependencies for each
   project separate and organized. Instructions for setting up a virual
   environment for your platform can be found in the
   [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running,
   install the required dependencies by navigating to the `/backend` directory
   and running :

```
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices
  framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM
  we'll use to handle the lightweight SQL database. You'll primarily work in
  `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension
  we'll use to handle cross-origin requests from our frontend server.

### setting-up Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

```windows
CRETAE DATABASE trivia;
```

Populate the database using the `trivia.psql` file provided. From the `backend`
folder in terminal run:

```bash
psql trivia < trivia.psql
```

for windows

```windows
\i 'path/trivia.pqsl'
```

### Running the Server

- **Start your virtual environment** From the backend folder run

```bash
# Mac users
python3 -m venv venv
source venv/bin/activate
# Windows users
> py -3 -m venv venv
> venv\Scripts\activate
```

From within the `./src` directory first ensure you are working using your
created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

```windows powershell
 for windows powershell
$env:FLASK_APP=<app_name>
flask run
```

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a
  base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`,
  which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require
  authentication or API keys.

### Handling Errors

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "error text"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable

### Endpoints

#### GET /categories

- General:
  - Returns an objects of categories in which the keys are IDs and the value is
    the corresponding string in this case (TYPE), success value, and tcategories
    and total number of categories -there is no request arguments for categories
  - Request Arguments: None
- Sample: `curl http://127.0.0.1:5000/categories`

```
   {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}

```

### GET/questions

- General:
  - Gets the lists of all questions , the number of total questions categories
    and current categories.
  - Query Parameter(optional)- ?page=#: page number
  - Request Arguments: None
  - Results apaginated in groups of 10
- Sample: `curl http://127.0.0.1:5000/question`

```
{
  "current_category": null,
  "categories":
  {"1":"Science",
  "2":"Art",
  "3":"Geography",
  "4":"History",
  "5":"Entertainment",
  "6":"Sports"
  },
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }

  ],
  "total_questions": 3
}

```

## DELETE /questions/{int:question_id}

- General:
  - Delets a question by using the question_id value
  - if success returns a success messgae true, deleted-id of question deleted
    and total question left
  - Request Arguments: `id`
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/2`

```
{
   "deleted": 2,
  "success": true,
  "total_questions":18
}

```

#### POST /questions

- General:
  - Creates a new question using the submitted question, answer ,dificulty and
    category .
  - Returns the id of the created book, success value and total questions
- Sample:`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "What is my name?", "answer": "noname","difficulty": 1,"category": 1}''`

```
{
  "success": true,
  "created":19,
  "total_questions":19

}
```

#### POST /questions/search

- General:

  - Get questions based on search term
  - Return question which matches the word searched for, t0tal questions,
    success value
  - Request Argument : `searchTerm`

- Sample:` curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"name"}'`

```
{
   "questions":[
      {"answer":"Muhammad Ali",
      "category":4,
      "difficulty":1,
      "id":9,
      "question":"What boxer's original name is Cassius Clay?"
      },
      {"answer":"Brazil",
      "category":6,
      "difficulty":3,
      "id":10,
      "question":"Which is the only team to play in every soccer World Cup tournament?"
      },
{"answer":"daniel",
"category":5,
"difficulty":5,
"id":28,
"question":"whats my name"
}],
"success":true,
"total_questions":3
}

```

## GET /categories/{int:category_id}/questions

- General:
  - Get questions based on categories -no request arguemnts required
  - Results are paginated in groups of 10
  - Request Arguments: `id` - integer
  - Returns a list of questions in that category id,success value, total
    questions, current category selected
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

```
{
   "current_category":"Science",
   "questions":[{
      "answer":"The Liver",
      "category":1,
      "difficulty":4,
      "id":20,
      "question":"What is the heaviest organ in the human body?"},
      {"answer":"Alexander Fleming"
      ,"category":1,
      "difficulty":3,
      "id":21,
      "question":"Who discovered penicillin?"},
      {"answer":"Blood",
      "category":1,
      "difficulty":4,
      "id":22,
      "question":"Hematology is a branch of medicine involving the study of what?"},
      {"answer":"Nothing",
      "category":1,
      "difficulty":1,
      "id":25,
      "question":"What is this test?"
      }],"success":true,
      "total_questions":4
      }
```

## POST /quizzes

- General:
  - Get questions to play the quiz
  - Return a random question within the given category, if provided, and that is
    not one of the previous questions and the success value
- Sample:` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category": {"id":4, "type":"History"}}'`

```
{
   {
      "question":{
         "answer":"Alexander Fleming",
         "category":1,
         "difficulty":3,
         "id":21,
         "question":"Who discovered penicillin?"},
         "success":true}
}
```

## Testing

To run test, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
