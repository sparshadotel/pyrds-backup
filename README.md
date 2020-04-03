<div align="center">
    <img src="assets/pyrdsbackup.png">

# pyrdsbackup

A library on top of pyodbc meant to simplify database backups from RDS to S3.
</div>

## Installation

```bash
sudo apt install -y unixodbc unixodbc-dev
pip install pyrdsbackup
```

## Prerequisite

[Make sure that RDS Backup is enabled for your RDS instance.](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.SQLServer.Options.BackupRestore.html)

## Usage

```py
from pyrdsbackup.db import mssql

# Initialize Credentials
credentials = {
    'server': 'rdsserver.amazon',
    'username': 'adminuser',
    'password': 'password',
    'port': 1433,
    'bucket': 'bucket_name',
    'driver_version': 17
}

# Test if the connection works. If this statement returns True, backup is possible.
mssql.test(credentials)

# Backup the database
mssql.backup(credentials, 'database_name')
```
