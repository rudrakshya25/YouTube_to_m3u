#! /usr/bin/python3



import requests
import os
import yt_dlp

def grab(url: str) -> str:
    """Extract the direct .m3u8 HLS URL from a YouTube live link."""
    ydl_opts = {"quiet": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            for f in formats:
                if ".m3u8" in f.get("url", ""):
                    return f["url"]
    except Exception as e:
        print(f"Error extracting stream for {url}: {e}")
    
    # fallback if yt-dlp fails
    return "https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u"


def generate_m3u() -> str:
    """Generate a full .m3u playlist from youtube_channel_info.txt"""
    playlist = '#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml"\n'
    
    with open('youtube_channel_info.txt') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("~~")]
        
        # process in pairs (metadata line + YouTube URL)
        for i in range(0, len(lines), 2):
            try:
                meta = lines[i].split("|")
                ch_name = meta[0].strip()
                grp_title = meta[1].strip().title()
                tvg_logo = meta[2].strip()
                tvg_id   = meta[3].strip()
                url      = lines[i+1].strip()

                # add EXTINF line
                playlist += f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}\n'
                
                # add stream URL
                playlist += grab(url) + "\n"
            
            except Exception as e:
                print(f"Error parsing channel block at line {i+1}: {e}")
                continue

    return playlist


if __name__ == "__main__":
    m3u = generate_m3u()
    with open("youtube.m3u", "w", encoding="utf-8") as f:
        f.write(m3u)
    print("✅ youtube.m3u generated successfully")
