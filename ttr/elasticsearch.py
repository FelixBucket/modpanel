from django.conf import settings
from datetime import datetime
import requests
import json

class ElasticSearch:

    def __init__(self, kibana=settings.KIBANA_ROOT, username=settings.KIBANA_USERNAME, password=settings.KIBANA_PASSWORD):
        # To access the API we need to specify a date
        self.endpoint = kibana + "%(date)s/_search"

        # We need to authenticate ourselves otherwise, rip
        self.username = username
        self.password = password

    """
    Searche's kibana for any given type.

    Two values are required: date and search term

    @param: date is in the format of 'ttr-YYYY.MM.DD'
    @param: term can be anything you want, format it the same way
            you would in kibana
    @param: amount is the number of objects you want returned in the response
    @param: fromDate: The time you want to start reading logs from
    @param: toDate: The time you want to stop reading logs from

    The default for fromDate and toDate is 1 day ago to now

    Example call:
    logs = ElasticSearch()
    logs.search('ttr-2014.08.20', "type:(\"chat-said\" \"whisper-said\")", 20)
    This would return 20 logs total for both chat-said and whisper-said in
    the same response
    """
    def search(self, date, term, amount=100, fromDate=datetime.utcnow() - timedelta(days=1), toDate=datetime.utcnow()):
        # Convert the date to a format elastic search likes
        # time4hax
        fromDate = fromDate.isoformat().split('.')[0]
        toDate = toDate.isoformat().split('.')[0]

        # Give the endpoint the required date
        endpoint = self.endpoint % {'date': date}

        # Specify what we want... elasticsearch pls...
        payload = {
                    "query": {
                        "filtered": {
                            "query": {
                                "bool": {
                                    "should": [
                                        {
                                            "query_string": {
                                                "query": term # I only care about this
                                            }
                                        }
                                    ]
                                }
                            },
                            "filter": {
                                "bool": {
                                    "must": [
                                        {
                                            "range": {
                                                "@timestamp": {
                                                    "from": fromDate,
                                                    "to": toDate
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    "highlight": {
                        "fields": {},
                        "fragment_size": 2147483647,
                        "pre_tags": [
                            "@start-highlight@"
                        ],
                        "post_tags": [
                            "@end-highlight@"
                        ]
                    },
                    "size": amount, # And this
                    "sort": [ # And lets not forget about sorting
                        {
                            "@timestamp": {
                                "order": "desc"
                            }
                        },
                        {
                            "@timestamp": {
                                "order": "desc"
                            }
                        },
                        {
                            "@timestamp": "desc"
                        }
                    ]
                }

        # Fire off the request. We use HTTP Basic Auth for kibana so lets pass in those
        # credients with the handy-dandy helper auth parameter
        request = requests.post(endpoint, auth=(self.username, self.password), data=json.dumps(payload))

        # We are all set, lets give the data back
        return request.json()
