# requests.py
from flask_restful import reqparse

class UserClickRequest:
    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('element_id', type=str, required=True, help='Element id is required')
        return parser

    @staticmethod
    def parse_args():
        return UserClickRequest.get_parser().parse_args()
