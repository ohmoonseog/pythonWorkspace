import os
import zipfile
import configparser
from datetime import datetime
from progress.bar import Bar



'''
https://pypi.org/project/progress/

cd C:\Python38\Scripts
pyinstaller -F --distpath c:/workSpace/pythonWorkspace/study/src_back --workpath c:/workSpace/pythonWorkspace/study/src_back/build c:/workSpace/pythonWorkspace/study/src_back/zipAndBackup.py
'''



def zipdir(path, zipf):
    fileTotCount = sum([len(files) for r, d, files in os.walk(path)])
    suffix = '%(percent)d%% [%(elapsed_td)s / %(eta)d / %(eta_td)s]'
    bar = Bar('Processing', max=fileTotCount,suffix=suffix)
    for root, dirs, files in os.walk(path):
        for file in files:
            bar.next()
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
  
if __name__ == '__main__':
    backupBasePath = "C:\\workSpace\\src_back"
    toDate = datetime.now().strftime("%Y_%m_%d")
    zipFilePath = backupBasePath + "\\" + 'cgv_fanpage_mobile_{0}.zip'.format(toDate)
    zipf = zipfile.ZipFile(zipFilePath, 'w', zipfile.ZIP_DEFLATED)
    workPath = "C:\\workSpace\\eGovFrameDev-3.9.0-64bit\\workspace\\cgv_fanpage_mobile"

    config = configparser.ConfigParser()
    config.read('backInfo.ini')

    zipdir(workPath, zipf)
    zipf.close()

