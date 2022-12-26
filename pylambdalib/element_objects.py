from abc import ABC, abstractmethod
from shapely.geometry import Polygon, Point
from pylambdalib.lambdaexceptions import ElementNotInGroupError, ValuesInConflictError

class Key:
    def __init__(self,s=''):
        self.company_id = ''
        self.network_id = ''
        self.object_id = ''
        if s != '':
            self.parse(s)
    def get_geoidx_key(self):
        return f'{self.company_id}.{self.network_id}:geoidx'
    def parse(self,s): ##c_id.n_id.o_id
        fp = s.index('.')
        sp = s.index('.',fp+1)
        self.company_id = int(s[:fp])
        self.network_id = int(s[fp+1:sp])
        self.object_id = int(s[sp+1:])
    def __str__(self):
        return f'{self.company_id}.{self.network_id}.{self.object_id}'
    def __eq__(self, other):
        return str(self) == str(other)
    def __hash__(self):
        return hash(str(self))
    ##implement gd, ld, ge, le

class Unixtime:
    def __init__(self):
        self.unixtime_up = ''
        self.unixtime_down = ''
        self.log_up = ''
        self.log_down = ''
    def parse(self,s):
        fp = s.index('.')
        sp = s.index('.',fp+1)
        tp = s.index('.',sp+1)
        self.unixtime_up = s[:fp]
        self.unixtime_down = s[fp+1:sp]
        self.log_up = s[sp+1:tp]
        self.log_down = s[tp+1:]
    def is_up(self):
        return self.unixtime_down == '' and self.log_down == ''
    def is_down(self):
        return not self.is_up()
    def __str__(self):
        return f'{self.unixtime_up}.{self.unixtime_down}.{self.log_up}.{self.log_down}'
    def __eq__(self, other):
        return str(self) == str(other)

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
        self.key.parse(s)
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
                ordered_vertices[vertice.n] = [vertice.latitude,vertice.longitude]
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

class ElementValue(ABC):
    def __init__(self):
        self.unixtime = Unixtime()
    def is_up(self):
        return self.unixtime.is_up()
    def in_conflict(self,other):
        return self.is_up() and other.is_up()
    @abstractmethod
    def parse(self,s):
        pass
    def __eq__(self, other):
        return str(self) == str(other)
    @abstractmethod
    def __str__(self):
        pass

def check_quotes(s):
    s = s.replace('"', '')
    s = s.replace("'", "")
    s = s.replace("\t", "")
    return s

class Val(ElementValue):
    def __init__(self,s=''):
        super(Val, self).__init__()
        self.var = ''
        self.val = ''
        if s != '':
            self.parse(s)
    def parse(self,s):
        s = check_quotes(s)
        colon = s.index(':')
        fp = s.index('|')
        sp = s.index('|',fp+1)
        self.unixtime.parse(s[:colon])
        self.var = s[colon+1:fp]
        self.val = s[fp+1:sp]
    def in_conflict(self,other):
        return self.is_up() and other.is_up() and self.var == other.var
    def __str__(self):
        return f'{self.unixtime}:{self.var}|{self.val}|0'

class Ocfg(ElementValue):
    def __init__(self,s=''):
        super(Ocfg, self).__init__()
        self.path = ''
        if s != '':
            self.parse(s)
    def parse(self,s):
        s = check_quotes(s)
        colon = s.index(':')
        self.unixtime.parse(s[:colon])
        self.path = s[colon+1:]
    def __str__(self):
        return f'{self.unixtime}:{self.path}'

class V(ElementValue):
    def __init__(self,s=''):
        super(V, self).__init__()
        self.n = None
        self.last_num = 0.0
        self.latitude = None
        self.longitude = None
        if s != '':
            self.parse(s)
    def parse(self,s):
        s = check_quotes(s)
        colon = s.index(':')
        fp = s.index('|')
        sp = s.index('|',fp+1)
        tp = s.index('|',sp+1)
        self.unixtime.parse(s[:colon])
        self.latitude = float(s[colon+1:fp])
        self.longitude = float(s[fp+1:sp])
        self.n = int(s[sp+1:tp])
        self.last_num = float(s[tp+1:])
    def in_conflict(self,other):
        return self.is_up() and other.is_up() and self.n == other.n
    def get_point(self):
        return Point(self.latitude,self.longitude)
    def __str__(self):
        return f'{self.unixtime}:{self.latitude}|{self.longitude}|{self.n}|{self.last_num}'

class IO(ElementValue):
    def __init__(self,s=''):
        super(IO, self).__init__()
        self.other_key = Key()
        if s != '':
            self.parse(s)
    def parse(self,s):
        s = check_quotes(s)
        colon = s.index(':')
        self.unixtime.parse(s[:colon])
        self.other_key = Key(s[colon+1:])
    def in_conflict(self,other):
        self.is_up() and other.is_up and self.other_key == other.other_key
    def __str__(self):
        return f'{self.unixtime}:{self.other_key}'

class Co(ElementValue):
    def __init__(self,s=''):
        super(Co, self).__init__()
        self.other_key = Key()
        self.conn_num_1 = None
        self.conn_num_2 = None
        if s != '':
            self.parse(s)
    def parse(self,s):
        s = check_quotes(s)
        colon = s.index(':')
        fp = s.index('|')
        sp = s.index('|',fp+1)
        self.unixtime.parse(s[:colon])
        self.conn_num_1 = int(s[colon+1:fp])
        self.other_key = Key(s[fp+1:sp])
        self.conn_num_2 = int(s[sp+1:])
    def in_conflict(self,other):
        return self.is_up() and other.is_up() and self.other_key == other.other_key
    def __str__(self):
        return f'{self.unixtime}:{self.other_key}'

class Geoidx(ElementValue):
    def __init__(self,s='',latitude = None, longitude = None):
        super(Geoidx, self).__init__()
        self.key = Key()
        self.n = None
        self.n_max = None
        self.latitude = latitude
        self.longitude = longitude
        if s != '':
            self.parse(s)
    def parse(self,s):
        s = check_quotes(s)
        colon = s.index(':')
        fp = s.index('|')
        sp = s.index('|',fp+1)
        self.unixtime.parse(s[:colon])
        self.key.parse(s[colon+1:fp])
        self.n = int(s[fp+1:sp])
        self.n_max = int(s[sp+1:])
    def set_coordinates(self,long,lat):
        self.latitude = float(lat)
        self.longitude = float(long)
    def in_conflict(self,other):
        return self.is_up() and other.is_up() and self.n == other.n
    def __str__(self):
        return f'{self.unixtime}:{self.key}|{self.n}|{self.n_max}'
    def coordinates_to_str(self):
        return f'{self.longitude} {self.latitude}'

class Sidx(ElementValue):
    def __init__(self, s=''):
        super(Sidx, self).__init__()
        self.value = ''
        self.key = Key()
        self.company_id = ''
        self.variable = ''
        if s != '':
            self.parse(s)

    def parse_sidx_key(self,s):
        fp = s.index('.')
        sp = s.index('.',fp+1)
        self.company_id = s[:fp]
        self.variable = s[fp+1:sp]

    def get_sidx_key(self):
        return f'{self.company_id}.{self.variable}.sidx'

    def parse(self, s):
        s = check_quotes(s)
        colon1 = s.index(':')
        colon2 = s.index(':',colon1+1)
        self.value = s[:colon1]
        self.unixtime.parse(s[colon1+1:colon2])
        self.key.parse(s[colon2+1:])

    def in_conflict(self, other):
        return self.is_up() and other.is_up() and self.key == other.key

    def __str__(self):
        return f'{self.value}:{self.unixtime}:{self.key}'