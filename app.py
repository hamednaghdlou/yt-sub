from youtube_transcript_api import YouTubeTranscriptApi
import re
import sys

def extract_video_id(url):
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"embed/([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def format_srt_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds)
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"

def convert_to_srt(transcript):
    srt_lines = []
    for i, item in enumerate(transcript, start=1):
        start = item["start"]
        duration = item.get("duration", 0)
        end = start + duration
        text = item["text"].replace("\n", " ").strip()
        srt_lines.append(str(i))
        srt_lines.append(f"{format_srt_time(start)} --> {format_srt_time(end)}")
        srt_lines.append(text)
        srt_lines.append("")
    return "\n".join(srt_lines)

def download_fa_subtitle(url, out_file="subtitle_fa.srt"):
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    transcript = None
    try:
        transcript = transcript_list.find_transcript(['fa'])
    except:
        try:
            transcript = transcript_list.find_transcript(['fa-IR'])
        except:
            transcript = None

    if transcript is None:
        raise ValueError("No Persian transcript found")

    data = transcript.fetch()
    srt = convert_to_srt(data)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(srt)

    print(f"Saved to {out_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <youtube_url>")
        sys.exit(1)

    download_fa_subtitle(sys.argv[1])
