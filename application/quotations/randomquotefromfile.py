import random

print("██████╗░██╗░░░░░░█████╗░░█████╗░███╗░░░███╗")
print("██╔══██╗██║░░░░░██╔══██╗██╔══██╗████╗░████║")
print("██████╦╝██║░░░░░██║░░██║██║░░██║██╔████╔██║")
print("██╔══██╗██║░░░░░██║░░██║██║░░██║██║╚██╔╝██║")
print("██████╦╝███████╗╚█████╔╝╚█████╔╝██║░╚═╝░██║")
print("╚═════╝░╚══════╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝")

# reading from quotes.txt file to generate random quote for 'quote of the day'
with open('quotes.txt', 'r') as file:
    quotes = file.readlines()

random_quote = random.choice(quotes)

print("Quote of the Day:")
print(random_quote)