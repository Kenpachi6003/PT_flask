import subprocess

li = []
result = subprocess.run(
    ["ls", "/Users/kenpachi/my_projects/PT_flask"], capture_output=True, text=True
)
mov_vids = subprocess.run(
    ["ls", "/Users/kenpachi/Desktop/Causey/Workout_vids"],
    capture_output=True,
    text=True,
)
# Print the output
print(result.stdout.split())
print(mov_vids.stdout.split())

for vid in mov_vids.stdout.split():
    split_vid = vid.split(".")
    # print(split_vid[0])
    # print("/Users/kenpachi/Desktop/Causey/Formatted_workout_vids/" + split_vid[0] + ".mp4")

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            "/Users/kenpachi/Desktop/Causey/Workout_vids/" + vid,  # Input file
            "-vcodec",
            "h264",  # Video codec
            "-acodec",
            "aac",  # Audio codec
            "/Users/kenpachi/Desktop/Causey/Formatted_workout_vids/"
            + split_vid[0]
            + ".mp4",  # Output file
        ]
    )
# the command to format videos
# ffmpeg -i video.mov -vcodec h264 -acodec aac video.mp4
# pwd /Users/kenpachi/my_projects/PT_flask
