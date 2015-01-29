import unittest
import twitterUpdate

class TwitterUpdateTestCase(unittest.TestCase):

    def setUp(self):
        self.app = twitterUpdate.app.test_client()
 
    def tearDown(self):
        pass

    def test_welcome(self):
        rv = self.app.get('/')
        assert '<h1>Welcome to the Twitter User Search Page!</h1>' in rv.data

    def test_result(self):
        try: # throws ValueError because no request has been sent
            rv = self.app.get('/results')

        except ValueError:
            pass

    def test_display(self):
        rv = self.app.get('/display')
        assert '<h1>List of Twitter Users on File</h1>' in rv.data

    def test_results(self):
        rv = self.app.post('/results', data = {'username' : 'twitter'})
        assert 'User has been found!' in rv.data

        rv = self.app.post('/results', data = {'username' : 'twitter', 'ID' : 1})
        assert 'User has been found!' not in rv.data

        rv = self.app.post('/results', data = {'ID' : 783214})
        assert 'User has been found!' in rv.data
        
if __name__ == '__main__':
    unittest.main()
