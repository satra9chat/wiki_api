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
    This function performs web-scraping on wikipedia. It finds the subcategories of the requested category by the user
    :param title: key + context inputted by user
    :param query: key + context inputted by user
    :return: sorted list of top 3 relevant subcategories
    """
    url1 = "http://en.wikipedia.org/w/api.php?action=parse&format=json&page="
    url1 = url1 + title  # getting json object data of the wikipedia page found
    response = rq.get(url1)
    data = response.json()
    pageid = str(data["parse"]["pageid"])  # searching by page id in json object
    url2 = "http://en.wikipedia.org/w/api.php?action=query&format=json&prop=categories&clshow=!hidden&" \
           "cllimit=max&titles="
    url2 = url2 + title  # getting the categories of the desired wikipedia page
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

    for i in categories:  # assigning a value to each category to help rank their relevance
        index[i] = len(set(dic[i]).intersection(pagescon))
        if len(dic[i]) != 0:
            index[i] = float(index[i]) / len(dic[i])
        else:
            index[i] = 0
    j = []
    final_categories = []
    for i in index:  # sorting the assigned category values in descending order
        j.append(index[i])
    j.sort(reverse=True)
    count = 0
    for x in range(len(index)):  # extracting the top 3 categories with highest relevance and returning them
                                                                                            #  to the calling function
        if count is 3:
            break
        count = count + 1
        for y in index:
            if j[x] is index[y]:
                final_categories.append(y)
    return final_categories


def category_link_builder(category):
    """
    This function is mapped and multi-threaded to run and return list of subcategories urls
    :param category: each subcategory as a string
    :return: url of each subcategory
    """
    dummy = 0
    find = ""
    for find in search(category + " wikipedia", num=1, stop=1):  # finding required subcategories
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
        """
            This if construct takes care of 2 potential exceptions:
            a) if a wikipedia page is not found
            b) if no web page exists
        """
        print("Wikipedia page does not exist")
        raise SystemExit
    findings = findings + ' '
    found = findings[findings.rfind('/') + 1:]  # extracting the required keyword at the end of scraped url
    return found


def calculate_parallel(category_list, threads=8):
    """
    This function performs the multi-threading task by creating threads and automatically relegating tasks to the
                                                    threads
    :param category_list: list of subcategories which are passed to category_link_builder(param)
    :param threads: Number of threads to be used. This value is to be changed depending upon number of cores on backend
                                            system
    :return: list of urls of subcategories
    """
    pool = ThreadPool(threads)  # creating specified number of threads
    results = pool.map(category_link_builder, category_list)  # mapping category_link_builder(params)
    pool.close()  # stopping parallel threads
    pool.join()  # reverting back to main thread
    return results


def url_builder(found, ID, query):
    """
    This function builds the json object of subcategories and their urls to be returned to the API caller
    :param found: found contains the key + context pair or subcategory name (depending on the type of API call)
    :param ID: ID tag to differentiate between API call. Use "1" to find roots of subcategory. Use "2" to find roots of
                    user key + context pair
    :param query: contains key + context pair
    :return: json object containing a dictionary of subcategories and their associated urls
    """
    if ID is 1:
        found = found[found.rfind('/') + 1:]  # extracting subcategory name from url
    category_list = wikipedia_searcher(found, query)  # function call
    category_list_url = calculate_parallel(category_list, 16)  # function call
    category_dict = {}
    keys = range(len(category_list))
    for x in keys:
        category_list[x] = category_list[x][category_list[x].find(':') + 1:]
        category_dict[category_list[x]] = category_list_url[x]
    json_string = json.dumps(category_dict)
    print(json.dumps(json_string, indent=2, sort_keys=True))  # building json object
    return json_string
