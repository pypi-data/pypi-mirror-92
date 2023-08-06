def get_api_base_http_uri(*, remote_host, remote_port, secure):
    return (
        ('https' if secure else 'http') +
        f'://{remote_host}' +
        (f':{remote_port}' if remote_port is not None else '') +
        '/api/v1'
    )


def get_api_base_ws_uri(*, remote_host, remote_port, secure):
    return (
        ('wss' if secure else 'ws') +
        f'://{remote_host}' +
        (f':{remote_port}' if remote_port is not None else '') +
        '/api/v1'
    )
