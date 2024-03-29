pyinstaller --onefile \
--add-data "glances/*.py:glances/" \
--add-data "glances/plugins/*.py:glances/plugins/" \
--add-data "glances/plugins/core/*.py:glances/plugins/core" \
--add-data "glances/plugins/plugin/*.py:glances/plugins/plugin" \
--add-data "glances/plugins/cpu/*.py:glances/plugins/cpu/" \
--add-data "glances/plugins/alert/*.py:glances/plugins/alert/" \
--add-data "glances/plugins/amps/*.py:glances/plugins/amps/" \
--add-data "glances/plugins/cloud/*.py:glances/plugins/cloud/" \
--add-data "glances/plugins/connections/*.py:glances/plugins/connections/" \
--add-data "glances/plugins/containers/*.py:glances/plugins/containers/" \
--add-data "glances/plugins/diskio/*.py:glances/plugins/diskio/" \
--add-data "glances/plugins/folders/*.py:glances/plugins/folders/" \
--add-data "glances/plugins/fs/*.py:glances/plugins/fs/" \
--add-data "glances/plugins/gpu/*.py:glances/plugins/gpu/" \
--add-data "glances/plugins/help/*.py:glances/plugins/help/" \
--add-data "glances/plugins/ip/*.py:glances/plugins/ip/" \
--add-data "glances/plugins/irq/*.py:glances/plugins/irq/" \
--add-data "glances/plugins/load/*.py:glances/plugins/load/" \
--add-data "glances/plugins/mem/*.py:glances/plugins/mem/" \
--add-data "glances/plugins/memswap/*.py:glances/plugins/memswap/" \
--add-data "glances/plugins/network/*.py:glances/plugins/network/" \
--add-data "glances/plugins/now/*.py:glances/plugins/now/" \
--add-data "glances/plugins/percpu/*.py:glances/plugins/percpu/" \
--add-data "glances/plugins/ports/*.py:glances/plugins/ports/" \
--add-data "glances/plugins/processcount/*.py:glances/plugins/processcount/" \
--add-data "glances/plugins/processlist/*.py:glances/plugins/processlist/" \
--add-data "glances/plugins/psutilversion/*.py:glances/plugins/psutilversion/" \
--add-data "glances/plugins/quicklook/*.py:glances/plugins/quicklook/" \
--add-data "glances/plugins/raid/*.py:glances/plugins/raid/" \
--add-data "glances/plugins/sensors/*.py:glances/plugins/sensors/" \
--add-data "glances/plugins/smart/*.py:glances/plugins/smart/" \
--add-data "glances/plugins/system/*.py:glances/plugins/system/" \
--add-data "glances/plugins/uptime/*.py:glances/plugins/uptime/" \
--add-data "glances/plugins/wifi/*.py:glances/plugins/wifi/" \
--add-data "glances/plugins/containers/engines/*.py:glances/plugins/containers/engines/" \
--add-data "glances/plugins/sensors/sensor/*.py:glances/plugins/sensors/sensor/" \
--add-data "glances/exports/*.py:glances/exports/" \
--add-data "glances/amps/*.py:glances/amps/" \
--add-data "glances/outputs/*.py:glances/outputs/" \
--add-data "glances/outputs/static/templates/*:glances/outputs/static/templates/" \
--add-data "glances/outputs/static/css/*:glances/outputs/static/css/" \
--add-data "glances/outputs/static/images/*:glances/outputs/static/images/" \
--add-data "glances/outputs/static/js/*:glances/outputs/static/js/" \
--add-data "glances/exports/json/*.py:glances/exports/json/" \
--add-data "glances/outputs/static/public/*:glances/outputs/static/public/" \
run.py
