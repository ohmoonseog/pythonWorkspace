import cx_Oracle
import db_config

#한글 지원 방법
import os
os.putenv('NLS_LANG', '.UTF8')

#연결에 필요한 기본 정보 (유저, 비밀번호, 데이터베이스 서버 주소)
connection = cx_Oracle.connect(db_config.user, db_config.pw, db_config.dsn)
cursor = connection.cursor()
cursor.execute("""  
SELECT LOG_GBN     
      ,REMOTE_IP   
      ,CONNT_DT    
      ,CALL_METHOD 
      ,URL         
      ,PARAMS      
      ,QUERY_STR   
      ,PROTOCOL    
      ,STATUS      
      ,PAGE_SIZE   
      ,REG_GBN     
      ,REG_DT      
  FROM TB_ACCESS_LOG 
  """)
for LOG_GBN,REMOTE_IP  ,CONNT_DT   ,CALL_METHOD,URL        ,PARAMS     ,QUERY_STR  ,PROTOCOL   ,STATUS     ,PAGE_SIZE  ,REG_GBN    ,REG_DT      in cursor:
   print("테스트 이름 리스트 : ", URL)

cursor.close()
connection.close()