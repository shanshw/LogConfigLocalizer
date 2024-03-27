import lxml
import pandas as pd
import os
from lxml import etree
import argparse
import csv
import openai
import os 
import sys
import re
import random
import string
import numpy as np
import time


openai.api_key = ''
xml_book = []

def load_triggered_descrip(propertyname,confPath):
    global xml_book
    if len(xml_book) == 0:
        df = pd.read_csv(confPath)
        df.fillna("<missing>", inplace=True) #astype(str).
        xml_book = df
    else: 
        df = xml_book
    for index,row in df.iterrows():
        # print(row.iloc[1] )
        # print(row.iloc[2] )
        # print(row.iloc[3] )
        if row.iloc[1] == propertyname:
            return row.iloc[3]
    return ""


def load_configuration_file(path):
    confPath = r"resources/property_corpus_numeric_only_with_des.csv"

    tree = etree.parse(path)
    root = tree.getroot()

    data = {'name': [], 'value': [],'description':[]}


    for property_elem in root.findall('.//property'):
        name_elem = property_elem.find('./name')
        value_elem = property_elem.find('./value')

        if name_elem is not None and value_elem is not None:
            name = name_elem.text
            value = value_elem.text
            des = load_triggered_descrip(name,confPath)
            data['name'].append(name)
            data['value'].append(value)
            data['description'].append(des)


    df = pd.DataFrame(data)

    return df
    
    

def write_rcconfig_direct_version(data,filename):

    columns = ['name', 'value', 'relevant log', 'explanation']

    df = pd.DataFrame(data, columns=columns)

    df.to_csv(os.path.join(filename,'RCConfig_Direct.csv'), index=False)




def write_response(filename,content):
    with open(filename,'w') as file:
        for line in content:
            file.write(line)
    print('file '+filename+' has finished writing')
    
    
def write_rcconfig(filename,input_content):
    filename =  os.path.join(filename,'RCConfig.csv')
    content_blocks = input_content.strip().split('\n\n')
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'value', 'relevant log', 'explanation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


        writer.writeheader()

        for block in content_blocks:
            block_lines = block.split('\n')
            data = {}
            for line in block_lines:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
            writer.writerow(data)

    print("output.csv")
    

def direct_inference(anomaly_path,xml):
    anomaly_file = 'anomaly_logs.csv'
    anomaly_real_path = os.path.join(anomaly_path,anomaly_file)
    # filter = ["job","hadoop","mapreduce"]
    # value_hit = []
    # property_hit = []
    hit = []
    filter = ["dfs","yarn","client","namenode","mapreduce","nodemanager","enabled","resourcemanager","datanode","ms","hadoop","fs","max","timeout","job","cache","size","interval","ipc","timeline-service"]   #top 20 
    with open(anomaly_real_path) as file:
        csv_reader = csv.DictReader(file)
        hits = set()
        for line in csv_reader:
            anomaly_degree = line['anomaly_degree']
            log = line['content']
            # logTem = line['template']
            # print(log)
            # print("-----------")
            # print("----------after-at-------------")
            print(log)
            if "at " in log:
                log = log.split("at ")[0]
            # print(log)
            # xml.fillna("", inplace=True)
            for index, row in xml.iterrows():
                property = row['name']
                if property in hits:
                    continue
                value = ""
                is_value_empty=False
                if row['value'] is None or row['value'] == "<missing>":
                    is_value_empty=True
                    value="<missing>"
                try:
                    if row['value'] == int(row['value']):
                        value = int(row['value'])
                    else:
                        value=str(row['value'])
                except:
                    value=str(row['value'])
                matches = False
                if is_value_empty ==False and str(value) in log:
                    matches = True
                if matches:
                    hit.append([property,value,log,"value-hit"])

                elif property in log:
                    hit.append([property,value,log,"property-hit"])
                else: #item hit
                    for item in property.split("."):
                        # singleitem = " "+item+" "
                        if item in log.lower():
                            if item in filter:
                                continue
                            # print("property-hit:",item,"\t",property,"\t",log
                            else:
                                # print()
                                hit.append([property,value,log,"property-item-hit"+"\t"+item])
                                # hits.add(property)


    # return value_hit,property_hit
    if len(hit) == 0:
        return None,False
    else:
        print(anomaly_path+"\t succeed")
        write_rcconfig_direct_version(hit,anomaly_path)
        return hit, True


def ask_GPT4(prompt,filename): 
    system_intel = "you are an expert in the filed of logs and software systems. When offered log and the configuration settings, please point out the anomaly of the logs and localize the most likely root-cause configuration properties. The offered information will be as follows: Configuration:name:<> value:<> des:<> Log:<>. The value and des could be <missing>, meaning that no value is set for the property. Please output the information in the following format: \"name:<>'\nvalue:<>'\nrelevant log:<index>-<>'\nexplanation:<>' \" for each suspected configuration property. The <index> indicates the line number. Splitting the logs within the same index is not allowed. The given logs may contain stack statements, please take them as reference. Please obey the rules:1. If some of the offered configuration properties seem to be irrelevant, please don't output them. 2. Don't output the same configuration property more than twice. At most 3 suspected properties while at least one required. 3. Please obey the aforementioned format, no other words should be output. "

    
    result = openai.ChatCompletion.create(model="gpt-4", 
                                 messages=[{"role": "system", "content": system_intel},
                                           {"role": "user", "content": prompt}],temperature=0)

    strd = result['choices'][0]['message']['content']
    usage = "prompt: "+str(result['usage']['prompt_tokens'])+"\t completion:"+str(result['usage']['completion_tokens'])+"\t total:"+str(result['usage']['total_tokens'])

    write_response(os.path.join(filename,'response.out'),strd)
    write_response(os.path.join(filename,'response_tokens_overhead.out'),usage)
    write_rcconfig(filename,strd)

def get_prompt(log_content,xml_content):
    strd = "Log:"
    strd = strd + log_content
    strd = strd+'\nConfiguration:\n'
    xml_content.fillna("<missing>", inplace=True) #astype(str).
    for index,row in xml_content.iterrows():
        # print(row)
        name = row['name']
        value = row['value']
        des = row['description']
        strd = strd+"name:"+str(name)+"\t value:"+str(value)+'\t des:'+str(des)+'\n'
    print(strd)
    print('prompt has been constructed.')
    return strd

def is_num(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def mutate_value(old_value):
    if is_num(old_value):
        mutate_rate = random.random()
        if 0 <= mutate_rate < 0.2:
            if 0 <= mutate_rate < 0.1:  # int
                new_value = str(abs(random.randint(0, 2**31 - 1)))
            else:
                new_value = str(abs(random.uniform(0, 1)))  # (0,1)
        elif 0.2 <= mutate_rate < 0.4:
            if 0.2 <= mutate_rate < 0.3:  # int
                new_value = str(abs(random.randint(0, 2**31 - 1)) * (-1))
            else:
                new_value = str(abs(random.uniform(-1, 0)))  # (-1,0)
        elif 0.4 <= mutate_rate < 0.6:
            new_value = "0"
        elif 0.6 <= mutate_rate < 0.8:
            new_value = generate_random_string(5)
        elif 0.8 <= mutate_rate < 1.0:
            new_value = ""


    return new_value.strip() if new_value != "" else new_value
    
def inject_xmls(csv_path,chosen_pr,fake_path,num_rows=9):
    if os.path.exists(fake_path):
        df = pd.read_csv(fake_path)
        return df,True

    df = pd.read_csv(csv_path)


    num_total_rows = df.shape[0]


    num_rows = min(num_rows, num_total_rows)

    random_indices = random.sample(range(num_total_rows), num_rows)


    random_rows = df.iloc[random_indices]
    data = {'name':[], 'value':[],'description':[]}
    for index,row in random_rows.iterrows():
        property = row.iloc[1]
        if chosen_pr == property:
            continue
        value = int(row.iloc[2])
        description = row.iloc[3]
        new_value = mutate_value(value)
        data['name'].append(property)
        data['value'].append(value)
        data['description'].append(description)
    return pd.DataFrame(data),False

def indirect_inference(anomaly_path,xml_content):
    anomaly_file = 'anomaly_logs.csv'
    anomaly_real_path = os.path.join(anomaly_path,anomaly_file)
    log_content = ""
    with open(anomaly_real_path) as file:
        csv_reader = csv.DictReader(file)
        i = 0
        for line in csv_reader:
            i = i+1
            anomaly_degree = line['anomaly_degree']
            log = line['content']
            log_content = str(i)+"-"+log_content + log.strip()


    
    ask_GPT4(get_prompt(log_content,xml_content),anomaly_path)



def ask_GPT4_ifSkip(prompt):
    system_intel = "you are an expert in the filed of logs and software systems. You receive information in the following format: \"<log content> root-cause configuration option: name:xxxx value:xxxx desc:xxxx\n \". Please output a probability value of the given configuration option on how likely it can trigger the offered log message. The standard are as follows: 1. The semanatic correlationship between them are strong and direct, output more than 90. 2. For others, output 30. Please output a single value in the following format:\"Probability is x.\""

        
    result = openai.ChatCompletion.create(model="gpt-4", 
                                 messages=[{"role": "system", "content": system_intel},
                                           {"role": "user", "content": prompt}],
                                 temperature=0
                                 )

    strd = result['choices'][0]['message']['content']
    usage = "prompt: "+str(result['usage']['prompt_tokens'])+"\t completion:"+str(result['usage']['completion_tokens'])+"\t total:"+str(result['usage']['total_tokens'])
    match = re.search(r'\d+', strd)
    if match:
        x = int(match.group())
        if x>=90:
            return x,True,usage
        else:
            return x,False,usage

def verify_direct(content,anomaly_path):

    flag = False
    responses = ""
    confPath = r"resources/property_corpus_numeric_only_with_des.csv"
    i=0
    hits = dict() 
    llm_start_time=time.time()
    for line in content:
        log = line[2]
        name = line[0]
        value = line[1] 
        desc = load_triggered_descrip(name,confPath)
        user_prompt = "log:"+log+"\n"
        user_prompt += "root-cause configuration option: name:" +str(name)+" value:"+str(value)
        user_prompt +=" des:"+str(desc)

        probability,if_pass,usage = ask_GPT4_ifSkip(user_prompt)
        responses+=str(probability)+"\t"
        if if_pass == True: 
            flag = True
            if name in hits:
                old_count = hits[name]
                hits[name] = old_count+1
            else:
                hits[name]=1
            i=i+1
            write_response(os.path.join(anomaly_path,'passed_option_'+str(i)+'_'+str(name)+"_"+str(probability)+'.out'),str(name)+"\t"+str(value)+"\t"+str(log)+"\t"+str(probability))
            write_response(os.path.join(anomaly_path,str(i)+"_tokens_overhead.out"),usage)

        else:
            i=i+1
            write_response(os.path.join(anomaly_path,'failed_option_'+str(i)+'_'+str(name)+"_"+str(probability)+'.out'),str(name)+"\t"+str(value)+"\t"+str(log)+"\t"+str(probability))
            write_response(os.path.join(anomaly_path,str(i)+"_tokens_overhead.out"),usage)
    llm_end_time=time.time()
    write_response(os.path.join(anomaly_path,'time_v_llm.log'),str(llm_end_time-llm_start_time))
    if len(hits)==0:
        write_response(os.path.join(anomaly_path,'response_ifSkip2.out'),responses)
        return False
    r_begin=time.time()
    max_value = max(hits.values())
    max_names = [name for name, value in hits.items() if value == max_value]
    j = 0
    for name in max_names:
        j = j+1
        write_response(os.path.join(anomaly_path,'most_likely_option_'+str(j)+'_'+name+".out"),name+"\t"+str(max_value))
    r_end=time.time()
    write_response(os.path.join(anomaly_path,'time_v_r.log'),str(r_end-r_begin))
    write_response(os.path.join(anomaly_path,'response_ifSkip2.out'),responses)
    return flag


def main(xml_file,records_path,rej):
    xml_content = load_configuration_file(xml_file) #original
    chosen_pr = ""
    xml_fake_content = []
    for index,row in xml_content.iterrows():
        chosen_pr = row['name']
    # inject
    if rej == False: #reject to inject
        xml_fake_content = xml_content
    else:
        corpus_path = r"resources/property_corpus_numeric_only_with_des.csv"
        fake_path=os.path.join(os.path.dirname(xml_file),"fake_configuration.csv")
        injected_xmls,if_exists = inject_xmls(corpus_path,chosen_pr,fake_path)
        if if_exists:
            xml_fake_content = injected_xmls
        else:
            xml_fake_content = pd.concat([xml_content,injected_xmls],ignore_index=True)
            xml_fake_content.to_csv(fake_path)
        xml_fake_content.fillna('<missing>',inplace=True)

    
    direct_start_time=time.time()
    content,skip = direct_inference(records_path,xml_fake_content)
    direct_end_time=time.time()
    write_response(os.path.join(records_path,'time_direct.log'),str(direct_end_time-direct_start_time))
    if skip:# to tell if there any hit for direct inference
        skip = verify_direct(content,records_path) # to tell if there is need to conduct indirect inference
    if skip == False:
        indirect_start_time=time.time()
        indirect_inference(records_path,xml_fake_content)
        indirect_end_time=time.time()
        write_response(os.path.join(records_path,'time_indirect.log'),str(indirect_end_time-indirect_start_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-cp",metavar ='specify the configuration file',help="configuration file path")
    parser.add_argument("-af",metavar = 'specify the anomaly log file', help="the anomaly_log file path")
    parser.add_argument("-rej",help='do not generate a fabricated configuration file', action='store_false')
    parser.add_argument("-api",help='the api key of openai to interact with GPT-4.')
    args = parser.parse_args()
    if args.cp == None or args.af == None or args.api == None:
        parser.print_help()
        sys.exit(1)
    openai.api_key=args.api
    main(args.cp,args.af,arg.rej)