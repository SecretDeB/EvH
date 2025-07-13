import os

input_dir = "wiki_data_1GB"
output_dir = "split_wiki_data"
os.makedirs(output_dir, exist_ok=True)

# Read and concatenate all input files
combined_data = bytearray()
file_list = sorted(os.listdir(input_dir), key=lambda x: int(os.path.splitext(x)[0]))

for filename in file_list:
    with open(os.path.join(input_dir, filename), "rb") as f:
        combined_data.extend(f.read())

# Split into 10 equal parts
total_size = len(combined_data)
chunk_size = total_size // 1000
remainder = total_size % 1000

start = 0
for i in range(100):
    end = start + chunk_size + (1 if i < remainder else 0)
    part_data = combined_data[start:end]
    with open(os.path.join(output_dir, f"{i+1}.txt"), "wb") as f:
        f.write(part_data)
    start = end

print(f"Split complete. Output in: {output_dir}/")

