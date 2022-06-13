from redis import Redis
from redis import ConnectionError

# prueba la conexion, si anda sin problemas la retorna
def get_connection(host, port):
    try:
        db = Redis(host=host, port=int(port), decode_responses=True,encoding="ISO-8859-1")
        db.ping()
        return db
    except ConnectionError:
        return None