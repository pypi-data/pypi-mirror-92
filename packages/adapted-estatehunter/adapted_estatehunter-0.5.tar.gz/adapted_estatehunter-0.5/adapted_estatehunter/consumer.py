import threading
import bugsnag
import pymongo
import requests


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


class Consumer:
    def __init__(self, db_uri, api_url, namespace, token):
        self.api_url = api_url
        self.header = {'token': token}
        self.db = self.database(db_uri)
        self.namespace = namespace

    @staticmethod
    def database(uri):
        client = pymongo.MongoClient(f"mongodb://{uri}", readPreference='secondary')
        mongodb = client["ADAPTED-MESSAGE-QUEUE"]
        db = mongodb["messages"]
        return db

    @staticmethod
    def _get_topic(event):
        s = event.__name__
        return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')

    def callback(self, topic, name, data):
        def wrapper(event):
            event.add_tab("CONSUMER", {"name": name, "topic": topic, "data": data, "namespace": self.namespace})
        return wrapper

    def _catchup(self, func, event, topic, name):
        data = self._get_messages(topic, name)
        while data:
            bugsnag.before_notify(self.callback(topic, name, data))
            new_data = event(**data['payload'])
            event._message = data
            func(new_data)
            self._acknowledge_message(data['_id'], name)
            data = self._get_messages(topic, name)

    def _get_messages(self, topic, name):
        response = requests.get(f"{self.api_url}/message/{self.namespace}/{topic}?consumer={name}", headers=self.header)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 204:
            return False

    def _acknowledge_message(self, message_id, name):
        return requests.patch(f"{self.api_url}/message/{message_id}?consumer={name}", headers=self.header).json()

    def _consume(self, function, event, name):
        topic = self._get_topic(event)
        self._catchup(function, event, topic, name)
        with self.db.watch([{'$match': {'operationType': 'insert'}}]) as stream:
            for insert_change in stream:
                if insert_change['fullDocument']['topic'] == topic and insert_change['fullDocument']['namespace'] == self.namespace:
                    data = self._get_messages(topic, name)
                    while data:
                        bugsnag.before_notify(self.callback(topic, name, data))
                        new_data = event(**data['payload'])
                        event._message = data
                        function(new_data)
                        self._acknowledge_message(str(data['_id']), name)
                        data = self._get_messages(topic, name)

    def consume(self, event, name, workers=1):
        def wrapper(func):
            for i in range(workers):
                _ThreadIT(self._consume, func, event, name)
            return func
        return wrapper
