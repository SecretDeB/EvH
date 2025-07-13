import random
import time
import string
import re
import os
import hashlib
import matplotlib.pyplot as plt
from BFULT import BloomFilter

ENABLE_NGRAMS = False
padding = 0
bf = None
key_size = 0
word_list = []
pk_length = 0
abc_size = []

files_key = ["Key1", "Key2", "Key3", "Key4", "Key5", "Key6", "Key7", "Key8", "Key9", "Key10"]
padding_flag = False
contents = []
files = []
k_letters_grams = set()
five_letters_grams = set()
items_count = 0
max_size = 10000
content_len = 0

alpha_list = []
fp_list = []
time_list = []
count_candidates = 0

def extract_k_grams(text, k, k_set):
    for i in range(len(text) - k + 1):
        k_set.add(text[i:i+k])

def readFiles(k):
    global items_count
    global content_len
    file_path = "data/"
    try:
        files_list = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f)) and not f.startswith('.')]
        print("Files found:", files_list)

        for file_name in files_list:
            file_path_ = os.path.join(file_path, file_name)
            print("Reading:", file_path_)
            with open(file_path_, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read(max_size)
                content = content.lower()
                cleaned_content = re.sub(r'[^a-z,.; ]', '', content)
                contents.append(cleaned_content)
                files.append(cleaned_content)
                content_len = len(cleaned_content)
                print(f"length of data is {content_len}")
            break

        output_dir = os.path.join(file_path, "new")
        os.makedirs(output_dir, exist_ok=True)

        for i, f in enumerate(files, start=1):
            items_count += len(f)
            try:
                with open(file_path + "/new/" + str(i) + ".txt", 'w', encoding='utf-8', errors='ignore') as file:
                    file.write(f)
            except IOError as e:
                print(f"Error writing file {i}: {str(e)}")

        print("Estimated total characters:", items_count)
        print(f"Unique {k}-letter sequences found: {len(k_letters_grams)}")

    except FileNotFoundError:
        print(f"Error: The file path '{file_path}' was not found.")

def insert_private_key():
    i = 0
    for file in files:
        sha = hashlib.sha256()
        sha.update(files_key[i].encode('utf-8'))
        i += 1

        j = 0
        start_time = time.time()
        for c in file:
            sha.update(c.encode('utf-8'))  
            snapshot = sha.copy()        
            bf.add(snapshot, "")         
            j += 1
            if j % 100000 == 0:
                print("Completed: " + str(j))
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        print(f"Insertion time for file {i}: {elapsed_time:.2f} ms")

    return bf.get_bit_array()

def initialize(fp_prob):
    global bf
    bf = BloomFilter(items_count, fp_prob, False, "SHA256")

def insert(fp_prob):
    print(f"@@@@ alpha = {fp_prob}")
    start_time = time.time()
    global key_size
    initialize(fp_prob)
    insert_private_key()
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    print(f"Insertion time: {elapsed_time:.2f} ms ({elapsed_time/1000:.2f} seconds)")

def common_prefix_length(s1, s2):
    length = min(len(s1), len(s2))
    for i in range(length):
        if s1[i] != s2[i]:
            return i
    return length

def retrieve_private_key(file_id, k, abc):
    global content_len, count_candidates
    count_candidates = 0
    answer_concat = files_key[file_id]
    data = ""
    sha = hashlib.sha256()
    sha.update(answer_concat.encode('utf-8'))
    bf.search.append((sha, data))
    data_len = len(files[file_id])

    while bf.search != []:
        sha, data = bf.search.pop(0)
        if len(data) < data_len:
            for item in abc:
                potential = data + item
                if ENABLE_NGRAMS:
                    if len(potential) >= k:
                        last_gram = potential[-k:]
                        if last_gram not in k_letters_grams:
                            continue
                    elif len(potential) >= 5:
                        last_gram = potential[-5:]
                        if last_gram not in five_letters_grams:
                            continue
                snapshot_undo = sha.copy()
                new_snapshot = bf.check(snapshot_undo, item)
                if new_snapshot != None:
                    new_data = data + item
                    bf.search.append((new_snapshot, new_data))
                    count_candidates += 1
        else:
            if data == contents[0]:
                break

    l = common_prefix_length(data, contents[0])
    if data == contents[0]:
        print("PASSED")
        print(f"@@@ candidates = {count_candidates}, m = {content_len}, fp = {count_candidates - content_len} ")
    else:
        print(f"FAILED, {l} equal bytes")
    return data

def retrieve(k, alpha, abc):
    start_time = time.time()
    private_keys = retrieve_private_key(0, k, abc)
    end_time = time.time()
    elapsed_time = end_time - start_time
    alpha_list.append(alpha)
    fp = count_candidates - content_len
    fp_list.append(fp)
    time_list.append(elapsed_time)

    if private_keys is not None:
        print(f"ecovered data length: {len(private_keys)} characters")
    else:
        print("Failed")

    print(f"@@@ Retrieve time: {elapsed_time*1000:.2f} ms ({elapsed_time:.2f} seconds)")

def plot_results():
    import matplotlib.pyplot as plt

    fp_rate_1 = [fp / content_len for fp in results["printable (σ= 223)"]['fp']]
    fp_rate_2 = [fp / content_len for fp in results["all (σ= 256)"]['fp']]
    alphas = results["printable (σ= 223)"]['alphas']

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.plot(alphas, fp_rate_1, marker='o', lw=2, color='C0', label="printable (σ= 223)")
    ax.plot(alphas, fp_rate_2, marker='o', lw=2, color='C1', label="all (σ= 256)")

    ax.set_xlabel(r"False Positive Rate $\alpha$", fontsize=12)
    ax.set_ylabel(r"Measured $\mathrm{FP} \div m$", fontsize=12)
    ax.set_xticks(alphas)
    ax.set_xticklabels([f"{a:.4f}" for a in alphas])
    ax.tick_params(labelsize=10)
    ax.grid(ls=':', lw=0.6)
    ax.legend(fontsize=10, loc="upper left")

    plt.tight_layout()
    plt.savefig("fp_rate_vs_alpha.png", dpi=300)
    plt.close()
    print("📊 Saved: fp_rate_vs_alpha.png")

# Main
k = 10
alphas = [0.0015,  0.002,  0.0025,  0.003, 0.0035]
readFiles(k)

printable = [chr(i) for i in range(32, 127)] + [chr(i) for i in range(128, 256)]
all_ascii = [chr(i) for i in range(256)]

# Store results separately
results = {}

def run_experiment(label, abc):
    local_alpha_list = []
    local_fp_list = []
    local_time_list = []

    for alpha in alphas:
        insert(alpha)
        retrieve(k, alpha, abc)
        local_alpha_list.append(alpha)
        local_fp_list.append(fp_list[-1])  # take latest appended fp
        local_time_list.append(time_list[-1])

    results[label] = {
        'alphas': local_alpha_list,
        'fp': local_fp_list,
        'times': local_time_list
    }

abc_size = [len(printable), len(all_ascii)]
run_experiment(f"printable (σ= {len(printable)})", printable)
run_experiment(f"all (σ= {len(all_ascii)})", all_ascii)
plot_results()