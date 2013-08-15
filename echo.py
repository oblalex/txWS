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


class FooResource(WebSocketResource):

    def process(self, request):
        request.channel.write("FOO: %s" % request.data)


def main():
    log.startLogging(stdout)

    root = WebSocketResource()
    root.putChild("bar", BarResource())
    root.putChild("foo", FooResource())
    reactor.listenTCP(5600, WebSocketFactory(root))

    reactor.run()


if __name__ == "__main__":
    main()
