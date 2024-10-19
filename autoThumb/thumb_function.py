import os
import time
import copy
import torch
import shutil
from PIL import Image, ImageDraw

from Agent.api import inference_chat, inference_chat_image
from Agent.text_localization import ocr
from Agent.icon_localization import det
from Agent.controller import get_screenshot, tap, slide, type, back, home, pause_show_more
from Agent.prompt import get_action_prompt, get_reflect_prompt, get_memory_prompt, get_process_prompt
from Agent.chat import init_action_chat, init_reflect_chat, init_memory_chat, add_response, add_response_two_image,return_chat
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope import snapshot_download, AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from dashscope import MultiModalConversation
import dashscope
import concurrent
import Fortool.pull_data as pull_data
import re
import random
import json
import sys
import logging
import time
from serverfuction import serverfunction
import os
import shutil
####################################### Edit your Setting #########################################
# Your ADB path
# adb_path = ""
adb_path = "C:\\Users\\19000\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"

# Choose between "api" and "local". api: use the qwen api. local: use the local qwen checkpoint
caption_call_method = "api"

# Choose between "qwen-vl-plus" and "qwen-vl-max" if use api method. Choose between "qwen-vl-chat" and "qwen-vl-chat-int4" if use local method.
caption_model = "qwen-vl-plus"



# Your GPT-4o API URL
API_url = "https://api.openai.com/v1/chat/completions"

# Your GPT-4o API Token
# input your gpt token
token=""

# input qwen api
qwen_api=""

###################################################################################################
memory_switch = True
reflection_switch = False
caption_call_method = "api"
caption_model = "qwen-vl-plus"

logger = logging.getLogger('myLogger')
# logger.info('hello world')
def log_time(action_id, operation_id,operation_name, step_name, duration):
    with open("timelog.txt", "a") as f: 
        f.write(f"Action ID: {action_id}, Operation ID: {operation_id}, Operation Name: {operation_name},{step_name} duration: {duration:.4f} seconds\n")
def clear_folder_contents(folder_path):
    """clear contents of folder"""
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)  
        else:
            os.remove(item_path)  

    print(f"cleared contents of folder: {folder_path}")



def create_insfolder(instruction):
    folder_name = str(instruction)
    base_folder=".\Record"
    folder_name = os.path.join(base_folder, folder_name)
    if os.path.exists(folder_name):
        print("instruction folder exists")
    else:
        os.mkdir(folder_name)
    return folder_name

def create_actionfolder(action_id,iter,action,instruction_folder):
    action_safe = re.sub(r'[<>:"/\\|?*]', "_", action.replace(" ", "_").replace("(", "_").replace(")", "_"))
    folder_name = "Action"+str(action_id)+str(iter)+str(action_safe)
    action_folder_name = os.path.join(instruction_folder, folder_name)
    if os.path.exists(action_folder_name):
        print("Action folder exists")
    else:
        os.mkdir(action_folder_name)
    return action_folder_name

    
def get_all_files_in_folder(folder_path):
    file_list = []
    for file_name in os.listdir(folder_path):
        file_list.append(file_name)
    return file_list


def draw_coordinates_on_image(image_path, coordinates):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    point_size = 10
    for coord in coordinates:
        draw.ellipse((coord[0] - point_size, coord[1] - point_size, coord[0] + point_size, coord[1] + point_size), fill='red')
    output_image_path = './screenshot/output_image.png'
    image.save(output_image_path)
    return output_image_path


def crop(image, box, i):
    image = Image.open(image)
    x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
    if x1 >= x2-10 or y1 >= y2-10:
        return
    cropped_image = image.crop((x1, y1, x2, y2))
    cropped_image.save(f"./temp/{i}.jpg")


def generate_local(tokenizer, model, image_file, query):
    query = tokenizer.from_list_format([
        {'image': image_file},
        {'text': query},
    ])
    response, _ = model.chat(tokenizer, query=query, history=None)
    return response


def process_image(image, query):
    dashscope.api_key = qwen_api
    image = "file://" + image
    messages = [{
        'role': 'user',
        'content': [
            {
                'image': image
            },
            {
                'text': query
            },
        ]
    }]
    response = MultiModalConversation.call(model=caption_model, messages=messages)
    
    try:
        response = response['output']['choices'][0]['message']['content'][0]["text"]
    except:
        response = "This is an icon."
    
    return response


def generate_api(images, query):
    icon_map = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_image, image, query): i for i, image in enumerate(images)}
        
        for future in concurrent.futures.as_completed(futures):
            i = futures[future]
            response = future.result()
            icon_map[i + 1] = response
    
    return icon_map


def merge_text_blocks(text_list, coordinates_list):
    merged_text_blocks = []
    merged_coordinates = []

    sorted_indices = sorted(range(len(coordinates_list)), key=lambda k: (coordinates_list[k][1], coordinates_list[k][0]))
    sorted_text_list = [text_list[i] for i in sorted_indices]
    sorted_coordinates_list = [coordinates_list[i] for i in sorted_indices]

    num_blocks = len(sorted_text_list)
    merge = [False] * num_blocks

    for i in range(num_blocks):
        if merge[i]:
            continue
        
        anchor = i
        
        group_text = [sorted_text_list[anchor]]
        group_coordinates = [sorted_coordinates_list[anchor]]

        for j in range(i+1, num_blocks):
            if merge[j]:
                continue

            if abs(sorted_coordinates_list[anchor][0] - sorted_coordinates_list[j][0]) < 10 and \
            sorted_coordinates_list[j][1] - sorted_coordinates_list[anchor][3] >= -10 and sorted_coordinates_list[j][1] - sorted_coordinates_list[anchor][3] < 30 and \
            abs(sorted_coordinates_list[anchor][3] - sorted_coordinates_list[anchor][1] - (sorted_coordinates_list[j][3] - sorted_coordinates_list[j][1])) < 10:
                group_text.append(sorted_text_list[j])
                group_coordinates.append(sorted_coordinates_list[j])
                merge[anchor] = True
                anchor = j
                merge[anchor] = True

        merged_text = "\n".join(group_text)
        min_x1 = min(group_coordinates, key=lambda x: x[0])[0]
        min_y1 = min(group_coordinates, key=lambda x: x[1])[1]
        max_x2 = max(group_coordinates, key=lambda x: x[2])[2]
        max_y2 = max(group_coordinates, key=lambda x: x[3])[3]

        merged_text_blocks.append(merged_text)
        merged_coordinates.append([min_x1, min_y1, max_x2, max_y2])

    return merged_text_blocks, merged_coordinates

# get_screenshot(adb_path)
def get_perception_infos(adb_path, screenshot_file,temp_file):
    
    get_screenshot(adb_path)
    
    width, height = Image.open(screenshot_file).size
    
    text, coordinates = ocr(screenshot_file, ocr_detection, ocr_recognition)
    text, coordinates = merge_text_blocks(text, coordinates)
    
    center_list = [[(coordinate[0]+coordinate[2])/2, (coordinate[1]+coordinate[3])/2] for coordinate in coordinates]
    draw_coordinates_on_image(screenshot_file, center_list)
    
    perception_infos = []
    for i in range(len(coordinates)):
        perception_info = {"text": "text: " + text[i], "coordinates": coordinates[i]}
        perception_infos.append(perception_info)
        
    coordinates = det(screenshot_file, "icon", groundingdino_model)
    
    for i in range(len(coordinates)):
        perception_info = {"text": "icon", "coordinates": coordinates[i]}
        perception_infos.append(perception_info)
        
    image_box = []
    image_id = []
    for i in range(len(perception_infos)):
        if perception_infos[i]['text'] == 'icon':
            image_box.append(perception_infos[i]['coordinates'])
            image_id.append(i)

    for i in range(len(image_box)):
        crop(screenshot_file, image_box[i], image_id[i])

    images = get_all_files_in_folder(temp_file)
    if len(images) > 0:
        images = sorted(images, key=lambda x: int(x.split('/')[-1].split('.')[0]))
        image_id = [int(image.split('/')[-1].split('.')[0]) for image in images]
        icon_map = {}
        prompt = 'This image is an icon from a phone screen. Please briefly describe the shape and color of this icon in one sentence,please all using english.'
        if caption_call_method == "local":
            for i in range(len(images)):
                image_path = os.path.join(temp_file, images[i])
                icon_width, icon_height = Image.open(image_path).size
                if icon_height > 0.8 * height or icon_width * icon_height > 0.2 * width * height:
                    des = "None"
                else:
                    des = generate_local(tokenizer, model, image_path, prompt)
                icon_map[i+1] = des
        else:
            for i in range(len(images)):
                images[i] = os.path.join(temp_file, images[i])
            icon_map = generate_api(images, prompt)
        for i, j in zip(image_id, range(1, len(image_id)+1)):
            if icon_map.get(j):
                perception_infos[i]['text'] = "icon: " + icon_map[j]
    
    for i in range(len(perception_infos)):
        perception_infos[i]['coordinates'] = [int((perception_infos[i]['coordinates'][0]+perception_infos[i]['coordinates'][2])/2), int((perception_infos[i]['coordinates'][1]+perception_infos[i]['coordinates'][3])/2)]
        
    return perception_infos, width, height

### Load caption model ###
device = "cuda"
torch.manual_seed(1234)
if caption_call_method == "local":
    if caption_model == "qwen-vl-chat":
        model_dir = snapshot_download('qwen/Qwen-VL-Chat', revision='v1.1.0')
        model = AutoModelForCausalLM.from_pretrained(model_dir, device_map=device, trust_remote_code=True).eval()
        model.generation_config = GenerationConfig.from_pretrained(model_dir, trust_remote_code=True)
    elif caption_model == "qwen-vl-chat-int4":
        qwen_dir = snapshot_download("qwen/Qwen-VL-Chat-Int4", revision='v1.0.0')
        model = AutoModelForCausalLM.from_pretrained(qwen_dir, device_map=device, trust_remote_code=True,use_safetensors=True).eval()
        model.generation_config = GenerationConfig.from_pretrained(qwen_dir, trust_remote_code=True, do_sample=False)
    else:
        print("If you choose local caption method, you must choose the caption model from \"Qwen-vl-chat\" and \"Qwen-vl-chat-int4\"")
        exit(0)
    tokenizer = AutoTokenizer.from_pretrained(qwen_dir, trust_remote_code=True)
elif caption_call_method == "api":
    pass
else:
    print("You must choose the caption model call function from \"local\" and \"api\"")
    exit(0)


### Load ocr and icon detection model ###
groundingdino_dir = snapshot_download('AI-ModelScope/GroundingDINO', revision='v1.0.0')
groundingdino_model = pipeline('grounding-dino-task', model=groundingdino_dir)
ocr_detection = pipeline(Tasks.ocr_detection, model='damo/cv_resnet18_ocr-detection-line-level_damo')
ocr_recognition = pipeline(Tasks.ocr_recognition, model='damo/cv_convnextTiny_ocr-recognition-document_damo')
def original_process(instruction,insfolder_name, package_name,databasePath,action_id):
    action="original_state"
    iter=0
    summary=instruction
    Thumbchecklist=[]
    insfolder_name=create_insfolder(insfolder_name)
    destination_folder = create_actionfolder(action_id,iter,action,insfolder_name)  
    final_path, screenshot_path=pull_data.pull_main(package_name,destination_folder)
    screenshot_path=None
    serverfunction.add_action_operation_first(databasePath,action_id,summary,final_path, screenshot_path,Thumbchecklist)
    return True
def execute_process(ocr_detection, ocr_recognition, API_url, token, adb_path, instruction, add_info, memory_switch, reflection_switch, insfolder_name, package_name,browser=True,home_flag=True,databasePath=None,action_id=None):
    

    
    thought_history = []
    summary_history = []
    action_history = []
    summary = ""
    action = ""
    completed_requirements = ""
    memory = ""
    insight = ""
    temp_file = "temp"
    screenshot = "screenshot"
    summary_list = []
    if not os.path.exists(temp_file):
        os.mkdir(temp_file)
    if not os.path.exists(screenshot):
        os.mkdir(screenshot)
    error_flag = False
    # which application to extract
    insfolder_name=create_insfolder(insfolder_name)
    print(insfolder_name)

    iter = 0
    while True:
        start_operation_time = time.time()
        Thumbchecklist=[]
        iter += 1
        if iter == 1:
            screenshot_file = "./screenshot/screenshot.jpg"

            perception_infos, width, height = get_perception_infos(adb_path, screenshot_file,temp_file)
            shutil.rmtree(temp_file)
            os.mkdir(temp_file)
            shutil.copy(screenshot_file, insfolder_name)
            keyboard = False
            keyboard_height_limit = 0.9 * height
            for perception_info in perception_infos:
                if perception_info['coordinates'][1] < keyboard_height_limit:
                    continue
                if 'ADB Keyboard' in perception_info['text']:
                    keyboard = True
                    break

        prompt_action = get_action_prompt(instruction, perception_infos, width, height, keyboard, summary_history, action_history, summary, action, add_info, error_flag, completed_requirements, memory,home_flag)
        chat_action = init_action_chat()
        chat_action = add_response("user", prompt_action, chat_action, screenshot_file)

        output_action = inference_chat(chat_action, 'gpt-4o', API_url, token)
        thought = output_action.split("### Thought ###")[-1].split("### Action ###")[0].replace("\n", " ").replace(":", "").replace("  ", " ").strip()
        summary = output_action.split("### Operation ###")[-1].replace("\n", " ").replace("  ", " ").strip()
        action = output_action.split("### Action ###")[-1].split("### Operation ###")[0].replace("\n", " ").replace("  ", " ").strip()
        chat_action = add_response("assistant", output_action, chat_action)
        status = "#" * 50 + " Decision " + "#" * 50
        summary_list.append(summary)
        print(action)
        # print(status)
        time.sleep(1)
        logger.info("[ACTION]"+str(action_id))
        time.sleep(0.5)
        logger.info('[OPERATION]'+summary)
        time.sleep(0.5)
        logger.info('[THINKING]'+thought)
        time.sleep(0.5)
        print("waiting for processing...")
        time.sleep(10)
        # print(output_action)
        print('#' * len(status))
        
        if memory_switch:
            prompt_memory = get_memory_prompt(insight)
            chat_action = add_response("user", prompt_memory, chat_action)
            output_memory = inference_chat(chat_action, 'gpt-4o', API_url, token)
            chat_action = add_response("assistant", output_memory, chat_action)
            status = "#" * 50 + " Memory " + "#" * 50
            print(status)
            print(output_memory)
            print('#' * len(status))
            output_memory = output_memory.split("### Important content ###")[-1].split("\n\n")[0].strip() + "\n"
            if "None" not in output_memory and output_memory not in memory:
                memory += output_memory
        
        if "Open app" in action:
            app_name = action.split("(")[-1].split(")")[0]
            text, coordinate = ocr(screenshot_file, ocr_detection, ocr_recognition)
            tap_coordinate = [0, 0]
            for ti in range(len(text)):
                if app_name == text[ti]:
                    name_coordinate = [int((coordinate[ti][0] + coordinate[ti][2])/2), int((coordinate[ti][1] + coordinate[ti][3])/2)]
                    tap(name_coordinate[0], name_coordinate[1]- int(coordinate[ti][3] - coordinate[ti][1]))# 
        if "Pause" in action:
            pause_show_more()
        elif "Tap" in action:
            coordinate = action.split("(")[-1].split(")")[0].split(", ")
            x, y = int(coordinate[0]), int(coordinate[1])
            tap(x, y)
        
        elif "Swipe" in action:
            coordinate1 = action.split("Swipe (")[-1].split("), (")[0].split(", ")
            coordinate2 = action.split("), (")[-1].split(")")[0].split(", ")
            x1, y1 = int(coordinate1[0]), int(coordinate1[1])
            x2, y2 = int(coordinate2[0]), int(coordinate2[1])
            slide(x1, y1, x2, y2)
            
        elif "Type" in action:
            if "(" in action:
                answer = action.split("(")[-1].split(")")[0]
            elif " \"" in action:
                answer = action.split(" \"")[-1].split("\"")[0]
            else:
                answer= action[len("Type: "):]
            print(answer)
            type(answer)
            Thumbchecklist.append(answer)
        
        elif "Back" in action:
            back()
        
        elif "Home" in action:
        
            home()
            
        elif "Stop" in action:
            if browser==True:
                return summary_list
            return True
            
        time.sleep(5)
        
        last_perception_infos = copy.deepcopy(perception_infos)
        last_screenshot_file = "./screenshot/last_screenshot.jpg"
        last_keyboard = keyboard
        if os.path.exists(last_screenshot_file):
            os.remove(last_screenshot_file)
        time.sleep(1)
        print("wait for copying...")
        if os.path.exists(screenshot_file):
            os.rename(screenshot_file, last_screenshot_file)
        else:
            print("test failed")
            break
        
  
        perception_infos, width, height = get_perception_infos(adb_path, screenshot_file,temp_file)
        print(perception_infos)
        extracted_texts = []
        for info in perception_infos:
            if info['text'].startswith("text: "):
                extracted_text = info['text'][len("text: "):]  
                extracted_texts.append(extracted_text)
        Thumbchecklist.extend(extracted_texts)
        shutil.rmtree(temp_file)
        os.mkdir(temp_file)
        keyboard = False
        for perception_info in perception_infos:
            if perception_info['coordinates'][1] < keyboard_height_limit:
                continue
            if 'ADB Keyboard' in perception_info['text']:
                keyboard = True
                break
        
        if reflection_switch:
            prompt_reflect = get_reflect_prompt(instruction, last_perception_infos, perception_infos, width, height, last_keyboard, keyboard, summary, action, add_info)
            chat_reflect = init_reflect_chat()
            chat_reflect = add_response_two_image("user", prompt_reflect, chat_reflect, [last_screenshot_file, screenshot_file])

            output_reflect = inference_chat(chat_reflect, 'gpt-4o', API_url, token)
            reflect = output_reflect.split("### Answer ###")[-1].replace("\n", " ").strip()
            chat_reflect = add_response("assistant", output_reflect, chat_reflect)
            status = "#" * 50 + " Reflcetion " + "#" * 50
            print(status)
            print(output_reflect)
            print('#' * len(status))
            if 'A' in reflect:
                thought_history.append(thought)
                summary_history.append(summary)
                action_history.append(action)
                
                prompt_planning = get_process_prompt(instruction, thought_history, summary_history, action_history, completed_requirements, add_info)
                chat_planning = init_memory_chat()
                chat_planning = add_response("user", prompt_planning, chat_planning)
                output_planning = inference_chat(chat_planning, 'gpt-4o', API_url, token)
                chat_planning = add_response("assistant", output_planning, chat_planning)
                status = "#" * 50 + " Planning " + "#" * 50
                print(status)
                print(output_planning)
                print('#' * len(status))
                completed_requirements = output_planning.split("### Completed contents ###")[-1].replace("\n", " ").strip()
                
                error_flag = False
            
            elif 'B' in reflect:    
                error_flag = False
                back()
                
                
            elif 'C' in reflect:
                error_flag = False
        
        else:
            thought_history.append(thought)
            summary_history.append(summary)
            action_history.append(action)
            
            prompt_planning = get_process_prompt(instruction, thought_history, summary_history, action_history, completed_requirements, add_info)
            chat_planning = init_memory_chat()
            chat_planning = add_response("user", prompt_planning, chat_planning)
            output_planning = inference_chat(chat_planning, 'gpt-4o', API_url, token)
            chat_planning = add_response("assistant", output_planning, chat_planning)
            status = "#" * 50 + " Planning " + "#" * 50
            print(status)
            print(output_planning)
            print('#' * len(status))
            completed_requirements = output_planning.split("### Completed contents ###")[-1].replace("\n", " ").strip()
        # create action folder and pull data inside
        destination_folder = create_actionfolder(action_id,iter,action,insfolder_name)
        if not pull_data.check_adb_devices():
            print("pleace connect device")
            break

        if browser==True and error_flag==False: 
            
            get_screenshot(adb_path,save_path = f"./browser_screenshot/screenshot_{iter}.jpg")

        else:
            start_pull_time = time.time()
            final_path, screenshot_path=pull_data.pull_main(package_name,destination_folder)
            end_pull_time = time.time()
            extraction_time = end_pull_time - start_pull_time
            print(f"extraction time: {extraction_time}")
            log_time(action_id,iter,summary,"extraction",extraction_time)
            serverfunction.add_action_operation(databasePath,action_id,summary,final_path, screenshot_path,Thumbchecklist)
        shutil.copy(screenshot_file, destination_folder)        
        os.remove(last_screenshot_file)
        end_operation_time = time.time()
        operation_time=end_operation_time-start_operation_time
        print(f"operation time: {operation_time}")
        log_time(action_id,iter,summary,"operation",operation_time)
        if iter>=7 and browser==False:
            print("Try to run 7 times, hard to complate this job, please try again")
            return False
def find_package_name(application_name):
    clear_folder_contents('./browser_screenshot')
    # clear_folder_contents('./Record')
    clear_folder_contents('./screenshot')

    # # first we let the user input which application he wanna to do th forensic experiment
    prompt=[("user",f"The {application_name} inside the android /data/data/ what is the package name, the answer format should be like this (including the square brackets): package_name: [package name1]; package_name: [package name2]")]
    response=inference_chat(prompt,'gpt-4o', API_url, token)
    print(response)
    # print (response)
    # # application_name="zhiliaoapp"
    package_names = re.findall(r'package_name:\s*\[(\w[\w\.]*)\]', response)
    print(package_names)
    return package_names

def found_package_name(package_names):
        if package_names:
            package_name = pull_data.find_package2(package_names)
        if package_name:
            return True
        else:
            return False

def initial_analysis(application_name,package_name):
    instruction = f"Find the {application_name} in the main interface. You may need to swipe left or right. if you found open it."
    add_info = "If you want to tap an icon of an app, use the action \"Open app\"."
    print(instruction.format(application_name=application_name))    
    insfolder_name="initial_analysis"
    execute_process(ocr_detection, ocr_recognition, API_url, token, adb_path, instruction, add_info, memory_switch, reflection_switch, insfolder_name,package_name,browser=True, home_flag=False)
    
    instruction=f"Now you are in the {application_name}'s first section. browse through the app's different sections in the navigation bar. When finished,return to the home screen."
# instruction = f"Find the {application_name}. You may need to swipe left or right. Open the {application_name} and browse through the app's different sections in the navigation bar. When finished,return to the home screen."
# add_info = "if you don't find any other icons, swipe left or right to see other icons; If you want to tap an icon of an app, use the action \"Open app\". "
    print(instruction)
    # instruction_summary = "youtube_forensic_browser"
    insfolder_name="youtube_forensic_browser"
    summary_list = execute_process(ocr_detection, ocr_recognition, API_url, token, adb_path, instruction, add_info, memory_switch, reflection_switch, insfolder_name,package_name,browser=True, home_flag=True)
# # send to the chatgpt to deduce
    browser_folder_path = './browser_screenshot'

# # # List to hold the relative paths of jpg files
    jpg_file_list = []

    # Iterate through the files in the folder
    for file_name in os.listdir(browser_folder_path)[:-1]:
        # Check if the file is a .jpg file
        if file_name.lower().endswith('.jpg'):
            # Combine the folder path with the file name to get the relative path
            relative_path = os.path.join(browser_folder_path, file_name)
            # Replace backslashes with forward slashes
            relative_path = relative_path.replace('\\', '/')
            # Add the relative path to the list
            jpg_file_list.append(relative_path)
    print(summary_list)
    summary_picture=""
    i=1
    summary_list=summary_list[0:-1]
    jpg_file_list=jpg_file_list[0:-1]
    for summary in summary_list:    
        summary_picture+= "after " + summary + "find the " +  "screenshot"  + str(i)+"\n"
        i+=1
    print("this is summary picture"+"\n"+summary_picture)
    # # Print the list of .jpg file paths
    # for jpg_file in jpg_file_list:
    #     print(jpg_file)
    # prompt=f"This is a non-standard GUI inside the {{application_name}} Application on an Android Smart Phone. I need to analyze what user actions could potentially alter or create thumbnail images inside of the phone excluding taking a screenshot. The actions could include things like in app homepage,watching the video, in short pagepausing the video, or sharing the video. Your answer format should be like this: action: [which seciton][action1]; action: [which section][action2]"
    # This is a non-standard GUI inside the Youtube Application on an Android Smart Phone. I need to analyze what user actions could potentially alter or create thumbnail images inside of the phone excluding taking a screenshot. The actions could include things like watching the video, pausing the video, or sharing the video. Your answer format should be like this: Action 1; Action 2; Action 3;
    # response=inference_chat_image(prompt,'gpt-4o', API_url, token,jpg_file_list)
    prompt=f"""
    This is a non-standard GUI inside the {application_name} Application on an Android Smartphone. 

    {summary_picture}

    I need to analyze what user actions could potentially alter or create thumbnail images inside of the phone, excluding taking a screenshot.

    Please recognize the section based on the content (such as video or navigation cues). If the section is related to video content (e.g., a video is playing or selected), perform video-related actions and include the section name in the output. Similarly, if the section is related to navigation (e.g., homepage, subscriptions), adjust the actions accordingly.

    Action Sequences:

    1. For video-related sections (e.g., homepage or video ,etc), follow this sequence, and you add add more according to the screenshot like click like button or subscribe:**
    - action: [section_name][slide the video one time]
    - action: [section_name][open the video]
    - action: [section_name][watch the video]
    - action: [section_name][pause the video]

    2. For short video-related sections (e.g., shorts or video, etc), follow this sequence. you can add more according to the screenshot like click like button or subscribe**
    - action: [section_name][pause the short]
    - action: [section_name][slide the short one time]

    3. For other sections (e.g.,  subscriptions, profile, settings , etc), adjust actions based on the user's interaction in that section:**


    ### Your answer format should be like this: "action: [which seciton][action1]; action: [which section][action2];"

    example action: [in home section][slide the YouTube application];

    """
    chat=return_chat(prompt,jpg_file_list)

    # print(len(chat))
    response=inference_chat(chat,'gpt-4o', API_url, token)
    print(response)
    def extract_key_information(response):
        
        actions = re.findall(r'action:\s+(.*?);', response)

        return actions
    actions_list = extract_key_information(response)
    formatted_actions = []
    for action in actions_list:
        section, action_detail = action.strip("[]").split("][")
        formatted_actions.append(f"In {section} section, {action_detail}")
    return formatted_actions

def execute_action(actions_list, application_name,package_name,database_path,experiment_name):
    

    # clear_folder_contents('./Record/')
    clear_folder_contents('./screenshot')
    for action in actions_list:
        print(action)
    foldername=f".\Record\{experiment_name}"
    if os.path.exists(foldername):
        clear_folder_contents(foldername)
    for id,instruction in enumerate(actions_list):
        insfolder_name=f"{experiment_name}"

        print(instruction)
        add_info="if you wanna pause the normal video please using the instruction [pause video], if it is a shorts or short video you should using the instruction \*tap (x,y)*\ tap of in the middle screen "
        if "pause" in instruction:
            reflection_switch=False
        else:
            reflection_switch=False
        if instruction=="original_state":
            result=original_process(instruction,insfolder_name, package_name,database_path,id)
        elif instruction==actions_list[-1]:
            result=execute_process(ocr_detection, ocr_recognition, API_url, token, adb_path, instruction, add_info, memory_switch, reflection_switch, insfolder_name,package_name,browser=False, home_flag=True,databasePath=database_path,action_id=id)
        else:
            result=execute_process(ocr_detection, ocr_recognition, API_url, token, adb_path, instruction, add_info, memory_switch, reflection_switch, insfolder_name,package_name,browser=False, home_flag=False,databasePath=database_path,action_id=id)
        if result==False:
            status="not completed"
        elif result==True:
            status="completed"
            serverfunction.add_status(database_path, id, status)
            if instruction==actions_list[-1]:
                time.sleep(0.5)
                logger.info('[THINKING]'+"Mission Completed")
                time.sleep(0.5)

            
    

