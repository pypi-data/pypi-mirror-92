from celery import shared_task, current_task, group, chord, chain
from SPARQLWrapper import SPARQLWrapper, JSON
import pymongo
import datetime
from lxml import html
import requests
import time
import random
import os

from django.conf import settings


@shared_task(time_limit=500)
def create_mongo_entries(entries, gnd, name, scrape_id, *args, kind="obv", **kwargs):
    if isinstance(entries, dict):
        entries = [entries]
    if len(entries) == 0:
        return f"no records found {gnd}"
    per = {"gnd": gnd, "name": name}
    per_res = db.person.find_one({"gnd": gnd})
    if per_res is None:
        per_id = db.person.insert_one(per).inserted_id
    else:
        per_id = per_res["_id"]
    entries_fin = []
    for e in entries:
        e["person_id"] = per_id
        e["scrape_id"] = scrape_id
        e["_scrape_time"] = datetime.datetime.now()
        entries_fin.append(e)
    getattr(db, f"scrapes_{kind}").insert_many(entries_fin)

    return f"created mongo entries for {kind}/{name}"


@shared_task(
    time_limit=1000, queue="limited_queue", routing_key="limited_queue.get_obv"
)
def get_obv_records(gnd, name, scrape_id, *args, limit=50, **kwargs):
    print(f"searching obv: {gnd}")
    token = requests.get(
        "https://search.obvsg.at/primo_library/libweb/webservices/rest/v1/guestJwt/OBV?isGuest=true&lang=de_DE&targetUrl=https%3A%2F%2Fsearch.obvsg.at%2Fprimo-explore%2Fsearch%3Fvid%3DOBV&viewId=OBV"
    ).json()

    url = "https://search.obvsg.at/primo_library/libweb/webservices/rest/primo-explore/v1/pnxs"

    querystring = {
        "blendFacetsSeparately": "false",
        "getMore": "0",
        "inst": "OBV",
        "lang": "de_DE",
        "limit": limit,
        "mode": "advanced",
        "newspapersActive": "false",
        "newspapersSearch": "false",
        "offset": "0",
        "pcAvailability": "false",
        "q": f"any,contains,{gnd},AND",
        "qExclude": "",
        "qInclude": "",
        "refEntryActive": "false",
        "rtaLinks": "false",
        "scope": "OBV_Gesamt",
        "skipDelivery": "Y",
        "sort": "rank",
        "tab": "default_tab",
        "vid": "OBV",
    }
    headers = {"authorization": f"Bearer {token}"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        res = response.json()
        fin = []
        for r in res["docs"]:
            fin.append(r["pnx"]["display"])
        res_nb = int(res["info"]["total"])
        pages = res_nb / limit
        if pages < 1:
            pages = 1
        pg = 2
        while pg <= pages:
            querystring["offset"] = limit * (pg - 1)
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.status_code == 200:
                res = response.json()
                for r in res["docs"]:
                    fin.append(r["pnx"]["display"])
            pg += 1
            time.sleep(random.randrange(2, 5))
        create_mongo_entries.delay(fin, gnd, name, scrape_id)
    time.sleep(random.randrange(2, 8))

    return f"obv resolved for {gnd}"


@shared_task(time_limit=1000)
def get_wikipedia_entry(url, gnd, name, scrape_id, *args, **kwargs):
    url_version_hist = f"https://de.wikipedia.org/w/index.php?title={url.split('/')[-1]}&offset=&limit=500&action=history"
    vers_hist_page = requests.get(url_version_hist)
    tree_vers_hist = html.fromstring(vers_hist_page.content)
    vers_hist_entries = tree_vers_hist.xpath('//*[@id="pagehistory"]/li')
    count_vers = len(vers_hist_entries)
    count_editors = [
        x.xpath("./span[1]/span[2]/a/bdi/text()")[0] for x in vers_hist_entries
    ]
    count_editors = len(list(dict.fromkeys(count_editors)))
    next_link = tree_vers_hist.xpath('//*[@id="mw-content-text"]/a[@rel="next"]')
    print(next_link)
    while len(next_link) == 2:
        vers_hist_page = requests.get(
            "https://de.wikipedia.org" + next_link[0].get("href")
        )
        print(vers_hist_page)
        tree_vers_hist = html.fromstring(vers_hist_page.content)
        vers_hist_entries = tree_vers_hist.xpath('//*[@id="pagehistory"]/li')
        count_vers += len(vers_hist_entries)
        count_editors_1 = [
            x.xpath("./span[1]/span[2]/a/bdi/text()")[0] for x in vers_hist_entries
        ]
        count_editors += len(list(dict.fromkeys(count_editors_1)))
        next_link = tree_vers_hist.xpath('//*[@id="mw-content-text"]/a[@rel="next"]')
        print(next_link)
    print(count_vers)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    txt = tree.xpath('.//div[@class="mw-parser-output"]')[0].text_content()
    fin = {"edits_count": count_vers, "number_of_editors": count_editors, "txt": txt}
    create_mongo_entries.delay(fin, gnd, name, scrape_id, kind="wikipedia")

    return f"wikipedia resolved for {url}"


@shared_task(time_limit=1000)
def get_wikidata_records(gnd, name, scrape_id, *args, **kwargs):
    query = f"""
    SELECT ?p ?pLabel ?date_of_birth ?date_of_death ?ndb ?loc ?viaf ?wiki_de ?parlAT ?wienWiki (GROUP_CONCAT(?ausz2;SEPARATOR=", ") AS ?auszeichnungen)
        WHERE {{
          ?p wdt:P227 "{gnd}".
          OPTIONAL {{ ?p wdt:P7902 ?ndb }}
          OPTIONAL {{ ?p wdt:P244 ?loc }}
          OPTIONAL {{ ?p wdt:P2280 ?parlAT }}
          OPTIONAL {{ ?p wdt:P7842 ?wienWiki }}
          OPTIONAL {{ ?p wdt:P569 ?date_of_birth }}
          OPTIONAL {{ ?p wdt:P570 ?date_of_death }}
          OPTIONAL {{ ?p wdt:P214 ?viaf }}
          OPTIONAL {{ ?wiki_de schema:about ?p .
            ?wiki_de schema:inLanguage "de" .
            ?wiki_de schema:isPartOf <https://de.wikipedia.org/> }}
          OPTIONAL {{ ?p wdt:P166 ?ausz2 }}
             SERVICE wikibase:label {{
             bd:serviceParam wikibase:language "[AUTO_LANGUAGE], de" .
           }}
          }}
        GROUP BY ?p ?pLabel ?date_of_birth ?date_of_death ?ndb ?loc ?viaf ?wiki_de ?parlAT ?wienWiki
    """
    sparqlwd = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparqlwd.setQuery(query)
    sparqlwd.setReturnFormat(JSON)
    results = sparqlwd.query().convert()
    fin = dict()
    if len(results["results"]["bindings"]) > 0:
        for k, v in results["results"]["bindings"][0].items():
            fin[k] = v["value"]
        create_mongo_entries.delay(fin, gnd, name, scrape_id, kind="wikidata")
        if "wiki_de" in fin.keys() and kwargs["include_wikipedia"]:
            get_wikipedia_entry.delay(fin["wiki_de"], gnd, name, scrape_id)
    return f"wikidata resolved for {gnd}"


default_scrapes = [get_wikidata_records, get_obv_records]


@shared_task(time_limit=2000)
def scrape(obj, scrapes=default_scrapes, wiki=True):
    ent = {
        "email": obj["email"],
        "started": datetime.datetime.now(),
        "celery_id": current_task.request.id,
    }
    print("testproint")
    scrape_id = str(db.scrape.insert_one(ent).inserted_id)
    attr = {"include_wikipedia": wiki}
    print(obj)
    res = group(
        scr.s(
            entry["gnd"],
            f"{entry['lastName']}, {entry['firstName']}",
            scrape_id,
            include_wikipedia=True,
        )
        for entry in obj["lemmas"]
        for scr in scrapes
    )()
    print(res)
    return f"started job for {obj['email']}"
