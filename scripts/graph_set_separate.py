import os
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

input_dir = "split_parts"

# List and sort files numerically
file_list = sorted(
    [f for f in os.listdir(input_dir) if f.endswith(".txt") and f.split(".")[0].isdigit()],
    key=lambda x: int(x.split(".")[0])
)

set_4gram = set()
set_7gram = set()
size_4gram = []
size_7gram = []

# Process each file incrementally
for filename in file_list:
    with open(os.path.join(input_dir, filename), "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().replace("\n", " ").strip()

    for i in range(len(text) - 3):
        set_4gram.add(text[i:i+4])
    size_4gram.append(len(set_4gram))

    for i in range(len(text) - 6):
        set_7gram.add(text[i:i+7])
    size_7gram.append(len(set_7gram))

# Branching: 3→4
prefix_map_3 = defaultdict(set)
for g4 in set_4gram:
    prefix_map_3[g4[:3]].add(g4)
counter_3 = Counter(len(v) for v in prefix_map_3.values())
total_3 = sum(counter_3.values())
x_vals = list(range(1, 31))
y_vals_3to4 = [100 * counter_3.get(x, 0) / total_3 for x in x_vals]

# Branching: 6→7
prefix_map_6 = defaultdict(set)
for g7 in set_7gram:
    prefix_map_6[g7[:6]].add(g7)
counter_6 = Counter(len(v) for v in prefix_map_6.values())
total_6 = sum(counter_6.values())
y_vals_6to7 = [100 * counter_6.get(x, 0) / total_6 for x in x_vals]

# Plot 1: 4-gram growth
plt.figure(figsize=(6, 4))
plt.plot(range(1, len(size_4gram) + 1), size_4gram, marker='o')
plt.xlabel("Files Added")
plt.ylabel("Unique 4-grams")
plt.tight_layout()
plt.savefig("4gram_growth.png")
plt.close()

# Plot 2: 3→4 branching
plt.figure(figsize=(6, 4))
plt.bar(x_vals, y_vals_3to4, color='orange')
plt.xlabel("# of Distinct 4-grams per 3-gram")
plt.ylabel("% of 3-grams")
plt.tight_layout()
plt.savefig("3to4_branching.png")
plt.close()

# Plot 3: 7-gram growth
plt.figure(figsize=(6, 4))
plt.plot(range(1, len(size_7gram) + 1), size_7gram, marker='o', color='green')
plt.xlabel("Files Added")
plt.ylabel("Unique 7-grams")
plt.tight_layout()
plt.savefig("7gram_growth.png")
plt.close()

# Plot 4: 6→7 branching
plt.figure(figsize=(6, 4))
plt.bar(x_vals, y_vals_6to7, color='blue')
plt.xlabel("# of Distinct 7-grams per 6-gram")
plt.ylabel("% of 6-grams")
plt.tight_layout()
plt.savefig("6to7_branching.png")
plt.close()

