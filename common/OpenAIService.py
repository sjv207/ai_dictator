import threading
from time import sleep
from common.common_data import BOT_MODEL, ERROR, SUCCESS
from openai import OpenAI
import logging
from multiprocessing import Process, Queue
from threading import Thread, active_count
from queue import Empty
import multiprocessing

# Set multiprocessing start method for macOS compatibility
try:
    multiprocessing.set_start_method('fork', force=True)
except RuntimeError:
    pass  # Start method already set

logger = logging.getLogger(__name__)
# This is the queue tha the main otree process will use to post requests to the AI service process
ai_queue = Queue()
# This is the queue that the AI service process will use to post results back to the main otree process
otree_queue = Queue()


DEBUGGING = False

# This is the main loop running in the child processes that handles AI requests


def ai_service(ai_queue):
    logger.info(f"Starting AI Service with Bot: {BOT_MODEL}")

    while True:
        try:
            data = ai_queue.get(timeout=0.5)
        except Empty:
            # Don't care if there is no data to process, not an error condition
            continue
        if data is not None:
            fetch_thread = Thread(target=async_fetch_suggestion, args=(
                data['playerId'],
                data['question'],
                data['timeout'],
            ))
            fetch_thread.start()
            # Don't wait for threads
            logger.info(
                f"Number of threads: {active_count()}, new thread: {fetch_thread.name}:{fetch_thread.native_id}")


# This method runs in a separate thread to avoid blocking the main ai_service loop
def async_fetch_suggestion(playerId: int, question: str, timeout: int):
    my_id = threading.get_native_id()

    status, answer = read_from_GTP(question, timeout)

    data = {'playerId': playerId, 'question': question, 'answer': answer, 'status': status}
    logger.info(f"{my_id}: Putting data on queue")
    otree_queue.put(data)


# This method makes the actual call to the OpenAI GTP service
def read_from_GTP(question: str, timeout: int):
    client = OpenAI()

    status = SUCCESS

    try:
        response = client.chat.completions.create(
            model=BOT_MODEL,
            messages=[{"role": "user", "content": question}],
            request_timeout=timeout)
        logger.info(f"\n\nResponse:\n{response}\n\n")
        text = response['choices'][0]['message']['content']

    except Exception as e:
        msg = f"Call to AI Service failed: {e}, please try again"
        logger.error(f"Failed. {msg}")
        text = msg
        status = ERROR

    return status, text


# Start the AI service process lazily
ai_process = None


def _ensure_ai_process_started():
    """Ensure the AI service process is started (lazy initialization)"""
    global ai_process
    if ai_process is None:
        ai_process = Process(target=ai_service, args=(ai_queue,))
        ai_process.start()
        sleep(0.5)  # Give process a moment to initialize


# This method is called by the main otree process to request a suggestion idea from the AI service
def get_new_idea(playerId: int, question: str, timeout: int):
    _ensure_ai_process_started()
    # Stuff this in the queue for the ai service process to pick up
    data = {'playerId': playerId, 'question': question, 'timeout': timeout}
    # logger.info(f"Posting data to ai process: {data}")
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
