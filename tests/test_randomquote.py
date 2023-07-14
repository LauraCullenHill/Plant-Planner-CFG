import unittest
from unittest import TestCase, mock
from unittest.mock import patch
from randomquote import Quotations


class TestRandomQuote(TestCase):
    
    def test_fetch_quotes_from_url_works(self):
        url = 'https://raw.githubusercontent.com/RubyBlues/Project/main/quotes.txt'
        quotations = Quotations(url) # create an instance of class

        response_mock = unittest.mock.Mock() # create mock object to mock response of requests.get()
        response_mock.status_code = 200 # mocking a good response
        response_mock.text = 'This is a test\nGardening is great fun\nHope this works!\n'

        #use patch to replace requests.get with the mocked object (response_mock)
        #Inside the 'with', call the instance with the method
        with patch('requests.get', return_value=response_mock):
            quotations.fetch_quotes_from_url()

            self.assertEqual(quotations.quotes, response_mock.text.splitlines())


    def test_fetch_quotes_from_url_fails(self):
        url = 'https://raw.githubusercontent.com/RubyBlues/Project/main/quotes.txt'
        quotations = Quotations(url) # create an instance of class

        response_mock = unittest.mock.Mock() # create mock object to mock response of requests.get()
        response_mock.status_code = 404 # mocking a failed response

        #use patch to replace requests.get with the mocked object (response_mock)
        #inside 'with', call the instance with the method
        with patch('requests.get', return_value=response_mock):
            quotations.fetch_quotes_from_url()

        # unlike previous example the 404 means quotes were not obtained so assert equal to empty list
            self.assertEqual(quotations.quotes, [])


    @patch('random.choice')
    def test_get_random_quote(self, random_mock):
        url = 'https://raw.githubusercontent.com/RubyBlues/Project/main/quotes.txt'
        quotations = Quotations(url)  # create an instance of class
        quotations.fetch_quotes_from_url()
        quotations.mock = ['This is a test', 'Gardening is great fun', 'Hope this works!']
        random_mock.return_value = 'Gardening is great fun'

        self.assertEqual(quotations.get_random_quote(), random_mock.return_value)


if __name__ == '__main__':
    unittest.main()


