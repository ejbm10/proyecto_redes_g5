def parse_interfaces(payload):
    root=payload.get('ietf-interfaces:interfaces',payload.get('interfaces',payload)); rows=root.get('interface',[]) if isinstance(root,dict) else []
    if isinstance(rows,dict): rows=[rows]
    return [{'name':x.get('name','N/D'),'oper_status':x.get('state',{}).get('oper-status','N/D'),'input_errors':x.get('state',{}).get('statistics',{}).get('in-errors'),'rx_mbps':x.get('state',{}).get('rx-mbps','N/D'),'tx_mbps':x.get('state',{}).get('tx-mbps','N/D')} for x in rows]
