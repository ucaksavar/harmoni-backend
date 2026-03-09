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
            "format": "bestaudio",
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False
            )
            formats = info.get("formats", [])
            
            # Önce sadece ses formatlarını dene
            audio_only = [
                f for f in formats
                if f.get("acodec") != "none" 
                and f.get("vcodec") in ("none", None)
                and f.get("url")
            ]
            
            if audio_only:
                best = max(audio_only, key=lambda f: f.get("abr") or f.get("tbr") or 0)
            else:
                # Ses+video karışık formatları dene
                mixed = [f for f in formats if f.get("url") and f.get("acodec") != "none"]
                if not mixed:
                    return jsonify({"error": "Format bulunamadı"}), 404
                best = mixed[-1]

            return jsonify({
                "url": best["url"],
                "title": info.get("title", ""),
                "duration": info.get("duration", 0),
                "thumbnail": info.get("thumbnail", ""),
                "ext": best.get("ext", ""),
                "abr": best.get("abr", 0)
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
