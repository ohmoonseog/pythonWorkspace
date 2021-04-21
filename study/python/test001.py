import os, io , time
from datetime import datetime
from lars import apache
from multiprocessing import Pool
from functools import partial

data_path = ""
terminated = ","
file_name = ""
accessJob = "Y"
loadJob = "Y"
log_path = "C:/workSpace/Urllog/WEB01"
data_name = ""

def fn_file_delete():
    global data_name
    with io.open(data_name , "w" , encoding="utf-8") as outfile:
        pass
    outfile.close()

def fn_file_create(data_name,log_file):
    global terminated
    startTime = int(time.time())
    print("log --> cvs data_name = [{0}] , log_filelog_file = [{1}]".format( data_name, log_file) ,end="")
    proc = os.getpid()
    idx = 0
    with io.open(data_name , "a" , encoding="utf-8") as outfile:
        with io.open(log_file, 'r',encoding="utf-8") as infile:
            with apache.ApacheSource(infile) as source:
                for row in source:
                    if ( row.status != 408 and  row.request.url.path_str.find("/fanpage/") > -1 ):
                        dt = str(row.time.year  ) + "-" + str(row.time.month ).zfill(2) + "-" + str(row.time.day   ).zfill(2) + " " + str(row.time.hour  ).zfill(2) + ":" + str(row.time.minute).zfill(2) + ":" + str(row.time.second).zfill(2)
                        row_size   = str(row.size  ) if str(row.size  ).isdecimal()  else "0"
                        row_status = str(row.status) if str(row.status).isdecimal()  else "0"
                        out = "W01"                    + terminated + \
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
    print(" by process id: [{0}] 작업시간 : [{1}초][{2}건]".format( str(proc).rjust(6," ") , endTime-startTime, str(idx).rjust(10," ")))

def fn_ctl_create():
    global terminated
    ctl_name = data_path + "\\" + file_name + ".ctl"
    log_name = data_path + "\\" + file_name + ".log"
    bad_name = data_path + "\\" + file_name + ".bad"
    dsc_name = data_path + "\\" + file_name + ".dsc"
    table_name = "TB_ACCESS_LOG"
    load_type = "APPEND"    # (INSERT, APPEND, REPLACE, TRUNCATE)
#    from cStringIO import StringIO as strIo
#    strIo.write("LOAD DATA\n")
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
        outfile.write(" ,URL                    \n")
        outfile.write(" ,PARAMS                 \n")
        outfile.write(" ,QUERY_STR              \n")
        outfile.write(" ,PROTOCOL               \n")
        outfile.write(" ,STATUS                 \n")
        outfile.write(" ,PAGE_SIZE              \n")
        outfile.write(" ,REG_GBN                \n")
        outfile.write(" ,REG_DT \"TO_DATE(:CONNT_DT,'YYYY-MM-DD HH24:MI:SS') + (  9 * 1 / 24 )\" \n")
        outfile.write(")             \n")
    outfile.close()
    return [ctl_name,log_name]

if __name__ == '__main__':
    file_name = "access"
    terminated = ","
    startTime = int(time.time())
    work_path = datetime.now().strftime("%Y_%m_%d")
    print("[{0}] start job".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S")))
    if ( os.path.isdir(log_path) ) == True:
        data_path = work_path
        if os.path.isdir(data_path) == False:
            os.mkdir(data_path)
        data_name = data_path + "\\" + file_name + ".csv"
        if (os.path.isfile(data_name) == False):
            accessJob = "Y"
        else :
            accessJob = "N"
        accessJob = "Y"
        if accessJob == "Y" :
            proc_cnt = 6
            print("[{0}] delete file [{1}]".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"),data_name))
            if (os.path.isfile(data_name)):
                fn_file_delete()
            log_fileList = []
            pool_fn = partial(fn_file_create,data_name)
            for file in os.listdir(log_path):
                log_fileList.append(log_path + "\\" + file)
                if len(log_fileList) >= proc_cnt:
                    pool = Pool(proc_cnt)
                    pool.map(pool_fn,log_fileList)
                    log_fileList = []
                    pool.close()
                    pool.join()
            proc_cnt = len(log_fileList)
            if proc_cnt > 0 :
                pool = Pool(proc_cnt)
                pool.map(pool_fn,log_fileList)
                pool.close()
                pool.join()
            """
            for file in os.listdir(log_path):
                log_file = log_path + "\\" + file
                fn_file_create(data_name,log_file,terminated)
            procs = []
            for file in os.listdir(log_path):
                log_file = log_path + "\\" + file
                proc = Process(target=fn_file_create, args=(data_name,log_file,terminated))
                procs.append(proc)
                proc.start()

            for proc in procs:
                proc.join()
            """
        if loadJob == "Y" :
            ctl_file = fn_ctl_create()
            print("[{0}] create {1}".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"),file_name))
            import subprocess as sproc
        #    ctl_option = "direct=true unrecoverable"
            ctl_option = "direct=true parallel=true"   
        #    ctl_option = "READSIZE=3145728 BINDSIZE=3145728 ROWS=5000"
            sproc.call("sqlldr userid=jinsaja/jinsaja@XE log={2} control={0} {1}".format(ctl_file[0],ctl_option,ctl_file[1]), shell=True,stdout=None)
    print("[{0}] end job".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S")))
    endTime = int(time.time())
    print("총 작업 시간", (endTime - startTime))
# TODO
# https://github.com/oracle/python-cx_Oracle/tree/master/samples
# https://docs.microsoft.com/ko-kr/sql/connect/python/python-driver-for-sql-server?view=sql-server-ver15
# https://pypi.org/project/mybatis-mapper2sql/
# 
