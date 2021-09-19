import sys
import requests
from google.cloud import pubsub_v1
from concurrent import futures
from typing import Callable
from time import sleep


class GetDataToPub:
    publish_futures = []

    def __init__(self):
        self.base_url = 'http://data.fixer.io/api/latest'
        self.project_id = "capstone1-project-326220"
        self.topic_id = "currency"
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    #get the data from API
    def get_currency_rate(self, currency):
        query = self.base_url + '?access_key=7d30f923cde87261ddc8b8c2acfa5bb4&symbols=%s' % (currency)
        try:
            response = requests.get(query)
            # print("[%s] %s" % (response.status_code, response.url))
            # print(response.status_code)
            if response.status_code != 200:
                response = 'N/A'
                return response
            else:
                #convert it to Json
                rates = response.json()
                #print(rates)
                rate_in_currency = rates
                return rate_in_currency
        except requests.ConnectionError as error:
            print(error)
            sys.exit(1)

    def get_callback(self, publish_future: pubsub_v1.publisher.futures.Future, data: str) -> Callable[
        [pubsub_v1.publisher.futures.Future], None]:
        def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
            try:
                # Wait 60 seconds for the publish call to succeed.
                print(publish_future.result(timeout=60))
            except futures.TimeoutError:
                print(f"Publishing {data} timed out.")

        return callback

    def publish_to_topic(self, i):
        data = str(i)
        # When you publish a message, the client returns a future.
        publish_future = self.publisher.publish(self.topic_path, data.encode("utf-8"))
        # Non-blocking. Publish failures are handled in the callback function.
        publish_future.add_done_callback(self.get_callback(publish_future, data))
        self.publish_futures.append(publish_future)


def getAndPublish():

    
    obj = GetDataToPub()
    result = []
    #loop over the currencies which you are interested in.
    for currency in ['GBP', 'USD', 'EUR']:
        rate = obj.get_currency_rate(currency)
        result.append(rate)
        sleep(5)

    #print(result)
    obj.publish_to_topic(result)

    # Wait for all the publish futures to resolve before exiting.
    futures.wait(obj.publish_futures, return_when=futures.ALL_COMPLETED)
    print(f"Published message successfully.")
