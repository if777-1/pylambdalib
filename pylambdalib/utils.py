from redis import Redis
from redis import ConnectionError
from pylambdalib.element_objects import Val

# prueba la conexion, si anda sin problemas la retorna
def get_connection(host, port):
    try:
        db = Redis(host=host, port=int(port), decode_responses=True,encoding="ISO-8859-1")
        db.ping()
        return db
    except ConnectionError:
        return None

def get_company_name(db, company_id):
    for s_val in db.smembers("0.2."+str(company_id) + ":val"):
        val = Val(s_val)
        if val.var == "@name":
            return val.val
    return "Unknown company"

def get_area_name(db,area_id):
    for s_val in db.smembers(str(area_id)+":val"):
        val = Val(s_val)
        if val.is_up() and val.var == "@oName":
            return val.val
    return "Unknown area"

def check_quotes(s):
    s = s.replace('"', '')
    s = s.replace("'", "")
    s = s.replace("\t", " ")
    s = s.replace("\n"," ")
    s = s.replace("\r", " ")
    s = s.replace(":", " ")
    s = s.replace("|", " ")
    s = s.replace('Á','A')
    s = s.replace('á','a')
    s = s.replace('É', 'E')
    s = s.replace('é', 'e')
    s = s.replace('Í', 'I')
    s = s.replace('í', 'i')
    s = s.replace('Ó', 'O')
    s = s.replace('ó', 'o')
    s = s.replace('Ú', 'U')
    s = s.replace('ú', 'u')
    s = s.replace('Ñ', 'N')
    s = s.replace('ñ', 'n')
    return s

def get_foSide_key(s):
    return s[s.index('-') + 1:]

# recibe un string del tipo clave:smth y retorna solamente la clave
def get_key_only(key):
    return key[:key.index(':')]