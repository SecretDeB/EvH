import os
import csv
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

def process_directory(input_dir, label):
    print(f"\n📁 Processing directory: {input_dir} ({label})")

    file_list = sorted(
        [f for f in os.listdir(input_dir) if f.endswith(".txt") and f.split(".")[0].isdigit()],
        key=lambda x: int(x.split(".")[0])
    )

    set_5gram = set()
    set_7gram = set()
    set_10gram = set()
    size_5gram = []
    size_7gram = []
    size_10gram = []

    for idx, filename in enumerate(file_list, 1):
        with open(os.path.join(input_dir, filename), "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().replace("\n", " ").strip()

        for i in range(len(text) - 4):
            set_5gram.add(text[i:i+5])
        size_5gram.append(len(set_5gram))

        for i in range(len(text) - 6):
            set_7gram.add(text[i:i+7])
        size_7gram.append(len(set_7gram))

        for i in range(len(text) - 9):
            set_10gram.add(text[i:i+10])
        size_10gram.append(len(set_10gram))

        if idx % 20 == 0 or idx == len(file_list):
            print(f"  • File {idx}/{len(file_list)}: 5-grams: {len(set_5gram)},  7-grams: {len(set_7gram)}, 10-grams: {len(set_10gram)}")

    return size_5gram, size_7gram, size_10gram

# ─────────── MAIN ───────────

input_dir = "split_wiki_data"
label = "wiki"
size_5gram, size_7gram, size_10gram = process_directory(input_dir, label)

# Save CSV for growth
with open("ngram_growth_sizes.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["File_Index", "5gram_size", "7gram_size", "10gram_size"])
    for i in range(len(size_5gram)):
        writer.writerow([i + 1, size_5gram[i], size_7gram[i], size_10gram[i]])


print("✅ Saved CSVs: ngram_growth_sizes.csv")

# Save 5-gram growth curve
plt.figure(figsize=(6, 4))
plt.plot(range(1, len(size_5gram)+1), size_5gram, color='purple')
plt.xlabel("Files Processed")
plt.ylabel("Cumulative Unique 5-grams")
plt.title("5-gram Set Growth")
plt.grid(True)
plt.tight_layout()
plt.savefig("5gram_growth_curve.png")
plt.close()

# Save 7-gram growth curve
plt.figure(figsize=(6, 4))
plt.plot(range(1, len(size_7gram)+1), size_7gram, color='darkred')
plt.xlabel("Files Processed")
plt.ylabel("Cumulative Unique 7-grams")
plt.title("7-gram Set Growth")
plt.grid(True)
plt.tight_layout()
plt.savefig("7gram_growth_curve.png")
plt.close()

# Save 10-gram growth curve
plt.figure(figsize=(6, 4))
plt.plot(range(1, len(size_10gram)+1), size_10gram, color='navy')
plt.xlabel("Files Processed")
plt.ylabel("Cumulative Unique 10-grams")
plt.title("10-gram Set Growth")
plt.grid(True)
plt.tight_layout()
plt.savefig("10gram_growth_curve.png")
plt.close()



