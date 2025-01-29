
import os
import subprocess

# Search term
search_query = "Hilton Hotel"

# Output directory
output_dir = "videos"
os.makedirs(output_dir, exist_ok=True)

# Video filenames
video_files = [f"{output_dir}/video{i+1}.mp4" for i in range(3)]

# Download commands
commands = {
    "torsocks": [
        "torsocks", "yt-dlp", f"ytsearch3:{search_query}",
        "-o", f"{output_dir}/video%(search_index)s.mp4",
        "--no-part"
    ],
    "tor_proxy": [
        "yt-dlp", "--proxy", "socks5h://localhost:9050",
        f"ytsearch3:{search_query}",
        "-o", f"{output_dir}/video%(search_index)s.mp4",
        "--no-part"
    ]
}

# Run tests
results = {}

for method, command in commands.items():
    print(f"\n🔍 Testing {method.upper()} method...\n{'='*40}")
    result = subprocess.run(command, capture_output=True, text=True)

    # Save results
    results[method] = {
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "success": result.returncode == 0
    }

    print(f"✅ STDOUT:\n{result.stdout.strip()}\n")
    print(f"❌ STDERR:\n{result.stderr.strip()}\n")

# Final check: Which videos were downloaded
print("\n📂 Checking downloaded videos...\n" + "="*40)
for file in video_files:
    if os.path.exists(file) and os.path.getsize(file) > 0:
        print(f"✅ Success: {file} downloaded")
    else:
        print(f"❌ Failed: {file} not found or empty")

# Print summary
print("\n🔍 Test Summary:\n" + "="*40)
for method, result in results.items():
    status = "✅ Success" if result["success"] else "❌ Failed"
    print(f"{method.upper()}: {status}")
