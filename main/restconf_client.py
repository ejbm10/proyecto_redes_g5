import time
import requests
from parser import parse_interfaces

class RestconfError(RuntimeError):
    pass

class RestconfClient:
    def __init__(self, config):
        self.config=config
        self.session=requests.Session()
        self.session.auth=(config.username, config.password)
        self.session.headers.update({'Accept':'application/yang-data+json', 'Content-Type':'application/yang-data+json'})

    def get_interfaces(self):
        url=f'https://{self.config.host}:{self.config.port}{self.config.restconf_path}'
        started=time.perf_counter()
        try:
            response=self.session.get(url, timeout=self.config.timeout, verify=self.config.verify_tls)
        except requests.Timeout as exc:
            raise RestconfError(f'Tiempo de espera agotado al consultar {url}') from exc
        except requests.RequestException as exc:
            raise RestconfError(f'No se pudo conectar con el dispositivo: {exc}') from exc
        elapsed=(time.perf_counter()-started)*1000
        if not 200 <= response.status_code < 300:
            raise RestconfError(f'RESTCONF respondió HTTP {response.status_code}: {response.text[:200]}')
        try:
            return parse_interfaces(response.json()), elapsed
        except ValueError as exc:
            raise RestconfError('El dispositivo devolvió JSON inválido') from exc
