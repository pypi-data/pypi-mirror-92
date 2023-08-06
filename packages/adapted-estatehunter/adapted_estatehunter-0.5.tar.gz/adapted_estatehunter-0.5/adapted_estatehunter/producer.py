import requests
import threading
import bugsnag


class _ThreadIT:
    def __init__(self, func, *args, **kwargs):
        self.name = func.__name__
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.job_result = None
        self.thread = self._start_thread()

    def _start_job(self, *args, **kwargs):
        self.job_result = self.func(*args, **kwargs)

    def _start_thread(self):
        thread = threading.Thread(target=self._start_job, args=self.args, kwargs=self.kwargs)
        thread.start()
        return thread

    def doing_work(self):
        return self.thread.is_alive()

    def result(self, timeout: int = None):
        self.thread.join(timeout=timeout)
        return self.job_result


class Producer:
    def __init__(self, api_url, namespace, token):
        self.api_url = api_url
        self.header = {'token': token}
        self.namespace = namespace

    @staticmethod
    def _get_topic(event):
        s = event.__class__.__name__
        return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')

    def callback(self, topic, payload):
        def wrapper(event):
            event.add_tab("CONSUMER", {"topic": topic, "data": payload, "namespace": self.namespace})
        return wrapper

    def _post_message(self, event):
        topic = self._get_topic(event)
        bugsnag.before_notify(self.callback(topic, event))
        requests.post(f"{self.api_url}/message/{self.namespace}/{topic}", headers=self.header, data=event.json())

    def send(self, event):
        _ThreadIT(self._post_message, event)
