from flask import Flask, jsonify, send_from_directory,request,send_file
from flask_cors import CORS
import os
import mimetypes
import subprocess
from Agent.controller import tap, slide, type, back, home, pause_show_more
app = Flask(__name__)
from thumb_function import find_package_name,found_package_name, initial_analysis, execute_action
import time
from flask_socketio import SocketIO, emit
import logging
import time
import threading
import sys
from Fortool import file_analysis
CORS(app)
from serverfuction import serverfunction
# screenshot directory
SCREENSHOT_DIR = 'screenshot2'

# define the socketio object
socketio = SocketIO(app, cors_allowed_origins="*",async_mode='eventlet')
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)


# check adb connection
def check_adb_connection():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        
        lines = result.stdout.splitlines()
        devices = [line for line in lines[1:] if line.strip() and 'device' in line]
        
        if len(devices) > 0:
            return True
        return False
    except Exception as e:
        print(f"Error checking ADB connection: {e}")
        return False

# check root authority
def check_root_authority():

    try:
        result = subprocess.run(['adb', 'shell', 'su', '-c', 'whoami'], capture_output=True, text=True)
        if 'root' in result.stdout:
            return True
        return False
    except Exception as e:
        print(f"Error checking Root authority: {e}")
        return False

# check adb connection and root authority
@app.route('/api/check-status', methods=['GET'])
def check_status():
    adb_connection = check_adb_connection()
    root_authority = check_root_authority()

    response = {
        "adbConnection": adb_connection,
        "rootAuthority": root_authority
    }
    return jsonify(response)

#  get the screenshot
@app.route('/api/screenshot', methods=['GET'])
def get_screenshot():
    screenshot_path = os.path.join(SCREENSHOT_DIR, 'output.png')
    try:
        
        subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=open(screenshot_path, 'wb'), check=True)
        return jsonify({'screenshotUrl': f'/screenshot2/output.png'})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

# acquire the click event
@app.route('/api/click', methods=['POST'])
def handle_click():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    if x is None or y is None:
        return jsonify({'error': 'Invalid parameters'}), 400
    try:
        tap(x,y)
        return jsonify({'message': 'Click operation performed successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

# acquire the swipe event
@app.route('/api/swipe', methods=['POST'])
def handle_swipe():
    data = request.get_json()
    startX = data.get('startX')
    startY = data.get('startY')
    endX = data.get('endX')
    endY = data.get('endY')
    if None in [startX, startY, endX, endY]:
        return jsonify({'error': 'Invalid parameters'}), 400

    try:
        slide(startX, startY, endX, endY)
        return jsonify({'message': 'Swipe operation performed successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500
    
# acquire the package name
@app.route('/api/get-packages', methods=['POST'])
def get_packages():
    data = request.get_json()
    software = data.get('software')

    if not software:
        return jsonify({'error': 'Software name is required.'}), 400


    packages = find_package_name(software)
    if not packages:
        return jsonify({'error': f'No packages found for software: {software}'}), 404

    return jsonify({'packages': packages}), 200

#  test the package whether it is exist
@app.route('/api/check-package', methods=['POST'])
def check_package():
    data = request.get_json()
    package = data.get('package')
    check = found_package_name(package)
    if not check:
        return jsonify({'error': f'something is wrong: {package}'}), 404
    return jsonify({'check': check}), 200

# build for normal submit form will return actionlist
@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    data=request.get_json()
    experimentName=data.get('experimentName')
    databasePath=data.get('databasePath')
    software=data.get('software')
    selectedPackage=data.get('selectedPackage')
    if not experimentName or not software or not selectedPackage:
        return jsonify({"error": "experimentName, software, and selectedPackage are required fields."}), 400

    # create database
    db_full_path = serverfunction.create_database(experimentName, databasePath)
    
    # create table
    serverfunction.create_table(db_full_path, experimentName, software, selectedPackage)

    # analysis the application
    action_list=initial_analysis(software,selectedPackage)

    return jsonify({
        "message": "Database and table created successfully.",
        "databasePath": db_full_path,
        "action_list": action_list
    }), 200

# build for design form don't return actionlist
@app.route('/api/design-form', methods=['POST'])
def design_form():
    data=request.get_json()
    experimentName=data.get('experimentName')
    databasePath=data.get('databasePath')
    software=data.get('software')
    selectedPackage=data.get('selectedPackage')
    if not experimentName or not software or not selectedPackage:
        return jsonify({"error": "experimentName, software, and selectedPackage are required fields."}), 400

    # create database
    db_full_path = serverfunction.create_database(experimentName, databasePath)
    
    # create table
    serverfunction.create_table(db_full_path, experimentName, software, selectedPackage)

    # analysis the application    
    return jsonify({
        "message": "Database and table created successfully.",  
        "databasePath": db_full_path,    
    }), 200

# from fronside get the action list
@app.route('/api/save-actions', methods=['POST'])
def save_actions():
    try:
        data = request.get_json()
        database_path = data.get('databasePath')
        actions = data.get('Actions', [])
        first_action = f"original_state"
        actions.insert(0, first_action)
        print(database_path)
        print(actions)
        if not actions:
            return jsonify({'error': 'No actions provided'}), 400  

        serverfunction.save_actions(database_path, actions)
        return jsonify({'message': 'Actions saved successfully!', 'actions': actions}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to save actions.', 'details': str(e)}), 500
    
# operation start we need create action_status and create action operation table
@app.route('/api/create-operation', methods=['POST'])
def create_operation():
    try:
        data = request.get_json()
        database_path = data.get('databasePath')
        serverfunction.add_status_list(database_path)
        serverfunction.create_action_operation_table(database_path)
        return jsonify({'message': 'Operation created successfully!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to create operation.', 'details': str(e)}), 500
    
# get all actions
@app.route('/api/get-actions', methods=['POST'])
def get_actions():
    try:
        print("start get actions")
        data = request.get_json()
        database_path = data.get('databasePath')
        print(database_path)
        serverfunction.add_status_list(database_path)
        application_name,package_name,experiment_name=serverfunction.get_software_and_package(database_path)
        first_action = f"original_state"
        serverfunction.add_status(database_path, first_action, "waiting")
        actions = serverfunction.read_actions(database_path)
        if not database_path:
            return jsonify({'error': 'No database path provided'}), 400  
        actions_list = [{'action_id': action[0], 'action_description': action[1], 'status': action[2]} for action in actions]
        return jsonify(actions_list),200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to retrieve actions.', 'details': str(e)}), 500

# io part
class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        print(f"Formatted log entry: {log_entry}")
       
        if '[OPERATION]' in log_entry:
            print("found")
            try:
                socketio.emit('operation', {'message': log_entry})
                print(f"Formatted log entry: {log_entry}")
            except Exception as e:
                print(f"Failed to emit operation log: {e}")
            
        elif '[THINKING]' in log_entry:
            print("found")
            try:
                socketio.emit('thinking', {'message': log_entry})
                print(f"Formatted log entry: {log_entry}")
            except Exception as e:
                print(f"Failed to emit operation log: {e}")
            
        elif '[ACTION]' in log_entry:
            try:
                socketio.emit('action', {'message': log_entry})
                print(f"Formatted log entry: {log_entry}")
            except Exception as e:
                print(f"Failed to emit operation log: {e}")

logger = logging.getLogger('myLogger')


console_handler = logging.StreamHandler(sys.stdout)  
formatter = logging.Formatter('%(message)s')
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)  
logger.addHandler(console_handler)  


handler = SocketIOHandler()

handler.setFormatter(formatter)
logger.addHandler(handler)


logger.setLevel(logging.DEBUG)

original_sleep = time.sleep       
def socketio_sleep(seconds):
    try:
        socketio.sleep(seconds)
        # print("Using socketio.sleep")
    except RuntimeError:
        original_sleep(seconds)
#  use monkey patch to modify time.sleep
def use_socketio_sleep():
    global time
    time.sleep = socketio_sleep
    print("Switched to socketio.sleep")
def use_original_sleep():
    global time
    time.sleep = original_sleep
    print("Switched back to original time.sleep")

# start to execute the operation
@app.route('/start-task', methods=['POST'])
def start_task():
    try:
        print("start task")
        data = request.get_json()
        database_path = data.get('databasePath')
        if not database_path:
            return jsonify({'error': 'No database path provided'}), 400  
        # need status
        actions=serverfunction.read_actions(database_path)
        actions_list = [ action[1] for action in actions]
        application_name,package_name,experiment_name=serverfunction.get_software_and_package(database_path)
        use_socketio_sleep()
        socketio.start_background_task(target=execute_action, actions_list=actions_list, application_name=application_name, package_name=package_name, database_path=database_path, experiment_name=experiment_name)
        return jsonify({"status": "Task started"}), 200      
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to start task.', 'details': str(e)}), 500

@app.route('/api/get-operations', methods=['POST'])    
def get_operation():
    try:
        print("start get operation")
        data = request.get_json()
        database_path = data.get('databasePath')
        print(database_path)
        operations=serverfunction.get_all_operations(database_path)
        if len(operations) == 0:
            return jsonify({'message': 'No operations found'}), 200
        
        merged_operations = {}

        for operation in operations:
            action_id,operation_id,operation_description,file_path,screenshot_path = operation
            action_key=f"Action_{action_id}"
            if action_key not in merged_operations:
                merged_operations[action_key] = []

            merged_operations[action_key].append({
            'operation_id': operation_id,
            'operation_description': operation_description,
            'file_path': file_path,
            'screenshot_path': screenshot_path
            })

        print(merged_operations)

        if not database_path:
            return jsonify({'error': 'No database path provided'}), 400  
        return jsonify(merged_operations),200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to retrieve actions.', 'details': str(e)}), 500   
@app.route('/api/start_to_analysis', methods=['POST']) 
def start_to_analysis():
    try:
        print("start to analysis")
        data = request.get_json()
        database_path = data.get('databasePath')
        if not database_path:
            return jsonify({'error': 'No database path provided'}), 400  
        operations=serverfunction.get_all_operations(database_path)
        serverfunction.insert_operation_modify_table(database_path)
        serverfunction.insert_operation_add_table(database_path)
        serverfunction.insert_operation_remove_table(database_path)
        serverfunction.clear_removetable(database_path)
        serverfunction.clear_modifytable(database_path)
        serverfunction.clear_addtable(database_path)
        serverfunction.insert_changed_jsonfile_table(database_path)
        serverfunction.create_thumbnail_table(database_path)
        serverfunction.create_keyword_table(database_path)
        print('create table')
        
        for i in range(len(operations)-1):
            print('This is the ' + str(i) + 'th operation')
            print(i)
            file_changed_result=file_analysis.compare_dirs(operations[i][3],operations[i+1][3])
            print(file_changed_result)
            if file_changed_result:
                detail_dict=file_analysis.distinguish_file(file_changed_result)
                print("#"*100)
                print(detail_dict["added"])
                result=file_analysis.prepare_data_for_insertion(detail_dict,i,i+1)
                if len(detail_dict["modified"]["db"])>0:
                    print("This is modified database")
                    print(detail_dict["modified"]["db"])
                    for j in range(len(detail_dict["modified"]["db"])):
                        print("This is the " + str(j) + "th modified database")
                        print("*" * 100)
                        print(detail_dict["modified"]["db"][j][0])
                        print(detail_dict["modified"]["db"][j][1])
                        jsondata=file_analysis.compare_databases(detail_dict["modified"]["db"][j][0],detail_dict["modified"]["db"][j][1])
                        print(jsondata)
                        serverfunction.insert_into_changed_jsonfile_table(database_path,detail_dict["modified"]["db"][j][1],"modified",i+1,jsondata)
                        target_keys=set()
                        for index1 in range(1, max(2, i + 2)):
                            keys=serverfunction.get_thumbnailchecklist_byid(database_path,index1)
                            target_keys.update(keys)
                        target_keys=list(target_keys)   
                        keyword_result=file_analysis.search_in_dict_with_keys_ignore_case(jsondata, target_keys)
                        print("this is the result"+str(keyword_result))
                        if len(keyword_result)>0:
                            serverfunction.insert_into_keyword_table(database_path,i+1,keyword_result,str(detail_dict["modified"]["db"][j][1]))
                               
                if len(detail_dict["modified"]["xml"])>0:
                    print("This is modified xml")
                    print(detail_dict["modified"]["xml"])
                    for j in range(len(detail_dict["modified"]["xml"])):
                        print("This is the " + str(j) + "th modified xml")
                        print("*" * 100)
                        print(detail_dict["modified"]["xml"][j][0])
                        print(detail_dict["modified"]["xml"][j][1])
                        jsondata=file_analysis.compare_xml_files(detail_dict["modified"]["xml"][j][0],detail_dict["modified"]["xml"][j][1])
                        print(jsondata)
                        serverfunction.insert_into_changed_jsonfile_table(database_path,detail_dict["modified"]["xml"][j][1],"modified",i+1,jsondata)
                        target_keys=set()
                        for index1 in range(1, max(2, i + 2)):
                            keys=serverfunction.get_thumbnailchecklist_byid(database_path,index1)
                            target_keys.update(keys)
                        target_keys=list(target_keys)
                        keyword_result=file_analysis.search_in_dict_with_keys_ignore_case(jsondata, target_keys)
                        if len(keyword_result)>0:
                            serverfunction.insert_into_keyword_table(database_path,i+1,keyword_result,detail_dict["modified"]["xml"][j][1])
                if len(detail_dict["added"]["xml"])>0:
                    print("This is added xml")
                    print(detail_dict["added"]["xml"])
                    for j in range(len(detail_dict["added"]["xml"])):
                        print("This is the " + str(j) + "th added xml")
                        print("*" * 100)
                        print(detail_dict["added"]["xml"][j])
                        addedxml=file_analysis.display_xml(detail_dict["added"]["xml"][j], added=True)
                        print(addedxml)
                        serverfunction.insert_into_changed_jsonfile_table(database_path,detail_dict["added"]["xml"][j],"added",i+1,addedxml)
                        target_keys=set()
                        for index1 in range(1, max(2, i + 2)):
                            keys=serverfunction.get_thumbnailchecklist_byid(database_path,index1)
                            target_keys.update(keys)
                        target_keys=list(target_keys)
                        print("this is target_keys",target_keys)
                        keyword_result=file_analysis.search_in_dict_with_keys_ignore_case(addedxml, target_keys)
                        
                        if len(keyword_result)>0:
                            print("this is the target_result"+str(keyword_result))
                            serverfunction.insert_into_keyword_table(database_path,i+1,keyword_result,detail_dict["added"]["xml"][j])
                if len(detail_dict["removed"]["xml"])>0:
                    print("This is removed xml")
                    print(detail_dict["removed"]["xml"])
                    for j in range(len(detail_dict["removed"]["xml"])):
                        print("This is the " + str(j) + "th removed xml")
                        print("*" * 100)
                        print(detail_dict["removed"]["xml"][j])
                        removedxml=file_analysis.display_xml(detail_dict["removed"]["xml"][j], added=False)
                        print(removedxml)
                        serverfunction.insert_into_changed_jsonfile_table(database_path,detail_dict["removed"]["xml"][j],"removed",i+1,removedxml)

                print("*" * 100)
                if len(detail_dict["modified"]["other"])>0:
                    print("This is modified other")
                    print(detail_dict["modified"]["other"])
                    for j in range(len(detail_dict["modified"]["other"])):
                        print("123")
                        pathlist1=file_analysis.carving_tool(str(detail_dict["modified"]["other"][j][0]),'./Thumbnail','./log.txt')
                        pathlist2=file_analysis.carving_tool(str(detail_dict["modified"]["other"][j][1]),'./Thumbnail','./log.txt')
                        print(pathlist1)
                        print(pathlist2)
                        if pathlist1 is not None:
                            metadatalist=[]
                            for path in pathlist1:
                                 metadata=file_analysis.exif_picture(path)
                                 metadatalist.append(metadata)

                            serverfunction.insert_into_thumbnail_table(database_path,detail_dict["modified"]["other"][j][0],i+1,pathlist1,metadatalist)

                        if pathlist2 is not None:
                            metadatalist=[]
                            for path in pathlist2:
                                 metadata=file_analysis.exif_picture(path)
                                 metadatalist.append(metadata)
                            serverfunction.insert_into_thumbnail_table(database_path,detail_dict["modified"]["other"][j][1],i+1,pathlist2,metadatalist)
                if len(detail_dict["added"]["other"])>0:
                    print("This is added other")
                    # print(detail_dict)
                    # print(detail_dict["added"])
                    # print(detail_dict["added"]["other"])
                    for j in range(len(detail_dict["added"]["other"])):
                       print("This is the " + str(j) + "th added other")
                       print(detail_dict["added"]["other"][j])
                       pathlist1=file_analysis.carving_tool(str(detail_dict["added"]["other"][j]),'./Thumbnail','./log.txt')#file_analysis.carving_tool(detail_dict["added"]["other"][j],'./Thumbnail','./log.txt')
                       print("*"*100)
                       print(pathlist1)
                       print("*"*100)
                       if pathlist1 is not None:
                            metadatalist=[]
                            for path in pathlist1:
                                 metadata=file_analysis.exif_picture(path)
                                 metadatalist.append(metadata)
                            serverfunction.insert_into_thumbnail_table(database_path,detail_dict["added"]["other"][j],i+1,pathlist1,metadatalist)
                    print("#"*100)
                if len(detail_dict["removed"]["other"])>0:
                    print("This is removed other")
                    # print(detail_dict["removed"]["other"])
                    for j in range(len(detail_dict["removed"]["other"])):
                       pathlist1=file_analysis.carving_tool(str(detail_dict["removed"]["other"][j]),'./Thumbnail','./log.txt')
                       print("*"*100)
                       print(pathlist1)
                       print("*"*100)
                       if pathlist1 is not None:
                            metadatalist=[]
                            for path in pathlist1:
                                 metadata=file_analysis.exif_picture(path)
                                 metadatalist.append(metadata)
                            serverfunction.insert_into_thumbnail_table(database_path,detail_dict["removed"]["other"][j],i+1,pathlist1,metadatalist)
                if len(detail_dict["added"]["db"])>0:  
                    print("This is added database")
                    for j in range(len(detail_dict["added"]["db"])):
                        added_table=file_analysis.fetch_added_table(detail_dict["added"]["db"][j])
                        print(added_table)
                        serverfunction.insert_into_changed_jsonfile_table(database_path,detail_dict["added"]["db"][j],"added",i+1,added_table)
                        target_keys=set()
                        for index1 in range(1, max(2, i + 2)):
                            keys=serverfunction.get_thumbnailchecklist_byid(database_path,index1)
                            target_keys=target_keys.update(keys)
                        target_keys=list(target_keys)
                        print("this is target_keys",target_keys)
                        keyword_result=file_analysis.search_in_dict_with_keys_ignore_case(added_table, target_keys)
                        if len(keyword_result)>0:
                            serverfunction.insert_into_keyword_table(database_path,i+1,keyword_result,detail_dict["added"]["db"][j])
                        print("*" * 100)
                        print("Added database is finished") 
                if len(detail_dict["removed"]["db"])>0:  
                    print("This is removed database")
                    for j in range(len(detail_dict["added"]["db"])):
                        removed_table=file_analysis.fetch_added_table(detail_dict["removed"]["db"][j])
                        print(removed_table)
                        serverfunction.insert_into_changed_jsonfile_table(database_path,detail_dict["added"]["db"][j],"added",i+1,removed_table)
                        print("*" * 100)
                        print("Removed database is finished")
                if len(detail_dict["modified"]["picture"])>0:
                    print("This is modified picture")
                    for j in range(len(detail_dict["modified"]["picture"])):
                        filelist1=[detail_dict["modified"]["picture"][j][0]]
                        filelist2=[detail_dict["modified"]["picture"][j][1]]
                        metadata1=[file_analysis.exif_picture(filelist1[0])]
                        metadata2=[file_analysis.exif_picture(filelist2[0])]
                        serverfunction.insert_into_thumbnail_table(database_path,detail_dict["modified"]["picture"][j][0],i+1,filelist1,metadata1)
                        serverfunction.insert_into_thumbnail_table(database_path,detail_dict["modified"]["picture"][j][1],i+1,filelist2,metadata2)
                if len(detail_dict["added"]["picture"])>0:
                    print("This is added picture")
                    print(detail_dict["added"]["picture"])
                    for j in range(len(detail_dict["added"]["picture"])):
                        print("this is ",j)
                        filelist1=[detail_dict["added"]["picture"][j]]
                        metadata1=[file_analysis.exif_picture(str(filelist1[0]))]
                        serverfunction.insert_into_thumbnail_table(database_path,str(detail_dict["added"]["picture"][j]),i+1,filelist1,metadata1)

                if len(detail_dict["removed"]["picture"])>0:
                    print("This is removed picture")
                    for j in range(len(detail_dict["removed"]["picture"])):
                        filelist1=[detail_dict["removed"]["picture"][j]]
                        metadata1=[file_analysis.exif_picture(filelist1[0])]
                        serverfunction.insert_into_thumbnail_table(database_path,detail_dict["removed"]["picture"][j],i+1,filelist1,metadata1)
                serverfunction.insert_into_modify_table(database_path,result["modified"])
                serverfunction.insert_into_add_table(database_path,result["added"])
                serverfunction.insert_into_remove_table(database_path,result["removed"])
                print(123,operations[i+1][3],operations[i][3])
                print("#"*100)
                
            
                
            else:
                return jsonify({'message': 'No file changed'}), 200
            id_sc=serverfunction.get_operation_id_screenshot(database_path)
            print("start check thumbnail")
            for id, sc in id_sc[1:]:
                print(str(id) +" s screenshot is in "+str(sc) )
                id=int(id)
                thumblist=serverfunction.fetch_thumbnailname_picture(database_path,id)
                print("this is thumblist")
                print(thumblist)
                print(1)
                thumbanaylseresult=file_analysis.find_images_with_sift(thumblist,sc,'./Thumbnail')
                metadata=None
                serverfunction.insert_into_thumbnail_table(database_path,str(id),id+1000,thumbanaylseresult,metadata)
            print("Task finished")

        return jsonify({"status": "Task started"}), 200  
    except Exception as e:
        print(e)
@app.route('/api/get-changed-files', methods=['POST'])
def get_changed_files():
    try:
        print("start get changed files")
        data = request.get_json()
        database_path = data.get('databasePath')
        print(database_path)
        operation_id = data.get('operation_id')
        print(operation_id)
        if not database_path:
            print("getting wrong")
            return jsonify({'error': 'No database path provided'}), 400  
        if not operation_id:
            print("getting wrong")
            return jsonify({'error': 'No operation id provided'}), 400  
        if operation_id==0:
            operation_id=1
        
        modified_list=serverfunction.get_modifytable_data(database_path,operation_id)
        added_list=serverfunction.get_addtable_data(database_path,operation_id)
        removed_list=serverfunction.get_removetable_data(database_path,operation_id)
        detail_dict={"modified":modified_list,"added":added_list,"removed":removed_list}
        print(detail_dict)
        backend_result=file_analysis.convert_to_detail_dict(detail_dict)
        print(operation_id)
        return jsonify(backend_result),200

    except Exception as e:
        print(e)
@app.route('/api/get-detail-jsondata', methods=['POST'])
def get_detail_jsondata():
    try:
        print("start get detail jsondata")
        data = request.get_json()
        print
        database_path = data.get('databasePath')
        print(database_path)
        filepath=data.get('filepath')
        print(filepath)
        operation_id = data.get('operation_id')
        print(operation_id)
        if not database_path:
            print("getting wrong")
            return jsonify({'error': 'No database path provided'}), 400  
        if not operation_id:
            print("getting wrong")
            return jsonify({'error': 'No operation id provided'}), 400  
        if not filepath:
            print("getting wrong")
            return jsonify({'error': 'No filepath provided'}), 400
        if operation_id==0:
            operation_id=1
        print(operation_id)
        jsondata_list=serverfunction.get_jsonfile_table(database_path,filepath,operation_id)
        print(jsondata_list)
        return jsonify(jsondata_list),200
    except Exception as e:
        print(e)
@app.route('/api/get-binary-files', methods=['POST'])
def get_binary_file():
    try:
        data=request.get_json()
        file_path = data.get('file')
        print(file_path)
        if not file_path:
            return jsonify({'error': 'No file path provided'}), 400
        return send_file(file_path, as_attachment=False)
    except Exception as e:
        print(e)
@app.route('/api/get-thumbnail', methods=['POST'])
def get_thumbnail():
    try:
        data = request.get_json()
        print(data)
        databasePath = data.get('databasePath') 
        print(databasePath)
        file_path = data.get('file_path')
        print(file_path)
        end_operation_id = data.get('end_operation_id')
        print(end_operation_id)
        if not databasePath or not file_path:
            return jsonify({'error': 'No database path or file path provided'}), 400
        path_list,metadata=serverfunction.fetch_thumbnail_data(databasePath, file_path, end_operation_id)
        # if not os.path.exists(path_list):
        print(path_list)
        file_path=path_list[0]
        if path_list==None:
            return jsonify({'error': 'File not found'}), 404
        mimetypes.add_type('image/webp', '.webp')     
     
        mime_type, _ = mimetypes.guess_type(file_path)
        
        if not mime_type:
            return jsonify({'error': 'Unable to determine file type'}), 400
        
       
        return send_file(file_path, mimetype=mime_type)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/get-thumbnailmeta', methods=['POST'])
def get_thumbnailmeta():
    try:
        data = request.get_json()
        print(data)
        databasePath = data.get('databasePath')  
        print(databasePath)
        file_path = data.get('file_path')
        print(file_path)
        end_operation_id = data.get('end_operation_id')
        print(end_operation_id)
        if not databasePath or not file_path:
            return jsonify({'error': 'No database path or file path provided'}), 400
        path_list,metadata=serverfunction.fetch_thumbnail_data(databasePath, file_path, end_operation_id)
        # if not os.path.exists(path_list):
        print(metadata)
        metadata=metadata[0]
        if metadata==None:
            return jsonify({'error': 'File not found'}), 404
        mimetypes.add_type('image/webp', '.webp')     
        return jsonify(metadata),200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/get-thumbnailan', methods=['POST'])
def get_thumbnailan():
    try:
        data = request.get_json()
        print(data)
        databasePath = data.get('databasePath')  
        file_path = data.get('file_path')
        print(file_path)
        end_operation_id = data.get('end_operation_id')
        print(end_operation_id)
        if not databasePath or not file_path:
            return jsonify({'error': 'No database path or file path provided'}), 400
        file_path,metadata=serverfunction.fetch_thumbnail_data(databasePath, file_path, end_operation_id)
        # if not os.path.exists(path_list):
        # print(path_list)
        print("this is file_path"+file_path)
        if file_path==None:
            return jsonify({'error': 'File not found'}), 404
        mimetypes.add_type('image/webp', '.webp')     
        mime_type, _ = mimetypes.guess_type(file_path)
        print(file_path)
        if not mime_type:
            return jsonify({'error': 'Unable to determine file type'}), 400
        
       
        return send_file(file_path, mimetype=mime_type)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/get-picture', methods=['POST'])
def get_picture():
    try:
        data = request.get_json()
        print(data)
        databasePath = data.get('databasePath')  
        print(databasePath)
        file_path = data.get('file_path')
        print(file_path)
        end_operation_id = data.get('end_operation_id')
        print(end_operation_id)
        if not databasePath or not file_path:
            return jsonify({'error': 'No database path or file path provided'}), 400
        if os.path.exists(file_path)==False:
            return jsonify({'error': 'File not found'}), 404
        else:
            mime_type, _ = mimetypes.guess_type(file_path)
            return send_file(file_path,mimetype=mime_type)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/test', methods=['post'])
def testhowmanyrequest():
    print("this is a post request")
    return jsonify({'good': 'work'})
@app.route('/api/get-thumbnailname', methods=['POST'])
def get_thumbnailname():
    try:
        print("this is thumbnailname")
        data = request.get_json()
        print(data)
        databasePath = data.get('databasePath')  
        print(databasePath)
        end_operation_id = data.get('end_operation_id')
        print(end_operation_id)
        if not databasePath or not end_operation_id:
            return jsonify({'error': 'No database path or file path provided'}), 400
        path_list=serverfunction.fetch_thumbnailnames(databasePath, end_operation_id)
        # if not os.path.exists(path_list):
        print(path_list)

        
        return jsonify(path_list),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/get-keywordmatch', methods=['POST'])
def get_keywordmatch():
    try:
        print("this is keywordmatch")
        data = request.get_json()
        print(data)
        databasePath = data.get('databasePath')  
        print(databasePath)
        end_operation_id = data.get('end_operation_id')
        print(end_operation_id)
        if not databasePath or not end_operation_id:
            return jsonify({'error': 'No database path or file path provided'}), 400
        keywordmatchlist=serverfunction.get_all_keyword_data(databasePath, end_operation_id)
        if len(keywordmatchlist)==0:
            return jsonify({'error': 'No keyword match found'}), 404
        return jsonify(keywordmatchlist),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/get_all_experiment', methods=['POST'])
def get_all_experiment():
    try:
        print("This is get all experiment")
        result=serverfunction.get_all_experiment_data()
        print(result)
        return jsonify(result),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route('/api/get-xmldata', methods=['POST'])
# monitor connection
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'message': 'Connected successfully!'})  

# monitor disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# define custom event
@socketio.on('custom_event')
def handle_custom_event(data):
    print('Received data from client:', data)
    emit('response', {'message': 'Received your data'})   

# provide static files for the screenshot  image
@app.route('/screenshot2/<path:filename>')
def serve_screenshot(filename):
    return send_from_directory(SCREENSHOT_DIR, filename)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)

