import os
import time
import requests

BASE_URL = "https://www.gutenberg.org/files"
BOOK_IDS = [
    1260, 768, 1400, 730, 120, 236, 21964, 145, 28520, 969,
    158, 43, 917, 1023, 15, 1661, 2600, 84, 11, 2701
]

DEST_FOLDER = "victorian_books"
MERGED_FILE = "victorian_merged.txt"
os.makedirs(DEST_FOLDER, exist_ok=True)

def extract_title(content):
    try:
        text = content.decode('utf-8', errors='ignore')
        for line in text.splitlines():
            if line.lower().startswith("title:"):
                return line.strip().replace("Title:", "").strip()
    except Exception:
        pass
    return "(title unknown)"

def download_and_append(book_id, merged_fp):
    urls = [f"{BASE_URL}/{book_id}/{book_id}-0.txt", f"{BASE_URL}/{book_id}/{book_id}.txt"]
    for url in urls:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200 and "html" not in r.headers.get("Content-Type", ""):
                content = r.content
                title = extract_title(content)
                print(f"📘 {title} ({book_id}) — {len(content)/1024:.1f} KB")

                with open(os.path.join(DEST_FOLDER, f"{book_id}.txt"), "wb") as f:
                    f.write(content)

                merged_fp.write(f"\n\n====== {title} (ID: {book_id}) ======\n\n")
                merged_fp.write(content.decode("utf-8", errors="ignore"))
                return len(content)
        except Exception as e:
            print(f"⚠️ Failed {url} — {e}")
        time.sleep(1)
    return 0

# Start download
target_bytes = 100 * 1024 * 1024
downloaded = 0

with open(MERGED_FILE, "w", encoding="utf-8") as merged_fp:
    for bid in BOOK_IDS:
        downloaded += download_and_append(bid, merged_fp)
        print(f"📦 Total so far: {downloaded / 1024 / 1024:.2f} MB\n")
        if downloaded >= target_bytes:
            break

print(f"\n✅ Done. Output saved to: {MERGED_FILE}")

