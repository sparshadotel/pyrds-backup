<div align="center">
    <img style="width: 8px;" src="assets/pyrdsbackup.png">
  </a>
  <br/>

# pyrdsbackup

A library on top of pyodbc meant to simplify backups of Databases from RDS to S3
</div>

### Installation
```
sudo apt install -y unixodbc unixodbc-dev
pip install pyrdsbackup
```
### Usage
#### MSSQL
[Make sure that RDS Bakcup is enabled for your RDS instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.SQLServer.Options.BackupRestore.html)

```python
from pyrds.backup import mssql

# Initialize Credentials
credentials = {
    'server': 'rdsserver.amazon',
    'username': 'adminuser',
    'password': 'password',
    'port': 1433,
    'bucket': 'bucket_name',
    'driver_version': 17
}

# Test if the connection works. If returns True then backup is possible
mssql.test(credentials)

# Backup the database
mssql.backup(credentials, 'database_name')
```


