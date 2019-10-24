import calendar, time, logging, os, json, sys
from match_details_fetcher import getMatchDetails
from constants import LOG_ROOT, NUM_MESSAGES, PROJECT_ID, SUBSCRIPTION_NAME

from google.cloud import pubsub_v1

# System Argument ProcesName is needed - Name of process for provenance
PROCESS_NAME = sys.argv[1]
# System Argument Key is needed - To decide which key to use
KEY = sys.argv[2]

logging.basicConfig(filename=LOG_ROOT + 'detail_fetcher.log', level=logging.DEBUG, format='%(levelname)s:%(asctime)s %(message)s')
logging.info(f'Fetching unique match details')

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)

while True:
    try:
        response = subscriber.pull(subscription_path, max_messages=NUM_MESSAGES)

        for message in response.received_messages:
            logging.debug(f'Calling matchDetails with matchID: {message.message.data}')
            getMatchDetails(message.message.data.decode("utf-8") , PROCESS_NAME, KEY)

            ack_list = []
            ack_list.append(message.ack_id)
            subscriber.acknowledge(subscription_path, ack_list)
            logging.info(f'Acknowledged: {message.ack_id}')

            time.sleep(1)

    except Exception as e:
        logging.error('Exception: ', e)