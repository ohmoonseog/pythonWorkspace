import os
import io
from datetime import datetime
from lars import apache
log_path =  "C:/workSpace/Urllog/WEB01"
file_name = "access"
data_name = file_name + ".csv"
print("[{0}] start job".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S")))
if ( os.path.isdir(log_path) ) == True:
    with io.open(data_name , "w" , encoding="utf-8") as outfile:
        pass
    outfile.close()
    print("[{0}] delete file {1}".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"),data_name))
    terminated = "|"
    with io.open(data_name , "w+" , encoding="utf-8") as outfile:
        outfile.write("LOG_GBN,REMOTE_IP,CONNT_DT,CALL_METHOD,URL,PARAMS,QUERY_STR,PROTOCOL,STATUS,PAGE_SIZE,REG_GBN,REG_DT\n")
        for file in os.listdir(log_path):
#            if file.find("2020-12") + file.find("2021-01") > -1 :
            if 0 > -1 :
                with io.open(log_path + "\\" + file, 'r',encoding="utf-8") as infile:
                    with apache.ApacheSource(infile) as source:
                        for row in source:
                            if ( row.status != 408 ):
                                dt = str(row.time.year  ) + "-" + str(row.time.month ).zfill(2) + "-" + str(row.time.day   ).zfill(2) + " " + str(row.time.hour  ).zfill(2) + ":" + str(row.time.minute).zfill(2) + ":" + str(row.time.second).zfill(2)
                                row_size   = str(row.size  ) if str(row.size  ).isdecimal()  else "0"
                                row_status = str(row.status) if str(row.status).isdecimal()  else "0"
                                out = "A01"                    + terminated + \
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
    infile.close()
    outfile.close()
    ctl_name = file_name + ".ctl"
#    ctl_option = "direct=true unrecoverable"
#    ctl_option = "READSIZE=3145728 BINDSIZE=3145728 ROWS=5000"
    ctl_option = "direct=true parallel=true"   
    bad_name = file_name + ".bad"
    dsc_name = file_name + ".dsc"
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
        outfile.write("( LOG_GBN     \n")
        outfile.write(" ,REMOTE_IP   \n")
        outfile.write(" ,CONNT_DT    \"TO_DATE(:CONNT_DT,'YYYY-MM-DD HH24:MI:SS') + (  9 * 1 / 24 )\"\n")
        outfile.write(" ,CALL_METHOD \n")
        outfile.write(" ,URL         \n")
        outfile.write(" ,PARAMS      \n")
        outfile.write(" ,QUERY_STR   \n")
        outfile.write(" ,PROTOCOL    \n")
        outfile.write(" ,STATUS      \n")
        outfile.write(" ,PAGE_SIZE   \n")
        outfile.write(" ,REG_GBN     \n")
        outfile.write(" ,REG_DT      \"TO_DATE(:CONNT_DT,'YYYY-MM-DD HH24:MI:SS') + (  9 * 1 / 24 )\"\n")
        outfile.write(")             \n")
    outfile.close()
    print("[{0}] create {1}".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"),file_name))
    import subprocess as sproc
    sproc.call("sqlldr userid=jinsaja/jinsaja@XE control={0} {1}".format(ctl_name,ctl_option), shell=True,stdout=None)
print("[{0}] end job".format(datetime.now().strftime("%Y/%m/%d, %H:%M:%S")))

# https://github.com/oracle/python-cx_Oracle/tree/master/samples
