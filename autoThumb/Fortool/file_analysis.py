import sqlite3
import os
import filecmp 
import exiftool
import xml.etree.ElementTree as ET
from pprint import pprint
import json
import cv2
import numpy as np
# import magic
def compare_dirs(dir1, dir2):
    dcmp = filecmp.dircmp(dir1, dir2)
    diff_dict = {
        "modified": [],
        "added": [],
        "removed": []
    }

    def list_diff_files(dcmp):
        # Recursively check all subdirectories first
        for sub_dcmp in dcmp.subdirs.values():
            list_diff_files(sub_dcmp)

        # Files that are different (only at the deepest level)
        for name in dcmp.diff_files:
            try:
                left_file_info = os.path.normpath(os.path.join(dcmp.left, name))
                right_file_info = os.path.normpath(os.path.join(dcmp.right, name))
                diff_dict["modified"].append((left_file_info, right_file_info))
            except Exception as e:
                print(f"Error processing modified file: {name}. Error: {e}")
        
        # Files only in the first directory (removed files or directories)
        for name in dcmp.left_only:
            try:
                left_file_info = os.path.normpath(os.path.join(dcmp.left, name))
                if os.path.isdir(left_file_info):
                    # Recursively add only the bottom-level files and directories in the removed directory
                    add_only_bottom_files(left_file_info, "removed")
                else:
                    diff_dict['removed'].append((left_file_info, None))
            except Exception as e:
                print(f"Error processing removed file: {name}. Error: {e}")
        
        # Files only in the second directory (added files or directories)
        for name in dcmp.right_only:
            try:
                right_file_info = os.path.normpath(os.path.join(dcmp.right, name))
                if os.path.isdir(right_file_info):
                    # Recursively add only the bottom-level files and directories in the added directory
                    add_only_bottom_files(right_file_info, "added")
                else:
                    diff_dict["added"].append((None, right_file_info))
            except Exception as e:
                print(f"Error processing added file: {name}. Error: {e}")
    
    def add_only_bottom_files(directory, change_type):
        """
        Recursively adds only bottom-level files and directories to the diff_dict.
        :param directory: The directory to check.
        :param change_type: Either "added" or "removed" depending on the context.
        """
        has_subdirs = False
        for root, dirs, files in os.walk(directory):
            if dirs:
                has_subdirs = True
            else:
                # If there are no subdirectories, add the current directory as a bottom-level directory
                if not files and change_type == "added":
                    diff_dict["added"].append((None, root))
                elif not files and change_type == "removed":
                    diff_dict["removed"].append((root, None))

            # Add bottom-level files
            for file in files:
                file_path = os.path.normpath(os.path.join(root, file))
                if change_type == "added":
                    diff_dict["added"].append((None, file_path))
                elif change_type == "removed":
                    diff_dict["removed"].append((file_path, None))

            # If this is a bottom-level directory (no subdirectories), add it
            if not dirs:
                break

    list_diff_files(dcmp)
    return diff_dict
# please use install labmagic in your environment
# def check_file_header(file_path):
#     """
#     Check the file header to identify file type using libmagic.
    
#     :param file_path: Path to the file to check.
#     :return: Detected file type, if known.
#     """
#     try:
        
#         mime = magic.Magic(mime=True)
#         file_type = mime.from_file(file_path)
        
#         if "sqlite" in file_type:
#             return "db"
#         elif "image" in file_type:
#             return "picture"
#         elif "xml" in file_type or "text/xml" in file_type:
#             return "xml"
#         else:
#             return "other"
#     except Exception as e:
#         print(f"Error reading file {file_path}: {e}")
#         return None

# def distinguish_file(diff_dict):
#     # init dict
#     detail_dict = {
#         "modified": {"xml": [], "db": [], "picture": [], "other": []},
#         "added": {"xml": [], "db": [], "picture": [], "other": []},
#         "removed": {"xml": [], "db": [], "picture": [], "other": []}
#     }
    
#     for change_type in ["modified", "added", "removed"]:
#         for file_tuple in diff_dict[change_type]:
#             if change_type == "modified":
#                 left_file, right_file = file_tuple
#                 categorized = False

#                 if left_file:
#                     detected_type = check_file_header(left_file)
#                     if detected_type:
#                         detail_dict[change_type][detected_type].append((left_file, right_file))
#                         categorized = True
#                 if not categorized and left_file:
#                     detail_dict[change_type]["other"].append((left_file, right_file))
#             else:
#                 file_path = file_tuple[0] if file_tuple[0] else file_tuple[1]
#                 if file_path:
#                     detected_type = check_file_header(file_path)
#                     if detected_type:
#                         detail_dict[change_type][detected_type].append(file_path)
#                     else:
#                         detail_dict[change_type]["other"].append(file_path)
    
#     print(detail_dict)
#     return detail_dict

def check_file_header(file_path):
    """
    Check the file header to identify file type based on magic numbers or specific signatures.
    
    :param file_path: Path to the file to check.
    :return: Detected file type, if known.
    """
    file_signatures = {
        "db": [b"SQLite format 3"],  # SQLite database signature
        "picture": [b"\xFF\xD8\xFF", b"\x89PNG\r\n\x1a\n", b"GIF89a", b"GIF87a"],  # JPEG, PNG, GIF signatures
        # You can add more file type signatures as needed
    }
    
    try:
        with open(file_path, "rb") as f:
            file_header = f.read(16)  # Read the first 16 bytes (most file signatures fit in this range)
        
        # Check against known signatures
        for file_type, signatures in file_signatures.items():
            for signature in signatures:
                if file_header.startswith(signature):
                    return file_type
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
def distinguish_file(diff_dict):

    file_types = {
        "xml": [".xml"],
        "db": [".db", ".sqlite", ".sql"],
        "picture": [".jpg", ".jpeg", ".png", ".gif", ".bmp","webp"],
        "other": []
    }
    
    # init dict
    detail_dict = {
        "modified": {"xml": [], "db": [], "picture": [],"other": []},
        "added": {"xml": [], "db": [], "picture": [], "other": []},
        "removed": {"xml": [], "db": [], "picture": [], "other": []}
    }
    
    # check file dict
    for change_type in ["modified", "added", "removed"]:
        for file_tuple in diff_dict[change_type]:
            # modified is tuple
            if change_type == "modified":
                left_file, right_file = file_tuple  
                categorized = False

                
                if left_file:
                    file_ext = os.path.splitext(left_file)[1].lower()
                    for category, extensions in file_types.items():
                        if file_ext in extensions:
                            detail_dict[change_type][category].append((left_file, right_file))  # add tuple
                            categorized = True
                            break
                    if not categorized:
                        detected_type = check_file_header(left_file)
                        if detected_type:
                            detail_dict[change_type][detected_type].append((left_file, right_file))
                            categorized = True
                # if the file is not in the file_types, then add as "other"
                if not categorized and left_file:
                    detail_dict[change_type]["other"].append((left_file, right_file))  # 作为元组加入
                    if detected_type:
                            detail_dict[change_type][detected_type].append((left_file, right_file))
                            categorized = True
            # added or removed
            else:
                # only left the effect path
                file_path = file_tuple[0] if file_tuple[0] else file_tuple[1]
                if file_path:
                    file_ext = os.path.splitext(file_path)[1].lower()
                    categorized = False

                    # check file type
                    for category, extensions in file_types.items():
                        if file_ext in extensions:
                            detail_dict[change_type][category].append(file_path)
                            categorized = True
                            break
                    if not categorized:
                        detected_type = check_file_header(file_path)
                        if detected_type:
                            detail_dict[change_type][detected_type].append(file_path)
                            categorized = True
                    # if the file is not in the file_types, then add as "other"
                    if not categorized:
                        detail_dict[change_type]["other"].append(file_path)
    print(detail_dict)
    return detail_dict
"""
function carving tool (analysis for the other files)-----for extract
input file_name/path/content
"""
MAGIC_NUMBERS = {
    "png": b"\x89PNG\r\n\x1a\n",       # Magic bytes for PNG files
    "jpeg": [b"\xff\xd8\xff\xe0", b"\xff\xd8\xff\xe1"],  # Magic bytes for JPEG files (multiple headers)
    "webp": b"RIFF",                    # Magic bytes for WebP files
}
# only focus on jpg webp png
def carving_tool(input, output_directory, log_file, original_path=None):
    """
    Extracts media files (PNG, JPEG, GIF) from the input and saves them to the specified directory,
    while logging the source file path.
    
    :param input: The input file path or content
    :param output_directory: The directory where extracted files will be saved
    :param log_file: The file where the source file path will be logged
    :param original_path: The original path of the file if the input is file content
    """
    path_for_check=[]
    # If the input is a file path, read the file content
    input=str(str(input))
    if isinstance(input, str) and os.path.isfile(input):
        with open(input, "rb") as file:
            file_content = file.read()
        original_path = input  # Record the original path
    else:
        return None  # Use content directly if it's provided
        
    
    files_extracted = False  # Flag to check if any files were extracted

    # Search for and extract files based on magic numbers
    for file_type, magic in MAGIC_NUMBERS.items():
        magics = magic if isinstance(magic, list) else [magic]  # Handle multiple magic numbers (like for JPEG)
        found = False  # Track if we found a match for this file type
        
        for m in magics:
            start = 0
            while True:
                pos = file_content.find(m, start)
                if pos == -1:
                    break
                
                found = True  # We found a match
                
                # Determine the file's end marker
                if file_type == "png":
                    end_marker = b"IEND"
                elif file_type == "jpeg":
                    end_marker = b"\xff\xd9"
                else:
                    end_marker = None
                
                # Find the end of the file
                if end_marker:
                    end_pos = file_content.find(end_marker, pos) + len(end_marker)
                    if end_pos == -1:
                        end_pos = len(file_content)
                else:
                    end_pos = len(file_content)

                # Extract the file segment
                extracted_content = file_content[pos:end_pos]
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory, exist_ok=True)
                output_directory = os.path.join(output_directory, "extracted")
                # print(12321)
                # print(output_directory)
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory, exist_ok=True)
                
                
                # Use the correct file extension based on file_type
                file_extension = file_type if file_type != "jpeg" else "jpg"
                file_name = f"{os.path.basename(original_path)}_{file_type}_{pos}.{file_extension}"
                output_path = os.path.join(output_directory, file_name)

                path_for_check.append(output_path)
                # Save the extracted file
                with open(output_path, "wb") as output_file:
                    output_file.write(extracted_content)
                
                # Log the extraction details
                with open(log_file, "a") as log:
                    log.write(f"Extracted {file_type.upper()} from {original_path}, saved as {file_name}\n")
                
                print(f"Successfully extracted {file_type.upper()} file: {output_path}")
                files_extracted = True  # Set flag to true once a file is extracted
                start = end_pos  # Update the start position for the next search
                if file_type == "webp":
                    list2=extract_webp_from_cache(input, output_directory,original_path)
                    if len(list2)>0:
                        path_for_check.extend(list2)

                   
        if not found:
            print(f"No {file_type.upper()} files found in {original_path}")
        
    # If no files were extracted, print a message
    if not files_extracted:
        print(f"No media files found in {original_path}")
        return None
    else:
        return path_for_check        

"""
function exif_picture(): show the metadata of the picture
pyexiftool
input file list or file
return is the string of the metadata
"""
def exif_picture(file):
    file_metadata = {}
    try:
        with exiftool.ExifToolHelper() as et:
            # Access the metadata
            metadata = et.get_metadata(file)
            # Populate the dictionary without including the filename
            
            for d in metadata:
                for tag, value in d.items():
                    if tag != 'SourceFile':  # Skip the SourceFile tag
                        file_metadata[tag] = value
    except Exception as e:
        print(f"Error accessing EXIF data for {file}: {e}")
        return {}
    return file_metadata

# Example usage
# metadata_dict = exif_picture("9-test.png")
# print(metadata_dict)

# check db file
## 1. show the data then check which tabel which information have been changeed
## input(file_name1, file_name2) filename1 2 is the path new is 2 old is 1
# function1 show the database data
        # dir_path modified 
def bytes_to_hex_string(data):
    if isinstance(data, bytes):
        return {"value": data.hex(), "is_bytes": True}  
    elif isinstance(data, (tuple, list)):
        return [bytes_to_hex_string(item) for item in data]  
    else:
        return {"value": data, "is_bytes": False} 
    
def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [table[0] for table in tables]

def get_table_content(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description] 
    return rows, columns

def compare_databases(db1_path, db2_path):
    try:
        conn1 = sqlite3.connect(db1_path)
        conn2 = sqlite3.connect(db2_path)
    except sqlite3.Error as e:
        print(f"Error connecting to databases: {e}")
        return None
    
    try:
        tables_db1 = get_table_names(conn1)
        tables_db2 = get_table_names(conn2)
    except sqlite3.Error as e:
        print(f"Error retrieving table names: {e}")
        conn1.close()
        conn2.close()
        return None
    
    diff_result = {
        "missing_tables_in_db2": [],
        "missing_tables_in_db1": [],
        "modified_tables": []
    }
    
    # compare db1 and db2
    for table in tables_db1:
        if table not in tables_db2:
            diff_result["missing_tables_in_db2"].append(table)
        else:
            try:
                rows_db1, columns_db1 = get_table_content(conn1, table)
                rows_db2, columns_db2 = get_table_content(conn2, table)
            except sqlite3.Error as e:
                print(f"Error retrieving data from table {table}: {e}")
                continue
            
            # find difference
            added = []
            removed = []
            modified = []
            try:
                for row in rows_db2:
                    if row not in rows_db1:
                        added.append([{"column": col, "value": bytes_to_hex_string(val)} for col, val in zip(columns_db2, row)])
                
                for row in rows_db1:
                    if row not in rows_db2:
                        removed.append([{"column": col, "value": bytes_to_hex_string(val)} for col, val in zip(columns_db1, row)])

                for row in rows_db1:
                    if row in rows_db2:
                        index_in_db2 = rows_db2.index(row)
                        if row != rows_db2[index_in_db2]:
                            modified.append({
                                "original": [{"column": col, "value": bytes_to_hex_string(val)} for col, val in zip(columns_db1, row)],
                                "modified": [{"column": col, "value": bytes_to_hex_string(val)} for col, val in zip(columns_db2, rows_db2[index_in_db2])]
                            })
                
                if added or removed or modified:
                    diff_result["modified_tables"].append({
                        "table": table,
                        "added_rows": added,
                        "removed_rows": removed,
                        "modified_rows": modified
                    })
            except Exception as e:
                print(f"Error while processing table {table}: {e}")
    # compare db2 and db1
    for table in tables_db2:
        if table not in tables_db1:
            diff_result["missing_tables_in_db1"].append(table)

    conn1.close() 
    conn2.close()
    
    return diff_result


import xml.etree.ElementTree as ET

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None

# compare nodes
def compare_nodes(node1, node2, path=""):
    diff_result = {
        "removed": [],
        "added": [],
        "modified": []
    }

    # check tag
    if node1.tag != node2.tag:
        diff_result["modified"].append({"path": path, "tag": {"before": node1.tag, "after": node2.tag}})
    
    # check attributes
    if node1.attrib != node2.attrib:
        diff_result["modified"].append({"path": path, "attributes": {"before": node1.attrib, "after": node2.attrib}})
    
    # check text content
    text1 = node1.text.strip() if node1.text is not None else ""
    text2 = node2.text.strip() if node2.text is not None else ""
    
    if text1 != text2:
        diff_result["modified"].append({"path": path, "text": {"before": text1, "after": text2}})
    
    # deal with child nodes
    children1 = list(node1)
    children2 = list(node2)
    
    # handle nodes that are removed
    for child1 in children1:
        match = False
        for child2 in children2:
            if child1.tag == child2.tag:
                match = True
                child_path = f"{path}/{child1.tag}" if path else child1.tag
                sub_diff = compare_nodes(child1, child2, child_path)
                diff_result["removed"].extend(sub_diff["removed"])
                diff_result["added"].extend(sub_diff["added"])
                diff_result["modified"].extend(sub_diff["modified"])
                break
        if not match:
            diff_result["removed"].append({"path": f"{path}/{child1.tag}", "element": ET.tostring(child1, encoding='unicode')})
    
    # deal with nodes that are added
    for child2 in children2:
        match = False
        for child1 in children1:
            if child2.tag == child1.tag:
                match = True
                break
        if not match:
            diff_result["added"].append({"path": f"{path}/{child2.tag}", "element": ET.tostring(child2, encoding='unicode')})
    
    return diff_result

# compare two xml files
def compare_xml_files(file1, file2):
    root1 = parse_xml(file1)
    root2 = parse_xml(file2)
    
    if root1 is None or root2 is None:
        return
    
    differences = compare_nodes(root1, root2)
    return differences


def pretty_print_diff(diff):
    print("\n=== Missing Tables in DB2 ===")
    if diff["missing_tables_in_db2"]:
        for table in diff["missing_tables_in_db2"]:
            print(f"- {table}")
    else:
        print("None")
    
    print("\n=== Missing Tables in DB1 ===")
    if diff["missing_tables_in_db1"]:
        for table in diff["missing_tables_in_db1"]:
            print(f"- {table}")
    else:
        print("None")
    
    print("\n=== Modified Tables ===")
    if diff["modified_tables"]:
        for modification in diff["modified_tables"]:
            table_name = modification["table"]
            added_rows = modification["added_rows"]
            removed_rows = modification["removed_rows"]
            print(f"\nTable: {table_name}")
            
            if added_rows:
                print("  Added Rows:")
                for row in added_rows:
                    print(f"    {row}")
            else:
                print("  No rows added.")
            
            if removed_rows:
                print("  Removed Rows:")
                for row in removed_rows:
                    print(f"    {row}")
            else:
                print("  No rows removed.")
    else:
        print("No modifications found.")
"""
for some other file we using carving tool and exiftool analysis
"""
def cache_thumbnail_analysis(file_name):
    output_directory = "./ttee2"
    log_file = "./log.txt"
    a=carving_tool(file_name,output_directory,log_file)
    print(a)
    if a==0:
        print("carving tool found nothing")
    else:
        for x in a:
            print(x)
            print(f"check for the thumbnail of {x}")
            b=exif_picture(x)
            print(b)

def prepare_data_for_insertion(detail_dict, start_operation_id, end_operation_id):

    data_to_insert = {
        "modified":[],
        "added":[],
        "removed":[]
    }

    for file_type, file_categories in detail_dict["modified"].items(): # detail_dict["modified"]:
        for files in file_categories:
            

                filepath1 = files[0]
                filepath2 = files[1]
                filename = os.path.basename(filepath1)
                
                
             
                record = (
                    filename,           
                    filepath1,
                    filepath2,          
                    file_type,          
                    start_operation_id, 
                    end_operation_id   
                )
                

                data_to_insert["modified"].append(record)

    for file_type, file_categories in detail_dict["added"].items(): # detail_dict["modified"]:
        for files in file_categories:
               
                filepath = files
                
                filename = os.path.basename(filepath)
                
                
                
                record = (
                    filename,           
                    filepath,         
                    file_type,          
                    start_operation_id, 
                    end_operation_id    
                )
                
                
                data_to_insert["added"].append(record)
    
    for file_type, file_categories in detail_dict["removed"].items(): 
        for files in file_categories:
            
                
                filepath = files
                filename = os.path.basename(filepath)
                
                record = (
                    filename,           
                    filepath,         
                    file_type,          
                    start_operation_id, 
                    end_operation_id   
                )

                data_to_insert["removed"].append(record)    
    print(data_to_insert)
    return data_to_insert

def convert_to_detail_dict(data_to_insert):
    """
    """
    detail_dict = {
        "modified": {"xml": [], "db": [], "picture": [],  "other": []},
        "added": {"xml": [], "db": [], "picture": [],  "other": []},
        "removed": {"xml": [], "db": [], "picture": [],  "other": []}
    }

    for record in data_to_insert["modified"]:
        filename, filepath1, filepath2, file_type, start_operation_id, end_operation_id = record
        if file_type in detail_dict["modified"]:
            detail_dict["modified"][file_type].append((filepath1, filepath2))

    for record in data_to_insert["added"]:
        filename, filepath, file_type, start_operation_id, end_operation_id = record
        if file_type in detail_dict["added"]:
            detail_dict["added"][file_type].append(filepath)

    for record in data_to_insert["removed"]:
        filename, filepath, file_type, start_operation_id, end_operation_id = record
        if file_type in detail_dict["removed"]:
            detail_dict["removed"][file_type].append(filepath)
    print(detail_dict)

    return detail_dict

def fetch_added_table(database_path):

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    result = {}

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [column[1] for column in cursor.fetchall()] 

            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            table_data = [ {column: bytes_to_hex_string(value) for column, value in zip(columns, row)}
                for row in rows]

            result[table_name] = table_data
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

    return result

def display_xml(file_path, added=True):
    def traverse_node(node, path=""):
        diff_result = {
            "added": [] if added else [],
            "removed": [] if not added else [],
            "modified": []
        }
        

        current_path = f"{path}/{node.tag}" if path else node.tag
        

        element_string = ET.tostring(node, encoding='unicode')
        

        if added:
            diff_result["added"].append({"path": current_path, "element": element_string})
        else:
            diff_result["removed"].append({"path": current_path, "element": element_string})
        

        for child in node:
            child_diff = traverse_node(child, current_path)
            diff_result["added"].extend(child_diff["added"])
            diff_result["removed"].extend(child_diff["removed"])
        
        return diff_result


    root = parse_xml(file_path)
    
    if root is None:
        return None  
    

    return traverse_node(root)


import random
import os

def find_images_with_sift(small_image_paths, large_image_path, output_path, min_match_count=10):
    """
    """
    
    img2_color = cv2.imread(large_image_path)
    if img2_color is None:
        print("can't read big big screenshot")
        return None

    
    img2_gray = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)

    
    sift = cv2.SIFT_create()

    
    matches_info = []

 
    for small_image_path in small_image_paths:
        img1_color = cv2.imread(small_image_path[1])  
        if img1_color is None:
            print(f"can't read small image file:{small_image_path[1]}")
            continue

       
        img1_gray = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)

      
        kp1, des1 = sift.detectAndCompute(img1_gray, None)
        kp2, des2 = sift.detectAndCompute(img2_gray, None)

       
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

      
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        
        if len(good_matches) >= min_match_count:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

          
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            
            h, w = img1_gray.shape
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            matches_info.append({
                "dst": dst,
                "path": small_image_path[0]
            })
        else:
            print(f"matchfailed - {len(good_matches)}/{min_match_count} in {small_image_path[0]}")


    if not matches_info:
        return None


    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)] 
    for i, match_info in enumerate(matches_info):
        dst = match_info['dst']
        file_path = match_info['path']

        color = colors[i % len(colors)]  
        img2_color = cv2.polylines(img2_color, [np.int32(dst)], True, color, 3, cv2.LINE_AA)

 
        parts = file_path.replace('\\', '/').split('/') 
        short_path = '/'.join(parts[-2:]) if len(parts) >= 2 else file_path

        x, y = np.int32(dst[0][0]) 
        cv2.putText(img2_color, short_path, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


    if not os.path.exists(output_path):
        os.makedirs(output_path)

    random_number = random.randint(1, 100)

    output_file_name = os.path.splitext(os.path.basename(large_image_path))[0] + str(random_number)+'_marked.png'
    output_file_path = os.path.join(output_path, output_file_name)


    cv2.imwrite(output_file_path, img2_color)


    return output_file_path

def extract_webp_from_cache(file_path, output_directory,filename):
    webp_files = []
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

            # Find all occurrences of "RIFF" followed by "WEBP"
            riff_indices = []
            idx = data.find(b'RIFF')
            while idx != -1:
                if data[idx+8:idx+12] == b'WEBP':
                    riff_indices.append(idx)
                idx = data.find(b'RIFF', idx + 1)

            # Extract each WebP file based on RIFF block
            for i, start_idx in enumerate(riff_indices):
                # Read the file size from the RIFF header (4 bytes after "RIFF")
                file_size = int.from_bytes(data[start_idx+4:start_idx+8], 'little') + 8
                webp_data = data[start_idx:start_idx + file_size]

                # Save extracted WebP to output directory
                output_file_path = os.path.join(output_directory,  f"{filename}_webp_{i}.webp")
                with open(output_file_path, 'wb') as out_file:
                    out_file.write(webp_data)
                webp_files.append(output_file_path)

        print(f"Extracted {len(webp_files)} WebP files.")
    except Exception as e:
        print(f"Error processing cache file: {e}")

    return webp_files

def search_in_dict_with_keys_ignore_case(data, target_keys):
    """

    """
    
    matches = set()  
    
    
    target_keys_lower = [str(key).lower() for key in target_keys]
    
   
    if isinstance(data, dict):
        for key, value in data.items():
          
            key_str = str(key).lower() if isinstance(key, (str, int, float)) else ""
            value_str = str(value).lower() if isinstance(value, (str, int, float)) else ""
            
           
            for target_key in target_keys_lower:
                if target_key in key_str:
                    matches.add(target_key) 
                elif target_key in value_str:
                    matches.add(target_key) 
            
          
            if isinstance(value, (dict, list)):
                matches.update(search_in_dict_with_keys_ignore_case(value, target_keys))

    
    elif isinstance(data, (list, tuple)):
        for item in data:
            if isinstance(item, (str, dict, list)):
                matches.update(search_in_dict_with_keys_ignore_case(item, target_keys))
    
    return list(matches)  



