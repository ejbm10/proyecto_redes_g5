from parser import parse_interfaces
from alerts import compare
from demo_client import DemoClient
from monitor import Monitor
def test_missing(): assert parse_interfaces({'interfaces':{'interface':[{'name':'x'}]}})[0]['oper_status']=='N/D'
def test_alerts():
 a=parse_interfaces({'interfaces':{'interface':[{'name':'x','state':{'oper-status':'up','statistics':{'in-errors':1}}}]}}); b=parse_interfaces({'interfaces':{'interface':[{'name':'x','state':{'oper-status':'down','statistics':{'in-errors':2}}}]}}); assert len(compare(a,b))==2
def test_demo(): m=Monitor(DemoClient()); m.run(); assert len(m.alerts)==3
