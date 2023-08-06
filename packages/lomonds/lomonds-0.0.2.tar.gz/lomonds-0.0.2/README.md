# Lomonds

@fork from dataplicity-lomond

Enhancement to allow a custom function to be called to get the data for a ping packet.

Tranquil WebSockets for Python.

You can custom ping data like this:

    websocket = Websocket('wss://ws.example.org')
    
    for event in WebSocket.connect(ping_rate=5, ping_data=b'hello'):
        on_event(event)
[![PyPI](https://img.shields.io/pypi/pyversions/lomond.svg)](https://pypi.org/project/lomond/)
[![Coverage Status](https://coveralls.io/repos/github/wildfoundry/dataplicity-lomond/badge.svg?branch=master)](https://coveralls.io/github/wildfoundry/dataplicity-lomond?branch=master)
[![CircleCI](https://circleci.com/gh/wildfoundry/dataplicity-lomond/tree/master.svg?style=svg)](https://circleci.com/gh/wildfoundry/dataplicity-lomond/tree/master)

Lomond is a Websocket client which turns a websocket connection in to
an orderly stream of _events_. No threads or callbacks necessary.

- [Documentation](https://lomond.readthedocs.io/)

- [GitHub Repository](https://github.com/wildfoundry/dataplicity-lomond)

- [Blog](https://www.willmcgugan.com/search/?s=lomond)



