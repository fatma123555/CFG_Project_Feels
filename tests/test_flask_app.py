try:
    from src.main import app
    from src import main
    from flask import session
    import unittest
    # Spotify API
    import os
    from dotenv import load_dotenv

    # Credentials
    load_dotenv('.env')
    SECRET_KEY = os.getenv('SECRET_KEY')
    import jinja2
except Exception as e:
    print("Some modules are missing {}".format(e))


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # check for a 200 response on index page
    def test_index_path(self):
        response = self.app.get("/")
        self.assertEquals(response.status_code, 200)

    # check for a 200 response on quiz page
    def test_quiz_path(self):
        response = self.app.get("/quiz")
        self.assertEquals(response.status_code, 200)

    # check for a 200 response on second quiz page
    def test_second_question_path(self):
        mood = "Happy"
        response = self.app.get("/quiz/{}".format(mood))
        self.assertEquals(response.status_code, 200)

    # check if the returned response if a HTML page
    def stest_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        actual = response.content_type
        expected = "text/html; charset=utf-8"
        self.assertEquals(actual, expected)


class TestLoadedForms(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SECRET_KEY'] = "Secret key"
        self.app = app.test_client()
        # self.app.post('/quiz/{}'.format("Happy"), data={'mood': 'Happy'})
        self.assertEqual(app.debug, False)

    # check that a form has been loaded on the quiz page
    def test_form_loaded_on_quiz_page(self):
        response = self.app.get("/quiz")
        self.assertIn('<form method="post">'.encode(), response.data)

    # check that a form has been loaded on the second quiz page
    def test_form_loaded_on_quiz_second_page(self):
        response = self.app.get("/quiz/{}".format("Happy"))
        self.assertIn('<form method="post">'.encode(), response.data)

    # check if the page loaded correctly as a happy mood
    def test_correct_response_tdo_happy_mood(self):
        resp = self.app.get("/quiz")
        self.assertIn("<h2>Here to take the quiz?</h2>".encode(), resp.data)

    # # check if form posts
    # def test_form_first_question_posts(self):
    #     response = self.app.post("/quiz", data={
    #             "mood": "Sad"
    #         })
    #     print(response.data)

    # check if the page loaded correctly as a happy mood
    def test_correct_response_to_happy_mood(self):
        resp = self.app.get("/quiz/{}".format("Happy"))
        self.assertIn("<h2>Feeling Happy? Let\'s dive deeper!</h2>".encode(), resp.data)

    # check if the second quiz page loaded correctly as a Sad mood
    def test_correct_html_output_to_sad_second_question_quiz_page(self):
        with app.test_client() as c:
            response = c.post("/quiz/{}".format("Sad"), data={
                "final_mood": "Sad"
            })
            self.assertIn("Lonely".encode(), response.data)

    # check if the page loaded correctly as a happy mood
    def test_correct_response_to_confident_mood(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['final_mood'] = 'Happy'
            # once this is reached the session was stored
            result = app.test_client().get("/quiz/{}".format("Happy"))
            response = c.post("/quiz/{}".format("Sad"), data={
                "final_mood": "Sad"
            })
            print(result)
            print(response.data)
            print(sess)
            assert sess.get("final_mood") == "Happy"
            # NOT part of the 2nd context
            # assert response.data == b"Username saved in session"

if __name__ == '__main__':
    unittest.main()





    # # check that a form has been loaded on the second quiz page
    # def test_form_loaded_on_rating_page(self):
    #     with self.app as c:
    #         rv = c.get('/quiz')
    #         print(help(rv))
    #         print(flask.session)
    #         assert flask.session['final_mood'] == 42


# class TestValidateOnSubmit(unittest.TestCase):
#
#     def test_not_submitted(self):
#         with self.request(method='GET', data={}):
#             f = FooForm(request.form, csrf_enabled=False)
#             self.assertEqual(f.is_submitted(), False)
#             self.assertEqual(f.validate_on_submit(), False)
#
#     if __name__ == '__main__':
#         unittest.main()

    # # check for a 200 response on the successful loading of results page
    # def test_result_path(self):
    #     client = self.app
    #     # assert client.get('/result/').status_code == 200
    #     # # response = client.post("/result/", data={
    #     # #         "data": "test"
    #     # #     })
    #     # assert response.headers['Location'] == 'http://localhost/'
    #
    #     with client:
    #         client.get('/quiz/')
    #         assert session[''] == "Happy"
    #         assert g.user['username'] == 'test'
    #
    #     #     response = client.post("/", data={
    #     #         "data": "test"
    #     #     })
    #     #     assert session.get("data") == "test"
    #     #     assert response.data == b"Username saved in session"
    #     # response = self.app.get("/result/")
    #     # self.assertEquals(response.status_code, 200)

    # # check if the page loaded correctly as a happy mood
    # def test_correct_response_to_confident_mood(self):
    #     with app.test_client() as c:
    #         with c.session_transaction() as sess:
    #             sess['final_mood'] = 'Happy'
    #
    #         # once this is reached the session was stored
    #         result = app.test_client().get("/quiz/{}".format("Happy"))
    #         # response = c.post("/quiz/{}".format("Happy"), data={
    #         #     "final_mood": "Happy"
    #         # })
    #         print(sess)
    #         assert sess.get("final_mood") == "Happy"
    #         # NOT part of the 2nd context
    #
    #         # assert response.data == b"Username saved in session"
