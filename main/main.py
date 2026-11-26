import time
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
    try:
        with Live(console=console, refresh_per_second=4, screen=False) as live:
            while True:
                try:
                    current, latency = client.get_interfaces()
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
