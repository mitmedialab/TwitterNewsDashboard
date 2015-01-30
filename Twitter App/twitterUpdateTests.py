import unittest
import twitterUpdate
import mockTwitter

class TwitterUpdateTestCase(unittest.TestCase):

    def setUp(self):
        self.posts = twitterUpdate.connect_db()[1]
        self.app = twitterUpdate.app.test_client()
        self.mockTwitter = mockTwitter.MockTwitter()
 
    def tearDown(self):
        pass

    def test_welcome(self):
        rv = self.app.get('/')
        assert '<h1>Welcome to the Twitter User Search Page!</h1>' in rv.data

    def test_results_one(self):
        try: # throws ValueError because no request has been sent
            rv = self.app.get('/results')

        except ValueError:
            pass

    def test_results_two(self):
        rv = self.app.post('/results', data = {'username' : 'twitter'})
        assert 'User has been found!' in rv.data

    def test_results_three(self):
        rv = self.app.post('/results', data = {'username' : 'twitter', 'ID' : 1})
        assert 'User has been found!' not in rv.data

    def test_results_four(self):
        rv = self.app.post('/results', data = {'ID' : 783214})
        assert 'User has been found!' in rv.data

    def test_results_five(self):
        rv = self.app.post('/results')
        assert 'Search fields are empty' in rv.data

    def test_redirect_home(self):
        rv = self.app.get('/')
        assert '<a href="/">Home</a>' in rv.data
        assert '<a href="/display">Twitter Users on File</a>' in rv.data
        
    def test_redirect_results(self):
        rv = self.app.post('/results')
        assert '<a href="/">Home</a>' in rv.data
        assert '<a href="/display">Twitter Users on File</a>' in rv.data

    def test_redirect_display(self):
        rv = self.app.get('/display')
        assert '<a href="/">Home</a>' in rv.data
        assert '<a href="/display">Twitter Users on File</a>' in rv.data
        
    def test_display_one(self):
        rv = self.app.get('/display')
        assert '<h1>List of Twitter Users on File</h1>' in rv.data

    def test_display_two(self):
        # make sure that the username 'SNICKERS' is actually not stored
        # in the database in case this file has been run before
        status = self.posts.remove({'Username' : 'SNICKERS'})
        rv = self.app.get('/display')
        assert 'SNICKERS' not in rv.data
        
        rv = self.app.post('/results', data = {'username' : 'SNICKERS'})
        rv = self.app.get('/display')
        assert 'SNICKERS' in rv.data

    def test_display_three(self):
        # make sure that the username 'ABC123' is actually not stored
        # in the database in case this file has been run before
        status = self.posts.remove({'Username' : 'ABC123'})
        rv = self.app.get('/display')
        assert 'ABC123' not in rv.data

        # user 'ABC123' does not exist, so we should not expect anything
        # to have been stored in our local database
        rv = self.app.post('/results', data = {'username' : 'SNICKERS'})
        rv = self.app.get('/display')
        assert 'ABC123' not in rv.data
        
    def test_database_insert(self):
        results = self.mockTwitter.postsTwitterData.find({'Username' : 'user1'})

        try: # make sure that the twitterData mock database does not
             # contain such a user on file
            match = results.next()
            raise ValueError("Expected no results but at least one was found")

        except StopIteration:
            request = mockTwitter.Request(**{'username' : 'user1'})
            result = self.mockTwitter.search(request)
            assert type(result) == dict, "Expected a result but none was found"

            results = self.mockTwitter.postsTwitterData.find({'Username' : 'user1'})
            match = results.next()

    def test_database_cache(self):
        results = self.mockTwitter.postsTwitterData.find({'Username' : 'user2'})
        match = results.next()

        currentTimestamp = match['Timestamp']
        request = mockTwitter.Request(**{'username' : 'user2'})
        result = self.mockTwitter.search(request)
        assert type(result) == dict, "Expected a result but none was found"
        
        results = self.mockTwitter.postsTwitterData.find({'Username' : 'user2'})
        match = results.next()

        # the timestamp on the entry for user2 will be current enough that
        # no update should have been made to the local database
        assert currentTimestamp == match['Timestamp']

    def test_database_update(self):
        results = self.mockTwitter.postsTwitterData.find({'Username' : 'user3'})
        match = results.next()

        currentTimestamp = match['Timestamp']
        request = mockTwitter.Request(**{'username' : 'user3'})
        result = self.mockTwitter.search(request)
        assert type(result) == dict, "Expected a result but none was found"
        
        results = self.mockTwitter.postsTwitterData.find({'Username' : 'user3'})
        match = results.next()
        
        # the timestamp on the entry for user3 will be stale, so we expect to
        # have made an update to the local database
        assert currentTimestamp < match['Timestamp']
        
        
if __name__ == '__main__':
    unittest.main()
