##### include mydir in distribution #######
def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
                print d
            else:
              print 'blah\n'
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))
   
    print '\n'
    return extra_datas
###########################################
# -*- mode: python -*-
a = Analysis(['awesomeStart.py'],
             pathex=['meshController',
             'extensionController',
             'meshController/mm',
             'meshController/pythonApi',
             'static'
             ],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

a.datas += extra_datas('extensionController/')
a.datas += extra_datas('meshController/')
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break


pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Wizard.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True,
          icon='logo.ico')

coll = COLLECT(exe,
               Tree('static',prefix='static'),
               Tree('history',prefix='history'),
               Tree('reference',prefix='reference'),
               Tree('socket',prefix='socket'),
               strip=None,
               upx=True,
               name='awsomeStart')

