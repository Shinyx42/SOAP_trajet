from spyne import ServiceBase, rpc, Unicode, Integer, Iterable, Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class CalculTemps(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield u'Hello, %s' % name
            
    @rpc(Integer, Integer, _returns=Integer)
    def addition(ctx, a, b):
        return a+b
    
    #renvoie le temps en second avec en entree la distance et l'autonomie en m 
    #et le temps de charge en s
    @rpc(Integer, Integer, Integer, _returns=Integer)
    def get_temps(ctx, distance, autonomie, tempsCharge):
        vitesseMoyenne = 28 #25m/s = 90km/h 28m/s = 100km/h 36m/s = 130km/h
        nbCharge = distance//autonomie
        return (distance//vitesseMoyenne)+(nbCharge*tempsCharge)
            
application = Application([CalculTemps], 'spyne.examples.hello.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11())
wsgi_application = WsgiApplication(application)

if __name__=="__main__":
    from wsgiref.simple_server import make_server
    serveur = make_server('127.0.0.1', 8000, wsgi_application)
    serveur.serve_forever()
    
#geo.api.gouv.fr