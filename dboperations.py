import os
import sqlite3 as sl

def init_db(db_name):
    con = None
    if not os.path.exists(db_name):
        create_video_table_sql = '''CREATE TABLE Video (
                UID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                VideoPath TEXT,
                AudioPath TEXT,
                TranscriptPath TEXT
            );'''
        
        con = sl.connect(db_name)
        cur = con.cursor()
        cur.execute(create_video_table_sql)
        con.commit()

    if con is None:
        con = sl.connect(db_name)

    return con


def add_info_to_db(con, uid, VideoPath, AudioPath, TranscriptPath):
    append_video_sql = 'INSERT INTO Video (UID, VideoPath, AudioPath, TranscriptPath) values(?, ?, ?, ?)'
    data = [
        (uid, VideoPath, AudioPath, TranscriptPath)
    ]

    con.executemany(append_video_sql, data)
    con.commit()

    return True


def create_db_dir(local_app_dir, file_name='database.py'):
    db_folder_path = os.path.join(local_app_dir, 'Databases')
    
    if not os.path.exists(db_folder_path):
        os.makedirs(db_folder_path)
    
    return os.path.join(db_folder_path, file_name)


def get_path(con, uid, file_type):
    path = None
    param = (uid,)
    cur = con.cursor()

    if file_type == 'mp4':
        get_record_sql = 'SELECT VideoPath FROM Video WHERE UID=?'
        path = cur.execute(get_record_sql, param)

    if file_type == 'wav':
        get_record_sql = 'SELECT AudioPath FROM Video WHERE UID=?'
        path = cur.execute(get_record_sql, param)

    if file_type == 'json':
        get_record_sql = 'SELECT TranscriptPath FROM Video WHERE UID=?'
        path = cur.execute(get_record_sql, param)


    if path:
        path = cur.fetchone()
        path = path[0]

    cur.close()
    return path


def print_video_table_data(con):
    cur = con.cursor()
    cur.execute('SELECT * FROM Video')
    print(cur.fetchall())