# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Teleop-Func_with_stop.py'],
             pathex=['/home/sergi/GitHub/TeleopApp_Build'],
             binaries=[],
             datas=[('ModBus_server_data.xlsx', '.')],
             hiddenimports=['URCommunicationClass.py', 'URDashBoardClass.py', 'URModbusClass.py', 'URScriptsTcpIpClass.py'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Teleop-Func_with_stop',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
