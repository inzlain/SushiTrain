from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected
from settings.authentication import create_user, verify_authentication
from settings.models import User


class SettingsView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        management = Sanic.get_app("Management")
        response = {'delivery_hostname': management.config['DELIVERY_HOSTNAME'],
                    'delivery_port': management.config['DELIVERY_PORT'],
                    'delivery_path': management.config['DELIVERY_PATH']}
        return json(response)


class UsersView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        users = await User.all().order_by('username').values('id',
                                                             'username',
                                                             'admin',
                                                             'created',
                                                             'last_successful_login',
                                                             'last_failed_login',
                                                             'failed_login_count')
        for user in users:
            if 'created' in user:
                if user['created'] is not None:
                    user['created'] = user['created'].isoformat()
            if 'last_successful_login' in user:
                if user['last_successful_login'] is not None:
                    user['last_successful_login'] = user['last_successful_login'].isoformat()
            if 'last_failed_login' in user:
                if user['last_failed_login'] is not None:
                    user['last_failed_login'] = user['last_failed_login'].isoformat()

        response = {'users': users}
        return json(response)

    async def post(self, request):
        action = 'validated'
        try:
            if request.json['username'] == '':
                response = {'error': 'Username cannot be blank', action: False}
                return json(response)
            if request.json['password'] == '':
                response = {'error': 'Password cannot be blank', action: False}
                return json(response)
            if await User.filter(username=request.json['username']).all().count() > 0:
                response = {'error': 'Username already exists', action: False}
                return json(response)

            action = 'created'
            new_user_id = await create_user(request.json['username'], request.json['password'])

        except Exception:
            response = {'error': 'Unknown error occurred while adding user', action: False}
            return json(response)

        response = {'id': new_user_id, 'error': '', action: True}
        return json(response)


class UserView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, user_id):
        user = await User.filter(pk=user_id).first().values('id',
                                                             'username',
                                                             'admin',
                                                             'created',
                                                             'last_successful_login',
                                                             'last_failed_login',
                                                             'failed_login_count')

        if user:
            return json(user)
        else:
            response = {'error': 'User not found'}
            return json(response)

    async def delete(self, request, user_id):
        user = await User.filter(pk=user_id).first()
        if user:
            await user.delete()
            response = {'id': user.pk, 'deleted': True}
            return json(response)
        else:
            response = {'error': 'User not found', 'deleted': False}
            return json(response)


class ProfileView(HTTPMethodView):
    decorators = [protected()]

    async def put(self, request):
        action = 'validated'
        try:
            if request.json['username'] == '':
                response = {'error': 'Username cannot be blank', action: False}
                return json(response)
            if request.json['current_password'] == '':
                response = {'error': 'Current password cannot be blank', action: False}
                return json(response)
            if request.json['new_password'] == '':
                response = {'error': 'New password cannot be blank', action: False}
                return json(response)
            if await User.filter(username=request.json['username']).all().count() == 0:
                response = {'error': 'Username doesn\'t exist', action: False}
                return json(response)

            action = 'modified'
            current_password_valid = await verify_authentication(request.json['username'],
                                                                 request.json['current_password'])

            if current_password_valid:
                user = await User.get(username=request.json['username'])
                if user:
                    await user.set_password(request.json['new_password'])
                    await user.save()
                else:
                    response = {'error': 'User not found', action: False}
                    return json(response)
            else:
                response = {'error': 'Password is incorrect', action: False}
                return json(response)

        except Exception:
            response = {'error': 'Unknown error occurred while changing password', action: False}
            return json(response)

        response = {'error': '', action: True}
        return json(response)
