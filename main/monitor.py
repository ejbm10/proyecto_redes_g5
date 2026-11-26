from alerts import compare
class Monitor:
    def __init__(self,c): self.c=c; self.previous=None; self.alerts=[]
    def poll(self):
        current,_=self.c.get_interfaces(); self.alerts+=compare(self.previous,current); self.previous=current; return current
    def run(self,cycles=3):
        for _ in range(cycles): self.poll()
