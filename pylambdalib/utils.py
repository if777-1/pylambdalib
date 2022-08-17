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
