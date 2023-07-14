import random
import requests
from images.ascii_art import ascii_quote


class Quotations:
    def __init__(self, url):
        self.url = url
        self.quotes = []

    def fetch_quotes_from_url(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.quotes = response.text.splitlines()

    def get_random_quote(self):
        if not self.quotes:
            return "No quotes found."
        return random.choice(self.quotes)

    def run(self):
        ascii_quote()

        self.fetch_quotes_from_url()

        # print("Quote of the Day:")
        print(self.get_random_quote())


def run_quotations():
    url = 'https://raw.githubusercontent.com/RubyBlues/Project/main/quotes.txt'
    quotations = Quotations(url)
    quotations.run()


run_quotations()
