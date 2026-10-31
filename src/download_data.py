import os
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Official CDC NHANES 2021-2023 URLs
URLS = {
    "DEMO_L.XPT": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.XPT",
    "BMX_L.XPT": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.XPT",
    "BPXO_L.XPT": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPXO_L.XPT",
}


def download_nhanes_files():
  for filename, url in URLS.items():
    dest = os.path.join(DATA_DIR, filename)
    if os.path.exists(dest):
      size_mb = os.path.getsize(dest) / (1024 * 1024)
      print(f"[EXISTS] {filename} ({size_mb:.2f} MB)")
      continue

    print(f"[DOWNLOADING] {filename} ...")
    try:
      response = requests.get(url, stream=True, timeout=60)
      response.raise_for_status()
      with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=65536):
          if chunk:
            f.write(chunk)
      size_mb = os.path.getsize(dest) / (1024 * 1024)
      print(f"[SAVED] {filename} ({size_mb:.2f} MB)")
    except Exception as e:
      print(f"[ERROR] Failed to download {filename}: {e}")


if __name__ == "__main__":
  download_nhanes_files()