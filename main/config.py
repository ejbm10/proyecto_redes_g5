import os
from dataclasses import dataclass
from dotenv import load_dotenv
@dataclass
class Config:
    host:str='localhost'; port:int=443; username:str=''; password:str=''; restconf_path:str='/restconf/data/ietf-interfaces:interfaces'; demo_mode:bool=True; timeout:float=10; verify_tls:bool=True; interval:float=5
    @classmethod
    def from_env(cls):
        load_dotenv()
        yes=lambda x:x.lower() in ('1','true','yes','si')
        return cls(os.getenv('DEVICE_HOST','localhost'),int(os.getenv('DEVICE_PORT','443')),os.getenv('DEVICE_USERNAME',''),os.getenv('DEVICE_PASSWORD',''),os.getenv('RESTCONF_PATH',cls.restconf_path),yes(os.getenv('DEMO_MODE','true')),float(os.getenv('REQUEST_TIMEOUT','10')),yes(os.getenv('VERIFY_TLS','true')),float(os.getenv('MONITOR_INTERVAL','5')))
