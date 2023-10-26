import redis
from redis.exceptions import ConnectionError, ResponseError, NoPermissionError
from pylambdalib.element_objects import Val
from pylambdalib.lambdaexceptions import EnviromentVariableNotFoundError, IncorrectRedisUserOrPassword, NoPermissionForRedisUser
# from dotenv import load_dotenv
import os

def get_connection(host, port):
    try:
        db = redis.Redis(host=host, port=int(port), decode_responses=True,encoding="ISO-8859-1")
        db.ping()
        return db
    except ConnectionError:
        return None

# USERENV = "REDIS-USER"
# PASSENV = "REDIS-PASSWORD"

# prueba la conexion, si anda sin problemas la retorna
# def get_connection(host, port, username = None, password = None):
#     if username is None or password is None:
#         load_dotenv()
#         username = os.getenv(USERENV)
#         password = os.getenv(PASSENV)
#     if username is None:
#         raise EnviromentVariableNotFoundError(USERENV)
#     if password is None:
#         raise EnviromentVariableNotFoundError(PASSENV)
#     auth_command = f"AUTH {username} {password}"
#     try:
#         db = redis.Redis(
#             host=host,
#             port=int(port),
#             decode_responses=True,
#             encoding="ISO-8859-1"
#         )
#         db.execute_command(auth_command)
#         db.ping()
#         return db
#     except NoPermissionError:
#         raise NoPermissionForRedisUser(username)
#     except ConnectionError:
#         return None
#     except ResponseError:
#         raise IncorrectRedisUserOrPassword

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


def get_value(db, key, var):
    for val in db.smembers(key + ":val"):
        val = Val(val)
        if not val.is_up() or val.get_variable() != var:
            continue
        return val.get_value()

def get_gis_id(db, id_odf):
    while True:
        id_nodo = get_value(db ,id_odf, '@io')
        nodo = id_nodo.split(".")
        if nodo[1] != "100":
            return id_nodo
        id_odf = id_nodo