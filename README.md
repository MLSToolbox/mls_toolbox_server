# MLS Toolbox Server (Gateway)

Gateway HTTP del MLS Toolbox. Recibe peticiones del cliente y las reenvía a:
- `mls_code_generator`
- `mls_toolbox_code_assessment`

## Endpoints

- `GET /` - Health check básico (`hello from mls_toolbox_server`)
- Rutas proxy:
  - `/api/create_app`
  - `/api/test_create_app`
  - `/api/get_config`
  - `/api/get_base_editor`
  - `/api/get_editor`
  - `/api/get_available_editor`
  - `/api/upload`
  - `/api/analyze/<uuid>`

## Configuración

Variables principales:
- `HOST` (default: `0.0.0.0`)
- `PORT` (default: `5000`)
- `DEBUG` (default: `False`)
- `CODE_GENERATOR_URL`
- `CODE_ASSESSMENT_URL`

Archivos de ejemplo:
- `.env.local.example`
- `.env.development.example`
- `.env.production.example`

## Ejecución local

```bash
pip3 install -r requirements.txt
python3 app/server.py
```

## Docker

```bash
./docker_run.sh --env=local
```
