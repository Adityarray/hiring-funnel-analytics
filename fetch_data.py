import urllib.request
import json
import csv
import time

BASE_URL = "https://mosaicfellowship.in/api/data/hr/applicants?page={page}&limit=100"
OUTPUT_FILE = "hr_applicants.csv"

all_rows = []

print("=" * 50)
print("  HR Data Fetcher — Mosaic Fellowship Challenge")
print("=" * 50)

for page in range(1, 31):
    url = BASE_URL.format(page=page)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)

            # Handle different response shapes
            if isinstance(data, list):
                rows = data
            elif isinstance(data, dict):
                rows = data.get("data") or data.get("applicants") or data.get("results") or []
            else:
                rows = []

            if not rows:
                print(f"  Page {page}: 0 rows returned — stopping.")
                break

            all_rows.extend(rows)
            print(f"  ✓ Page {page:02d}: +{len(rows)} rows  (total so far: {len(all_rows)})")

    except Exception as e:
        print(f"  ✗ Page {page}: ERROR — {e}")

    time.sleep(0.1)  # be polite to the server

print()
print(f"Fetch complete: {len(all_rows)} total rows")

if not all_rows:
    print("No data fetched. Check your internet connection.")
    exit()

# ── Save to CSV ──
fields = list(all_rows[0].keys())

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"Saved to: {OUTPUT_FILE}")
print()

# ── Quick Data Profile ──
print("=" * 50)
print("  DATA PROFILE")
print("=" * 50)
print(f"  Rows     : {len(all_rows)}")
print(f"  Columns  : {len(fields)}")
print(f"  Fields   : {', '.join(fields)}")
print()

# Show unique values for each non-numeric field
for field in fields:
    values = [r[field] for r in all_rows if r.get(field) not in (None, "", "null")]
    unique = sorted(set(str(v) for v in values))

    try:
        nums = [float(v) for v in values]
        mn = min(nums); mx = max(nums); avg = sum(nums)/len(nums)
        print(f"  [{field}]  numeric  |  min={mn:.1f}  max={mx:.1f}  avg={avg:.1f}")
    except:
        if len(unique) <= 20:
            print(f"  [{field}]  categorical  |  {len(unique)} values: {', '.join(unique)}")
        else:
            print(f"  [{field}]  text/id  |  {len(unique)} unique values  (sample: {', '.join(unique[:5])}...)")

print()
print("Done! Share the output above back in the chat.")
