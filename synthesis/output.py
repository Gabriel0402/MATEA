import os
import re
from utils import nodes_trans
def cent_output(lst, num_agents,target):
    result = []  
    kz=lst
    for i in range(len(lst) - 1):
        prev = set(lst[i].split(', ')) if lst[i] else set()
        curr = set(lst[i + 1].split(', ')) if lst[i + 1] else set()
        added = prev - curr 
        retained =curr - prev
        formatted = "&".join(sorted(retained))  
        if added:
            formatted += ("&" if formatted else "") + "&".join(f"!{x}" for x in sorted(added)) 
        result.append(formatted)  
        
    prev = set(lst[-1].split(', ')) if lst[-1] else set()
    curr = set(lst[target].split(', ')) if lst[target] else set()
    added = prev - curr 
    retained =curr - prev 
    formatted = "&".join(sorted(retained))  
    if added:
        formatted += ("&" if formatted else "") + "&".join(f"!{x}" for x in sorted(added))    
    result.append(formatted)  
    save_to_file(result, num_agents,kz,target)
    return result


def extract_and_format(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        last_line = lines[-1].strip()  
    matches = re.findall(r'\((\w)\)', last_line)
    if matches==[]:
        formatted_result = re.findall(r'[a-z]', last_line)
        formatted_result=formatted_result[0]
    else:
        formatted_result = '&'.join(sorted(matches))   
    return formatted_result

def is_subset(lst, kz):
    for item in kz:
        item_set = set(item.replace(', ', ',').split(','))  
        if all(elem in item_set for elem in lst):  
            return True  
    return False  

def save_to_file(lst, num_agents,kz,target):
    temple=0
    base_path = "../result"
    dir_path = os.path.join(base_path, f"{num_agents}agent") 
    base_path1 = "../examples"
    filename1 = os.path.join(base_path1, f"cop_{num_agents}agent")  
    filename = os.path.join(dir_path, "cent.txt")
    num_list = len(lst)
    os.makedirs(dir_path, exist_ok=True)
    label=extract_and_format(filename1)
    with open(filename, "w") as file:
        file.write("0 # initial state\n")  
        file.write(f"[{num_list}] # terminal state\n")  
        processed_lst = []
        for item in kz:
            if item:  
                sorted_item = "&".join(sorted(item.split(', ')))
                processed_lst.append(sorted_item)
            else:
                processed_lst.append("")
        for i in range(len(lst) - 1):
            if len(label)==1:
                
                if label in kz[i+1]:
                    line = f"({i},{i+1},'{lst[i]}',ConstantRewardFunction(1))\n"
                else:
                    line = f"({i},{i+1},'{lst[i]}',ConstantRewardFunction(0))\n"
                file.write(line)
            else:
                if label in processed_lst[i+1]:
                    line = f"({i},{i+1},'{lst[i]}',ConstantRewardFunction(1))\n"
                else:
                    line = f"({i},{i+1},'{lst[i]}',ConstantRewardFunction(0))\n"
                file.write(line)  
        temple = i + 1
        file.write(f"({temple},1,'{lst[-1]}', ConstantRewardFunction(0))")
def decent_output(lst,num_agents,target,alphabets):
    base_path = "../examples"
    base_path1 = "../result"
    filename = os.path.join(base_path, f"cop_{num_agents}agent")
    filename1 = os.path.join(base_path1, f"{num_agents}agent/cent.txt")
    controls_label=parse_module(filename)
    new_nodes=combina_nodes(controls_label,filename1,num_agents,target,alphabets)  
def parse_module(path):
    controls = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if "controls" in line:
                controls_part = line.split("controls")[1].strip()
                variables = [var.strip() for var in controls_part.split(',')]
                controls.append(variables)
    return controls
def filter_conditions(controls_label, conditions,num_agents,target,alphabets):
    filtered_conditions = []  
    for k in range(len(controls_label)):
        current_label = controls_label[k]  
        current_conditions = []  
        temple_label=[]
        end_label=[]
        new_label=[]
        nodes=[]
        cnt=1
        for condition in conditions:           
            condition_parts = re.findall(r'[a-zA-Z!&]+', condition)  
            include_condition = True
            condition_result = [] 
            for part in condition_parts:
                parts = re.findall(r'[!]*[a-zA-Z]+', part)
                for i in range (len(parts)):
                    current_parts=parts[i]
                    if current_parts.startswith('!'):
                        temple_parts=current_parts[1:]
                        if temple_parts in current_label:
                            temple_label=current_parts
                        else:
                            temple_label=[]
                    else:
                        if current_parts in current_label:
                            temple_label=current_parts
                        else:
                            temple_label=[]
                    if temple_label!=[]:
                        current_conditions.append(temple_label)   
                if current_conditions!=[]:
                    end_label.append(current_conditions)
                new_label.append(current_conditions)
                current_conditions=[]
                temple_label=[]
        end_label=merge_single_element_lists(end_label)
        str_label=end_label
        end_label = ['&'.join(item) for item in end_label]
        base_path1 = "../result"
        if num_agents==5:
            alphabets=['b','c','e','g','i']
        filename1 = os.path.join(base_path1, f"{num_agents}agent/mat{k+1}.txt")
        with open(filename1, "w") as file:
            file.write("0 # initial state\n")  
            file.write(f"[{len(end_label)}] # terminal state\n")              
            for z in range (len(end_label)-1):
                for x in range(len(str_label[z])):
                    if alphabets[k]==str_label[z][x]: 
                    
                        line = f"({z},{z+1},'{end_label[z]}',ConstantRewardFunction(1))\n"
                        break
                    else:
                        line = f"({z},{z+1},'{end_label[z]}',ConstantRewardFunction(0))\n"
                file.write(line)
            if nodes_trans(alphabets[k]):
                if num_agents==3:
                    file.write(f"({len(end_label)-1},{target-1},'{end_label[-1]}',ConstantRewardFunction(0))")
                else:
                    file.write(f"({len(end_label)-1},{target},'{end_label[-1]}',ConstantRewardFunction(0))")
            else:
                if num_agents==5 and alphabets[k]==end_label[0]:
                    file.write(f"({len(end_label)-1},{target},'{end_label[0]}&{end_label[-1]}',ConstantRewardFunction(1))")
                else:
                    if num_agents==5:
                        file.write(f"({len(end_label)-1},{target},'{end_label[0]}&{end_label[-1]}',ConstantRewardFunction(0))")
                    else:  
                        file.write(f"({len(end_label)-1},{target},'{end_label[-1]}',ConstantRewardFunction(0))")
    return filtered_conditions,str_label
def combina_nodes(controls_label, path,num_agents,target,alphabets):
    all_path = path
    conditions = []  
    excluded_keywords = ['initial', 'state','terminal','ConstantRewardFunction']  
    with open(all_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  
            condition_match = re.findall(r'[a-zA-Z!&]+', line)            
            if condition_match:
                condition_match = [cond for cond in condition_match if cond not in excluded_keywords]               
                if condition_match: 
                    conditions.extend(condition_match)
    str_label=filter_conditions(controls_label, conditions,num_agents,target,alphabets)
    return str_label

def merge_single_element_lists(data):
    result = []
    i = 1
    result.append(data[0])
    while i < len(data):
        if i < len(data) - 1 and len(data[i]) == 1 and len(data[i + 1]) == 1:
            result.append(data[i] + data[i + 1])
            i += 2  
        else:
            result.append(data[i])
            i += 1  
    return result






