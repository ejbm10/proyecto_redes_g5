from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns

def _card(label, value, color='white'):
    return Panel(Text(str(value), style=f'bold {color}', justify='center'), title=label, border_style='grey50', expand=True)

def dashboard(snapshot, alerts, device='Cisco IOS XE', mode='DEMO', latency=0.0, interval=5, page=0, page_size=18):
    interfaces = snapshot or []
    up = sum(str(i.get('oper_status', '')).lower() == 'up' for i in interfaces)
    down = sum(str(i.get('oper_status', '')).lower() == 'down' for i in interfaces)
    total_pages = max(1, (len(interfaces) + page_size - 1) // page_size)
    page = page % total_pages
    visible = interfaces[page * page_size:(page + 1) * page_size]
    header = Text('▣  NETWORK MONITOR v1.0', style='bold green')
    connection = Text('● CONNECTED', style='green')
    title = Table.grid(expand=True); title.add_column(); title.add_column(justify='right'); title.add_row(header, connection)
    subtitle = Text(f'{device} | RESTCONF | YANG | MODO {mode}', style='dim')
    cards = Columns([_card('Total interfaces', len(interfaces), 'white'), _card('Operativas', up, 'green'), _card('Inactivas', down, 'red')], equal=True, expand=True)
    table = Table(show_header=True, header_style='dim', expand=True, box=None)
    for column in ('INTERFAZ', 'ESTADO', 'RX Mbps', 'TX Mbps', 'ERRORES'): table.add_column(column)
    for item in visible:
        status = str(item.get('oper_status', 'N/D')).lower(); style = 'green' if status == 'up' else 'red' if status == 'down' else 'grey50'
        errors = item.get('input_errors') or 0
        table.add_row(item.get('name','N/D'), Text(status.upper(), style=style), str(item.get('rx_mbps','N/D')), str(item.get('tx_mbps','N/D')), Text(str(errors), style='yellow' if errors else 'white'))
    events = Text('EVENT LOG\n', style='bold yellow')
    for event in alerts[-5:]:
        interface, event_type = event[0], event[1]
        description = {
            'oper_status_changed': 'Cambio de estado operativo',
            'errors_increased': 'Aumento de errores',
            'interface_added': 'Interfaz nueva detectada',
            'interface_removed': 'Interfaz eliminada',
            'connection_lost': 'Comunicación perdida',
            'connection_restored': 'Comunicación restablecida',
        }.get(event_type, event_type)
        style = 'red' if event_type == 'oper_status_changed' else 'yellow'
        events.append(f'[{interface}] {description}\n', style=style)
    if not alerts: events.append('Sin eventos registrados\n', style='dim')
    footer = Text(f'Página {page + 1}/{total_pages} | Mostrando {len(visible)} de {len(interfaces)} | Polling: {interval}s | Latency: {latency:.0f}ms | Ctrl+C para finalizar', style='dim')
    return Group(title, subtitle, cards, table, Panel(events, border_style='grey50'), footer)
