import os
import time
import subprocess
from PIL import Image


def get_size():
    command = "adb shell wm size"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    resolution_line = result.stdout.strip().split('\n')[-1]
    width, height = map(int, resolution_line.split(' ')[-1].split('x'))
    return width, height
    
    
def get_xml(adb_path):
    process = subprocess.Popen([adb_path, 'shell', 'uiautomator', 'dump'], stdout=subprocess.PIPE)
    process.communicate()
    subprocess.run([adb_path, 'pull', '/sdcard/window_dump.xml', './xml/window_dump.xml'])


def take_screenshots(adb_path, num_screenshots, output_folder, crop_y_start, crop_y_end, slide_y_start, slide_y_end):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(num_screenshots):
        command = adb_path + f" shell rm /sdcard/screenshot{i}.png"
        subprocess.run(command, capture_output=True, text=True, shell=True)
        command = adb_path + f" shell screencap -p /sdcard/screenshot{i}.png"
        subprocess.run(command, capture_output=True, text=True, shell=True)
        command = adb_path + f" pull /sdcard/screenshot{i}.png {output_folder}"
        subprocess.run(command, capture_output=True, text=True, shell=True)
        image = Image.open(f"{output_folder}/screenshot{i}.png")
        cropped_image = image.crop((0, crop_y_start, image.width, crop_y_end))
        cropped_image.save(f"{output_folder}/screenshot{i}.png")
        subprocess.run([adb_path, 'shell', 'input', 'swipe', '500', str(slide_y_start), '500', str(slide_y_end)])

adb_path = "C:\\Users\\19000\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"
def get_screenshot(adb_path,image_path = "./screenshot/screenshot.png",save_path = "./screenshot/screenshot.jpg", socketio = None):
    print("zhixing")
    command = adb_path + " shell rm /sdcard/screenshot.png"
    subprocess.run(command, capture_output=True, text=True, shell=True)
    time.sleep(1)
    command = adb_path + " shell screencap -p /sdcard/screenshot.png"
    result=subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print("Failed to take screenshot on device:", result.stderr)
    time.sleep(1)
    command = adb_path + " pull /sdcard/screenshot.png ./screenshot/screenshot.png"
    subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print("Failed to pull screenshot to local:", result.stderr)
    time.sleep(1)
    print("wancheng")
    image = Image.open(image_path)
    image.convert("RGB").save(save_path, "JPEG")
    
    # os.remove(image_path)
# get_screenshot(adb_path)
def get_keyboard(adb_path):
    command = adb_path + " shell dumpsys input_method"
    process = subprocess.run(command, capture_output=True, text=True, shell=True, encoding='utf-8')
    output = process.stdout.strip()
    for line in output.split('\n'):
        if "mInputShown" in line:
            if "mInputShown=true" in line:
                
                for line in output.split('\n'):
                    if "hintText" in line:
                        hintText = line.split("hintText=")[-1].split(" label")[0]
                        break
                
                return True, hintText
            elif "mInputShown=false" in line:
                return False, None


def tap(x, y):
    shell=subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    command = f"input tap {x} {y} \n"
    shell.stdin.write("su\n")
    shell.stdin.flush()
    shell.stdin.write(command)
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    print(command)
# tap(444,468)
def clear(shell):
    shell.stdin.write("input keyevent 28\n")  # Move cursor to the start
    shell.stdin.write("input keyevent 123\n") # Move cursor to the end
    for _ in range(100):  # Adjust the number based on expected text length
        shell.stdin.write("input keyevent 67\n")  # Delete characters one by one
    shell.stdin.flush()
def type(text):
    text = text.replace("\\n", "_").replace("\n", "_")
    shell=subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    shell.stdin.write("su\n")
    if "#CLEAR#" in text:
        clear(shell)
        # Remove "CLEAR" from the text so it doesn’t get typed
        text = text.replace("#CLEAR#", "")
    if "#ENTER#" in text:
        command0="input keyevent KEYCODE_ENTER\n"
        shell.stdin.write(command0)
        shell.stdout.flush()
        text = text.replace("#ENTER#", "")
    for char in text:
        if char == ' ':
            command1 = f"input text %s \n"
            shell.stdin.write(command1)
            shell.stdout.flush()
        elif char == '_':
            command2 = f"input keyevent 66 \n"
            shell.stdin.write(command2)
            shell.stdout.flush()
        elif 'a' <= char <= 'z' or 'A' <= char <= 'Z' or char.isdigit():
            command3 = f"input text {char} \n"
            shell.stdin.write(command3)
            shell.stdout.flush()
        elif char in '-.,!?@\'°/:;()':
            command4 = f"input text \"{char}\" \n"
            shell.stdin.write(command4)
            shell.stdout.flush()
        else:
            command5 = f" am broadcast -a ADB_INPUT_TEXT --es msg \"{char}\" \n"
            shell.stdin.write(command5)
            shell.stdout.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
# type("#ENTER#")

def slide(x1, y1, x2, y2):
    shell=subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    command = f"input swipe {x1} {y1} {x2} {y2} 260 \n"
    shell.stdin.write("su\n")
    shell.stdin.flush()
    shell.stdin.write(command)
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    print(command)
# slide(400,1000,400,400)


def back():
    shell=subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    command = f"input keyevent 4 \n"
    shell.stdin.write("su\n")
    shell.stdin.flush()
    shell.stdin.write(command)
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    print(command)
# back()   
def home():
    x,y=get_size()
    shell=subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    command1 = f"input keyevent 82 \n"
    shell.stdin.write("su\n")
    shell.stdin.flush()
    shell.stdin.write(command1)
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    print(command1)
    
    time.sleep(3)
    slide(x/2,y/2,x/2,0)
def pause_show_more():
    shell=subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    command = f"input keyevent KEYCODE_MEDIA_PAUSE \n"
    shell.stdin.write("su\n")
    shell.stdin.flush()
    shell.stdin.write(command)
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    shell.stdin.write("exit\n")
    shell.stdin.flush()
    print(command)