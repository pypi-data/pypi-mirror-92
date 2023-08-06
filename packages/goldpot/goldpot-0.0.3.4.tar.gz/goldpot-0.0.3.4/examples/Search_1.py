from goldpot import *

api_key = "<enter you api key>"

def search_sample(api_key):
    gp = Goldpot(api_key)
    docs = ['I like pizza.', 'Python is a scripting language.', 'Socrates is an ancient philosopher.']
    si = SearchInput(query="I like beer.", docs=docs, max_chars=8000)
    out = gp.search(si)
    print(out.scores)
    print(out.scores_sorted)


if __name__ == '__main__':
    search_sample(api_key)