# Network Monitor

### RESTCONF · YANG · Cisco IOS XE

Monitor de interfaces de red desarrollado en Python para consultar estados operativos y detectar cambios en dispositivos compatibles con RESTCONF. El proyecto incluye un modo de demostración offline para probar el flujo completo sin depender de un dispositivo externo.

## ✨ Funcionalidades

| Funcionalidad | Descripción |
|---|---|
| Modo demo | Reproduce una secuencia de estados a partir de fixtures JSON. |
| Procesamiento YANG | Normaliza respuestas `ietf-interfaces` y campos ausentes como `N/D`. |
| Monitoreo | Conserva el estado anterior y compara consultas sucesivas. |
| Alertas | Detecta cambios operativos e incrementos de errores de entrada. |
| RESTCONF | Incluye configuración de host, puerto, credenciales y ruta del modelo. |
| Pruebas | Suite automatizada con Pytest, sin conexión a Internet. |

## 🚀 Inicio rápido

Desde la carpeta `main/`:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python main.py
```

Para abrir el menú interactivo:

```bash
python main.py --menu
```

En Linux:

```bash
cd main
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python main.py
```

> **Nota:** el modo demo es el flujo predeterminado. Permite validar la aplicación sin credenciales ni acceso a Cisco DevNet Sandbox.

## 🧪 Modo demostración

La demo reproduce tres snapshots:

1. Cinco interfaces activas con tráfico simulado.
2. `GigabitEthernet3` cambia a DOWN y `GigabitEthernet4` incrementa sus errores.
3. Recuperación de la interfaz.

```text
Demo completada: 3 alertas
```

Los datos son simulados y no representan resultados de un dispositivo real.

## ⚙️ Configuración RESTCONF

Copiar el archivo de ejemplo y completar los valores del dispositivo:

```powershell
Copy-Item .env.example .env
```

Variables principales:

| Variable | Uso |
|---|---|
| `DEVICE_HOST` | IP o hostname del dispositivo. |
| `DEVICE_PORT` | Puerto HTTPS, normalmente `443`. |
| `DEVICE_USERNAME` / `DEVICE_PASSWORD` | Credenciales RESTCONF. |
| `RESTCONF_PATH` | Ruta del modelo YANG consultado. |
| `DEMO_MODE` | Mantener `true` para demo offline. |

La integración real debe ejecutarse con `DEMO_MODE=false` y con una ruta YANG confirmada para la versión de IOS XE utilizada. Este repositorio no afirma una conexión real hasta validarla contra el Sandbox.

### Nota sobre la integración real

El cliente RESTCONF y la configuración del modo real están implementados. La validación contra el Cisco DevNet Sandbox quedó pendiente porque OpenConnect autenticó correctamente, pero Windows no pudo crear el adaptador VPN virtual (`Set up tun device failed`). Por esta razón, los resultados presentados por defecto corresponden al modo demostración y no deben confundirse con mediciones de un dispositivo real.

## 🧱 Estructura

```text
main/
├── main.py              # Punto de entrada
├── config.py            # Variables de entorno
├── demo_client.py       # Proveedor de datos simulados
├── parser.py            # Normalización de respuestas JSON/YANG
├── monitor.py           # Ciclo de monitoreo
├── alerts.py            # Detección de cambios
├── fixtures/             # Estados de demostración
├── tests/                # Pruebas automatizadas
├── requirements.txt      # Dependencias
└── .env.example          # Plantilla de configuración
```

## ✅ Estado actual

- [x] Modo demostración offline.
- [x] Detección de cambios de estado.
- [x] Detección de incrementos de errores.
- [x] Configuración base para RESTCONF.
- [x] Pruebas unitarias.
- [ ] Validación de integración contra Cisco DevNet Sandbox.
- [x] Interfaz Rich para el dashboard de consola.
- [x] Exportación de reportes CSV y JSON al finalizar el monitoreo.
- [x] Menú interactivo con consulta, alertas y configuración.

## 👥 Contexto académico

Proyecto para el curso **CE-5301 Redes de Computadoras** del Instituto Tecnológico de Costa Rica. La implementación prioriza modularidad, trazabilidad y facilidad de explicación durante la presentación.
