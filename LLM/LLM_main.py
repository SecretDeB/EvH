import random
import time
import string
import re
from collections import deque
from google import genai

# import streamlit as st
import os

from sympy import false

# from tensorflow.python.data.experimental import snapshot
# from torch import candidate

from BFULT import BloomFilter

padding = 0
bf = BloomFilter(0, 0)
key_size = 0
word_list = []
pk_length = 0
items_count = 0
max_size = 1000000
count_bf = 0
count_llm = 0
file_length = 0
# threshold_ = 10000
threshold_ = 1
fan_out = {}
print_threshold = 11
flag_print_thresh = True

# files = ["apple is a fruit", "tiger is an animal"]
files = []
# files_key=["100","101"]
# files_key = [
#     "1101101111000110110010101101101000111111000100101010100110111101101111010110101101011010101001111111110011011111100110100111110111111011001101000111100101111011100001100111101100101111000111110000100111111110011100110000110001110101000100100010101100101101",
#     "1101101111000110110010101101101000111111000100101010100110111101101111010110101101011010101001111111110011011111100110100111110111111011001101000111100101111011100001100111101100101111000111110001100111111110011100110000110001110101000100100010101100101101",
# "11011011110001101100101011011010001111110001001010101001101111011011110101101011010110101010011111111100110111111001101001111101111110110011010001111001011110111000011001111011001011110001111100001001111111100111001100001100011101010001001000101011001011011",
# ]

files_key = ["Key1", "Key2", "Key3", "Key4", "Key5", "Key6", "Key7", "Key8", "Key9", "Key10"]
padding_flag = False
contents = []

client = genai.Client(api_key="AIzaSyCbkbNPR6K2rbAnkYrGTYCYTUKBOjq0RK4")


def check_llm_dot(value):
    # print("Came to dot")
    # print("Value Len: " + str(len(value)))
    # print("Value: " + str(value))
    value_old = value
    if value[len(value) - 1] == ".":
        value = value[0: len(value) - 1]
    value = value.rstrip()
    value1 = value
    last_space_index = value.rfind(' ')
    value = value[last_space_index + 1: len(value)]

    # print("Processed Value: " + str(value))
    response = None
    while response == None:
        response = client.models.generate_content(
            # model="gemini-2.5-flash-preview-05-20",
            # model="gemini-2.5-pro-preview-06-05",
            model="gemini-2.0-flash",

            contents=f"""Can the string '{value}' form a valid, meaningful English word? 
            This is possible only if '{value}' is already a word. Your answer must be ONLY "true" or "false". 
            Do not add any other words, explanations, or punctuation to your response""")
        # if response.text.strip() == "true":
        #     print("Came to dot")
        #     print("Value: " + str(value))
        #     print("Response Text:" + response.text.strip())

    if response.text.strip() == "true":
        # print("value1:" + value1)
        first_dot_index = value1.rfind('.')
        value1 = value1[first_dot_index + 1:len(value1)]
        # print("sentence space:" + value1)
        response = None
        while response == None:
            response = client.models.generate_content(
                # model="gemini-2.5-flash-preview-05-20",
                # model="gemini-2.5-pro-preview-06-05",
                model="gemini-2.0-flash",

                contents=f""" You are an AI language analysis assistant. Your job is to find meaningful English sentence with a given sentence.
                Does "{value1}" form as meaningful English sentence? Your answer must be ONLY "true" or "false". 
            Do not add any other words, explanations, or punctuation to your response""")

        # response__ = client.models.generate_content(
        #     # model="gemini-2.5-flash-preview-05-20",
        #     # model="gemini-2.5-pro-preview-06-05",
        #     model="gemini-2.0-flash",
        #
        #     contents=f""" You are an AI language analysis assistant. Your job is to find meaningful English sentence with a given sentence.
        #            Does "{value1}" form as meaningful English sentence? if true give an exmaple""")
        # print("Response Text:" + response__.text.strip())

        # if response.text.strip() == "false":
        #     response__ = client.models.generate_content(
        #         # model="gemini-2.5-flash-preview-05-20",
        #         model="gemini-2.5-pro-preview-06-05",
        #         # model="gemini-2.0-flash",
        #
        #         contents=f""" You are an AI language analysis assistant. Your job is to find meaningful English sentence with a given sentence.
        #                 Does "{value1}" form as meaningful English sentence? if false justify""")
        #     print("Response Text:" + response__.text.strip())

    if response.text.strip() == "true":
        print("Came to dot")
        print("Value Len: " + str(len(value_old)))
        print("Value: " + str(value_old))
        # print("Response Text:" + response.text.strip())
        print("\n")
    return response.text.strip()


def check_llm_space(value):
    # print("Came to space")
    # print("Value Len: " + str(len(value)))
    # print("Value: " + str(value))
    value_old = value
    value1 = value
    value = value.rstrip()
    last_dot_index = value.rfind('.')
    last_space_index = value.rfind(' ')
    if last_dot_index > last_space_index:
        value = value[last_dot_index + 1: len(value)]
    else:
        value = value[last_space_index + 1: len(value)]

    # print("Processed Value: " + str(value))
    response = None
    while response == None:
        response = client.models.generate_content(
            # model="gemini-2.5-flash-preview-05-20",
            # model="gemini-2.5-pro-preview-06-05",
            model="gemini-2.0-flash",

            contents=f"""Can the string '{value}' form a valid, meaningful English word? 
            This is possible only if '{value}' is already a word. Assume single letter words are only the well know words such as 'a', 'i'.
            Your answer must be ONLY "true" or "false". 
            Do not add any other words, explanations, or punctuation to your response""")

        # if response.text.strip() == "true":
        #     print("Came to space")
        #     print("Value: " + str(value))
        #     print("Response Text:" + response.text.strip())

    # response__ = client.models.generate_content(
    #     # model="gemini-2.5-flash-preview-05-20",
    #     model="gemini-2.5-pro-preview-06-05",
    #     # model="gemini-2.0-flash",
    #
    #     contents=f"""Can the string '{value}' form a valid, meaningful English word?
    #         This is possible only if '{value}' is already a word.
    #         Output format: Result:true/false, reason: Example word if true, if false justify""")
    #
    # print("Response Text:" + response__.text.strip())

    value1 = value1[last_dot_index + 1:len(value1)]
    if value1.count(" ") >= 2:
        if response.text.strip() == "true":
            # print("space:" + str(value1.count(" ")))
            # print("sentence:" + value1)
            response = None
            while response == None:
                response = client.models.generate_content(
                    # model="gemini-2.5-flash-preview-05-20",
                    # model="gemini-2.5-pro-preview-06-05",
                    model="gemini-2.0-flash",

                    contents=f""" You are an AI language analysis assistant. Your job is to find meaningful English sentence with a given sentence.
    
                Given prefix '{value1}', can you form a valid, meaningful English sentence?
    
                **Important Rule:** A "valid, meaningful English sentence" must be **correctly spelled** and **grammatically sound**, and **logically recognized as a standard English sentence**. It should NOT be a mere misspelling or typo. **For this task, initial capitalization of the sentence should NOT be a factor that makes it invalid, IF all other content, spelling, and grammar rules are met.**
    
                Here's how to determine this:
                1.  Check if '{value1}' is **already a complete, correctly spelled, and meaningful English sentence on its own**. This includes having a valid grammatical structure and conveying a complete thought.
                2.  If not, check if a correctly spelled, grammatically sound, and meaningful English sentence can be formed by **ONLY APPENDING new words not letters to the very end of '{value1}', without changing or inserting anything into the original '{value1}' characters.** The final appended sentence must meet all criteria for a valid, meaningful English sentence.
                Try to frame such sentences and then answer.
    
                Your answer must be ONLY "true" or "false". Do not add any other words, explanations, or punctuation to your response.
                """)

            # response_ = client.models.generate_content(
            #     # model="gemini-2.5-flash-preview-05-20",
            #     # model="gemini-2.5-pro-preview-06-05",
            #     model="gemini-2.0-flash",
            #
            #     contents=f""" You are an AI language analysis assistant. Your job is to find meaningful English sentence with a given sentence.
            #
            #             Given prefix '{value1}', can you form a valid, meaningful English sentence?
            #
            #             **Important Rule:** A "valid, meaningful English sentence" must be **correctly spelled** and **grammatically sound**, and **logically recognized as a standard English sentence**. It should NOT be a mere misspelling or typo. **For this task, initial capitalization of the sentence should NOT be a factor that makes it invalid, IF all other content, spelling, and grammar rules are met.**
            #
            #             Here's how to determine this:
            #             1.  Check if '{value1}' is **already a complete, correctly spelled, and meaningful English sentence on its own**. This includes having a valid grammatical structure and conveying a complete thought.
            #             2.  If not, check if a correctly spelled, grammatically sound, and meaningful English sentence can be formed by **ONLY APPENDING new words not letters to the very end of '{value1}', without changing or inserting anything into the original '{value1}' characters.** The final appended sentence must meet all criteria for a valid, meaningful English sentence.
            #
            #             if false, justify. if true give an exmaple""")
            # print("Response Text:" + response_.text.strip())

    if response.text.strip() == "true":
        print("Came to space")
        print("Value Len: " + str(len(value_old)))
        print("Value: " + str(value_old))
        # print("Response Text:" + response.text.strip())
        print("\n")
    return response.text.strip()


def check_llm(value):
    # print("Checking LLM...")
    # print("Value: " + str(value))
    # print("Value Len: " + str(len(value)))
    # value1 = value
    # print(" Value1: " + str(value1))
    value_old = value
    last_stop_index = value.rfind('.')
    last_space_index = value.rfind(' ')
    if last_stop_index > last_space_index:
        value = value[last_stop_index + 1: len(value)]
    else:
        value = value[last_space_index + 1: len(value)]

    # print(" last_space_index:" + str(last_space_index))
    # print(" last_stop_index:" + str(last_stop_index))

    # print("Processed Value: " + str(value))
    if len(value) == 1:
        return "true"

    response = None
    while response == None:
        response = client.models.generate_content(
            # model="gemini-2.5-flash-preview-05-20",
            # model="gemini-2.5-pro-preview-06-05",
            model="gemini-2.0-flash",

            contents=f""" You are an AI language analysis assistant. Your job is to find  common, meaningful English words with a given prefix.
                    Given prefix '{value}', can you form a valid, common, meaningful English word?
        
                    **Important Rule:** A "valid, common, meaningful English word" must be **correctly spelled** and **recognized as a standard word in English dictionaries**, not merely a common misspelling or typo of another word.
        
                    Here's how to determine this:
                    1.  Check if '{value}' is **already a complete, correctly spelled, recognized, common, and meaningful English word on its own**. Do not consider abbreviations. 
                    2.  If not, check if a correctly spelled, recognized, common, and meaningful English word can be formed by **ONLY APPENDING new letters to the very end of '{value}', without changing or reorganising or inserting anything into the original '{value}' characters.** Do not consider forming abbreviations.
                    3. Include **inflected forms** such as:
                       - verbs with -ing, -ed, -s (e.g., run → running, act → acting)
                       - nouns with plural or suffixes (e.g., act → action, act → actor)
                       
                    4. 'ag' can become 'ago'
                    5. 'glist' can become 'glistens'
                    6. 'breez' can become 'breeze'
                        
                    If {value} is not a word on its own, think of atleast one possible word that starts with {value}.
                    Output as : result:true/false + response: only the word staring with '{value}' or {value} if {value} itself is word else N/A: justify.
                    """)

    result__ = ""
    if "response:" in response.text.strip():
        result__ = str(response.text.strip().split("response:", 1)[1].strip())

    # print("result:" + result__)

    if result__.startswith(value):
        print("Checking LLM...")
        print("Value Len: " + str(len(value_old)))
        print("Value: " + str(value_old))
        print("\n")
        return "true"
    else:
        # print("Response:false")
        return "false"


def readFiles():
    global items_count
    file_path = "data/"
    try:
        # List all files in the directory
        files_list = [f for f in os.listdir(file_path + "original/") if
                      os.path.isfile(os.path.join(file_path + "original/", f)) and not f.startswith('.')]

        print("List of files:" + str(files_list))
        # Read each file
        for file_name in files_list:
            file_path_ = os.path.join(file_path + "original/", file_name)
            print(file_path_)
            with open(file_path_, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read(max_size)
                content = content.lower()
                cleaned_content = re.sub(r'[^a-z. ]', ' ', content)
                cleaned_content = cleaned_content.replace("  ", " ")
                cleaned_content = cleaned_content.replace(". ", ".")
                contents.append(cleaned_content)
                files.append(cleaned_content)

        i = 1
        for f in files:
            print("Length:" + str(len(f)))
            items_count = items_count + len(f)
            try:
                with open(file_path + "processed/" + str(i) + ".txt", 'w', encoding='utf-8', errors='ignore') as file:
                    file.write(f)
            except IOError as e:
                print(f"Error: {str(e)}")
            i = i + 1

    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."


def insert_file():
    i = 0
    str_ = ""
    for file in files:
        bf.add(files_key[i], True)
        i = i + 1
        j = 0
        start_time = time.time()
        print("Started for file:" + str(i))
        for c in file:
            str_ = str_ + c
            # print("String:" + str_)
            bf.add(c, False)
            j = j + 1
            if (j % 100000 == 0):
                print("Completed:" + str(j))

        end_time = time.time()
        elapsed_time = (end_time - start_time)
        print("Insertion time for file " + str(i) + ":" + str(elapsed_time) + " s")

    return bf.get_bit_array()


def initialize():
    global bf, word_list

    # fp_prob = 0.00000000000000000000000000000000000000000000000000000000000000001
    # fp_prob = 0.0000001
    # fp_prob = pow(10, -5)
    fp_prob = pow(10, -1)

    # static_allocation = True
    # # bf_fixed_size=4638813
    # bf_fixed_size = 7000000
    # # bf_fixed_size = 20000000
    # bf = BloomFilter(items_count, fp_prob, static_allocation, 1, bf_fixed_size=bf_fixed_size,
    #                  hash_function="SHA256")

    static_allocation = False
    bf = BloomFilter(items_count, fp_prob, static_allocation, hash_function="SHA256")

    # this is same as the sum of number of characters in each file
    print("Estimated number of items to be stored in BFULT:" + str(items_count))
    print("False positive rate:" + str(fp_prob))
    print("Bloom filter size: " + str(bf.size) + " bits")
    print("Bloom filter size: " + str(bf.size / (8 * 1024 * 1024)) + " MiB")
    print("Number of hash function:" + str(bf.hash_count))


def insert():
    start_time = time.time()
    print("Storing files to bloom filter...")

    global key_size
    initialize()
    insert_file()
    end_time = time.time()
    elapsed_time = (end_time - start_time)
    print("Insertion time:" + str(elapsed_time) + " s")


def common_prefix_length(s1, s2):
    length = min(len(s1), len(s2))  # Get the shortest length
    for i in range(length):
        if s1[i] != s2[i]:  # Stop at first mismatch
            return i
    return length  # If one string is a prefix of the other


def retrieve_file(file_id):
    pk_key = files_key[file_id]
    file_length = len(pk_key)
    split_values = []

    special_characters = [' ', ',', ';', '.']
    special_characters = [' ', '.']
    formatted_alphabet = list(string.ascii_lowercase) + special_characters

    queue = []
    for i in formatted_alphabet:
        queue.append(i)

    temp = len(files[file_id])
    # for q in queue:
    #     print(q)
    k = 0
    while queue:
        entry = queue.pop(0)
        # print(entry)
        if bf.check(entry):
            # print(entry, " Present")
            if len(entry) < file_length + temp:
                for i in formatted_alphabet:
                    queue.append(entry + i)
            else:
                split_values.append(entry[file_length:])

    print("Files are:")
    for i in split_values:
        print(i)

    return split_values

    # answer_concat = files_key[file_id]
    # answer_len = len(answer_concat)
    # split_values = []
    # data = ""
    #
    # special_characters = [' ', ',', ';', '.']
    # formatted_alphabet = list(string.ascii_lowercase) + special_characters
    #
    # bf.reset_hash()
    #
    # queue = []
    # for i in formatted_alphabet:
    #     queue.append(i)
    #
    # bf.check(answer_concat, False)
    # data_len = len(files[file_id])
    # while len(data) < data_len:
    #     found = False
    #     for item in queue:
    #         # print(entry)
    #         if bf.check(item, True):
    #             data += item
    #             found = True
    #             break
    #     if found == False:
    #         print(f"Deadend at {len(data)}")
    #         break
    #     if (len(data) % 100000) == 0:
    #         print(len(data))
    #
    # l = common_prefix_length(data, contents[0])
    #
    # if (data == contents[0]):
    #     print("PASSED")
    # else:
    #     print(f"FAILED, {l} equal bytes")

    # return data


def check_alphabet(formatted_alphabet, queue_hash, queue_string, snapshot=None, flag=None, file_string=None):
    # print("Checking alphabet...")
    # print("***********************************")
    # print("file_string:" + str(file_string))
    global count_bf, threshold_, fan_out, print_thres, flag_print_thresh
    if flag:
        entry_hash = snapshot.copy()
    else:
        entry_hash = queue_hash.pop(0)
    baseline_hex = entry_hash.copy()

    for i in formatted_alphabet:
        # print("alphabet:" + str(i))
        # print("entry_hash:" + str(int(entry_hash.hexdigest(), 16)))

        presence, snapshot_ = bf.get(snapshot=entry_hash, item=i, flag=False)

        if presence == 1:
            if len(file_string + i) == 1:
                count_bf = count_bf + 1
                if len(file_string + i) in fan_out:
                    fan_out[len(file_string + i)] = fan_out[len(file_string + i)] + 1
                else:
                    fan_out[len(file_string + i)] = 1

                queue_hash.append(snapshot_)
                queue_string.append(file_string + i)
            else:
                if i != " " and i != ".":
                    if check_llm(file_string + i) == 'true':
                        # if i == " ":
                        #     print("her" + file_string + i)
                        #     if check_llm_(file_string + i) == 'true':
                        #         queue_hash.append(snapshot_)
                        #         print("file_string LLM1:" + file_string + i)
                        #         # print("=================================================")
                        #         queue_string.append(file_string + i)
                        #         count = count + 1
                        # else:
                        count_bf = count_bf + 1
                        if len(file_string + i) in fan_out:
                            fan_out[len(file_string + i)] = fan_out[len(file_string + i)] + 1
                        else:
                            fan_out[len(file_string + i)] = 1

                        queue_hash.append(snapshot_)
                        # print("file_string LLM:" + file_string + i)
                        # print("=================================================")
                        queue_string.append(file_string + i)

                else:
                    if i == " ":
                        if check_llm_space(file_string + i) == 'true':
                            count_bf = count_bf + 1
                            if len(file_string + i) in fan_out:
                                fan_out[len(file_string + i)] = fan_out[len(file_string + i)] + 1
                            else:
                                fan_out[len(file_string + i)] = 1

                            queue_hash.append(snapshot_)
                            # print("file_string LLM:" + file_string + i)
                            # print("=================================================")
                            queue_string.append(file_string + i)
                    elif i == ".":
                        if check_llm_dot(file_string + i) == 'true':
                            count_bf = count_bf + 1
                            if len(file_string + i) in fan_out:
                                fan_out[len(file_string + i)] = fan_out[len(file_string + i)] + 1
                            else:
                                fan_out[len(file_string + i)] = 1

                            queue_hash.append(snapshot_)
                            # print("file_string LLM:" + file_string + i)
                            # print("=================================================")
                            queue_string.append(file_string + i)

        entry_hash = baseline_hex.copy()
        if print_threshold in fan_out and flag_print_thresh == True:
            flag_print_thresh = False
            print("Fan out:" + str(fan_out))

    return queue_hash, queue_string


# def check_alphabet_(formatted_alphabet, queue_hash, queue_string, snapshot=None, flag=None, file_string=None):
#     # print("Checking alphabet...")
#     # print("***********************************")
#     # print("file_string:" + str(file_string))
#     global count, threshold_
#     if flag:
#         entry_hash = snapshot.copy()
#     else:
#         entry_hash = queue_hash.pop(0)
#     baseline_hex = entry_hash.copy()
#
#     for i in formatted_alphabet:
#         # print("alphabet:" + str(i))
#         # print("entry_hash:" + str(int(entry_hash.hexdigest(), 16)))
#
#         presence, snapshot_ = bf.get(snapshot=entry_hash, item=i, flag=False)
#         if presence == 1:
#             # if len(file_string + i) % threshold_ == 0:
#                 if check_llm(file_string + i) == 'True':
#                     queue_hash.append(snapshot_)
#                     print("file_string LLM:" + file_string + i)
#                     print("=================================================")
#                     queue_string.append(file_string + i)
#                     count = count + 1
#             # else:
#             #     queue_hash.append(snapshot_)
#             #     # print("file_string:" + file_string + i)
#             #     # print("=================================================")
#             #     queue_string.append(file_string + i)
#             #     count = count + 1
#         entry_hash = baseline_hex.copy()
#
#     # print("queue_hash")
#     # for q in queue_hash:
#     #     print(str(int(q.hexdigest(), 16)))
#     print("queue_string")
#     for q in queue_string:
#         print(q)
#     return queue_hash, queue_string


def bfs(file_id):
    global file_length
    global alpha_count
    pk_key = files_key[file_id]
    file_length = len(files[file_id])

    # special_characters = [' ', ',', ';', '.']
    special_characters = [' ', '.']
    formatted_alphabet = list(string.ascii_lowercase) + special_characters
    # formatted_alphabet=['i',' ','l','o','v','e']
    print("Alphabet count: " + str(len(formatted_alphabet)))
    _, snapshot = bf.get(item=pk_key, flag=True)
    queue_hash = []
    queue_string = []
    queue_hash, queue_string = check_alphabet(formatted_alphabet, queue_hash, queue_string, snapshot, True, "")

    candidate_files = []
    while queue_string:
        entry_string = queue_string.pop(0)
        if len(entry_string) < file_length:
            queue_hash, queue_string = check_alphabet(formatted_alphabet, queue_hash, queue_string, None, False,
                                                      entry_string)
        elif len(entry_string) == file_length:
            candidate_files.append(entry_string)
        else:
            break

    print("Files are:")
    for i in candidate_files:
        print(i)
        print("==========================================================================")

    return candidate_files


def retrieve():
    start_time = time.time()
    print("Retrieving private key from bloom filter...")
    for i in range(len(files)):
        # candidate_files = retrieve_file(i)
        candidate_files = bfs(i)
    print("number of candidate files:", str(len(candidate_files)))

    end_time = time.time()
    elapsed_time = (end_time - start_time)
    print("Retrieve time:" + str(elapsed_time) + " s")


#
# for model in genai.list_models():
#     print(model.name, model.supported_generation_methods)

readFiles()
insert()
# print("Bloom Filter:")
# bf.display()
print("Load factor:" + str(bf.get_load_factor()))

retrieve()
print("Number of items added into the queue for exploration:" + str(count_bf))
print("Extra items searched:" + str(count_bf - file_length))
# print("Fan out:"+str(fan_out))
