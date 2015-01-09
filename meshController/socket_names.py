# these are hardcoded strings that are used in various places

def ConnectorName():
    return "connector"

connectorPath ='socket.obj'
def setConnectorPath(path):
    connectorPath = path
def ConnectorPath():
    # [RMS] can we get a relative path for this?
    return connectorPath


def SocketName():
    return 'socket'