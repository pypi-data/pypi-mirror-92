from . import work
import threading
import time
from datetime import datetime

from rq import Queue
from bos_incidents import factory

from . import INCIDENT_CALLS
from .log import log
from .config import loadConfig
from .redis_con import get_redis

config = loadConfig()


def check_scheduled(
    storage=None, func_callback=None, proposer=None, approver=None
):  # pragma: no cover
    """
    """
    log.info(
        "Scheduler checking incidents database ... "
        "(approver: {}/ proposer: {})".format(approver, proposer)
    )

    # Invident Storage
    if not storage:
        storage = factory.get_incident_storage()

    if not proposer:
        proposer = config.get("BOOKIE_PROPOSER")
    if not approver:
        approver = config.get("BOOKIE_APPROVER")

    push_to_queue = []

    for call in INCIDENT_CALLS:
        log.info("- querying call {}".format(call))

        events = []

        # midway is the status of the incidents which are terminated intentionally as creating bms took time.
        for status_name in ["midway"]:
            for event in storage.get_events_by_call_status(
                call=call, status_name=status_name
            ):
                events.append(event)

        for status_name in ["postponed", "unhandled exception, retrying soon"]:
            for event in storage.get_events_by_call_status(
                call=call,
                status_name=status_name,
                status_expired_before=datetime.utcnow(),
            ):
                events.append(event)

        for status_name in ["connection lost", "unknown"]:
            for event in storage.get_events_by_call_status(
                call=call, status_name=status_name
            ):
                events.append(event)

        ids = list()
        log.info("Scheduler retriggering " + str(len(events)) + " incident ...")
        for event in events:
            for incidentid in event.get(call, {}).get("incidents", []):
                incident = storage.resolve_to_incident(incidentid)
                if func_callback:
                    push_to_queue.append(incident)
                    # it is enough to trigger one incident, worker will check the whole call
                    break

    # Flask queue
    q = Queue(connection=get_redis())

    # If push_to_queue has events, then empty queue and fill it again with push_to_queue
    # This approach ensures that events which are on the chain but not all bms are created shall be processed first.
    if len(push_to_queue) > 0:
        q.empty()
        for incident in push_to_queue:
            job = q.enqueue(
                func_callback,
                args=(incident,),
                kwargs=dict(proposer=proposer, approver=approver),
            )
            ids.append(job.id)

    return ids


class PeriodicExecutor(threading.Thread):  # pragma: no cover
    """ Periodically execute a task
    """

    def __init__(self, sleep, func, *args, **kwargs):

        """ execute func(params) every 'sleep' seconds """
        self.func = func
        self.sleep = sleep
        self.args = args
        self.kwargs = kwargs
        threading.Thread.__init__(self, name="PeriodicExecutor")
        self.setDaemon(True)

    def run(self):
        while True:
            try:
                self.func(*self.args, **self.kwargs)
                time.sleep(self.sleep)
            except Exception as e:
                log.error(str(e))
                time.sleep(self.sleep)


def scheduler(delay=None, proposer=None, approver=None):  # pragma: no cover
    """
    """

    if not delay:
        delay = config["scheduler"]["interval"]

    if not proposer:
        proposer = config.get("BOOKIE_PROPOSER")
    if not approver:
        approver = config.get("BOOKIE_APPROVER")

    check_scheduled(
        storage=None, func_callback=work.process, proposer=proposer, approver=approver
    )

    PeriodicExecutor(
        delay,
        check_scheduled,
        storage=None,
        func_callback=work.process,
        proposer=proposer,
        approver=approver,
    ).run()
