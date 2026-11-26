import time
from datetime import datetime
from rich.live import Live
from rich.console import Console
from demo_client import DemoClient
from restconf_client import RestconfClient, RestconfError
from config import Config
from monitor import Monitor
from display import dashboard

def main():
    config = Config.from_env()
    client = DemoClient() if config.demo_mode else RestconfClient(config)
    monitor = Monitor(client)
    console = Console()
    page = 0
    previous_time = None
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
                    monitor.alerts.extend(__import__('alerts').compare(monitor.previous, current))
                    monitor.previous = current
                    live.update(dashboard(current, monitor.alerts, device=config.host, mode='DEMO' if config.demo_mode else 'REAL', latency=latency, interval=config.interval, page=page))
                    page += 1
                except RestconfError as error:
                    live.update(dashboard(monitor.previous or [], monitor.alerts + [('RESTCONF', 'connection_lost')], device=config.host, mode='REAL', latency=0, interval=config.interval))
                    console.print(f'[red]{error}[/red]')
                time.sleep(config.interval)
    except KeyboardInterrupt:
        console.print('\n[green]Monitoreo finalizado correctamente.[/green]')
if __name__=='__main__': main()
