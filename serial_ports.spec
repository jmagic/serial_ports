# -*- mode: python -*-
a = Analysis(['serial_ports.py'],
             pathex=['C:\\Users\\jim.maciejewski\\Documents\\serial_ports'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('dsub.png', 'dsub.png', 'DATA')]
a.datas += [('dsub.ico', 'dsub.ico', 'DATA')]

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='serial_ports.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='dsub.ico')


coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='serial_ports')

