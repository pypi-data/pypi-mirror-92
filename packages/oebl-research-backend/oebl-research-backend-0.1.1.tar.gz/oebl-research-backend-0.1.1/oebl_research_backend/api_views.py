from rest_framework.views import APIView
from .tasks import scrape
from rest_framework.response import Response
from .tasks import db
from bson.objectid import ObjectId
from bson.json_util import dumps


class LemmaResearchView(APIView):
    """APIView to process scraping requests

    Args:
        GenericAPIView ([type]): [description]
    """

    def post(self, request):
        job_id = scrape.delay(request.data)
        return Response({"success": job_id.id})

    def get(self, request, crawlerid):
        scrape_id = db.scrape.find_one({"celery_id": crawlerid})
        wikidata = db.scrapes_wikidata.find({"scrape_id": str(scrape_id["_id"])})
        wikipedia = db.scrapes_wikipedia.find({"scrape_id": str(scrape_id["_id"])})
        res = dict()
        for ent in wikidata:
            person = db.person.find_one({"_id": ent["person_id"]})
            res[str(ent["person_id"])] = {
                "gnd": person.get("gnd"),
                "query_name": person.get("name"),
                "viaf": ent.get("viaf", None),
                "loc": ent.get("loc", None),
                "wien wiki": ent.get("wienWiki", None),
                "label": ent.get("pLabel", None),
                "geburtstag": ent.get("date_of_birth", None),
                "todestag": ent.get("date_of_death", None),
            }
            wikipedia = db.scrapes_wikipedia.find_one(
                {"scrape_id": str(scrape_id["_id"]), "person_id": ent["person_id"]}
            )
            if wikipedia:
                res[str(ent["person_id"])]["wikipedia_edits"] = wikipedia["edits_count"]
                res[str(ent["person_id"])]["wikipedia_distinct_editors"] = wikipedia[
                    "number_of_editors"
                ]
                res[str(ent["person_id"])]["wikipedia_txt"] = wikipedia["txt"].strip()

        obv = db.scrapes_obv.find({"scrape_id": str(scrape_id["_id"])})
        for ent in obv:
            if str(ent["person_id"]) not in res.keys():
                res[str(ent["person_id"])] = dict()
            if "obv_entries" not in res[str(ent["person_id"])]:
                res[str(ent["person_id"])]["obv_entries"] = []
            res[str(ent["person_id"])]["obv_entries"].append(str(ent["_id"]))
        for pers in res.keys():
            if res[pers].get("obv_entries"):
                res[pers]["obv_count"] = len(res[pers]["obv_entries"])
        resfin = [res[key] for key in res.keys()]

        return Response({"count": len(resfin), "results": resfin})
