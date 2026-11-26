import json
from pathlib import Path
from parser import parse_interfaces
class DemoClient:
    def __init__(self): self.files=sorted(Path('fixtures').glob('demo_*.json')); self.i=0
    def get_interfaces(self):
        f=self.files[min(self.i,len(self.files)-1)]; self.i+=1; return parse_interfaces(json.loads(f.read_text())),0.1
