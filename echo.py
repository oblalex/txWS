from sys import stdout

#===============================================================================
# Import Twisted
#===============================================================================
from twisted.application.strports import listen
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.server import Site
from txws import WebSocketFactory, WebSocketResource

#===============================================================================
# Business Logic
#===============================================================================


class BarResource(WebSocketResource):

    def process(self, request):
        request.channel.write("BAR: %s" % request.data)


class BazResource(WebSocketResource):

    def process(self, request):
        request.channel.write("BAZ: %s" % request.data)


class QuxResource(WebSocketResource):

    def process(self, request):
        request.channel.write("QUX: %s" % request.data)


def main():
    """
    Routing:
        ws://127.0.0.1:5600/bar     -> BarResource
        ws://127.0.0.1:5600/foo/baz -> BazResource
        ws://127.0.0.1:5600/foo/qux -> QuxResource
    """
    log.startLogging(stdout)

    root = WebSocketResource()
    root.putChild("bar", BarResource())

    foo = WebSocketResource()
    root.putChild("foo", foo)
    foo.putChild("baz", BazResource())
    foo.putChild("qux", QuxResource())

    reactor.listenTCP(5600, WebSocketFactory(root))
    reactor.run()


if __name__ == "__main__":
    main()
