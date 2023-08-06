Tornado web services @ your fingertips
===============================================================================

**dizzydecor** is a python library that makes it easy to create web services 
in tornado. To accomplish this, the library adds two new classes and decorators 
that help eliminate the need for boilerplate code. 

Example
----------------------------------------------------------------------------

Here is an example to show how **dizzydecor**, works:

.. code:: python

    from tornado.ioloop import IOLoop

    from dizzydecor import (
        WSApplication,
        WebserviceHandler,
        webservice,
        servicemethod
    )
    
    @webservice
    class MyWebService(WebserviceHandler):
        
        @servicemethod()
        async def echo(self, message):
            return f"You said: {message}"
            
        @servicemethod(httpmethod="GET")
        async def my_greeting(self):
            return dict(greeting="Hello, welcome to my web service demo!")
            
    if __name__ == "__main__":
        app = WSApplication()
        app.listen(8080)
        IOLoop.current().start()
    
This will create a web service with two service methods: echo and my_greeting.
By default, service methods respond to POST requests; however, the ``httpmethod``
argument to ``servicemethod`` can change this behaviour. For instance, 
my_greeting is setup to respond to GET requests.

Paths are generated based on class and method names. 
    - A web service's path is the lower-case class name with each word joined by a hyphen. (MyWebService -> my-web-service)
    - A method's path is the method's name with underscores replaced with hyphens. (my_greeting -> my-greeting)

It's also worth noting that if a service method does not get all of its 
arguments, the service handler sends a 400 HTTP status code.

To test, you can use curl::

    $ curl http://localhost:8080/my-web-service/echo -d '{"message": "This is my message"}'
    "You said: This is my message"
    $ curl http://localhost:8080/my-web-service/my-greeting
    {"greeting": "Hello, welcome to my web service demo!"}
    
You may have noticed that the example uses JSON.

What if I do not want to use JSON?
----------------------------------------------------------------------------

In this case, all you need to do is override the ``load`` and ``dump``
methods in a subclass of ``WebserviceHandler`` or ``SyncWebserviceHandler``

Here is an example with `PyYAML <http://pyyaml.org/wiki/PyYAML>`_:

.. code:: python

    # -- snip --

    import yaml

    class YAMLServiceHandler(WebserviceHandler):
        
        def load(self, request):
            return yaml.safe_load(request)
            
        def dump(self, response):
            # You can also set content-type here with self.set_header
            return yaml.safe_dump(response)
    
    @webservice
    class YetAnotherService(YAMLServiceHandler):
        
        @servicemethod()
        async def join(self, arr, delim):
            return dict(message=delim.join(map(str, arr)))

    # -- snip --
            
The rest is exactly the same, except now your service will use YAML.

Here's how to test it with curl::
    
    $ curl http://localhost:8080/yet-another-service/join --data-binary @"/dev/stdin"<<_eof_
    arr:
        - Hello
        - world
    delim: " "
    _eof_
    message: Hello world

Installation
----------------------------------------------------------------------------

Install with pip or easy_install::

    $ pip install dizzydecor

**dizzydecor** is only available for Python 3

What about non-standard HTTP methods? (Experimental)
----------------------------------------------------------------------------

In this case, all you need to do is extend the SUPPORTED_METHODS property 
of the service handler class.

.. code:: python

    # -- snip --

    @webservice
    class NotificationService(WebserviceHandler):
        SUPPORTED_METHODS = WebserviceHandler.SUPPORTED_METHODS + ("NOTIFY",)

        @servicemethod(httpmethod="NOTIFY")
        async def notification(self, message):
            # etc
    
    # -- snip --

The script for the new HTTP method is added to the service handler 
during the creation of the web service. After that, all you need to 
do is setup to service method to respond to that request type. Depending 
on the situation, you might also need to customize the way arguments are 
parsed by overriding prepare.

Synchronous services
----------------------------------------------------------------------------

The ``WebserviceHandler`` is asynchronous; however, you can make synchronous 
service handlers using the ``SyncWebserviceHandler`` class.

.. code:: python

    # -- snip --

    @webservice
    class MySyncService(SyncWebserviceHandler):

        # This time the method is not async
        @servicemethod(httpmethod="GET")
        def my_greeting(self):
            return dict(greeting="Hello...")

    # -- snip --