from flask import Flask, jsonify, request
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
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False
            )
            # En iyi ses formatını bul
            formats = info.get("formats", [])
            audio_formats = [
                f for f in formats
                if f.get("acodec") != "none" and f.get("vcodec") == "none"
            ]
            if audio_formats:
                best = max(audio_formats, key=lambda f: f.get("abr") or 0)
                return jsonify({
                    "url": best["url"],
                    "title": info.get("title", ""),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail", "")
                })
            else:
                # Ses formatı yoksa video+ses karışık al
                return jsonify({
                    "url": info["url"],
                    "title": info.get("title", ""),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail", "")
                })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
