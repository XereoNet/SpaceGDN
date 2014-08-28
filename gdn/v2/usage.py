from ..mongo import db
from ..app import app
import datetime


class Usage():
    def process(self, request):
        base_dict = {'ip': request.remote_addr}

        record = db.usage.find_one(base_dict)
        if not record:
            record = base_dict

        record['agent'] = request.user_agent.string
        record['total_requests'] = record.setdefault('total_requests', 0) + 1

        result = True

        if app.config['RATE_LIMIT'] != False:
            result = self.run_limits(record)

        db.usage.save(record)
        return result

    def run_limits(self, record):

        limit, bucket = app.config['RATE_LIMIT']
        now = datetime.datetime.now()
        delta = limit * (now - record.setdefault('last_request', now)).total_seconds() / (bucket * 60)

        record['request_limit'] = max(record.setdefault('request_limit', 0) - delta, 0) + 1
        record['last_request'] = now
        print(record)

        return record['request_limit'] < limit

    def show_usage(self):
        return db.usage.find()