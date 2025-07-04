from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

@app.route('/get-transcript', methods=['POST'])
def get_transcript():
    data = request.json
    youtube_url = data.get('url', '')

    try:
        parsed_url = urlparse(youtube_url)
        query = parse_qs(parsed_url.query)
        video_id = query.get("v")
        if video_id:
            video_id = video_id[0]
        else:
            video_id = parsed_url.path.strip("/")

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([entry['text'] for entry in transcript])
        return jsonify({ "transcript": full_text })

    except Exception as e:
        return jsonify({ "error": str(e) }), 400

@app.route('/')
def home():
    return "Flask app is running!"

if __name__ == '__main__':
    app.run()