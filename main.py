from lxml import html
from lxml import etree
import json;
import requests

def script_to_json(script):
    i = script.index("{")
    data = json.loads(script[i:len(script)-1])
    return data

def findEmail(tree):
    data = tree.xpath("(//script[contains(text(),'window.__PRELOADED_STATE__')])[1]")[0]
    data = script_to_json(data.text_content())
    email = data["businessProfile"]["contactInformation"]["emailAddress"]
    email = email.replace("!~xK_bL!", "")
    email = email.replace("__at__", "@")
    email = email.replace("__dot__", ".")
    return email

def findCompanies(tree):
    data = tree.xpath("(//script[@id='BbbDtmData'])[1]")[0]
    dataString = data.text_content()
    data = script_to_json(dataString)
    results = data["search"]['results']
    return results

def makeRequestAndGetTree(URL):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    r = requests.get(URL, headers=headers) 
    tree = html.fromstring(r.content)
    return tree

def queryByCategoryAndPageNumber(query, i): 
    URL = "https://www.bbb.org/search?find_country=USA&find_entity=50589-000&find_id=50589-000&find_text=" + query + "&find_type=Category&page=" + str(i) + "&sort=Distance"
    print(URL)
    tree = makeRequestAndGetTree(URL)
    results = findCompanies(tree)
    for company in results:
        page = "https://www.bbb.org/us/wa/battle-ground/profile/paintball-games/" + company["businessName"].replace(" ", "-") + "-" + company["bbbId"] + "-" + company["businessId"]
        email = findEmail(makeRequestAndGetTree(page))
        print(email)

def scrape(pageLimit):
    for p in range(1, 5):
        queryByCategoryAndPageNumber("Skateboards", p)

scrape(5)

# URL = "https://www.bbb.org/us/wa/battle-ground/profile/paintball-games/nw-ambush-paintball-llc-1296-22465230"
# r = requests.get(URL, headers=headers) 
# tree = html.fromstring(r.content)
# print(json.dumps(results, indent=2, sort_keys=True))
