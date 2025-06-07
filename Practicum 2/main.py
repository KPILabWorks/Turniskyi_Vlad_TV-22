import pandas as pd
import numpy as np
from faker import Faker
import matplotlib.pyplot as plt
import zstandard as zstd
import json
import pandas as pd
from tqdm import tqdm
import orjson

# === STEP 1 === 
print("STEP 1 - Read data from zst-file")
file_path = "RS_2019-04.zst" #reddit data

print("We read the posts...")
rows = []
max_rows = 1_000_000
with open(file_path, 'rb') as fh:
    dctx = zstd.ZstdDecompressor()
    with dctx.stream_reader(fh) as reader:
        buffer = b""
        total = 0

        for chunk in iter(lambda: reader.read(2**23), b""):
            buffer += chunk
            lines = buffer.split(b"\n")
            buffer = lines.pop()

            for line in lines:
                try:
                    data = orjson.loads(line.decode('utf-8'))
                    if 'created_utc' in data and ('selftext' in data or 'title' in data):
                        rows.append({
                            'created_at': pd.to_datetime(data['created_utc'], unit='s'),
                            'text': data.get('selftext') or data.get('title', '')
                        })
                        total += 1
                        if total % 10000 == 0:
                            print(f"Read: {total} records")

                        if total >= max_rows:
                            break
                except json.JSONDecodeError:
                    continue

            if total >= max_rows:
                break

print(f"Completed: {len(rows)} records read")

df = pd.DataFrame(rows)
df['text'] = df['text'].astype('string')
print(df.head())



# === STEP 2 === 
print("STEP 2 - Split on quantiles")
df['timestamp'] = df['created_at'].astype('int64')
df['time_quantile'] = pd.qcut(df['timestamp'], q=4)
print(df['time_quantile'].value_counts())



# === STEP 3 === 
print("STEP 3 - Show data")
intervals = df['time_quantile'].cat.categories

for interval in intervals:
    start = pd.to_datetime(interval.left)
    end = pd.to_datetime(interval.right)
    count = df[df['time_quantile'] == interval].shape[0]
    print(f"Quantile: {start} -> {end}, Number of posts: {count}")


# === STEP 4 === 
print("STEP 4 - Building a graph")
durations = []
counts = []

intervals = df['time_quantile'].cat.categories

for interval in intervals:
    start = pd.to_datetime(interval.left)
    end = pd.to_datetime(interval.right)
    duration = (end - start).total_seconds() / 3600  
    count = df[df['time_quantile'] == interval].shape[0]
    
    durations.append(duration)
    counts.append(count)

density = [c/d for c, d in zip(counts, durations)]

plt.figure(figsize=(10, 6))
bars = plt.bar(range(len(density)), density, color='salmon', edgecolor='black')
max_height = max(density)
plt.ylim(0, max_height * 1.2)

for i, bar in enumerate(bars):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f"{counts[i]} posts\n{durations[i]:.1f} hours", 
             ha='center', va='bottom', fontsize=10)


plt.title('Post density in time quantiles (posts per hour)', fontsize=16)
plt.xlabel('Time quantiles', fontsize=14)
plt.ylabel('Posts per hour', fontsize=14)
plt.xticks(range(len(density)), [f'Q{i+1}' for i in range(len(density))])
plt.grid(axis='y')
plt.tight_layout()
plt.show()
