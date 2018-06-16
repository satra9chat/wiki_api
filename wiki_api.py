"""
created by satra9chat
www.github.com/satra9chat
satrajitdchatterjee@gmail.com
"""

from googlesearch import search
import requests as rq
import json
from multiprocessing.dummy import Pool as ThreadPool


def wikipedia_searcher(title, query):
    """
    This function performs
    :param title:
    :param query:
    :return:
    """
    url1 = "http://en.wikipedia.org/w/api.php?action=parse&format=json&page="
    url1 = url1 + title
    response = rq.get(url1)
    data = response.json()
    pageid = str(data["parse"]["pageid"])
    url2 = "http://en.wikipedia.org/w/api.php?action=query&format=json&prop=categories&clshow=!hidden&" \
           "cllimit=max&titles="
    url2 = url2 + title
    response = rq.get(url2)
    data = response.json()
    data = data["query"]["pages"][pageid]["categories"]
    categories = []
    dic = {}
    pagescon = []
    index = {}
    for v in data:
        categories.append(v["title"])
    for i in categories:
        url3 = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=categorymembers&cmlimit=max&cmtitle=" \
               + i + "&cmtype=page"
        response = rq.get(url3).json()
        subpages = response["query"]["categorymembers"]
        l = []
        for names in subpages:
            l.append(names["title"])
        dic[i] = l

    url4 = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srwhat=text&srlimit=max&srprop=" \
           "wordcount&srsearch=" + query
    response = rq.get(url4).json()
    data = response["query"]["search"]

    for p in data:
        pagescon.append(p["title"])

    for i in categories:
        index[i] = 0

    for i in categories:
        index[i] = len(set(dic[i]).intersection(pagescon))
        if len(dic[i]) != 0:
            index[i] = float(index[i]) / len(dic[i])
        else:
            index[i] = 0
    j = []
    final_categories = []
    for i in index:
        j.append(index[i])
    j.sort(reverse=True)
    count = 0
    for x in range(len(index)):
        if count is 3:
            break
        count = count + 1
        for y in index:
            if j[x] is index[y]:
                final_categories.append(y)
    return final_categories


def category_link_builder(category):
    """
    this function is mapped and multithreaded to run and return list of subcategories
    :param category: each
    :return:
    """
    dummy = 0
    find = ""
    for find in search(category + " wikipedia", num=1, stop=1):
        dummy = dummy + 1
        break
    return find


def google_searcher(query):
    """
    This function performs the initial google search to ascertain whether wikipedia page exists
    :param query: key + ' ' + context from user input
    :return: found: url substring to be appended in other functions
    """
    global findings
    findings = ""
    for findings in search(query + " wikipedia", num=1, stop=1):  # for loop to scrape desired wikipedia url
        print(findings)
        break
    if 'wikipedia' not in findings or findings == "":
        print("Wikipedia page does not exist")
        raise SystemExit
    findings = findings + ' '
    found = findings[findings.rfind('/') + 1:]
    return found


def calculate_parallel(category_list, threads=8):
    """

    :param category_list:
    :param threads:
    :return:
    """
    pool = ThreadPool(threads)
    results = pool.map(category_link_builder, category_list)
    pool.close()
    pool.join()
    return results


def url_builder(found, ID, query):
    """

    :param found:
    :param ID:
    :param query:
    :return:
    """
    if ID is 1:
        found = found[found.rfind('/') + 1:]
    category_list = wikipedia_searcher(found, query)
    category_list_url = calculate_parallel(category_list, 16)
    category_dict = {}
    keys = range(len(category_list))
    for x in keys:
        category_list[x] = category_list[x][category_list[x].find(':') + 1:]
        category_dict[category_list[x]] = category_list_url[x]
    json_string = json.dumps(category_dict)
    print(json.dumps(json_string, indent=2, sort_keys=True))
    return json_string
