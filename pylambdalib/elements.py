from abc import ABC
from shapely.geometry import Polygon, Point

class Key(str):
    def get_company_id(self):
        return self[:self.index('.')]
    def get_network_id(self):
        return self[self.index('.')+1:self.index('.',self.index('.')+1)]
    def get_object_id(self):
        return self[self.index('.',self.index('.')+1)+1:]
    def set_company_id(self,company_id):
        return Key(str(company_id) + self[self.index('.'):])
    def set_network_id(self,network_id):
        return Key(self.get_company_id() + "." + str(network_id) + "." +self.get_object_id())
    def set_object_id(self,object_id):
        return Key(self[:self.index('.',self.index('.')+1)] + "." + str(object_id))
    def get_geoidx_key(self):
        return self[:self.index('.',self.index('.')+1)]+':geoidx'
    def __gt__(self,other):
        return int(self.get_object_id()) > int(other.get_object_id())
    def __lt__(self,other):
        return not self.__gt__(other)

class Unixtime(str):

    def __new__(cls, value='', unixtime_up = '', unixtime_down= '', log_up = '', log_down = ''):
        if unixtime_up != '' and log_up != '':
            return str.__new__(cls,f"{unixtime_up}.{unixtime_down}.{log_up}.{log_down}")
        return str.__new__(cls,value)
    def __init__(self, value='',unixtime_up = '', unixtime_down= '', log_up = '', log_down = ''):
        pass
    def get_unixtime_up(self):
        return self[:self.index('.')]
    def get_unixtime_down(self):
        fp = self.index('.')
        return self[fp+1:self.index('.',fp+1)]
    def get_log_up(self):
        fp = self.index('.')
        sp = self.index('.',fp+1)
        return self[sp+1:self.index('.',sp+1)]
    def get_log_down(self):
        fp = self.index('.')
        sp = self.index('.',fp+1)
        return self[self.index('.',sp+1)+1:]
    def set_down(self,unixtime_down,log_down):
        return self.get_unixtime_up() + "." + str(int(unixtime_down)) + "." + \
               self.get_log_up() + "." + str(int(log_down))
    def set_up(self):
        return self.get_unixtime_up() + ".." + self.get_log_up() + "."
    def is_up(self):
        return self.get_unixtime_down() == '' and self.get_log_down() == ''
    def is_down(self):
        return not self.is_up()

class Element:

    def __init__(self):
        self.key = Key()
        self.unixtime = Unixtime()
        self.ocfg = ValueGroup()
        self.val = ValueGroup()
        self.v = ValueGroup()
        self.geoidx = ValueGroup()
        self.co = ValueGroup()
        self.io = ValueGroup()
    def set_key(self,s):
        self.key = Key(s)
    def get_ocfg(self):
        return list(filter(lambda x: x.is_up(),self.ocfg))[0]
    def is_connected_to(self,other):
        fcheck = any(map(lambda x: x.other_key == other.key and x.is_up(),self.co))
        scheck = any(map(lambda x: x.other_key == self.key and x.is_up(),other.co))
        return fcheck and scheck
    def get_polygon(self):
        ordered_vertices = {}
        for vertice in self.v:
            if vertice.is_up():
                latitude, longitude = vertice.get_coordinates()
                ordered_vertices[vertice.get_vertex_num()] = [latitude,longitude]
        vertices = []
        for vertice in sorted(ordered_vertices):
            vertices.append(ordered_vertices[vertice])
        vertices.append(vertices[0])  ##closing the polygon
        return Polygon(vertices)

    def __str__(self):
        return str(self.key)

class ValueGroup(list):
    def __init__(self, *args, **kwargs):
        super(ValueGroup, self).__init__()
        for element in args:
            self.add(element)
    def is_alive(self):
        return any(map(lambda x: x.is_up(),self))
    def in_conflict(self,element): # if the element gets in conflict with one already added
        for member in self:
            if element.in_conflict(member):
                return True
        return False
    def add(self,element):
        if self.in_conflict(element):
            raise ValuesInConflictError(element)
        self.append(element)
    def remove(self,element):
        try:
            self.remove(element)
        except ValueError:
            raise ElementNotInGroupError("The member you are trying to remove is already not a member")
    def __str__(self):
        s = ""
        for member in self:
            s+=str(member)+"\n"
        return s

class ElementValue(ABC,str):
    def __new__(cls, content=''):
        return str.__new__(cls, check_quotes(content))
    def is_up(self):
        return self.get_unixtime().is_up()
    def is_down(self):
        return self.get_unixtime().is_down()
    def set_down(self,unixtime_down,log_down):
        unixt = self.get_unixtime().set_down(unixtime_down,log_down)
        return unixt + ":" +self[self.index(':')+1:]
    def set_up(self,unixtime_down,log_down):
        unixt = self.get_unixtime().set_down(unixtime_down,log_down)
        return unixt + ":" +self[self.index(':')+1:]
    def get_unixtime(self):
        return Unixtime(self[:self.index(':')])
    def in_conflict(self,other):
        return self.is_up() and other.is_up()

def check_quotes(s):
    s = s.replace('"', '')
    s = s.replace("'", "")
    s = s.replace("\t", "")
    return s

# 1648490054..1.:@oStyle|#msn_ylw-pushpin412|0
class Val(ElementValue):
    def get_variable(self):
        return self[self.index(':')+1:self.index('|')]
    def get_value(self):
        fp = self.index('|')
        sp = self.index('|',fp+1)
        return self[fp + 1:sp]
    def get_n(self):
        fp = self.index('|')
        sp = self.index('|',fp+1)
        return self[sp+1:]
    def set(self,unixtime=None,variable=None,value=None,n='0'):
        if unixtime is None:
            unixtime = self.get_unixtime()
        if variable is None:
            variable = self.get_variable()
        if value is None:
            value = self.get_value()
        return Val(Unixtime(unixtime) + ":" + str(variable) + "|" + str(value) + "|" + str(n))
    def in_conflict(self,other):
        return self.is_up() and other.is_up() and self.get_variable() == other.get_variable()

# 1648490054..1.:a/zona
class Ocfg(ElementValue):
    def get_path(self):
        return self[self.index(':') + 1:]
    def set_path(self,new_path):
        return self.get_unixtime() + ":" + new_path
    def set(self,unixtime = None,path = None):
        if unixtime is None:
            unixtime = self.get_unixtime()
        if path is None:
            path = self.get_path()
        return Ocfg(Unixtime(unixtime) + ":" + str(path))

# 1618489855.1618489873.17186.17188:-30.77093347|-57.96592712|0|0.0
class V(ElementValue):
    def get_last_num(self):
        fp = self.index('|')
        sp = self.index('|',fp+1)
        tp = self.index('|',sp+1)
        return float(self[tp+1:])
    def get_vertex_num(self):
        fp = self.index('|')
        sp = self.index('|',fp+1)
        tp = self.index('|',sp+1)
        return int(self[sp+1:tp])
    def get_coordinates(self):
        colon = self.index(':')
        fp = self.index('|')
        sp = self.index('|',fp+1)
        longitude = float(self[colon+1:fp])
        latitude = float(self[fp+1:sp])
        return longitude, latitude
    def in_conflict(self,other):
        return self.is_up() and other.is_up() and self.get_vertex_num() == other.get_vertex_num()
    def get_point(self):
        lat, long = self.get_coordinates()
        return Point(lat,long)
    def set(self,unixtime=None,longitude=None,latitude=None,vertex_num=None,last_num = '0.0'):
        if unixtime is None:
            unixtime = self.get_unixtime()
        if longitude is None and latitude is None:
            longitude, latitude = self.get_coordinates()
        if vertex_num is None:
            vertex_num = self.get_vertex_num()
        return V(Unixtime(unixtime) + ":" + str(longitude) + "|" + str(latitude)
                   + "|" + str(vertex_num) + "|" + str(last_num))

# 1650371152..32902.:106.100.100010"
class IO(ElementValue):
    def get_other_key(self):
        return Key(self[self.index(':')+1:])
    def in_conflict(self,other):
        self.is_up() and other.is_up and self.get_other_key() == other.get_other_key()
    def set(self,unixtime=None,other_key=None):
        if unixtime is None:
            unixtime = self.get_unixtime()
        if other_key is None:
            other_key = self.get_other_key()
        return IO(Unixtime(unixtime) + ":" + Key(other_key))

# 1618489855.1618489873.17186.17188:106.1.100001
class Co(ElementValue):
    def get_con_num1(self):
        return int(self[self.index(':')+1:self.index('|')])
    def get_con_num2(self):
        fp = self.index('|')
        sp = self.index('|',fp+1)
        return int(self[sp+1:])
    def get_other_key(self):
        fp = self.index('|')
        sp = self.index('|', fp + 1)
        return Key(self[fp + 1:sp])
    def in_conflict(self,other):
        return self.is_up() and other.is_up() and self.get_other_key() == other.get_other_key()
    def set(self,unixtime=None,n1='0',other_key=None,n2='0'):
        if unixtime is None:
            unixtime = self.get_unixtime()
        if other_key is None:
            other_key = self.get_other_key()
        return Co(Unixtime(unixtime) + ":" + str(n1) + "|" + Key(other_key) + "|" + str(n2))

# 1618489855.1618489873.17186.17188:106.1.100000|0|1
class Geoidx(ElementValue):
    def __new__(cls, value='',lat = '',long=''):
        cls.latitude = lat
        cls.longitude = long
        return str.__new__(cls, value)
    def __init__(self,content='',lat = '',long=''):
        self.latitude = lat
        self.longitude = long
    def get_key(self):
        return Key(self[self.index(':') + 1:self.index('|')])
    def get_vertex_num(self):
        fp = self.index('|')
        sp = self.index('|',fp+1)
        return int(self[fp+1:sp])
    def get_vertex_total(self):
        fp = self.index('|')
        sp = self.index('|',fp+1)
        return int(self[sp+1:])
    def set_coordinates(self,lat,long):
        self.latitude = float(lat)
        self.longitude = float(long)
    def get_coordinates(self):
        return self.latitude,self.longitude
    def in_conflict(self,other):
        return self.is_up() and other.is_up() and self.get_vertex_num() == other.get_vertex_num()
    def coordinates_to_str(self):
        return f'{self.latitude} {self.longitude}'
    def set(self,unixtime=None,vertex_num=None,vertex_total=None,key=None):
        if unixtime is None:
            unixtime = self.get_unixtime()
        if vertex_num is None:
            vertex_num = self.get_vertex_num()
        if vertex_total is None:
            vertex_total = self.get_vertex_total()
        if key is None:
            key = self.get_key()
        return Geoidx(Unixtime(unixtime) + ":" + Key(key) + "|" + str(vertex_num) + "|" + str(vertex_total))

# T2 F26 C3:1648582761..31590.:106.1.100032
class Sidx(ElementValue):
    def __new__(cls, content, variable=''):
        cls.variable = variable
        return str.__new__(cls,content)
    def __init__(self, content='',variable=''):
        self.variable = variable
    def set_down(self,unixtime_down,log_down):
        unixt = self.get_unixtime().set_down(unixtime_down,log_down)
        return self.get_value() + ":" + unixt + ":" + self.get_key()
    def get_unixtime(self):
        colon1 = self.index(':')
        colon2 = self.index(':',colon1+1)
        return Unixtime(self[colon1+1:colon2])
    def get_value(self):
        return self[:self.index(':')]
    def get_variable(self):
        return self.variable
    def get_key(self):
        colon1 = self.index(':')
        colon2 = self.index(':',colon1+1)
        return Key(self[colon2+1:])
    def parse_sidx_key(self,s):
        fp = s.index('.')
        sp = s.index('.',fp+1)
        self.variable = s[fp+1:sp]
    def get_sidx_key(self):
        return f'{self.get_key().get_company_id()}.{self.variable}.sidx'
    def in_conflict(self, other):
        return self.is_up() and other.is_up() and self.get_key() == other.get_key() \
               and self.variable == other.variable
    def set(self,unixtime=None,key=None,value=None):
        if unixtime is None:
            unixtime = self.get_unixtime()
        if value is None:
            value = self.get_value()
        if key is None:
            key = self.get_key()
        return Sidx(str(value) + ":" + Unixtime(unixtime) + ":" + Key(key))

class LambdaError(Exception):
    pass
class ValuesInConflictError(LambdaError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f'You cannot add a value that gets in conflict with another already added: {self.value}'

class ElementNotInGroupError(LambdaError):
    pass