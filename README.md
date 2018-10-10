## Установка для CentOS 7

1. Установить Python 3.7

```bash
yum install gcc gcc-c++ openssl-devel bzip2-devel libffi-devel
cd /usr/src
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
tar xzf Python-3.7.0.tgz
cd Python-3.7.0
./configure --enable-optimizations
make altinstall
```

2. Проверить Python

```bash
python3.7 -V
```

3. Установить ODBC Driver for MS SQL

Полная инструкция: https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server

4. Установить ODBC Driver for MySQL

```bash
yum install mysql-connector-odbc
```

5. Склонировать этот репозитарий в удобный каталог

```bash
git clone https://github.com/alexmon1989/kas_sync.git
```

6. Создать и активировать виртуальное окружение Python

```bash
cd kas_sync
python3.7 -m venv .env
source .env/bin/activate
```

7. Установить зависимости Python

```bash
pip install -r requirements.txt
```

8. Создать конфигурационные файлы и внести в них изменения в части подключения к API и БД

```bash
cp settings.py.example settings.py
cp settings.py.example settings.testing.py
```

9. Проверить способна ли программа соединяться с БД и API

```bash
python -m unittest
```

## Использование

С активированием виртуального окружения Python:

```bash
source .env/bin/activate
python sync.py
```

Без него:

```bash
.env/bin/python sync.py
```
