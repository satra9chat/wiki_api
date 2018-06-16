"""
created by satra9chat
www.github.com/satra9chat
satrajitdchatterjee@gmail.com
"""

import wiki_api
import json

if __name__ == '__main__':
    key = input("Enter Keyword: ")  # main topic user is looking for
    context = input("Enter context: ")  # context of the user's keyword
    query = key + ' ' + context
    findings = ""

    #json_string = json.loads(wiki_api.url_builder(wiki_api.google_searcher(query), 2, query))
    json_string = json.loads(wiki_api.url_builder("https://en.wikipedia.org/wiki/Category:Bases_(chemistry)",
                                                  1, query))
