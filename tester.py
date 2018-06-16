import wiki_api
import json

key = input("Enter Keyword: ")  # main topic user is looking for
context = input("Enter context: ")  # context of the user's keyword
query = key + ' ' + context
findings = ""

json_string = json.loads(wiki_api.url_builder(wiki_api.google_searcher(query), 2))
print(json.dumps(json_string))
