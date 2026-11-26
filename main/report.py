import csv, json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

def write_reports(directory, device, mode, snapshots, alerts, metrics):
    target=Path(directory); target.mkdir(exist_ok=True)
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S'); prefix=target/f'{device.replace(" ","_")}_{stamp}'
    interfaces=[{'device':device,'mode':mode,'timestamp':s['timestamp'],**item} for s in snapshots for item in s['interfaces']]
    with (prefix.with_name(prefix.name+'_interfaces.csv')).open('w',newline='',encoding='utf-8') as stream:
        fields=list(interfaces[0]) if interfaces else ['device','mode','timestamp','name']; writer=csv.DictWriter(stream,fieldnames=fields); writer.writeheader(); writer.writerows(interfaces)
    with (prefix.with_name(prefix.name+'_alerts.csv')).open('w',newline='',encoding='utf-8') as stream:
        fields=['interface','event_type']; writer=csv.DictWriter(stream,fieldnames=fields); writer.writeheader(); writer.writerows({'interface':a[0],'event_type':a[1]} for a in alerts)
    payload={'device':device,'mode':mode,'snapshots':snapshots,'alerts':[{'interface':a[0],'event_type':a[1]} for a in alerts],'metrics':metrics}
    json_path=prefix.with_name(prefix.name+'.json'); json_path.write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding='utf-8')
    return str(json_path), str(prefix.with_name(prefix.name+'_interfaces.csv'))
