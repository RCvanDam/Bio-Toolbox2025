import unittest
from flask import Flask, render_template

class TestAboutPage(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__, template_folder="templates")  # Makes sure Flask can find the right file
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Definieer benodigde routes
        @self.app.route('/about')
        def about():
            return render_template('about.html')

        @self.app.route('/kegg_home')  # Dummy route for Error prevention
        def kegg_home():
            return "KEGG Home"

        @self.app.route('/kegg_tool')  # Dummy route for Error prevention
        def kegg_tool():
            return "KEGG Tool"

        @self.app.route('/contact')  # Dummy route for Error prevention
        def contact():
            return "Contact Page"

    def test_about_page_loads(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Behind Map My KEGG', response.data)
        self.assertIn(b'Who Are We?', response.data)
        self.assertIn(b'Our Vision', response.data)
        self.assertIn(b'What We Offer', response.data)
        self.assertIn(b'The Tools We Use', response.data)
        self.assertIn(b'Explore Tools', response.data)

if __name__ == '__main__':
    unittest.main()
