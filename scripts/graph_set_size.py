import os
import matplotlib.pyplot as plt

print("🚀 Starting n-gram growth analysis...")

input_dir = "split_parts"

# List and sort files numerically
file_list = sorted(
    [f for f in os.listdir(input_dir) if f.endswith(".txt") and f.split(".")[0].isdigit()],
    key=lambda x: int(x.split(".")[0])
)

print(f"📄 Found {len(file_list)} files to process: {file_list}")

set_4gram = set()
set_7gram = set()
size_4gram = []
size_7gram = []

# Process each file incrementally
for idx, filename in enumerate(file_list, 1):
    print(f"🔍 Processing file {idx}: {filename}")
    with open(os.path.join(input_dir, filename), "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().replace("\n", " ").strip()

    # Extract and count 4-grams
    for i in range(len(text) - 4):
        set_4gram.add(text[i:i+4])
    size_4gram.append(len(set_4gram))
    print(f"   ➤ Unique 4-grams so far: {len(set_4gram)}")

    # Extract and count 7-grams
    for i in range(len(text) - 9):
        set_7gram.add(text[i:i+7])
    size_7gram.append(len(set_7gram))
    print(f"   ➤ Unique 7-grams so far: {len(set_7gram)}")

print("📊 Plotting results...")

# Plot
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(range(1, len(size_4gram) + 1), size_4gram, marker='o', linestyle='-')
plt.title("4-letter-gram Growth")
plt.xlabel("Files Added")
plt.ylabel("Unique 4-letter-grams")
plt.xticks(range(1, len(size_4gram) + 1))

plt.subplot(1, 2, 2)
plt.plot(range(1, len(size_7gram) + 1), size_7gram, marker='o', linestyle='-', color='green')
plt.title("7-letter-gram Growth")
plt.xlabel("Files Added")
plt.ylabel("Unique 7-letter-grams")
plt.xticks(range(1, len(size_7gram) + 1))

plt.tight_layout()
plt.savefig("ngram_growth.png")
print("✅ Plot saved as ngram_growth.png")
plt.show()

