"""
Re-encode welding video with:
1. moov atom at beginning (faststart) - browser can start playing immediately
2. Correct duration metadata
3. Proper keyframe interval (every 2 seconds)
4. Reasonable file size (~5MB)
"""
import av
import os
from fractions import Fraction

INPUT = '/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/videos/welding-video-original.mp4'
OUTPUT = '/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/videos/welding-video.mp4'

# Open input
inp = av.open(INPUT)
in_stream = inp.streams.video[0]
in_codec = in_stream.codec_context

print(f"Input: {INPUT}")
print(f"  Resolution: {in_codec.width}x{in_codec.height}")
print(f"  Codec: {in_codec.codec.name}")
print(f"  Frame rate: {in_stream.average_rate}")

# Target settings
TARGET_WIDTH = 854
TARGET_HEIGHT = 480
TARGET_FPS = 24
CRF = 35  # slightly better quality than 38, still small

# Create output with faststart
out = av.open(OUTPUT, 'w', options={
    'movflags': '+faststart',  # Put moov atom at beginning!
})

# Set up encoder
out_stream = out.add_stream('h264', rate=TARGET_FPS)
out_stream.codec_context.width = TARGET_WIDTH
out_stream.codec_context.height = TARGET_HEIGHT
out_stream.codec_context.pix_fmt = 'yuv420p'
out_stream.codec_context.options = {
    'crf': str(CRF),
    'preset': 'medium',
    'tune': 'fastdecode',  # Optimize for fast decoding (less CPU = smoother playback)
    'profile': 'high',
    'g': str(TARGET_FPS * 2),  # Keyframe every 2 seconds
}

print(f"\nOutput: {OUTPUT}")
print(f"  Resolution: {TARGET_WIDTH}x{TARGET_HEIGHT}")
print(f"  FPS: {TARGET_FPS}")
print(f"  CRF: {CRF}")
print(f"  Keyframe interval: {TARGET_FPS * 2} frames (2 seconds)")
print(f"  Faststart: enabled (moov at beginning)")

# Encode
frame_count = 0
for frame in inp.decode(in_stream):
    # Resize if needed
    if frame.width != TARGET_WIDTH or frame.height != TARGET_HEIGHT:
        frame = frame.reformat(width=TARGET_WIDTH, height=TARGET_HEIGHT)

    # Set correct PTS
    frame.pts = frame_count
    frame.time_base = Fraction(1, TARGET_FPS)

    # Encode
    for packet in out_stream.encode(frame):
        out.mux(packet)

    frame_count += 1
    if frame_count % 100 == 0:
        print(f"  Encoded {frame_count} frames...")

# Flush
for packet in out_stream.encode():
    out.mux(packet)

inp.close()
out.close()

# Verify
fsize = os.path.getsize(OUTPUT)
print(f"\nDone! Encoded {frame_count} frames")
print(f"File size: {fsize/1024/1024:.2f} MB")

# Check moov position
with open(OUTPUT, 'rb') as f:
    data = f.read()
moov_pos = data.find(b'moov')
mdat_pos = data.find(b'mdat')
print(f"moov at: {moov_pos} ({moov_pos/len(data)*100:.1f}% into file)")
print(f"mdat at: {mdat_pos} ({mdat_pos/len(data)*100:.1f}% into file)")
if moov_pos < mdat_pos:
    print("Faststart: YES - browser can start playing immediately!")
else:
    print("Faststart: NO - still needs to download full file first")

# Verify with PyAV
verify = av.open(OUTPUT)
v = verify.streams.video[0]
duration = float(verify.duration) / 1e6
print(f"Duration: {duration:.2f}s")
print(f"Resolution: {v.codec_context.width}x{v.codec_context.height}")
print(f"Frame rate: {v.average_rate}")
verify.close()
