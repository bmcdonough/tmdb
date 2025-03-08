#!/usr/bin/env python3
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

def update_metadata(input_file, ffmpeg_version):
    """Updates the 'Writing application' metadata and clears 'muxing-application-version'."""
    try:
        command = [
            'mkvpropedit',
            input_file,
            '--edit', 'info',
            '--set', f'writing-application=ffmpeg {ffmpeg_version}',
            '--delete', 'muxing-application-version'
        ]
        subprocess.run(command, check=True)
        print(f"Metadata updated successfully. Input file: {input_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error updating metadata: {e}")
    except FileNotFoundError:
        print("mkvpropedit not found. Please install MKVToolNix.")

if __name__ == "__main__":
    input_file = "video.mkv"  # Replace with your input file
    ffmpeg_version = get_ffmpeg_version()

    if "FFmpeg not found" in ffmpeg_version or "Could not parse" in ffmpeg_version:
        print(ffmpeg_version)
    else:
        print(f"FFmpeg version: {ffmpeg_version}")
        update_metadata(input_file, ffmpeg_version)
