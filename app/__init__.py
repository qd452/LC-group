from flask import Flask
from flask_restplus import Api, Resource, fields, reqparse
from werkzeug.contrib.fixers import ProxyFix
from app.util.contest_requests import get_user_info, get_user_info_parallel

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app,
    version='1.0',
    title='LC Contest API',
    description='A simple LC contest API',
)

user_ns = api.namespace('user', description='simple operations')

user = api.model(
    'User', {
        'username': fields.String(readonly=True),
        'rating': fields.String(required=False),
        'solved_questions': fields.String(required=False),
        'cache': fields.Boolean(required=False)
    })

user_post_parser = reqparse.RequestParser(bundle_errors=True)
user_post_parser.add_argument('username',
                              type=str,
                              help='must be a valid lc username')


class UserDAO(object):
    def __init__(self):
        self.users = []

    def get(self, username: str) -> dict:
        for user in self.users:
            if user['username'] == username:
                return user
        api.abort(404, "User {} doesn't exist".format(username))

    def create(self, username: str) -> dict:
        user = {
            'username': username,
            'rating': None,
            'solved_questions': None,
            'cache': False
        }
        self.users.append(user)
        return user

    def update(self, username, rating=None, solved_questions=None,
               cache=False) -> dict:
        user = self.get(username)
        user['rating'] = rating
        user['solved_questions'] = solved_questions
        user['cache'] = cache
        return user

    def delete(self, username) -> None:
        user = self.get(username)
        self.users.remove(user)


DAO = UserDAO()
USERS = {
    'qd452', 'guoqiang2648', 'thread_start', 'liu_diansheng', 'sylyongli',
    'lijiang3800045', 'jessica_x_1028', 'lqianzhen', 'coffeebenzene',
    'gohuishan', 'M00nwell', 'pumbaa5', 'farmerboy'
}

for u in USERS:
    DAO.create(u)


@user_ns.route('/')
class UserList(Resource):
    '''Shows a list of all users, and lets you POST to add new users'''
    @user_ns.doc('list_users')
    @user_ns.marshal_list_with(user)
    def get(self):
        '''List all users'''
        user_no_cache = [
            user['username'] for user in DAO.users if not user['cache']
        ]
        user_info_dct = get_user_info_parallel(user_no_cache)
        for user in DAO.users:
            un = user['username']
            if un in user_info_dct:
                user['rating'], user['solved_questions'] = user_info_dct[un]
                user['cache'] = True

        return DAO.users

    @user_ns.doc('add_user')
    @user_ns.expect(user_post_parser)
    @user_ns.marshal_with(user, code=201)
    def post(self):
        '''Create a new User'''
        args = user_post_parser.parse_args()
        return DAO.create(args['username']), 201


@user_ns.route('/<string:username>')
@user_ns.response(404, 'User not found')
@user_ns.param('id', 'The task identifier')
class User(Resource):
    '''Show a single todo item and lets you delete them'''
    @user_ns.doc('get_user')
    @user_ns.marshal_with(user)
    def get(self, username):
        '''Fetch a given resource'''
        user = DAO.get(username)
        if not user['cache']:
            user['rating'], user['solved_questions'] = get_user_info(
                user['username'])
            user['cache'] = True
        return user

    @user_ns.doc('delete_user')
    @user_ns.response(204, 'User deleted')
    def delete(self, username):
        '''Delete a user given its username'''
        DAO.delete(username)
        return '', 204

    @user_ns.expect(user)
    @user_ns.marshal_with(user)
    def put(self, username):
        '''Update a username given its identifier'''
        pl = api.payload
        return DAO.update(username, **pl)