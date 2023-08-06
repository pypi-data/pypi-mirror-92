import asyncio
import json
import itertools
import websockets
from .utils import get_api_base_ws_uri


class ProtocolError(Exception):
    pass


class CredentialsError(Exception):
    pass


SUBSCRIPTION_ITERATOR_QUEUE_MAX_SIZE = 100


class SubscriptionIterator:
    def __init__(self):
        self.queue = asyncio.Queue(SUBSCRIPTION_ITERATOR_QUEUE_MAX_SIZE)

    def enqueue_payload(self, payload):
        queue_item = ('payload', payload)
        self.queue.put_nowait(queue_item)

    def close_iterator(self, exception):
        self.queue.put_nowait(('stop', exception))

    def __aiter__(self):
        return self

    async def __anext__(self):
        queue_item = await self.queue.get()
        if queue_item[0] == 'payload':
            return queue_item[1]
        elif queue_item[0] == 'stop':
            if isinstance(queue_item[1], websockets.ConnectionClosed):
                raise StopAsyncIteration
            else:
                raise queue_item[1]
        else:
            raise NotImplementedError()


class StreamSeaConnection:
    def __init__(self, *, remote_host, remote_port=None, secure=False, client_id, client_secret, loop=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.loop = loop or asyncio.get_event_loop()
        self.ensure_ws = self.loop.create_future()
        self.ensure_authenticated = self.loop.create_future()
        self.replies_map = {}
        self.msg_id_sequence = itertools.count(1)
        self.uri = get_api_base_ws_uri(remote_host=remote_host, remote_port=remote_port, secure=secure) + '/streams'

    async def __aenter__(self):
        return await self

    async def __aexit__(self, exc_type, exc_value, traceback):
        ws = await self.ensure_ws
        await ws.close()

    def __await__(self):
        # Create a suitable iterator by calling __await__ on a coroutine.
        return self.__await_impl__().__await__()

    async def __await_impl__(self):
        ws = await websockets.connect(self.uri)
        self.ensure_ws.set_result(ws)

        auth_request_msg_json = {
            "id": next(self.msg_id_sequence),
            "action": "authenticate",
            "payload": {
                "type": "basic",
                "clientId": self.client_id,
                "clientSecret": self.client_secret,
            },
        }
        await self.send(auth_request_msg_json)
        auth_response_msg = await self.recv()
        try:
            auth_response_json = json.loads(auth_response_msg)
            if not isinstance(auth_response_json, dict):
                raise ProtocolError('Authentication Response must be object')
            if ('id' not in auth_response_json) or auth_response_json['id'] != 1:
                raise ProtocolError('Authentication Response must have an id of 1')
            if auth_response_json['action'] != 'authenticate':
                raise ProtocolError('Reply to a authenticate action must be a authenticate action')
            if ('success' not in auth_response_json):
                raise ProtocolError('Authentication Response does not have a success field')
            if not auth_response_json['success']:
                raise CredentialsError('Authentication unsuccessful')
            self.ensure_authenticated.set_result(True)

        except json.decoder.JSONDecodeError:
            raise ProtocolError('Could not decode JSON for Authentication Response')

        self.loop.create_task(self.authenticated_listen())
        return self

    async def send(self, message_json):
        ws = await self.ensure_ws
        await ws.send(json.dumps(message_json))

    async def authenticated_listen(self):
        # Receive messages forever. May only be called once authentication has succeeded
        try:
            while True:
                r = await self.recv()
                await self.on_authenticated_message(r)
        except Exception as e:
            # Pass any exceptions to the SubscriptionIterator
            for k, replies_map_entry in self.replies_map.items():
                if not replies_map_entry['first_reply_future'].done():
                    replies_map_entry['first_reply_future'].set_exception(e)
                replies_map_entry['other_replies_iterator'].close_iterator(e)

    async def recv(self):
        ws = await self.ensure_ws
        return await ws.recv()

    async def subscribe(self, stream_name):
        await self.ensure_authenticated
        msg_id = next(self.msg_id_sequence)
        subscription_request_msg_json = {
            "id": msg_id,
            "action": "subscribe",
            "payload": stream_name
        }
        first_reply_future = self.loop.create_future()

        other_replies_iterator = SubscriptionIterator()

        self.replies_map[msg_id] = {
            "first_reply_future": first_reply_future,
            "other_replies_iterator": other_replies_iterator,
        }
        await self.send(subscription_request_msg_json)

        first_reply_json = await first_reply_future
        if first_reply_json['action'] != 'subscription':
            raise ProtocolError('Reply to a subscribe action must be a subscription action')

        return other_replies_iterator

    # Callback for every message after the authentication phase
    # TODO: does this need to be async?
    async def on_authenticated_message(self, message):
        try:
            message_json = json.loads(message)
            if 'id' not in message_json:
                raise ProtocolError('Message must have an id')
            msg_id = message_json['id']
            if msg_id not in self.replies_map:
                raise ProtocolError('Server sent a response but the message id could not be resolved to a request')

            replies_map_entry = self.replies_map[msg_id]
            if replies_map_entry['first_reply_future'].done():
                replies_map_entry['other_replies_iterator'].enqueue_payload(message_json['payload'])
            else:
                replies_map_entry['first_reply_future'].set_result(message_json)

        except json.decoder.JSONDecodeError:
            raise ProtocolError('Could not decode JSON for message')
