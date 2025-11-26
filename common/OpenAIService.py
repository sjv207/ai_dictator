import threading
from time import sleep
from common.common_data import BOT_MODEL, ERROR, SUCCESS
from openai import OpenAI
import logging
from threading import Thread, active_count
from queue import Queue, Empty

logger = logging.getLogger(__name__)
# This is the queue that the main otree process will use to post requests to the AI service thread
ai_queue = Queue()
# This is the queue that the AI service thread will use to post results back to the main otree process
otree_queue = Queue()

# Flag to stop the AI service thread
_stop_flag = threading.Event()

DEBUGGING = False

# This is the main loop running in the background thread that handles AI requests


def ai_service():
    logger.info(f"Starting AI Service with Bot: {BOT_MODEL}")

    while not _stop_flag.is_set():
        try:
            data = ai_queue.get(timeout=0.5)
        except Empty:
            # Don't care if there is no data to process, not an error condition
            continue
        if data is not None:
            fetch_thread = Thread(target=async_fetch_suggestion, args=(
                data['playerId'],
                data['index'],
                data['question'],
                data['timeout'],
                data['use_canned_responses']
            ), daemon=True)
            fetch_thread.start()
            # Don't wait for threads
            logger.info(
                f"Number of threads: {active_count()}, new thread: {fetch_thread.name}:{fetch_thread.native_id}")


# This method runs in a separate thread to avoid blocking the main ai_service loop
def async_fetch_suggestion(playerId: str, index: int, question: str, timeout: int, use_canned_responses: bool):
    my_id = threading.get_native_id()
    logger.info(f"PlayerId: {playerId}, Index: {index}, Question: {question}, Timeout: {timeout}, Use Canned Responses:"
                f" {use_canned_responses}")

    if use_canned_responses:
        logger.info(f"{my_id}: Using canned responses for player: {playerId}")
        status = SUCCESS
        answer = "£5 - This is a fair amount that balances generosity and self-interest."
        sleep(5)  # Simulate some delay

    else:
        status, answer = read_from_GTP(question, timeout)

    data = {'playerId': playerId, 'index': index, 'suggestion': answer, 'status': status}
    logger.info(f"Putting data on queue {data}")
    otree_queue.put(data)


# This method makes the actual call to the OpenAI GTP service
def read_from_GTP(question: str, timeout: int):
    client = OpenAI()

    status = SUCCESS

    try:
        response = client.chat.completions.create(
            model=BOT_MODEL,
            messages=[{"role": "user", "content": question}],
            r_timeout=timeout)
        logger.info(f"\n\nResponse:\n{response}\n\n")
        text = response['choices'][0]['message']['content']

    except Exception as e:
        msg = f"Call to AI Service failed: {e}, please try again"
        logger.error(f"Failed. {msg}")
        text = msg
        status = ERROR

    return status, text


# Start the AI service thread lazily
ai_thread = None


def _ensure_ai_thread_started():
    """Ensure the AI service thread is started (lazy initialization)"""
    global ai_thread
    if ai_thread is None or not ai_thread.is_alive():
        _stop_flag.clear()
        ai_thread = Thread(target=ai_service, daemon=True, name="AI-Service")
        ai_thread.start()
        sleep(0.1)  # Give thread a moment to initialize


# This method is called by the main otree process to request a suggestion idea from the AI service
def get_new_idea(playerId: str, index: int, question: str, timeout: int, use_canned_responses: bool):
    _ensure_ai_thread_started()
    # Stuff this in the queue for the ai service thread to pick up
    data = {'playerId': playerId, 'index': index, 'question': question, 'timeout': timeout, 'use_canned_responses': use_canned_responses}
    # logger.info(f"Posting data to ai thread: {data}")
    ai_queue.put(data)


# This method is called by the main otree process to check for any returned suggestions
def get_queue_data():
    queue_data = dict()
    # Limit the number an individual player has to pull off the queue to 10, leave the rest for the next person
    for _ in range(11):
        try:
            data = otree_queue.get_nowait()
            playerId = data['playerId']
            if playerId not in queue_data:
                queue_data[playerId] = []
            queue_data[playerId].append(data)

        except Empty:
            # We are done, nothing left on queue
            break

    return queue_data
