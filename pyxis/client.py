"""
Pyxis Client
usages:
    python client.py port_number pyxis_client_code
    port_number: The port number to run
    pyxis_client_code: A random password to connect with server.
"""

import sys
from sqlite3 import connect
from SimpleXMLRPCServer import SimpleXMLRPCServer
import subprocess
from multiprocessing import Process
from datetime import datetime as DateTime
from xmlrpclib import ServerProxy

LOG_FILE = "pyxis.client.db"
SERVER_ADDRESS = "0.0.0.0"
LOCAL_PROXY = "".join(["http://", SERVER_ADDRESS, ":%d"])
PORT_NUMBER = 12547
PYXIS_CLIENT_CODE = "oicn892#_kSE"


SQL_CREATE_LOG_TABLE = """CREATE TABLE IF NOT EXISTS PYXIS_CLIENT_LOG (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100),
    command TEXT,
    job_folder TEXT,
    stamp_0 TIMESTAMP,
    stamp_z TIMESTAMP NULL DEFAULT NULL,
    status INTEGER NULL DEFAULT NULL
);
"""

SQL_SELECT_LOG_TABLE = """SELECT id, username, command, job_folder, stamp_0, stamp_z, status 
    FROM PYXIS_CLIENT_LOG
    WHERE id IN (%s)
"""

SQL_INSERT_LOG = """INSERT INTO  PYXIS_CLIENT_LOG
    (username, command, job_folder, stamp_0)
    VALUES (?, ?, ?, ?)
"""

SQL_UPDATE_LOG_STATUS = """UPDATE PYXIS_CLIENT_LOG
    SET stamp_z=?, status=?
    WHERE id=?
"""

LOG_TITLES = "id username command job_folder stamp_0 stamp_z status".split()


user_lists = {}

def check_user(func):
    def new_func(username, password, *args, **kwargs):
        global user_lists
        if True: # user_lists[username] == password:
            return func(username, *args, **kwargs)
        else:
            # TODO: Add log here.
            return "Access Denied"
    return new_func

def check_password(func):
    def new_func(password, *args, **kwargs):
        global PYXIS_CLIENT_CODE
        if PYXIS_CLIENT_CODE == password:
            return func(*args, **kwargs)
        else:
            # TODO: Add log here.
            return "Access Denied"
    return new_func

def create_table(conn):
    cursor = conn.cursor()
    for sql in SQL_CREATE_LOG_TABLE.split(';'):
        sql = sql.strip()
        if sql:
            cursor.execute(sql)

def call_command(password, id, cmd, job_folder, recall_url):
    if sys.platform.startswith("win"):
        # Don't display the Windows GPF dialog if the invoked program dies.
        # See comp.os.ms-windows.programmer.win32
        # How to suppress crash notification dialog?, Jan 14,2004 -
        # Raymond Chen's response [1]

        import ctypes
        SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX);
        subprocess_flags = 0x8000000 #win32con.CREATE_NO_WINDOW?
    else:
        subprocess_flags = 0

    process = subprocess.Popen(cmd, cwd=job_folder, creationflags=subprocess_flags)
    ret_code = process.wait()

    client = ServerProxy(LOCAL_PROXY % PORT_NUMBER)
    client.update_status(password, id, ret_code)



@check_user
def run_shell(username, cmd, job_folder, recall_url):
    global connection
    cursor = connection.cursor()
    cursor.execute(SQL_INSERT_LOG, (username, cmd, job_folder, DateTime.now()))
    id = cursor.lastrowid
    connection.commit()
    Process(target=call_command, args=(PYXIS_CLIENT_CODE, id, cmd, job_folder, recall_url)).start()
    return id

@check_password
def query_jobs(ids):
    global connection
    cursor = connection.cursor()
    ids = ",".join(["%d" % int(i) for i in ids])
    cursor.execute(SQL_SELECT_LOG_TABLE % ids)
    return LOG_TITLES + cursor.fetchall()

@check_password
def update_users(users):
    global user_lists
    for username, password in users:
        user_lists[username] = password
    return len(users)

@check_password
def update_status(id, ret_code):
    global connection
    cursor = connection.cursor()
    cursor.execute(SQL_UPDATE_LOG_STATUS, (DateTime.now(), ret_code, id))
    connection.commit()
    return id

if __name__ == '__main__':
    connection = connect(LOG_FILE)
    create_table(connection)

    server = SimpleXMLRPCServer((SERVER_ADDRESS, PORT_NUMBER), allow_none=True)
    server.register_function(run_shell, 'run_shell')
    server.register_function(query_jobs, 'query_jobs')
    server.register_function(update_users, 'update_users')
    server.register_function(update_status, 'update_status')
    
    print "Listening on port %d..." % PORT_NUMBER
    server.serve_forever()
