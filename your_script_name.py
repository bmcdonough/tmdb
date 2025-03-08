#!/usr/bin/env python3
import ffmpeg
import subprocess

def get_ffmpeg_version():
    """Captures the FFmpeg version."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()
        version_line = output_lines[0]
        version_string = version_line.split("version ")[1].split(" ")[0]
        return version_string
    except FileNotFoundError:
        return "FFmpeg not found"
    except IndexError:
        return "Could not parse FFmpeg version"

def update_metadata(input_file, output_file, ffmpeg_version):
    """Updates the 'Writing application' metadata."""
    try:
        ffmpeg.input(input_file).output(
            output_file,
            **{'metadata': f'Writing application=ffmpeg {ffmpeg_version}'},
            c='copy'  # Copy streams without re-encoding
        ).run(overwrite_output=True)
        print(f"Metadata updated successfully. Output file: {output_file}")
    except ffmpeg.Error as e:
        if e.stderr:
            print(f"Error updating metadata: {e.stderr.decode()}")
        else:
            print("An unknown error occurred during metadata update.")

if __name__ == "__main__":
    input_file = "video.mkv"  # Replace with your input file
    output_file = "output.mkv" # replace with your output file
    ffmpeg_version = get_ffmpeg_version()

    if "FFmpeg not found" in ffmpeg_version or "Could not parse" in ffmpeg_version:
        print(ffmpeg_version)
    else:
        print(f"FFmpeg version: {ffmpeg_version}")
        update_metadata(input_file, output_file, ffmpeg_version)
