# -*- mode: python -*-
a = Analysis(['serial_ports.pyw'],
             pathex=['C:\\Users\\jim.maciejewski\\Documents\\serial_ports'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='serial_ports.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
