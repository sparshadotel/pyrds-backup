import os
import yaml
import pymssql
import time
import datetime

def generate_rds_backup_path(db):
    return 'backups/{}/{}-{}.bak'.format(db, db, datetime.datetime.now().strftime("%I-%M-%B-%d-%Y"))

def generate_native_backup_path(db):
    return '{}-{}.bak'.format(db, datetime.datetime.now().strftime("%I-%M-%B-%d-%Y"))

def initialize_cursor(server, username, password):
    conn = pymssql.connect(server, username, password, 'msdb')
    conn.autocommit(True)
    return conn.cursor()

def rds_backup_procedure_exists(cursor):
    cursor.execute(""" SELECT * FROM sys.objects
            WHERE object_id = OBJECT_ID(N'dbo.rds_backup_database'); """)
    if cursor.fetchall() != []:
            return True
    return False

def start_rds_backup(db, s3_bucket, s3_backup_object_path, cursor):
    cursor.execute(""" exec msdb.dbo.rds_backup_database 
    @source_db_name={},     
    @s3_arn_to_backup_to='arn:aws:s3:::{}/{}',
    @overwrite_S3_backup_file=1,
    @type='full'; 
    """.format(db, s3_bucket, s3_backup_object_path))
    return cursor.fetchall()[0][0]

def start_native_backup(db, backup_location, backup_path, cursor):
    print('Backing up DB: {} \n'.format(db))
    try:
            cursor.execute("BACKUP DATABASE {} TO DISK='{}/{}' ;".format(db, backup_location, backup_path))
    except Exception as e:
            print('Oops!!! Something went wrong.\n', e)

def task_status(task_id, cursor):
    cursor.execute(""" exec msdb.dbo.rds_task_status @task_id={}""".format(task_id))
    return cursor.fetchall()

def task_completed(task_id, cursor):
    status = task_status(task_id, cursor)
    if status[0][5] == 'ERROR':
        print('Error')
        return True
    return (status[0][3] == 100 and status[0][5] == 'SUCCESS')