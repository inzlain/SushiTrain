import secrets
from sanic.response import file
from tortoise import Tortoise, run_async
from sanic_jwt import Initialize
from os import environ
from environs import Env
from delivery.handlers import http_request_handler
from payloads.views import *
from redirectors.views import *
from policies.views import *
from files.views import *
from settings.views import *
from delivery.views import *
from payloads.library import refresh_module_library
from settings.authentication import authenticate, create_initial_user

management = Sanic("Management")
listener = Sanic("Listener")

# Set Sushi Train configuration variables
env = Env()
env.read_env()
settings = {
    'DELIVERY_HOSTNAME': env("DELIVERY_HOSTNAME"),
    'DELIVERY_BIND_IP': env("DELIVERY_BIND_IP"),
    'DELIVERY_PORT': env("DELIVERY_PORT"),
    'DELIVERY_PATH': env("DELIVERY_PATH"),
    'MANAGEMENT_HOSTNAME': env("MANAGEMENT_HOSTNAME"),
    'MANAGEMENT_BIND_IP': env("MANAGEMENT_BIND_IP"),
    'MANAGEMENT_PORT': env("MANAGEMENT_PORT"),
    'SLACK_WEBHOOK_URL': env("SLACK_WEBHOOK_URL"),
}
if 'SUSHIDEVMODE' in environ:
    print("Sushi Train running in Dev Mode!")
    settings['DELIVERY_HOSTNAME'] = "127.0.0.1"
    settings['DELIVERY_PORT'] = 9000
    settings['MANAGEMENT_HOSTNAME'] = "127.0.0.1"
    settings['MANAGEMENT_PORT'] = 8000
management.config.update(settings)
listener.config.update(settings)

# Database Setup
if 'SUSHIDEVMODE' in environ:
    print("Sushi Train using SQLite database")

    async def database_init():
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['files.models',
                                'payloads.models',
                                'policies.models',
                                'redirectors.models',
                                'delivery.models',
                                'settings.models']},
            use_tz=True
        )
        await Tortoise.generate_schemas()
    run_async(database_init())
else:
    async def database_init():
        print("Sushi Train using Postgres database")
        await Tortoise.init(
            db_url='asyncpg://sushitrain:sushitrain@postgres:5432/sushitrain',
            modules={'models': ['files.models',
                                'payloads.models',
                                'policies.models',
                                'redirectors.models',
                                'delivery.models',
                                'settings.models']},
            use_tz=True
        )
        await Tortoise.generate_schemas()
    run_async(database_init())

# Setup authentication
jwt_secret = env("JWT_SECRET")
if jwt_secret == "":
    print("JWT secret not configureed in .env file -> A randomly generated secret will be used instead.")
    jwt_secret = secrets.token_bytes(128)
Initialize(management,
           authenticate=authenticate,
           url_prefix='/api/authentication',
           secret=jwt_secret,
           cookie_set=True,
           cookie_httponly=True,
           cookie_split=True,
           cookie_access_token_name='access-token',
           cookie_split_signature_name='access-token-signature',
           cookie_samesite='Strict',
           expiration_delta=43200)  # 12 hours

# Create the initial user
run_async(create_initial_user(env("ADMIN_USERNAME"), env("ADMIN_PASSWORD")))

# Frontend Static Routes
management.static('/management', './frontend/index.html', name='login')
management.static('/management/monitor', './frontend/index.html', name='monitor')
management.static('/management/logs', './frontend/index.html', name='logs')
management.static('/management/redirectors', './frontend/index.html', name='redirectors')
management.static('/management/redirectors/add', './frontend/index.html', name='redirector_add')
management.static('/management/policies', './frontend/index.html', name='policies')
management.static('/management/policies/add', './frontend/index.html', name='policy_add')
management.static('/management/payloads', './frontend/index.html', name='payloads')
management.static('/management/payloads/add', './frontend/index.html', name='payload_add')
management.static('/management/files', './frontend/index.html', name='files')
management.static('/management/settings', './frontend/index.html', name='settings')
management.static('/management/profile', './frontend/index.html', name='profile')
management.static('/management/assets', './frontend/assets', name='assets')


# Frontend Dynamic Routes
@management.get("/management/logs/<log_id>")
async def request_log(request, log_id):
    return await file('./frontend/index.html')


@management.get("/management/redirectors/edit/<redirector_id>")
async def redirector_edit(request, redirector_id):
    return await file('./frontend/index.html')


@management.get("/management/redirectors/deploy/<redirector_id>")
async def redirector_deploy(request, redirector_id):
    return await file('./frontend/index.html')


@management.get("/management/redirectors/edit/<redirector_id>/paths/<path_id>")
async def path_edit(request, redirector_id, path_id):
    return await file('./frontend/index.html')


@management.get("/management/redirectors/addpath/<redirector_id>")
async def path_add(request, redirector_id):
    return await file('./frontend/index.html')


@management.get("/management/policies/edit/<policy_id>")
async def policy_edit(request, policy_id):
    return await file('./frontend/index.html')


@management.get("/management/payloads/edit/<payload_id>")
async def payload_edit(request, payload_id):
    return await file('./frontend/index.html')


@management.get("/management/payloads/logs/<payload_id>")
async def payload_logs(request, payload_id):
    return await file('./frontend/index.html')


@management.get("/management/payloads/logs/<payload_id>/view/<log_id>")
async def payload_log(request, payload_id, log_id):
    return await file('./frontend/index.html')


# API Routes (Require Authentication)
management.add_route(MonitorView.as_view(), "/api/monitor")
management.add_route(RequestLogsView.as_view(), "/api/requests")
management.add_route(RequestLogView.as_view(), "/api/requests/<request_id>")
management.add_route(RequestLogDownloadView.as_view(), "/api/requests/<request_id>/<download_type>/download")
management.add_route(RedirectorsView.as_view(), "/api/redirectors")
management.add_route(RedirectorView.as_view(), "/api/redirectors/<redirector_id>")
management.add_route(RedirectorPathsView.as_view(), "/api/redirectors/<redirector_id>/paths")
management.add_route(RedirectorDeployView.as_view(), "/api/redirectors/<redirector_id>/deploy/<redirector_type>")
management.add_route(PathsView.as_view(), "/api/paths")
management.add_route(PathsEnableAllView.as_view(), "/api/paths/all/enable")
management.add_route(PathsDisableAll.as_view(), "/api/paths/all/disable")
management.add_route(PathView.as_view(), "/api/paths/<path_id>")
management.add_route(URLsView.as_view(), "/api/urls")
management.add_route(PoliciesView.as_view(), "/api/policies")
management.add_route(PolicyView.as_view(), "/api/policies/<policy_id>")
management.add_route(PayloadsView.as_view(), "/api/payloads")
management.add_route(PayloadView.as_view(), "/api/payloads/<payload_id>")
management.add_route(PayloadGenerateView.as_view(), "/api/payloads/<payload_id>/generate")
management.add_route(PayloadLogsView.as_view(), "/api/payloads/<payload_id>/logs")
management.add_route(PayloadLogView.as_view(), "/api/payloads/<payload_id>/logs/<log_id>")
management.add_route(PayloadLogDownloadView.as_view(), "/api/payloads/<payload_id>/logs/<log_id>/download")
management.add_route(ModulesView.as_view(), "/api/modules")
management.add_route(ModuleView.as_view(), "/api/modules/<module_id>")
management.add_route(ModulesLibraryView.as_view(), "/api/modules/library/")
management.add_route(ModuleLibraryView.as_view(), "/api/modules/library/<module_library_id>")
management.add_route(FilesView.as_view(), "/api/files")
management.add_route(FileView.as_view(), "/api/files/<file_id>")
management.add_route(SettingsView.as_view(), "/api/settings")
management.add_route(UsersView.as_view(), "/api/users")
management.add_route(UserView.as_view(), "/api/users/<user_id>")
management.add_route(ProfileView.as_view(), "/api/profile")


# Log Out Route
@management.route('/api/authentication/logout')
async def request_handler(request):
    response = text("OK")
    response.cookies.delete_cookie("access-token")
    response.cookies.delete_cookie("access-token-signature")
    response.cookies.delete_cookie("sessionid")
    return response


# Payload Delivery Routes
@listener.route(management.config['DELIVERY_PATH'], methods=["GET", "POST", "PUT", "HEAD", "OPTIONS", "PATCH", "DELETE"])
async def request_handler(request):
    return await http_request_handler(request)

# Refresh the payload module library
run_async(refresh_module_library())

# Run the Sanic applications instances
if __name__ == "__main__":
    # We run the management application and the listener application on different ports
    # See https://sanic.dev/en/guide/release-notes/v22.3.html#application-multi-serve for how this works
    management.prepare(host="0.0.0.0", port=8000, debug=False)
    listener.prepare(host="0.0.0.0", port=9000, debug=False)
    print("Sushi Train management interface will be located at:")
    print(" - Hostname: https://{0}:{1}/management/".format(settings['MANAGEMENT_HOSTNAME'], settings['MANAGEMENT_PORT']))
    print(" - IP address: https://{0}:{1}/management/".format(settings['MANAGEMENT_BIND_IP'], settings['MANAGEMENT_PORT']))
    Sanic.serve()
