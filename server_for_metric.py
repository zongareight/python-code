import asyncio


def run_server(host, port):

    store = dict()

    def store_in(key, value, stmp):
        if key not in store:
            store[key] = []
        if (value, stmp) in store[key]:
            store[key].remove((value, stmp))
        store[key] = store[key] + [(value, stmp)]
        return 'ok\n\n'

    def store_out(key):
        if key == '*':
            rsp = ''
            for key in store:
                for _ in store[key]:
                    rsp += ''.join([key + ' ' + ' '.join(_) + '\n'])
            return 'ok\n' + rsp + '\n'
        if key not in store:
            return 'ok\n\n'
        else:
            return 'ok\n' + ''.join(
                [
                    key + ' ' + ' '.join(_) + '\n'
                    for _ in store[key]
                ]
            ) + '\n'

    def handler(data):
        req = data.split()[0]
        if req == 'put':
            key, value, stmp = data.split()[1:]
            return store_in(key, value, stmp)
        elif req == 'get':
            key = data.split()[1]
            return store_out(key)
        else:
            return f'error\nwrong command\n\n'

    class ClientServerProtocol(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport
            peername = transport.get_extra_info('peername')
            print(f'Connection from: {peername}')

        def data_received(self, data):
            data_in = data.decode()
            print(f'Data received: {data_in}')
            data_out = handler(data_in)
            self.transport.write(data_out.encode())
            print(f'Send: {data_out}')

    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('stop server')
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
