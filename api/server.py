import csv
import json
from os import path
from flask import Flask
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int, required=False,
                    location='args')
parser.add_argument('offset', type=int, required=False, location='args')


def get_path(filename):
    return 'csv/' + filename + '.csv'


def csv_exists(filename):
    return path.isfile(get_path(filename))


def read_csv(filename, limit=-1, offset=0):
    limit = limit or -1
    offset = offset or 0
    data = []

    with open(get_path(filename)) as csvfile:
        reader = csv.DictReader(csvfile)

        for idx, row in enumerate(reader):
            if idx < offset:
                continue
            if len(data) == limit:
                break

            for k, v in row.items():
                try:
                    row[k] = json.loads(v)
                except:
                    continue

            data.append(row)

        return data


class CsvData(Resource):
    def get(self, filename):
        if not csv_exists(filename):
            abort(404, message='The requested resource does not exist!')

        args = parser.parse_args()
        return read_csv(filename, **args)


api.add_resource(CsvData, '/<filename>')

if __name__ == '__main__':
    app.run(debug=True)
