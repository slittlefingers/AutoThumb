import os
import sqlite3
import datetime
import json
def is_valid_path(path):
    
    return os.path.exists(path)

def create_database(experiment_name, database_path):
    
    # create database name
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    db_name = f"{experiment_name}_{current_time}.db"  
    if not is_valid_path(database_path):
        database_path = os.path.join(os.getcwd(), "Datafolder")
        os.makedirs(database_path, exist_ok=True)
    db_full_path = os.path.join(database_path, db_name)
    conn = sqlite3.connect(db_full_path)
    conn.close()
    return db_full_path

def create_table(db_path, experiment_name, software, selected_package):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sqliteinformation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_name TEXT NOT NULL,
            database_path TEXT NOT NULL,
            software TEXT NOT NULL,
            selected_package TEXT NOT NULL
        )
    """)
    
    # 插入数据
    cursor.execute("""
        INSERT INTO sqliteinformation (experiment_name, database_path, software, selected_package)
        VALUES (?, ?, ?, ?)
    """, (experiment_name, db_path, software, selected_package))
    
    conn.commit()
    conn.close()
def get_software_and_package(db_path):
   

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    

    cursor.execute("""
        SELECT software, selected_package,experiment_name FROM sqliteinformation
    """)
    

    results = cursor.fetchall()
    

    conn.close()
    softwarename=results[0][0] 
    selected_package=results[0][1]
    experiment_name=results[0][2]
    return softwarename,selected_package,experiment_name
def save_actions(database_path, actions):
    """
    将 actions 列表中的动作保存到指定的 SQLite 数据库中。
    
    参数:
    - database_path: str, SQLite 数据库文件的路径
    - actions: list of tuples, 每个元组包含 (action_id, action_description)
    """
    # connect to database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    # if not exit create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS action_list (
        action_id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_description TEXT NOT NULL
    )
    ''')
    # clear table
    cursor.execute('DELETE FROM action_list')

    # incert actions list
    for action_id, action_description in enumerate(actions):
        cursor.execute('''
        INSERT INTO action_list (action_id, action_description)
        VALUES (?, ?)
        ''', (action_id, action_description))
    
    # commit event
    conn.commit()
    
    # close the database connection
    conn.close()

def read_actions(database_path):
  

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    cursor.execute('SELECT action_id, action_description, status FROM action_list')
    

    actions = cursor.fetchall()
    
   
    conn.close()
    
    return actions
def add_status_list(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(action_list);")
    columns = [column[1] for column in cursor.fetchall()]
    if 'status' not in columns:
        cursor.execute('ALTER TABLE action_list ADD COLUMN status TEXT DEFAULT "waiting"')
        print("Added 'status' column to 'action_list' table.")
    else:
        print("'status' column already exists in 'action_list' table.")
    conn.commit()
    conn.close()

def add_status(database_path, action_id, status):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE action_list SET status = ? WHERE action_id = ?", (status, action_id))
    conn.commit()
    conn.close()

def create_action_operation_table(database_path):
  
 
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS action_operation (
        action_id INTEGER,
        operation_id INTEGER PRIMARY KEY,
        operation_description TEXT NOT NULL,
        extraction_file_path TEXT,
        screenshot_path TEXT,
        thumbnailchecklist TEXT,
        FOREIGN KEY (action_id) REFERENCES action_list (action_id)
    )
    ''')
    

    conn.commit()
    conn.close()

def add_action_operation(database_path, action_id, operation_description, extraction_file_path, screenshot_path,thumbnailchecklist=None):
    
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    if thumbnailchecklist is None:
        thumbnailchecklist=[]
    thumbnailchecklist = json.dumps(thumbnailchecklist)

    cursor.execute('''
    INSERT INTO action_operation (action_id, operation_description, extraction_file_path, screenshot_path,thumbnailchecklist)
    VALUES (?, ?, ?, ?, ?)
    ''', (action_id, operation_description, extraction_file_path, screenshot_path,thumbnailchecklist))
    

    operation_id = cursor.lastrowid
    

    conn.commit()
    conn.close()
    
    return operation_id
def add_action_operation_first(database_path, action_id, operation_description, extraction_file_path, screenshot_path,thumbnailchecklist=None):
   
 
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    if thumbnailchecklist is None:
        thumbnailchecklist=[]
    thumbnailchecklist = json.dumps(thumbnailchecklist)
 
    operation_id=0
    cursor.execute('''
    INSERT INTO action_operation (action_id,operation_id, operation_description, extraction_file_path, screenshot_path,thumbnailchecklist)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (action_id,operation_id, operation_description, extraction_file_path, screenshot_path,thumbnailchecklist))
    

    

    conn.commit()
    conn.close()
    
    return operation_id
def get_thumbnailchecklist_byid(database_path,operation_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

 
    cursor.execute('''
    SELECT thumbnailchecklist FROM action_operation WHERE operation_id = ?
    ''', (operation_id,))
    
    result = cursor.fetchone()
    

    conn.close()

 
    if result is None:
        return []

   
    thumbnailchecklist = json.loads(result[0])
    return thumbnailchecklist
def insert_action_at_start(database_path, new_description, new_status='waiting'):
   
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        
        cursor.execute('UPDATE action_list SET action_id = action_id + 1')

     
        cursor.execute('''
        INSERT INTO action_list (action_id, action_description, status)
        VALUES (?, ?, ?)
        ''', (0, new_description, new_status))

   
        conn.commit()
        print("New action inserted at the start successfully.")
    except Exception as e:

        conn.rollback()
        print(f"An error occurred: {e}")
    finally:

        conn.close()

def get_all_operations(database_path):

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT action_id,operation_id,operation_description,extraction_file_path,screenshot_path FROM action_operation')
    operations = cursor.fetchall()
    conn.close()
    return operations
def get_operation_id_screenshot(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT operation_id, screenshot_path FROM action_operation')
    screenshot= cursor.fetchall()
    conn.close()
    return screenshot

def insert_operation_modify_table(database_path):

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS modifytable (
        changed_id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filepath1 TEXT NOT NULL,
        filepath2 TEXT NOT NULL,
        filetype TEXT NOT NULL,
        start_operation_id INTEGER,
        end_operation_id INTEGER
    );
    """
    
    try:

        cursor.execute(create_table_sql)
        print("Table 'changedfile' created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:

        conn.commit()
        conn.close()

def insert_operation_add_table(database_path):
 
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS addtable (
        changed_id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        filetype TEXT NOT NULL,
        start_operation_id INTEGER,
        end_operation_id INTEGER
    );
    """
    
    try:

        cursor.execute(create_table_sql)
        print("Table 'changedfile' created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:

        conn.commit()
        conn.close()

def insert_operation_remove_table(database_path):

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS removetable (
        changed_id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        filetype TEXT NOT NULL,
        start_operation_id INTEGER,
        end_operation_id INTEGER
    );
    """
    
    try:

        cursor.execute(create_table_sql)
        print("Table 'changedfile' created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:

        conn.commit()
        conn.close()
def clear_removetable(database_path):
    

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    clear_table_sql = "DELETE FROM removetable;"
    
    try:

        cursor.execute(clear_table_sql)
        print("All data from 'removetable' has been cleared.")
    except sqlite3.Error as e:
        print(f"An error occurred while clearing 'removetable': {e}")
    finally:

        conn.commit()
        conn.close()
def clear_modifytable(database_path):


    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    clear_table_sql = "DELETE FROM modifytable;"
    
    try:

        cursor.execute(clear_table_sql)
        print("All data from 'removetable' has been cleared.")
    except sqlite3.Error as e:
        print(f"An error occurred while clearing 'removetable': {e}")
    finally:

        conn.commit()
        conn.close()
def clear_addtable(database_path):


    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    clear_table_sql = "DELETE FROM addtable;"
    
    try:

        cursor.execute(clear_table_sql)
        print("All data from 'removetable' has been cleared.")
    except sqlite3.Error as e:
        print(f"An error occurred while clearing 'removetable': {e}")
    finally:

        conn.commit()
        conn.close()
def insert_into_modify_table(database_path, data):
 
 
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    insert_sql = """
    INSERT INTO modifytable (filename, filepath1, filepath2, filetype, start_operation_id, end_operation_id)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    

    data_with_ids = [(filename, filepath1, filepath2, filetype, start_operation_id, end_operation_id) for filename, filepath1, filepath2, filetype,start_operation_id, end_operation_id in data]
    
    try:

        cursor.executemany(insert_sql, data_with_ids)
        conn.commit()
        print(f"Inserted {cursor.rowcount} records into 'modifytable' successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred during data insertion into 'modifytable': {e}")
    finally:

        conn.close()

def insert_into_add_table(database_path, data):


    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    insert_sql = """
    INSERT INTO addtable (filename, filepath, filetype, start_operation_id, end_operation_id)
    VALUES (?, ?, ?, ?, ?);
    """

    data_with_ids = [(filename, filepath, filetype, start_operation_id, end_operation_id) for filename, filepath, filetype, start_operation_id, end_operation_id in data]
    
    try:

        cursor.executemany(insert_sql, data_with_ids)
        conn.commit()
        print(f"Inserted {cursor.rowcount} records into 'addtable' successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred during data insertion into 'addtable': {e}")
    finally:

        conn.close()

def insert_into_remove_table(database_path, data):


    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    insert_sql = """
    INSERT INTO removetable (filename, filepath, filetype, start_operation_id, end_operation_id)
    VALUES (?, ?, ?, ?, ?);
    """
    
 
    data_with_ids = [(filename, filepath, filetype, start_operation_id, end_operation_id) for filename, filepath, filetype, start_operation_id, end_operation_id in data]
    
    try:

        cursor.executemany(insert_sql, data_with_ids)
        conn.commit()
        print(f"Inserted {cursor.rowcount} records into 'removetable' successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred during data insertion into 'removetable': {e}")
    finally:

        conn.close()
def get_modifytable_data(database_path, end_id):
 

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    select_sql = """
    SELECT filename, filepath1, filepath2, filetype, start_operation_id, end_operation_id
    FROM modifytable
    WHERE end_operation_id = ?;
    """
    
    try:

        cursor.execute(select_sql, (end_id,))

        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f"An error occurred during data retrieval from 'modifytable': {e}")
        return []
    finally:

        conn.close()
def get_addtable_data(database_path, end_id):
  

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    select_sql = """
    SELECT filename, filepath, filetype, start_operation_id, end_operation_id
    FROM addtable
    WHERE end_operation_id = ?;
    """
    
    try:

        cursor.execute(select_sql, (end_id,))

        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f"An error occurred during data retrieval from 'addtable': {e}")
        return []
    finally:

        conn.close()
def get_removetable_data(database_path, end_id):
    """
    根据 end_id 从 removetable 提取数据，排除 changed_id 列。
    
    :param database_path: 数据库路径
    :param end_id: 结束操作的ID
    :return: 包含提取数据的列表，每个元素是一个元组 (filename, filepath, filetype, start_operation_id, end_operation_id)
    """

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
 
    select_sql = """
    SELECT filename, filepath, filetype, start_operation_id, end_operation_id
    FROM removetable
    WHERE end_operation_id = ?;
    """
    
    try:

        cursor.execute(select_sql, (end_id,))

        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f"An error occurred during data retrieval from 'removetable': {e}")
        return []
    finally:

        conn.close()
def insert_changed_jsonfile_table(database_path):

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS changedjsontable (
        json_id INTEGER PRIMARY KEY AUTOINCREMENT,
        filepath TEXT NOT NULL,
        filechangetype TEXT NOT NULL,
        end_operation_id INTEGER,
        jsondata TEXT NOT NULL
    );
    """
    
    try:

        cursor.execute(create_table_sql)
        print("Table 'changedjsontable' created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"An error changedjsontable occurred: {e}")
    finally:

        conn.commit()
        conn.close()

def insert_into_changed_jsonfile_table(database_path, filepath, filechangetype, end_operation_id, jsondata):

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    

    check_existence_sql = """
    SELECT json_id FROM changedjsontable WHERE filepath = ? AND filechangetype = ? AND end_operation_id = ?;
    """
    
    cursor.execute(check_existence_sql, (filepath, filechangetype, end_operation_id))
    result = cursor.fetchone()
    
    if result:
        print(f"Record with filepath '{filepath}' and filechangetype '{filechangetype}' and end_operation_id '{end_operation_id}' already exists with id {result[0]}.")
    else:
        jsondata = json.dumps(jsondata)

        insert_sql = """
        INSERT INTO changedjsontable (filepath, filechangetype, end_operation_id, jsondata)
        VALUES (?, ?, ?, ?);
        """
        try:
            cursor.execute(insert_sql, (filepath, filechangetype, end_operation_id, jsondata))
            conn.commit() 
            print("New record inserted successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred during insertion: {e}")
def get_jsonfile_table(database_path, filepath, end_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    select_sql = """
    SELECT jsondata FROM changedjsontable WHERE filepath = ? AND end_operation_id = ?;
    """
    

    
    try:
        # 执行查询
        cursor.execute(select_sql, (filepath, end_id))

        result = cursor.fetchone()
        result = json.loads(result[0])
        return result
    except sqlite3.Error as e:
        print(f"An error occurred during data retrieval from 'changedjsontable': {e}")
        return []
    finally:

        conn.close()

def create_thumbnail_table(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Thumbnailtable (
        thumb_id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        end_operation_id INTEGER,
        metadata TEXT ,
        thumbnaildatapath TEXT NOT NULL
    );
    """
    try:

        cursor.execute(create_table_sql)
        print("Table 'Thumbnailtable' created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"An error Thumbnailtable occurred: {e}")
    finally:

        conn.commit()
        conn.close()
def insert_into_thumbnail_table(database_path, filename, end_operation_id,pathlist, metadata=None):

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    

    check_existence_sql = """
    SELECT thumb_id FROM thumbnailtable WHERE filename = ? AND end_operation_id = ?;
    """
    
    cursor.execute(check_existence_sql, (filename, end_operation_id))
    result = cursor.fetchone()
    
    if result:
        print(f"Record with filepath '{filename}' and already exists with id {result[0]}.")
    else:
        pathlist = json.dumps(pathlist)

        insert_sql = """
        INSERT INTO thumbnailtable (filename, end_operation_id, thumbnaildatapath,metadata)
        VALUES (?, ?, ?, ?);
        """
        if metadata is not None:
            metadata = json.dumps(metadata)
        try:
            cursor.execute(insert_sql, (filename, end_operation_id, pathlist, metadata))
            conn.commit()  # 提交更改
            print("New record inserted successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred during insertion: {e}")
    


def fetch_thumbnail_data(database_path, filename, end_operation_id):


    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()


    fetch_sql = """
    SELECT thumbnaildatapath, metadata FROM thumbnailtable WHERE filename = ? AND end_operation_id = ?;
    """
    
    cursor.execute(fetch_sql, (filename, end_operation_id))
    result = cursor.fetchone()
    
    conn.close()  

    if result:

        thumbnaildatapath = json.loads(result[0])
        if result[1] is not None:
            metadata = json.loads(result[1])
        else:
            metadata = None
        return thumbnaildatapath, metadata
    else:
        print(f"No record found for filename '{filename}' and end_operation_id '{end_operation_id}'.")
        return None

def fetch_thumbnailnames(database_path, end_operation_id):


    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()


    fetch_sql = """
    SELECT filename FROM thumbnailtable WHERE end_operation_id = ?;
    """
    
    cursor.execute(fetch_sql, (end_operation_id,))
    results = cursor.fetchall()  
    
    conn.close()  

    if results:

        return [row[0] for row in results]
    else:
        print(f"No records found for end_operation_id '{end_operation_id}'.")
        return []
def fetch_thumbnailname_picture(database_path, end_operation_id):


    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

  
    fetch_sql = """
    SELECT filename, thumbnaildatapath FROM thumbnailtable WHERE end_operation_id = ?;
    """
    
    cursor.execute(fetch_sql, (end_operation_id,))
    results = cursor.fetchall() 
    
    conn.close() 
    fresult=[]
    for filename,thumbnaildatapath in results:
        if thumbnaildatapath is not None or len(thumbnaildatapath)==0:
            thumbnails=json.loads(thumbnaildatapath)
            for thumbnail in thumbnails:
                fresult.append((filename,thumbnail))
    return fresult

def create_keyword_table(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS keywordtable (
        end_operation_id INTEGER PRIMARY KEY,
        datainformation TEXT,
        filename TEXT
    );
    """
    try:
       
        cursor.execute(create_table_sql)
        print("Table 'keywordtable' created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
      
        conn.commit()
        conn.close()
def create_keyword_table(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS keywordtable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 新增自增主键
        end_operation_id INTEGER,
        datainformation TEXT,
        filename TEXT
    );
    """
    try:
      
        cursor.execute(create_table_sql)
        print("Table 'keywordtable' created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
  
        conn.commit()
        conn.close()

def insert_into_keyword_table(database_path, end_operation_id, datainformation, filename):
 
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
 
    check_sql = """
    SELECT COUNT(*) FROM keywordtable WHERE end_operation_id = ? AND filename = ?;
    """
    cursor.execute(check_sql, (end_operation_id, filename))
    count = cursor.fetchone()[0]  
    
    if count > 0:
        print(f"Record with end_operation_id {end_operation_id} and filename '{filename}' already exists. No insertion made.")
        conn.close()  
        return  


    insert_sql = """
    INSERT INTO keywordtable (end_operation_id, datainformation, filename)
    VALUES (?, ?, ?);
    """
    datainformation = json.dumps(datainformation)  
    try:
        cursor.execute(insert_sql, (end_operation_id, datainformation, filename))
        conn.commit()  #
        print("New record inserted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred during insertion: {e}")
    finally:
        conn.close()  

def get_all_keyword_data(database_path, end_operation_id):

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()


    fetch_sql = """
    SELECT datainformation, filename FROM keywordtable WHERE end_operation_id = ?;
    """
    
    cursor.execute(fetch_sql, (end_operation_id,))
    results = cursor.fetchall()
    
    conn.close() 


    if results:
        all_data = []
        for result in results:
            datainformation_json = result[0]  
            filename = result[1] 
            try:

                datainformation = json.loads(datainformation_json)
                all_data.append((datainformation, filename))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for record with filename '{filename}': {e}")
                all_data.append((None, filename))
        return all_data
    else:
        print(f"No records found for end_operation_id '{end_operation_id}'.")
        return []
def get_all_database():

    database_info = []
    

    for root, dirs, files in os.walk('./Datafolder'):
        for file in files:

            if file.endswith('.db'):
                db_path = os.path.join(root, file)
                database_info.append(db_path)
    
    return database_info

def read_sqliteinformation(db_path):
    """
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查询 sqliteinformation 表中的数据
        cursor.execute("SELECT experiment_name, database_path FROM sqliteinformation")
        rows = cursor.fetchall()

        # 返回读取的数据
        return rows

    except sqlite3.Error as e:
        print(f"Error reading database {db_path}: {e}")
        return []
    
    finally:
        if conn:
            conn.close()

def get_all_experiment_data():
    """
    """
    experiment_data = []
    
    # 获取所有数据库文件的路径
    db_paths = get_all_database()
    print("start get experiment")
    print(db_paths)
    # 遍历每个数据库路径，连接并读取数据
    for db_path in db_paths:
        rows = read_sqliteinformation(db_path)
        
        # 将每个数据库中的数据添加到实验数据列表中
        for row in rows:
            experiment_name, database_path = row
            experiment_data.append((experiment_name, database_path))
    
    return experiment_data
# a=get_all_experiment_data()
# print(a)