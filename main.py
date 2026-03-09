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
            "format": "best",
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False
            )
            url = info.get("url") or info.get("webpage_url")
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
