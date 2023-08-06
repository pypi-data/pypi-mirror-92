from .enviroment import Enviroment
from .network import Network, Protocol
from .flavor import Flavor
from typing import List
import yaml
import copy

class Service():
    def __init__(self, name:str, image:str, env:Enviroment=None, volumes=None, net:List[Network]=None, cmd:str=None, flavor:Flavor=None, replicas = 1):
        self.container_name = name
        self.image = image 
        self.env = env
        self.volumes = volumes
        self.net = net
        self.cmd = cmd
        self.flavor = flavor
        self.replicas = replicas

class Application():
    def __init__(self):
        self._services = []
        self._volume_dict = {}
        pass

    
    def parse(self, path):
        with open(path) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            comp_list = yaml.load(file, Loader=yaml.FullLoader)
            if 'volumes' in comp_list:
                self._volume_dict = comp_list['volumes'] 
            else:
                print("No volume inside!")

            if 'services' in comp_list:
                service_list = comp_list['services']
                services = []
                for key in service_list:
                    services.append(service_list[key])       
                services = sort_service_dicts(services)
                for service in services:
                    print("process service "+service['container_name'])
                    env = None
                    mount = None
                    net = None
                    cmd = ''
                    flavor = None
                    replicas = 1
                    if 'environment' in service:
                        env = Enviroment()
                        service_env = service['environment']
                        for env_key in service_env:
                            if len(service_env[env_key]) == 0:
                                service_env[env_key] = ' '
                            env.set(env_key, service_env[env_key])
                    if 'ports' in service:        
                        net = []
                        service_port = service['ports']
                        for port in service_port:
                            ports = port.split(':')
                            net.append(Network(int(ports[0]), Protocol.TCP, publish=True, nodePort=int(ports[1])))
                    if 'command' in service:
                        service_cmd = service['command']
                        if isinstance(service_cmd, list):
                            cmd = ' '.join(service_cmd)
                        else:
                            cmd = service['command'] 
                        # print(cmd)
                    if 'deploy' in service:
                        replicas = service['deploy'].get('replicas',1)
                    
                    self._services.append(Service(service['container_name'],service.get('image',None),env, service.get('volumes',None), net, cmd, flavor, replicas))          

            else:
                print("No service inside!")

    def getVolumes(self) -> dict:
        return copy.copy(self._volume_dict)

    def getServices(self) -> List[Service]:
        return self._services.copy()

    def getService(self, name:str)->Service:    
        find = None
        for service in self._services:
            if service.container_name == name:
                find = service
                break
        return copy.copy(find)

    def updateService(self, name:str, service:Service=None):
        for idx, ser in enumerate(self._services):
            if ser.container_name == name:
                if service is None:
                    self._services.remove(ser)
                else:    
                    self._services[idx] = service
                break       
                     



def get_service_dependents(service_dict, services):
    name = service_dict['container_name']
    return [
        service for service in services
        if (name in service.get('depends_on', []))
    ]


def sort_service_dicts(services):
    # Topological sort (Cormen/Tarjan algorithm).
    unmarked = services[:]
    temporary_marked = set()
    sorted_services = []

    def visit(n):
        if n['container_name'] in temporary_marked:
            if n['container_name'] in n.get('depends_on', []):
                print('A service can not depend on itself: %s' % n['name'])
            print('Circular dependency between %s' % ' and '.join(temporary_marked))

        if n in unmarked:
            temporary_marked.add(n['container_name'])
            for m in get_service_dependents(n, services):
                visit(m)
            temporary_marked.remove(n['container_name'])
            unmarked.remove(n)
            sorted_services.insert(0, n)

    while unmarked:
        visit(unmarked[-1])

    return sorted_services
    

