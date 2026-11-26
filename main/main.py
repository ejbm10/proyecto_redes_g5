import time
import sys
from rich.live import Live
from rich.console import Console
from demo_client import DemoClient
from restconf_client import RestconfClient, RestconfError
from config import Config
from monitor import Monitor
from display import dashboard
from report import write_reports
from datetime import datetime

def main():
    config = Config.from_env()
    client = DemoClient() if config.demo_mode else RestconfClient(config)
    monitor = Monitor(client)
    console = Console()
    page = 0
    previous_time = None
    snapshots = []
    response_times = []
    try:
        with Live(console=console, refresh_per_second=4, screen=False) as live:
            while True:
                try:
                    current, latency = client.get_interfaces()
                    current_time = time.monotonic()
                    elapsed = current_time - previous_time if previous_time else 0
                    if elapsed > 0 and monitor.previous:
                        previous_by_name = {item.get('name'): item for item in monitor.previous}
                        for item in current:
                            previous = previous_by_name.get(item.get('name'))
                            if not previous:
                                continue
                            for counter, metric in (('rx_bytes', 'rx_mbps'), ('tx_bytes', 'tx_mbps')):
                                before, after = previous.get(counter), item.get(counter)
                                if before is not None and after is not None and after >= before:
                                    item[metric] = round((after - before) * 8 / elapsed / 1_000_000, 2)
                                else:
                                    item[metric] = 'N/D'
                    previous_time = current_time
                    response_times.append(latency)
                    snapshots.append({'timestamp': datetime.now().isoformat(), 'interfaces': current})
                    monitor.alerts.extend(__import__('alerts').compare(monitor.previous, current))
                    monitor.previous = current
                    live.update(dashboard(current, monitor.alerts, device=config.host, mode='DEMO' if config.demo_mode else 'REAL', latency=latency, interval=config.interval, page=page))
                    page += 1
                except RestconfError as error:
                    live.update(dashboard(monitor.previous or [], monitor.alerts + [('RESTCONF', 'connection_lost')], device=config.host, mode='REAL', latency=0, interval=config.interval))
                    console.print(f'[red]{error}[/red]')
                time.sleep(config.interval)
    except KeyboardInterrupt:
        mode='DEMO' if config.demo_mode else 'REAL'
        metrics={'queries':len(snapshots),'successful_queries':len(snapshots),'failed_queries':0,'avg_response_ms':sum(response_times)/len(response_times) if response_times else 0,'min_response_ms':min(response_times) if response_times else 0,'max_response_ms':max(response_times) if response_times else 0}
        paths=write_reports('reports',config.host,mode,snapshots,monitor.alerts,metrics)
        console.print(f'\n[green]Monitoreo finalizado correctamente.[/green] Reportes: {paths[0]}, {paths[1]}')
def menu():
    config=Config.from_env(); client=DemoClient() if config.demo_mode else RestconfClient(config); monitor=Monitor(client); console=Console()
    while True:
        console.print('\n[bold green]NETWORK MONITOR[/bold green]  1) Conexión  2) Interfaces  3) Monitoreo  4) Alertas  5) Reportes  6) Configuración  7) Salir')
        choice=input('Opción: ').strip()
        if choice in ('1','2'):
            try: console.print(monitor.poll())
            except RestconfError as error: console.print(f'[red]{error}[/red]')
        elif choice=='3': main()
        elif choice=='4': console.print(monitor.alerts or 'Sin alertas')
        elif choice=='5': console.print('Los reportes se generan al finalizar el monitoreo con Ctrl+C.')
        elif choice=='6': console.print({**config.__dict__, 'password':'********' if config.password else '<vacía>'})
        elif choice=='7': break
if __name__=='__main__': menu() if '--menu' in sys.argv else main()
