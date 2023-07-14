# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[('glances/*.py', 'glances/'), ('glances/plugins/*.py', 'glances/plugins/'), ('glances/plugins/core/*.py', 'glances/plugins/core'), ('glances/plugins/plugin/*.py', 'glances/plugins/plugin'), ('glances/plugins/cpu/*.py', 'glances/plugins/cpu/'), ('glances/plugins/alert/*.py', 'glances/plugins/alert/'), ('glances/plugins/amps/*.py', 'glances/plugins/amps/'), ('glances/plugins/cloud/*.py', 'glances/plugins/cloud/'), ('glances/plugins/connections/*.py', 'glances/plugins/connections/'), ('glances/plugins/containers/*.py', 'glances/plugins/containers/'), ('glances/plugins/diskio/*.py', 'glances/plugins/diskio/'), ('glances/plugins/folders/*.py', 'glances/plugins/folders/'), ('glances/plugins/fs/*.py', 'glances/plugins/fs/'), ('glances/plugins/gpu/*.py', 'glances/plugins/gpu/'), ('glances/plugins/help/*.py', 'glances/plugins/help/'), ('glances/plugins/ip/*.py', 'glances/plugins/ip/'), ('glances/plugins/irq/*.py', 'glances/plugins/irq/'), ('glances/plugins/load/*.py', 'glances/plugins/load/'), ('glances/plugins/mem/*.py', 'glances/plugins/mem/'), ('glances/plugins/memswap/*.py', 'glances/plugins/memswap/'), ('glances/plugins/network/*.py', 'glances/plugins/network/'), ('glances/plugins/now/*.py', 'glances/plugins/now/'), ('glances/plugins/percpu/*.py', 'glances/plugins/percpu/'), ('glances/plugins/ports/*.py', 'glances/plugins/ports/'), ('glances/plugins/processcount/*.py', 'glances/plugins/processcount/'), ('glances/plugins/processlist/*.py', 'glances/plugins/processlist/'), ('glances/plugins/psutilversion/*.py', 'glances/plugins/psutilversion/'), ('glances/plugins/quicklook/*.py', 'glances/plugins/quicklook/'), ('glances/plugins/raid/*.py', 'glances/plugins/raid/'), ('glances/plugins/sensors/*.py', 'glances/plugins/sensors/'), ('glances/plugins/smart/*.py', 'glances/plugins/smart/'), ('glances/plugins/system/*.py', 'glances/plugins/system/'), ('glances/plugins/uptime/*.py', 'glances/plugins/uptime/'), ('glances/plugins/wifi/*.py', 'glances/plugins/wifi/'), ('glances/plugins/containers/engines/*.py', 'glances/plugins/containers/engines/'), ('glances/plugins/sensors/sensor/*.py', 'glances/plugins/sensors/sensor/'), ('glances/exports/*.py', 'glances/exports/'), ('glances/amps/*.py', 'glances/amps/'), ('glances/outputs/*.py', 'glances/outputs/'), ('glances/outputs/static/templates/*', 'glances/outputs/static/templates/'), ('glances/outputs/static/css/*', 'glances/outputs/static/css/'), ('glances/outputs/static/images/*', 'glances/outputs/static/images/'), ('glances/outputs/static/js/*', 'glances/outputs/static/js/'), ('glances/exports/json/*.py', 'glances/exports/json/'), ('glances/outputs/static/public/*', 'glances/outputs/static/public/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='run',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
