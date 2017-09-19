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

from os import listdir
from os.path import isfile, join
assets_path = './assets'
assets = [('assets/%s' % f, assets_path + '/' + f, 'DATA') for f in listdir(assets_path) if isfile(join(assets_path, f))]
a.datas.extend(assets)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('asmminator'))
