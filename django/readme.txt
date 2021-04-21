https://www.inflearn.com/course/%EB%82%98%EC%9D%98-%EC%B2%AB-django-%EC%95%B1-%EB%A7%8C%EB%93%A4%EA%B8%B0/lecture/4541?tab=curriculum

site 생성
django-admin startproject mysite
app생성 
cd mysite
C:/Python38/python.exe manage.py startapp polls
C:/Python38/python.exe manage.py runserver 

C:/Python38/python.exe manage.py migrate

C:/Python38/python.exe manage.py makemigrations polls
C:/Python38/python.exe manage.py sqlmigrate polls 0001

C:/Python38/python.exe manage.py shell