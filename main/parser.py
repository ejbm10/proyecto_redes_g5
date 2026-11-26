def normalize_status(value):
    status=str(value or 'N/D').lower()
    if status in ('up','if-oper-state-ready','if-oper-state-up','if-state-up','true') or status.endswith('-up'):
        return 'up'
    if status in ('down','if-oper-state-lower-layer-down','if-oper-state-down','if-state-down','false') or status.endswith('-down'):
        return 'down'
    return 'N/D'

def parse_interfaces(payload):
    root=payload.get('Cisco-IOS-XE-interfaces-oper:interfaces', payload.get('ietf-interfaces:interfaces', payload.get('interfaces', payload)))
    rows=root.get('interface',[]) if isinstance(root,dict) else []
    if isinstance(rows,dict): rows=[rows]
    result=[]
    for item in rows:
        # IOS XE may namespace the operational state according to RFC 7950.
        state=item.get('ietf-interfaces:interface-state', item.get('Cisco-IOS-XE-interfaces-oper:interface-state', item.get('state', {})))
        if not state and any(key in item for key in ('oper-status', 'input-errors', 'output-errors')):
            state=item
        statistics=state.get('statistics', {}) if isinstance(state, dict) else {}
        result.append({
            'name': item.get('name', 'N/D'),
            'oper_status': normalize_status(state.get('oper-status', 'N/D')),
            'admin_status': item.get('enabled', 'N/D'),
            'input_errors': statistics.get('in-errors', item.get('input-errors')),
            'output_errors': statistics.get('out-errors', item.get('output-errors')),
            'rx_mbps': state.get('rx-mbps', 'N/D'),
            'tx_mbps': state.get('tx-mbps', 'N/D'),
        })
    return result
