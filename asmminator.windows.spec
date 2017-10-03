# -*- mode: python -*-
a = Analysis(['asmminator/app.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.win32/app', 'asmminator.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False )

import fnmatch
import os

assets = []
assets_path = './assets'
for root, dirnames, filenames in os.walk(assets_path):
    for filename in fnmatch.filter(filenames, '*'):
        assets.append(
            (
                os.path.join(root, filename),
                os.path.join(root[2:], filename),
                'DATA'
            )
        )

a.datas.extend(assets)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('asmminator'))
