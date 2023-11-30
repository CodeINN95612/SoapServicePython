from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class SoapService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Unicode)
    def say_hello(ctx, name, times):
        return f"Hello, {name}! " * times
    
    @rpc(Integer, Integer, _returns=Integer)
    def add_numbers(ctx, num1, num2):
        return num1 + num2
    
    @rpc(Integer, _returns=Unicode)
    def fibonacci_sequence(ctx, n):
        def generate_fibonacci(n):
            fib_sequence = []
            a, b = 0, 1
            for _ in range(n):
                fib_sequence.append(str(a))
                a, b = b, a + b
            return ' '.join(fib_sequence)
        return generate_fibonacci(n)

application = Application([SoapService], 'your.namespace.here',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

if __name__ == '__main__':
    wsgi_application = WsgiApplication(application)

    server = make_server('0.0.0.0', 8000, wsgi_application)
    print("Servicio SOAP iniciado en http://0.0.0.0:8000")
    server.serve_forever()
