#※ 로컬환경 구축법
1. Python 설치 (버전 확인)
```
C:\> python -V
Python 3.8.9
``` 
2. 로컬 가상환경 생성
```C:\> mkdir venvs
C:\> cd venvs
C:\> python -m venv mysite 
```
3. DJANGO 설치
```
(mysite) C:\> pip install django==3.1.3
```
4. PIP 최신버전 업그레이드
```
(mysite) C:\> python -m pip install --upgrade pip
```
5. 프로젝트 생성
```
 (mysite) C:\> mkdir projects
 (mysite) C:\> cd projects 
 (mysite) C:\projects> mkdir mysite
 (mysite) C:\projects> cd mysite 
 (mysite) C:\projects\mysite> django-admin startproject config . <-현 디렉토리
```
6.  가상환경 접속 배치 프로그램 설정 (환경변수 Path 추가)  
**<u>[파일 이름: C:/venvs/mysite.cmd]</u>**
```
@echo off
cd C:/projects/mysite
C:/venvs/mysite/scripts/activate
``````
7.  APP 생성
```
(mysite) C:\projects\mysite> django-admin startapp board
```
8. MySQL 클라이언트 설치
```
(mysite) C:\> pip install mysqlclient 
```
9. Database 스키마 및 계정 생성
```
create database mysite;

use mysite;

create user 'mysite'@'localhost' identified by '1qaz!QAZ';

grant all privileges on *.* to 'mysite'@'localhost';

flush privileges;
```
10. 계층 트리 구조 MPTT 설치
```
pip install django-mptt
```
11. 장고 슈퍼유저 생성  
(ID : admin, PW : 1qaz!QAZ)
```
python manage.py createsuperuser --settings=config.settings.local
```