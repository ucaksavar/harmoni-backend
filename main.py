from flask import Flask, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"status": "Harmoni Backend çalışıyor 🎵"})

@app.route("/stream/<video_id>")
def get_stream(video_id):
    try:
        ydl_opts = {
            "format": "18/bestvideo+bestaudio/best",
            "quiet": False,
            "no_warnings": False,
            "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False
            )
            # Tüm formatları logla
            for f in info.get("formats", []):
                print(f"FORMAT: {f.get('format_id')} | {f.get('ext')} | acodec:{f.get('acodec')} | vcodec:{f.get('vcodec')} | url:{str(f.get('url',''))[:50]}")
            
            url = info.get("url")
            if not url:
                formats = info.get("formats", [])
                playable = [f for f in formats if f.get("url") and f.get("acodec") != "none"]
                if playable:
                    url = playable[-1]["url"]
            
            return jsonify({
                "url": url,
                "title": info.get("title", ""),
                "duration": info.get("duration", 0),
                "thumbnail": info.get("thumbnail", "")
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
