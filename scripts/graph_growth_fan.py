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

    # Prefix branching
    prefix_map_4 = defaultdict(set)
    for g5 in set_5gram:
        prefix_map_4[g5[:4]].add(g5)
    counter_4 = Counter(len(v) for v in prefix_map_4.values())
    total_4 = sum(counter_4.values())
    y_vals_4to5 = [100 * counter_4.get(x, 0) / total_4 for x in range(1, 31)]

    prefix_map_6 = defaultdict(set)
    for g7 in set_7gram:
        prefix_map_6[g7[:6]].add(g7)
    counter_6 = Counter(len(v) for v in prefix_map_6.values())
    total_6 = sum(counter_6.values())
    y_vals_6to7 = [100 * counter_6.get(x, 0) / total_6 for x in range(1, 31)]

    prefix_map_9 = defaultdict(set)
    for g10 in set_10gram:
        prefix_map_9[g10[:9]].add(g10)
    counter_9 = Counter(len(v) for v in prefix_map_9.values())
    total_9 = sum(counter_9.values())
    y_vals_9to10 = [100 * counter_9.get(x, 0) / total_9 for x in range(1, 31)]

    return size_5gram, size_7gram, size_10gram, y_vals_4to5, y_vals_6to7, y_vals_9to10

# ─────────── MAIN ───────────

input_dir = "split_wiki_data"
label = "wiki"
size_5gram, size_7gram, size_10gram, branch_4to5, branch_6to7, branch_9to10 = process_directory(input_dir, label)

# Save CSV for growth
with open("ngram_growth_sizes.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["File_Index", "5gram_size", "7gram_size", "10gram_size"])
    for i in range(len(size_5gram)):
        writer.writerow([i + 1, size_5gram[i], size_7gram[i], size_10gram[i]])

# Save CSV for prefix branching
with open("ngram_prefix_branching.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Branch_Size", "4to5_pct", "6to7_pct", "9to10_pct"])
    for i in range(30):
        writer.writerow([
            i + 1,
            branch_4to5[i] if i < len(branch_4to5) else 0,
            branch_6to7[i] if i < len(branch_6to7) else 0,
            branch_9to10[i] if i < len(branch_9to10) else 0,
        ])

print("✅ Saved CSVs: ngram_growth_sizes.csv and ngram_prefix_branching.csv")

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

# Branching plots
def save_branching_chart(data, filename, xlabel, color):
    plt.figure(figsize=(6, 4))
    plt.bar(range(1, 31), data, color=color)
    plt.xlabel(xlabel)
    plt.ylabel("% of Prefixes")
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"✅ Saved: {filename}")

save_branching_chart(branch_4to5, "4to5_branching.png", "# of Distinct 5-grams per 4-gram", 'purple')
save_branching_chart(branch_6to7, "6to7_branching.png", "# of Distinct 7-grams per 6-gram", 'firebrick')
save_branching_chart(branch_9to10, "9to10_branching.png", "# of Distinct 10-grams per 9-gram", 'darkblue')

