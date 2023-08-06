import json
import gzip
import logging
from base64 import b64encode
from multiprocessing.dummy import Pool
import requests
from .stream_sea_schema_definition import SchemaDefinition

STREAM_SEA_CLIENT_THREAD_COUNT = 4 # TODO: make configurable

logger = logging.getLogger(__name__)
pool = Pool(STREAM_SEA_CLIENT_THREAD_COUNT)

def __generate_url(remote_url: str, stream: str, action: str):
    return f'{remote_url}/api/v1/streams/{stream}/{action}'

def __get_default_headers(client_id, client_secret):
    token = b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
    return {
        'Content-encoding': 'gzip',
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Basic {token}'
    }

def publish(*, remote_url: str, client_id: str, client_secret: str, stream: str, payload):
    def on_publish_error(error):
        logger.error(f"Error while publishing to stream sea: {error.__cause__}")

    pool.apply_async(requests.post,
                        [__generate_url(remote_url, stream, 'publish')],
                        dict(headers=__get_default_headers(client_id, client_secret),
                            data=gzip.compress(json.dumps({'payload': payload}).encode('utf-8'))),
                        error_callback=on_publish_error)

def define_stream(*, remote_url: str, client_id: str, client_secret: str, stream: str, schema: SchemaDefinition):
    data = gzip.compress(json.dumps(schema.json_serialize()).encode('utf8'))
    url = __generate_url(remote_url, stream, 'define')
    headers = __get_default_headers(client_id, client_secret)

    return requests.post(
        url=url,
        data=data,
        headers=headers
    )

def describe_stream(*, remote_url: str, client_id: str, client_secret: str, stream: str):
    url = __generate_url(remote_url, stream, 'schema')
    headers = __get_default_headers(client_id, client_secret)
    response = requests.get(
        url=url,
        headers=headers
    )

    if response.status_code != 200:
        return None

    return SchemaDefinition(**json.loads(response.content.decode('utf-8')))

def get_schema_version(*, remote_url: str, client_id: str, client_secret: str, stream: str):
    versions = get_schema_versions_vector(
        remote_url=remote_url,
        client_id=client_id,
        client_secret=client_secret,
        streams=[stream],
    )
    return versions[0] if versions else None

def get_schema_versions_vector(*, remote_url: str, client_id: str, client_secret: str, streams: [str]):
    url = f'{remote_url}/api/v1/schema-versions-vector'
    stream_versions = requests.post(
        url=url,
        data=gzip.compress(json.dumps({'schemaNames': streams}).encode('utf-8')),
        headers=__get_default_headers(client_id, client_secret)
    )
    return json.loads(stream_versions.content.decode('utf-8'))['versionsVector']


