import logging
import urllib.parse
import time
from typing import TypeVar
from getpass import getpass

import requests

Task = TypeVar('Task')

LOGGER = logging.getLogger(__name__)
SESSION = None

DEV = True
UNSAFE = DEV

BASE_URL = 'https://cog-uk-dev.shef.ac.uk/api/v0/' if DEV else 'https://cog-uk.shef.ac.uk/api/v0/'

POLL_INTERVAL = 10.0


def call(endpoint: str, **kwargs):
    """
    Call API endpoint and return response data (maybe dict, list, number or string)
    """
    global SESSION

    if not SESSION:
        SESSION = get_session()

    url = urllib.parse.urljoin(BASE_URL, endpoint)

    response = SESSION.get(url, **kwargs)
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        LOGGER.error(exc)
        LOGGER.error(exc.response.text)
        raise

    return response.json()


class Task:
    """
    Celery task
    """

    def __init__(self, task_id: str, status: str = None, failed: bool = False, ready: bool = False,
                 successful: bool = False, traceback: str = None, name: str = None):
        self.id = task_id
        self.status = status
        self.failed = failed
        self.ready = ready
        self.successful = successful
        self.traceback = traceback
        self.name = name

    class State:
        """
        Celery task states
        https://docs.celeryproject.org/en/stable/reference/celery.states.html
        """
        FAILURE = 'FAILURE'
        PENDING = 'PENDING'
        RECEIVED = 'RECEIVED'
        RETRY = 'RETRY'
        SUCCESS = 'SUCCESS'
        STARTED = 'STARTED'
        REVOKED = 'REVOKED'

    @classmethod
    def call(cls, task_name: str, **kwargs) -> Task:
        LOGGER.info("%s(%s)", task_name, ', '.join(("{}={}".format(k, v) for k, v in kwargs.items())))
        task = call("task/run/{}".format(task_name), json=kwargs)
        LOGGER.info(task)
        return Task(task_id=task['id'], status=task['status'])

    def get(self, **kwargs):
        """
        Retrieve task result data
        """
        return call(f"task/{self.id}/get", **kwargs)

    def update(self):
        """
        Refresh task status
        """
        result = call(f'task/{self.id}')
        for key, value in result.items():
            setattr(self, key, value)
        LOGGER.debug(self.__dict__)

    @property
    def revoked(self) -> bool:
        return self.status == Task.State.REVOKED

    def fail(self):
        for key, value in self.__dict__.items():
            LOGGER.error("%s=%s", key, value)
        raise RuntimeError(f"Task id {self.id} failed")

    def poll(self, poll_interval: float = 10.):
        """
        Loop until task is complete (or fails)
        """
        while True:

            # If ready, retrieve result data
            if self.successful:
                return self.get()
            elif self.failed:
                self.fail()
            elif self.revoked:
                return

            # Poll for task status
            self.update()

            time.sleep(poll_interval)


def get_session() -> requests.Session:
    """
    Initialise HTTP transport
    """
    session = requests.Session()
    session.headers['token'] = getpass('Enter token:')

    if UNSAFE:
        # Don't check SSL certificates
        session.verify = False

    return session


def run_task(task_name: str, poll_interval: float = POLL_INTERVAL, **kwargs):
    """
    Run a task on the worker synchronously (wait until the result is returned)

    @param task_name: Module name of the task e.g. 'worker.tasks.get_config'
    @param kwargs: The keyword arguments for the task
    @param poll_interval: How frequently to check the task status
    @return: The task info
    """

    task = Task.call(task_name, **kwargs)

    return task.poll(poll_interval)
