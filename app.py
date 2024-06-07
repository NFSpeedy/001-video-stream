from pathlib import Path
from flask import Flask, Response, request, send_file
import logging


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
)
log = logging.getLogger('flask')

# Start Flask app
app = Flask(__name__)

# main video file
video_file = 'video_lib/video.mkv'
pl_video_file = Path(f"./{video_file}")


def m3u_creator(data: dict[tuple[int, str, str, Path]]) -> str:
    """
    Creating the M3U file that is going to be sent.

    Args:
        ...

    Returns:
        str: The ready m3u file.
    """
    log.info(f"Creating M3U file with {len(data)} entries.")
    m3u_header = "#EXTM3U\n"
    m3u_footer = "#EXTGENRE:TV Series\n#EXTART:Vince Gilligan, John Shiban\n"

    m3u_content = ''

    for duration, author, title, path in data:
        m3u_content += f"#EXTINF:{duration},{author},{title}\n"
        m3u_content += f"http://{request.host}/videos/{path.name}\n"

    m3u_file = m3u_header + m3u_content + m3u_footer

    log.info("Saving the M3U file.")
    with open('last_playlist.m3u', 'w') as latest_m3u_file:
        latest_m3u_file.write(m3u_file)

    return m3u_file



@app.route('/')
def index():

    # TODO: Get the files from a folder and populate the list_of_episodes
    list_of_episodes: dict[tuple[int, str, str, Path]] = {
        (123, 'John Shiban', pl_video_file.name.removesuffix('.mkv'), pl_video_file)
    }
    m3u_file = m3u_creator(data=list_of_episodes)
    # TODO: Subtitles - add them if they exist
    # TODO: Poster - add it to the m3u file (if it exists)
    log.info(f"Sending {len(list_of_episodes)} files.")
    return Response(m3u_file, 200, mimetype='audio/x-mpegurl')


@app.route('/videos/<filename>')
def serving_files(filename):
    log.info(f"Received a request for {filename}.")
    if pl_video_file.exists():
        return send_file(
            pl_video_file, mimetype='video/matroska',
            as_attachment=True, max_age=3*24*60*60
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)





# @app.route('/')
# def index():
#     # Generate M3U playlist
#     m3u_content = "#EXTM3U\n"
#     for filename in os.listdir(app.config['MEDIA_DIR']):
#         if filename.endswith('.mkv'):
#             # Assuming subtitle file has the same name but with .srt extension
#             subtitle_file = filename.replace('.mkv', '.srt')
#             file_url = f"http://{request.host}/stream/{filename}"
#             subtitle_url = f"http://{request.host}/subtitles/{subtitle_file}"
#             m3u_content += f"#EXTINF:-1,{filename}\n"
#             m3u_content += f"{file_url}\n"
#             if os.path.exists(os.path.join(app.config['MEDIA_DIR'], subtitle_file)):
#                 m3u_content += f"#EXTVLCOPT:sub-file={subtitle_url}\n"

#     return Response(m3u_content, mimetype='audio/x-mpegurl')
