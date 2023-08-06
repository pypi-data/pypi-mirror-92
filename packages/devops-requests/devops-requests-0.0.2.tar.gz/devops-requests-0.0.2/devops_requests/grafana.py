import requests, json, os


grafana_url = None
api_key = None


###############################################################################
# Utilities
###############################################################################

def normalize_name(name: str):
    return name.lower().replace(' ', '-')


###############################################################################
# API Request
###############################################################################

def set_url(url):
    '''
    Set the grafana url to use for requests. This should be the base url for your grafana instance (without `/api`). For example: `https://grafana.mydomain.com`.
    The url must be set prior to making any requests.

    :param url: The grafana url to use during requests
    '''
    global grafana_url
    grafana_url = url


def set_api_key(key):
    '''
    Set the Grafana API key. The API key must be set prior to making any requests.

    :param key: The api key.
    '''
    global api_key
    api_key = key


def make_request(api_path, method='get', data={}):
    '''
    Make a request to the specified API path. The grafana url and `/api` should be omitted.
    For example, to make a request to `https://grafana.mydomain.com/api/dashboards/uid/0`, provide `dashboards/uid/0` for the `api_path`.

    Full Grafana API documentation can be found here: https://grafana.com/docs/grafana/latest/http_api/

    :param api_path: The API path of the request
    :param method: The request method to use. One of `get`, `post`, `delete`. Default: `get`
    :param data: The json data to include in the body of the request. Only applicable for `post` requests
    :return: The json response from the API
    '''
    if not grafana_url:
        raise ValueError('Grafana URL not set. Must call set_grafana_url() prior to making requests')
    if not api_key:
        raise ValueError('API key not set. Must call set_api_key() prior to making requests')

    request_url = os.path.join(grafana_url, 'api', api_path)
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    if method == 'get':
        response = requests.get(request_url, headers=headers)
    elif method == 'post':
        response = requests.post(request_url, headers=headers, json=data)
    elif method == 'delete':
        response = requests.delete(request_url, headers=headers)
    else:
        raise ValueError(f'Unkown request method: {method}')
    
    response.raise_for_status()

    return json.loads(response.text)


def get(api_path):
    '''
    Make a GET request to the specified api_path.

    :param api_path: The API path
    :return: The json response from the API
    '''
    return make_request(api_path, method='get')


def post(api_path, data):
    '''
    Make a POST request to the specified api_path.

    :param api_path: The API path
    :param data: The json data to include in the body of the request
    :return: The json response from the API
    '''
    return make_request(api_path, method='post', data=data)


def delete(api_path):
    '''
    Make a DELETE request to the specified api_path.

    :param api_path: The API path
    :return: The json response from the API
    '''
    return make_request(api_path, method='delete')


###############################################################################
# Dashboards
###############################################################################

def search_dashboards(**params):
    '''
    Retrieve a list of dashboards using the specified query parameters.
    Note, the items in this list contain only identifying information (uid, etc.). For a complete specification, call get_dashboard(uid)

    The parameter `query` should be used to search for strings such as the dashboard title.
    Other search parameters can be found here: https://grafana.com/docs/grafana/latest/http_api/folder_dashboard_search/

    For example, to search for "mydashboard" in the default folder (`/api/search?folderIds=0&query=mydashboard`)::

        dashboards = search_dashboards(folderIds=0, query=mydashboard)

    :param params: Keyword parameters representing the http query parameters to use
    :return: A list of dashboards resulting from the search query
    '''
    formatted_params = [ f'{param}={value}' for param, value in params.items() ]
    params_string = '&'.join(formatted_params)
    return get(f'search?{params_string}')


def list_dashboards():
    '''
    Retrieve a list of all dashboards.
    Note, the items in this list contain only identifying information (uid, etc.). For a complete specification, call get_dashboard(uid)

    :return: A list of all dashboards
    '''
    return search_dashboards()


def get_dashboard(uid):
    '''
    Retrieve a dashboard by its uid.

    :param uid: The dashboard uid
    :return: The dashboard if found else None
    '''
    try:
        return get(f'dashboards/uid/{uid}')['dashboard']
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
        else:
            raise


def get_dashboard_by_name(name):
    '''
    Retrieve a dashboard by name.

    :param name: The dashboard name/title
    :return: The dashboard if found else None
    '''
    results = search_dashboards(query=name)
    if results:
        return get_dashboard(results[0]['uid'])


def create_dashboard(dashboard: dict, keep_uid=False):
    '''
    Create a new dashboard using the given spec.

    :param dashboard: The json specification for the dashboard
    :param keep_uid: If set, the uid found in the dashboard specification will be reused. Otherwise, a new one will be generated. Default: False
    :return: The uid of the created dashboard
    '''
    dashboard = dashboard.copy()
    dashboard['id'] = None
    if not keep_uid:
        dashboard['uid'] = None
    data = { 'dashboard': dashboard }
    result = post('dashboards/db', data=data)
    return result['uid']


def delete_dashboard(uid):
    '''
    Deletes the dashboard with the given uid.

    :param uid: The dashboard uid
    '''
    try:
        delete(f'dashboards/uid/{uid}')
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return False
        else:
            raise
    
    return True


def import_dashboard(file_path):
    '''
    Import a dashboard from the given json file.

    :param file_path: The path to the json file.
    :return: The uid of the created dashboard
    '''
    with open(file_path, 'r') as file:
        dashboard = json.load(file)
    return create_dashboard(dashboard)


def import_dashboards(dir_name):
    '''
    Import dashboards from a given directory.
    All files in this directory should be valid dashboard specifications in json format

    :param dir_name: The directory to import from
    '''
    imported = []
    for file_name in os.listdir(dir_name):
        file_path = os.path.join(dir_name, file_name)
        uid = import_dashboard(file_path)
        imported.append(uid)
    return imported


def export_dashboard(uid, file_path):
    '''
    Export a dashboard with the given uid to a json file.

    :param uid: The uid of the dashboard
    :param file_path: Path to file
    '''
    dashboard = get_dashboard(uid)
    if not dashboard:
        raise ValueError(f'Dashboard with uid {uid} not found')

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'w+') as file:
        json.dump(dashboard, file, indent=2)


def export_all_dashboards(dir_name='dashboards'):
    '''
    Export all dashboards to the given directory.

    :param dir_name: The directory to put the exported files
    '''
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    for dashboard in list_dashboards():
        file_name = normalize_name(dashboard['title']) + '.json'
        export_dashboard(dashboard['uid'], os.path.join(dir_name, file_name))


###############################################################################
# Notification Channels
###############################################################################

def list_notification_channels():
    '''
    Retrieve a list of all notification channels.

    :return: A list of all notification channels
    '''
    return get('alert-notifications')


def get_notification_channel(uid):
    '''
    Retrieve a notification channel by uid.

    :param uid: The channel uid
    '''
    try:
        return get(f'alert-notifications/uid/{uid}')
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
        else:
            raise


def get_notification_channel_by_name(name):
    '''
    Retrieve a notification channel by name.

    :param name: The channel name
    :return: The channel if found, else None
    '''
    channels = list_notification_channels()
    for channel in channels:
        if channel['name'] == name:
            return channel


def create_notification_channel(channel: dict, keep_uid=False):
    '''
    Create a notification channel from the given specification.

    :param channel: The json specification for the channel
    :return: The uid of the created channel
    '''
    channel = channel.copy()
    channel['id'] = None
    if not keep_uid:
        channel['uid'] = None
    result = post('alert-notifications', channel)
    return result['uid']


def delete_notification_channel(uid):
    '''
    Delete the notification channel with the given uid

    :param uid: The channel uid
    '''
    if not get_notification_channel(uid):
        return False

    delete(f'alert-notifications/uid/{uid}')

    return True


def import_notification_channel(file_path):
    '''
    Import a notification channel from a json file

    :param file_path: The path to the json file
    :return: The uid of the imported channel
    '''
    with open(file_path, 'r') as file:
        channel = json.load(file)
    return create_notification_channel(channel)


def import_notification_channels(dir_name):
    '''
    Import notification channels from a given directory.
    All files in this directory should be valid channel specifications in json format

    :param dir_name: The directory to import from
    '''
    imported = []
    for file_name in os.listdir(dir_name):
        file_path = os.path.join(dir_name, file_name)
        uid = import_notification_channel(file_path)
        imported.append(uid)
    return imported


def export_notification_channel(uid, file_path):
    '''
    Export a notification channel with the given uid to a json file

    :param uid: The channel uid
    :param file_path: Path to file
    '''
    channel = get_notification_channel(uid)
    if not channel:
        raise ValueError(f'Channel with uid {uid} not found')

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'w+') as file:
        json.dump(channel, file, indent=2)


def export_all_notification_channels(dir_name='notification-channels'):
    '''
    Export all notification channels to the given directory.

    :param dir_name: The directory to put the exported files
    '''
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    for channel in list_notification_channels():
        file_name = normalize_name(channel['name']) + '.json'
        export_notification_channel(channel['uid'], os.path.join(dir_name, file_name))