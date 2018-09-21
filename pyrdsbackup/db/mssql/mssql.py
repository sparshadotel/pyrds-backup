import os
import time
import pyodbc
import datetime


def generate_rds_backup_path(db):
    '''
    Generate a name for rds backup.
    '''
    return 'backups/{}/{}-{}.bak'.format(db, db, datetime.datetime.now().strftime('%I-%M-%B-%d-%Y'))


def generate_native_backup_path(db):
    '''
    Generate a name for ec2 db backup.
    '''
    return '{}-{}.bak'.format(db, datetime.datetime.now().strftime('%I-%M-%B-%d-%Y'))


def initialize_cursor(server, username, password, port, version):
    '''
    Initialize db cursor using given connection details.
    '''
    ODBC_DRIVER = '{ODBC Driver %d for SQL Server}' % version
    CONNECTION_STRING = 'DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password}'
    connection_str = CONNECTION_STRING.format(
        driver=ODBC_DRIVER,
        server=server,
        database='msdb',
        username=username,
        password=password,
        port=port
    )
    conn = pyodbc.connect(connection_str)
    conn.autocommit = True
    return conn.cursor()


def rds_backup_procedure_exists(cursor):
    '''
    Returns true if dbo.rds_backup_database procedure exists.
    '''
    cursor.execute('''
        SELECT * FROM sys.objects
        WHERE object_id = OBJECT_ID(N'dbo.rds_backup_database');
    ''')

    if cursor.fetchall() != []:
        return True
    return False


def start_rds_backup(db, s3_bucket, s3_backup_object_path, cursor):
    '''
    Trigger dbo.rds_backup_database procedure and return its task id.
    '''
    cursor.execute('''
        EXEC msdb.dbo.rds_backup_database
            @source_db_name={},
            @s3_arn_to_backup_to='arn:aws:s3:::{}/{}',
            @overwrite_S3_backup_file=1,
            @type='full';
    '''.format(db, s3_bucket, s3_backup_object_path))
    return cursor.fetchall()[0][0]


def start_native_backup(db, backup_location, backup_path, cursor):
    '''
    Run native backup query and return its task id.
    '''
    print('Backing up DB: {} \n'.format(db))
    try:
        cursor.execute('''
            BACKUP DATABASE {} TO DISK='{}/{}';
        '''.format(db, backup_location, backup_path))
        cursor.nextset()  # Need this for persistence of local backup file.

    except Exception as e:
        print('Oops!!! Something went wrong.\n', e)


def task_status(task_id, cursor):
    '''
    Returns rds task status of given task id.
    '''
    cursor.execute('''
        EXEC msdb.dbo.rds_task_status @task_id={}
    '''.format(task_id))
    return cursor.fetchall()


def task_completed(task_id, cursor):
    '''
    Returns true if a task is complete and raises an exception if it fails.
    '''
    status = task_status(task_id, cursor)
    if status[0][5] == 'ERROR':
        print('Error')
        return True
    return (status[0][3] == 100 and status[0][5] == 'SUCCESS')
