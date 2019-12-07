from flask_restplus import Resource, fields, reqparse, Namespace
from app.util.contest_requests import get_contest, get_user_ranking
from .user import DAO
from dataclasses import asdict
import json

contest_ns = Namespace('contest', description='simple contest operations')

# questions = contest_ns.model(
#     'questions', {
#         'questions_num_score': fields.String(readonly=True),
#         'questions_id': fields.String(readonly=True)
#     })

# user_rank = contest_ns.model('user_rank', {
#     'rank': fields.Raw,
#     'submissions': fields.Raw
# })

contest = contest_ns.model(
    'contest', {
        'contest_num': fields.String(required=True),
        'start_time': fields.String(readonly=True),
        'participated_user_num': fields.Integer(readonly=True),
        'registered_user_num': fields.Integer(readonly=True),
        'questions': fields.Raw,
        'user_ranks': fields.List(fields.Raw),
        'cache': fields.Boolean(required=False)
    })

user_post_parser = reqparse.RequestParser(bundle_errors=True)
user_post_parser.add_argument('username',
                              type=str,
                              help='must be a valid lc username')

# simple dict as cache
CONTEST_CACHE = {}


@contest_ns.route('/<string:contest_num>')
class ContestInfo(Resource):
    @contest_ns.doc(
        'get_contest',
        description=
        'get contest overview info based on contest_num given:\nweekly-contest-xx or biweekly-contest-xx'
    )
    @contest_ns.marshal_list_with(contest)
    def get(self, contest_num):
        '''get contest overview info'''
        if contest_num not in CONTEST_CACHE:
            contest = get_contest(contest_num)
            # print(json.dumps(asdict(contest), indent=4))
            CONTEST_CACHE[contest_num] = asdict(contest)
        return CONTEST_CACHE[contest_num]


@contest_ns.route('/ranking/<string:contest_num>')
class ContestUserRanks(Resource):
    @contest_ns.doc('get_contest_user_ranks')
    @contest_ns.marshal_list_with(contest)
    def get(self, contest_num):
        '''get contest ranking'''
        if contest_num not in CONTEST_CACHE:
            contest = get_contest(contest_num)
            # print(json.dumps(asdict(contest), indent=4))
            CONTEST_CACHE[contest_num] = asdict(contest)

        user_names = {user['username'] for user in DAO.users}

        if not CONTEST_CACHE[contest_num]['user_ranks'] or not {
                user_rank['rank']['username']
                for user_rank in CONTEST_CACHE[contest_num]['user_ranks']
        } <= user_names:
            total_pages = CONTEST_CACHE[contest_num][
                'registered_user_num'] // 25
            user_ranks = get_user_ranking(contest_num, total_pages, user_names)
            sorted(user_ranks, key=lambda x: x['rank']['rank'])
            CONTEST_CACHE[contest_num]['user_ranks'] = user_ranks
        return CONTEST_CACHE[contest_num]