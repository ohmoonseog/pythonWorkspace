import os, io , time
import subprocess as sproc
from datetime import datetime
from lars import apache
from multiprocessing import Pool , Lock
from functools import partial

data_path = ""
terminated = ","
file_name = ""
accessJob = "Y"
loadJob = "Y"
load_type = ""
#log_path = "C:\\workSpace\\Weblog"
#log_path = "C:\\workSpace\\prd01Weblog"
#log_path = "C:/workSpace/Urllog/WAS02"
#log_gbn = ""
data_name = ""
#log_data = { "file_gbn" : ["W01","W02","A01"] , "file_path" : ["C:/workSpace/Urllog/WEB01","C:/workSpace/Urllog/WEB02","C:/workSpace/Urllog/WAS01"]}
log_data = { "file_gbn" : ["W01","W02"] , "file_path" : ["C:/workSpace/Urllog/WEB01","C:/workSpace/Urllog/WEB02"]}

def fn_file_delete():
    global data_name
    with io.open(data_name , "w" , encoding="utf-8") as outfile:
        pass
    outfile.close()

def fn_file_create(log_gbn,fileList):
    global terminated
    startTime = int(time.time())
    log_file = fileList.get("log_file")
    data_name = fileList.get("data_name")
    print("log --> cvs data_name = [{0}] , log_filelog_file = [{1}]".format( data_name, log_file) ,end="")
    proc = os.getpid()
    idx = 0
    with io.open(data_name , "a" , encoding="utf-8") as outfile:
        with io.open(log_file, 'r',encoding="utf-8") as infile:
            with apache.ApacheSource(infile) as source:
                for row in source:
                    if ( row.status != 408  ):
                        file = ""
                        ext = ""
                        path_str = row.request.url.path_str
                        if ( "." in path_str):
                            file = path_str[:path_str.rindex(".")]
                            ext = path_str[path_str.rindex(".")+1:]
                        else :
                            file = path_str
                        if ( 
                             not file.startswith("/favicon") and 
                             not file.startswith("/aliveCheck") 
                            ):
                            dt = str(row.time.year  ) + "-" + str(row.time.month ).zfill(2) + "-" + str(row.time.day   ).zfill(2) + " " + str(row.time.hour  ).zfill(2) + ":" + str(row.time.minute).zfill(2) + ":" + str(row.time.second).zfill(2)
                            row_size   = str(row.size  ) if str(row.size  ).isdecimal()  else "0"
                            row_status = str(row.status) if str(row.status).isdecimal()  else "0"
                            out = log_gbn                  + terminated + \
                                row.remote_host.exploded   + terminated + \
                                dt                         + terminated + \
                                row.request.method         + terminated + \
                                row.request.url.path_str   + terminated + \
                                row.request.url.params     + terminated + \
                                row.request.url.query_str  + terminated + \
                                row.request.protocol       + terminated + \
                                row_status                 + terminated + \
                                row_size                   + terminated + \
                                "BAT"                      + terminated + \
                                dt                         + "\n"
                            outfile.write(out)
                    idx += 1
        infile.close()
    outfile.close()
    endTime = int(time.time())
    print(" by process id: [{0}] 작업시간 : [{1}초][{2}건]".format( str(proc).rjust(6," ") , str(endTime-startTime).rjust(4," "), str(idx).rjust(10," ")))

def fn_ctl_create():
    global terminated
    global load_type
    ctl_name = data_path + "\\" + file_name + ".ctl"
    log_name = data_path + "\\" + file_name + ".log"
    bad_name = data_path + "\\" + file_name + ".bad"
    dsc_name = data_path + "\\" + file_name + ".dsc"
    table_name = "TB_ACCESS_LOG"
    # (INSERT, APPEND, REPLACE, TRUNCATE)
    if load_type == "" :
        load_type = "TRUNCATE"
    else :
        load_type = "APPEND"
    
#    from cStringIO import StringIO as strIo
#    strIo.write("LOAD DATA\n")
    data_name = data_path + "\\" + file_name + ".data"
    with io.open(ctl_name , "w" , encoding="utf-8") as outfile:
        outfile.write("LOAD DATA\n")
        outfile.write("INFILE '{0}'\n".format(data_name))
        outfile.write("BADFILE  '{0}'\n".format(bad_name))
        outfile.write("DISCARDFILE  '{0}'\n".format(dsc_name))
        outfile.write("{0} \n".format(load_type))    
        outfile.write("INTO TABLE {0}\n".format(table_name))
        outfile.write("FIELDS TERMINATED BY '{0}' \n".format(terminated))
        outfile.write("( LOG_GBN                \n")
        outfile.write(" ,REMOTE_IP              \n")
        outfile.write(" ,CONNT_DT \"TO_DATE(:CONNT_DT,'YYYY-MM-DD HH24:MI:SS') + (  9 * 1 / 24 )\" \n")
        outfile.write(" ,CALL_METHOD            \n")
        outfile.write(" ,URL         CHAR(4000) \n")
        outfile.write(" ,PARAMS      CHAR(4000) \n")
        outfile.write(" ,QUERY_STR   CHAR(4000) \n")
        outfile.write(" ,PROTOCOL               \n")
        outfile.write(" ,STATUS                 \n")
        outfile.write(" ,PAGE_SIZE              \n")
        outfile.write(" ,REG_GBN                \n")
        outfile.write(" ,REG_DT \"TO_DATE(:CONNT_DT,'YYYY-MM-DD HH24:MI:SS') + (  9 * 1 / 24 )\" \n")
        outfile.write(")             \n")
    outfile.close()
    return [ctl_name,log_name]
    
def zipdir(path, zipf):
    fileTotCount = sum([len(files) for r, d, files in os.walk(path)])
    suffix = '%(percent)d%% [%(elapsed_td)s / %(eta)d / %(eta_td)s]'
    bar = Bar('Processing', max=fileTotCount,suffix=suffix)
    for root, dirs, files in os.walk(path):
        for file in files:
            bar.next()
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))    

if __name__ == '__main__':
    file_name = "access"
    terminated = ","
    startTime = int(time.time())
    work_path = datetime.now().strftime("%Y_%m_%d")

    print("[{0}] start job".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S")))
    kidx = 0
    idx = 0
    for log_gbn in log_data['file_gbn']:
        log_path = log_data['file_path'][kidx]
        kidx = kidx + 1
        if ( os.path.isdir(log_path) ) == True:
            data_path = work_path
            if os.path.isdir(data_path) == False:
                os.mkdir(data_path)
            if ( accessJob == "N" and len(os.listdir(data_path)) > 0 ):
                accessJob = "N"
            else :
                accessJob = "Y"
            #accessJob = "N"    
            if accessJob == "Y" :
                proc_cnt = 6
                print("[{0}] delete file [{1}]".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"),data_name))
                # if ( len(os.listdir(data_path)) > 0 ):
                    # sproc.call("del /q {0}\\*.*".format(data_path), shell=True,stdout=None)

                log_fileList = []
                for file in os.listdir(log_path):
                    idx += 1
                    data_name = data_path + "\\access" + str(idx).rjust(5,"0") + ".csv"
                    log_file = log_path + "\\" + file
                    log_fileList.append({"data_name":data_name,"log_file" : log_file})
                    if len(log_fileList) >= proc_cnt:
                        pool = Pool(proc_cnt)
                        func = partial(fn_file_create, log_gbn)
                        pool.map(func,log_fileList)
                        log_fileList = []
                        pool.close()
                        pool.join()
                proc_cnt = len(log_fileList)
                if proc_cnt > 0 :
                    pool = Pool(proc_cnt)
                    func = partial(fn_file_create, log_gbn)
                    pool.map(func,log_fileList)
                    pool.close()
                    pool.join()
    sproc.call("copy {0}\\*.csv {0}\\access.data".format(data_path), shell=True,stdout=None)            
    #        sproc.call("del {0}\\*.csv ".format(data_path), shell=True,stdout=None)
    if loadJob == "Y" :
        ctl_file = fn_ctl_create()
        print("[{0}] create {1}".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"),file_name))
    #   ctl_option = "direct=true unrecoverable"
    #   ctl_option = "direct=true parallel=true"   
        ctl_option = "READSIZE=3145728 BINDSIZE=3145728 ROWS=5000"
        sproc.call("sqlldr userid=jinsaja/jinsaja@XE log={2} control={0} {1}".format(ctl_file[0],ctl_option,ctl_file[1]), shell=True,stdout=None)
    print("[{0}] end job".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S")))
    endTime = int(time.time())
    print("총 작업 시간", (endTime - startTime))

 
 
