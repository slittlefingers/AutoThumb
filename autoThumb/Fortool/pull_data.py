import os
import subprocess
import hashlib
import time
def check_adb_devices():
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.splitlines()
    
    if len(lines) > 2:
        return True
    else:
        return False

def check_root_access():
    result = subprocess.run(['adb', 'root'], stdout=subprocess.PIPE, text=True)
    if 'cannot run as root' in result.stdout:
        return False
    return True

def create_unique_folder(base_path):
    folder_index = 0
    while True:
        if folder_index == 0:
            new_folder = os.path.join(base_path, "test")
        else:
            new_folder = os.path.join(base_path, f"test_{folder_index}")
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
            return new_folder
        folder_index += 1

def pull_app_data(package_name, destination_folder):
    pull_command = f"adb pull /data/data/{package_name} {destination_folder}"
    print(f"Pulling data for {package_name} to {destination_folder}...")
    os.system(pull_command)
import subprocess
def delete_file(file_path):
    delete_command = ["adb", "shell", "rm", "-r", file_path]
    try:
        subprocess.run(delete_command, check=True)
        print(f"Successfully deleted {file_path}")
    except subprocess.CalledProcessError:
        print(f"Failed to delete {file_path}, skipping...")
def pull_file(file_path, destination_folder):
    print(file_path)
    pull_command = ["adb", "pull", file_path, destination_folder]
    try:
        subprocess.run(pull_command, check=True)
        print(f"Successfully pulled {file_path}")
    except subprocess.CalledProcessError:
        print(f"Failed to pull {file_path}, skipping...")

# def pull_directory_files(directory, destination_folder):
#     list_command = ["adb", "shell", "ls", directory]
#     try:
#         files = subprocess.check_output(list_command, text=True).split()
#         for file in files:
#             full_path = f"{directory}/{file}"
#             pull_file(full_path, destination_folder)
#     except subprocess.CalledProcessError:
#         print(f"Failed to list files in {directory}")
def sha256sum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
# print(sha256sum("ttee/file/com.google.android.youtube.tar"))
# import tarfile
# def sanitize_path(path):
#     # 替换不支持的字符
#     invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
#     for char in invalid_chars:
#         path = path.replace(char, '_')
#     return path

# def extract_tar_file(tar_file_path, destination_folder):
#     if not os.path.exists(destination_folder):
#         os.makedirs(destination_folder)
    
#     with tarfile.open(tar_file_path, 'r:*') as tar_ref:
#         for member in tar_ref.getmembers():
#             sanitized_name = sanitize_path(member.name)
#             member.name = sanitized_name
#             tar_ref.extract(member, path=destination_folder)
#         print(f"Extracted all files to {destination_folder}")
def extract_tar_with_powershell(tar_path, destination_folder):
    command = f"powershell -Command \"tar -xf {tar_path} -C {destination_folder}\""
    subprocess.run(command, shell=True, check=True)
    print(f"Extracted tar file to: {destination_folder}")

def pull_main(package_name, destination_folder,d_folder="./sdcard/"):
    Package_name = "/data/data/"+package_name
    D_folder=d_folder+package_name
    tar_name = package_name+".tar"
    tar_folder=d_folder+tar_name
        # adb shell
    # with subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as shell:
    #     shell.stdin.write("su\n")
    #     shell.stdin.flush() 
    #     shell.stdin.write(f"cp -a {Package_name} {d_folder} \n")
    #     shell.stdin.flush()
    #     shell.stdin.write("cd sdcard/ \n")
    #     shell.stdin.flush()
    #     shell.stdin.write(f"tar cf {tar_name} {package_name}\n")
    #     shell.stdin.flush()
    #     shell.stdin.write(f"sha256sum {tar_name} \n")
    #     shell.stdin.flush()
    #     shell.stdin.write("exit\n")
    #     shell.stdin.flush()
    #     shell.stdin.write("exit\n")
    #     shell.stdin.flush()
    #     # 打印输出
    #     sha256output = shell.stdout.read()
    #     print(sha256output)
    with subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as shell:
        commands = f"""
        su
        cp -a {Package_name} {d_folder}
        cd sdcard/
        tar cf {tar_name} {package_name}
        sha256sum {tar_name}
        exit
        exit
        """
        sha256output, stderr = shell.communicate(commands)
    print(sha256output)
    foldername="file"
    destination_folder = os.path.join(destination_folder, foldername )  
    os.makedirs(destination_folder, exist_ok=True)
    print(tar_folder)
    pull_file(tar_folder, destination_folder)
    tar_L_files=os.path.join(destination_folder, tar_name)
    
    print(sha256output)
    hash_value=sha256sum(tar_L_files)
    print(hash_value)
    if hash_value == sha256output.split(" ")[0]:
        print("file integrity")
    else:
        print("not intergrity")
    stime=time.time()
    extract_tar_with_powershell(tar_L_files, destination_folder)
    etime=time.time()
    print("extract time equal to",etime-stime)
    delete_file(D_folder)
    delete_file(tar_folder)
    final_path = os.path.join(destination_folder, package_name)
    destination_folder_up_two_levels = os.path.dirname(destination_folder)
    screenshot_path = os.path.join(destination_folder_up_two_levels, "screenshot.jpg")
    return final_path, screenshot_path
# pull_main("com.zhiliaoapp.musically","ttee")

# pull_main("com.instagram.android","ttee")
# pull_main("tv.twitch.android.app","ttee")
# pull_main("com.snapchat.android","ttee")
# pull_main("org.telegram.messenger","ttee")
# pull_main("com.twitter.android","ttee")
# tar_file_path = 'C:/path/to/your/file.tar'  # 也可以是 .tar.gz 或 .tar.bz2
# destination_folder = 'C:/path/to/your/destination'
# extract_tar_file(tar_file_path, destination_folder) 
import subprocess
import re
def find_package(keyword):
    try:
        # Run the adb command to list packages and capture the output
        shell=subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        command = f"pm list packages\n"
        shell.stdin.write("su\n")
        shell.stdin.flush()
        shell.stdin.write(command)
        shell.stdin.flush()
        shell.stdin.write("exit\n")
        shell.stdin.flush()
        shell.stdin.write("exit\n")
        shell.stdin.flush()
        result, stderr = shell.communicate()
        print(result)
        if shell.returncode != 0:
            print(f"Error occurred: {stderr}")
            return None
        # Convert the keyword to lowercase for case-insensitive matching
        keyword_lower = keyword.lower()
        # Filter the results using Python instead of grep
        package_pattern = re.compile(r'^package:(.*)$', re.MULTILINE)
        packages = package_pattern.findall(result)
        matching_packages = [pkg for pkg in packages if keyword_lower in pkg.lower()]
        if matching_packages:
            print("Found the following packages:")
            for index, package in enumerate(matching_packages, start=1):
                print(f"{index}. {package}")
            # Let the user choose a package
            choice = int(input("Enter the number of the package you want to select: "))
            if 1 <= choice <= len(matching_packages):
                selected_package = matching_packages[choice - 1]
                print(f"You selected: {selected_package}")
                return selected_package
            else:
                print("Invalid choice")
        else:
            print("No packages found containing the keyword:", keyword)

    except Exception as e:
        print(f"An error occurred: {e}")
def find_package2(keyword):
    try:
        # Run the adb command to list packages and capture the output
        shell=subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        command = f"pm list packages\n"
        shell.stdin.write("su\n")
        shell.stdin.flush()
        shell.stdin.write(command)
        shell.stdin.flush()
        shell.stdin.write("exit\n")
        shell.stdin.flush()
        shell.stdin.write("exit\n")
        shell.stdin.flush()
        result, stderr = shell.communicate()
        print(result)
        if shell.returncode != 0:
            print(f"Error occurred: {stderr}")
            return None
        # Convert the keyword to lowercase for case-insensitive matching
        keyword_lower = keyword.lower()
        # Filter the results using Python instead of grep
        package_pattern = re.compile(r'^package:(.*)$', re.MULTILINE)
        packages = package_pattern.findall(result)
        return packages

    except Exception as e:
        print(f"An error occurred: {e}")
# print(1)
# pull_main("com.google.android.youtube","ttee2")
