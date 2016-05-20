# -*- mode: python -*-
# need to install this: http://slproweb.com/products/Win32OpenSSL.html

block_cipher = None


a = Analysis(['music.py'],
             pathex=['C:\\Users\\sashg\\PycharmProjects\\VK-P-P-Music-Project'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

for d in range(len(a.binaries)):
    if a.binaries[d][0].lower() == 'ssleay32.dll':
        print(a.binaries[d])
        a.binaries[d] = ('ssleay32.dll', 'C:\\\OpenSSL-Win32\\ssleay32.dll', 'BINARY')
    if a.binaries[d][0].lower() == 'libeay32.dll':
        print(a.binaries[d])
        a.binaries[d] = ('libeay32.dll', 'C:\\OpenSSL-Win32\\libeay32.dll', 'BINARY')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='music',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='music')
