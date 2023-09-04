from tortoise import exceptions as tortoise_exceptions, timezone
from sanic_jwt import exceptions as jwt_exceptions
from settings.models import User


async def authenticate(request):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise jwt_exceptions.AuthenticationFailed()

    try:
        user = await User.get(username=username)
        if await user.check_password(password) is True:
            user.last_successful_login = timezone.now()
            await user.save()
            return dict(user_id=user.username)
        else:
            user.last_failed_login = timezone.now()
            user.failed_login_count = user.failed_login_count + 1
            await user.save()
            raise jwt_exceptions.AuthenticationFailed()
    except tortoise_exceptions.DoesNotExist:
        raise jwt_exceptions.AuthenticationFailed()


async def verify_authentication(username, password):
    if not username or not password:
        return False

    try:
        user = await User.get(username=username)
        if await user.check_password(password) is True:
            user.last_successful_login = timezone.now()
            await user.save()
            return True
        else:
            user.last_failed_login = timezone.now()
            user.failed_login_count = user.failed_login_count + 1
            await user.save()
            return False
    except tortoise_exceptions.DoesNotExist:
        return False


async def create_user(username, password):
    new_user = User()
    new_user.username = username
    await new_user.set_password(password)
    new_user.admin = True
    await new_user.save()
    return new_user.pk


async def create_initial_user(username, password):
    if await User.filter(username=username).all().count() == 0:
        await create_user(username, password)


