#!/usr/bin/env python3
import argparse
import ffmpeg
import json
import os
import re
# import shutil
import subprocess
import urllib.parse

import requests
from dotenv import load_dotenv
from pymediainfo import MediaInfo


class TMDBApi:
    def __init__(self, source_dir, tv_series):
        self.load_env()
        self.tmdb_token = os.getenv("TMDB_ACCESS_TOKEN")
        if not self.tmdb_token:
            raise ValueError("Missing TMDB_ACCESS_TOKEN in environment variables")
        self.source_dir = source_dir
        self.tv_series = tv_series
        self.series_data = None

    def load_env(self):
        if os.path.isfile(".env"):
            load_dotenv()
        else:
            raise FileNotFoundError("Missing .env file")

    def auth_tmdb(self):
        url = "https://api.themoviedb.org/3/authentication"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.tmdb_token}",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if "status_message" in response_json:
                return response_json["status_message"]
            elif "success" in response_json:
                return response_json["success"]
            else:
                return json.loads(response.text)
        else:
            return json.loads(response.text)

    def search_tmdb_tv(self, search_string: str):
        encoded_string = urllib.parse.quote(search_string)
        query = f"{encoded_string}&include_adult=false&language=en-US&page=1"
        url = f"https://api.themoviedb.org/3/search/tv?query={query}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.tmdb_token}",
        }
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def get_series_details(self, series_id: str):
        url = f"https://api.themoviedb.org/3/tv/{series_id}?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.tmdb_token}",
        }
        response = requests.get(url, headers=headers)
        json_dict = json.loads(response.text)
        return {key: json_dict[key] for key in sorted(json_dict.keys())}

    def get_season_details(self, series_id: str, season_num: int):
        url = (
            f"https://api.themoviedb.org/3"
            f"/tv/{series_id}"
            f"/season/{season_num}"
            f"?language=en-US"
        )
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.tmdb_token}",
        }
        response = requests.get(url, headers=headers)
        json_dict = json.loads(response.text)
        return {key: json_dict[key] for key in sorted(json_dict.keys())}

    def get_episode_details(self, series_id: str, season: int, episode: int):
        url = (
            f"https://api.themoviedb.org/3"
            f"/tv/{series_id}"
            f"/season/{season}"
            f"/episode/{episode}"
            f"?language=en-US"
        )
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.tmdb_token}",
        }
        response = requests.get(url, headers=headers)
        json_dict = json.loads(response.text)
        return {key: json_dict[key] for key in sorted(json_dict.keys())}

    def gather_series_data(self):
        search_results = self.search_tmdb_tv(self.tv_series)
        if not search_results["results"]:
            raise ValueError(f"No results found for TV series: {self.tv_series}")

        series_id = search_results["results"][0]["id"]
        series_details = self.get_series_details(series_id)
        self.series_data = {
            "id": series_id,
            "name": series_details["name"],
            "seasons": {},
        }

        for season in range(1, series_details["number_of_seasons"] + 1):
            season_details = self.get_season_details(series_id, season)
            self.series_data["seasons"][season] = {"episodes": {}}
            for episode in season_details["episodes"]:
                episode_details = self.get_episode_details(
                    series_id, season, episode["episode_number"]
                )
                self.series_data["seasons"][season]["episodes"][
                    episode["episode_number"]
                ] = episode_details

    def process_video_files(self):
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if self.is_video_file(file_path):
                    self.process_single_video(file_path)

    def is_video_file(self, file_path):
        media_info = MediaInfo.parse(file_path)
        for track in media_info.tracks:
            if track.track_type == "Video":
                return True
        return False

    def extract_movie_info(self, file_path):
        media_info = MediaInfo.parse(file_path)
        all_tracks = {}
        for track in media_info.tracks:
            track_info = {}
            for key, value in track.to_data().items():
                track_info[key] = value
            all_tracks[track.track_type] = all_tracks.get(track.track_type, [])
            all_tracks[track.track_type].append(track_info)
        return all_tracks

    def print_movie_info(self, all_tracks):
        for track_type, tracks in all_tracks.items():
            print(f"Track Type: {track_type}")
            for i, track in enumerate(tracks):
                print(f"  Track {i + 1}:")
                for key, value in sorted(track.items()):
                    print(f"    {key}: {value}")
            print()  # Add a newline for better readability
            return None

    def parse_name_season_episode(self, name):
        pattern = r"[sS]\d{2}[eE]\d{2}"
        season_pattern = r"[sS](\d{2})"
        episode_pattern = r"[eE](\d{2})"
        match = re.search(pattern, name)
        if match:
            extracted = match.group()
            season_match = re.search(season_pattern, extracted)
            episode_match = re.search(episode_pattern, extracted)
            if season_match and episode_match:
                return {
                    "season": season_match.group(1).lstrip('0'),
                    "episode": episode_match.group(1).lstrip('0'),
                }
        return {"season": None, "episode": None}
    
    def match_episode(self, episode_details, *search_terms):
        episode_name = episode_details.get("name", "").lower()
        episode_overview = episode_details.get("overview", "").lower()
        episode_season_number = episode_details.get("season_number", "")
        episode_number = episode_details.get("episode_number", "")
        for term in search_terms:
            print(f"type(term):{type(term)}")
            print(f"type(episode_season_number):{type(episode_season_number)}")
            print(f"type(episode_number):{type(episode_number)}")
            print(f"term: {term};  episode_name:{episode_name}, episode_overview:{episode_overview}, episode_season_number:{episode_season_number}, episode_number:{episode_number}")
            if term == str(episode_season_number) and term == str(episode_number):
                print("###Season Match")
                print("###Episode Match")
        return any(
            term.lower() in episode_name
            or term.lower() in episode_overview
            or term == str(episode_season_number)
            or term == str(episode_number)
            for term in search_terms
        )
    
    def set_mkv_title(self, file_path, title):
        """Sets the title metadata in an MKV file."""

        try:
            subprocess.run(
                ["mkvpropedit", file_path, "--edit", "info", "--set", f"title={title}"],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"Title set to '{title}' successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error setting title: {e.stderr}")
        except FileNotFoundError:
            print("mkvpropedit not found. Make sure MKVToolNix is installed.")

    def set_mkv_tag(self, file_path, tagName, tagValue):
        """Sets a tag metadata in an MKV file."""

        try:
            subprocess.run(
                ["mkvpropedit", file_path, "--edit", "info", "--set", f"tag:{tagName}={tagValue}"],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"Tag {tagName} set to '{tagValue}' successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error setting tag: {e.stderr}")
        except FileNotFoundError:
            print("mkvpropedit not found. Make sure MKVToolNix is installed.")

    def get_ffmpeg_version(self):
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

    def update_metadata(self, input_file, output_file, metadata):
        """Updates the 'Writing application' metadata."""
        try:
            ffmpeg.input(input_file).output(
                output_file,
                metadata,
                c='copy'  # Copy streams without re-encoding
            ).run(overwrite_output=True)
            print(f"Metadata updated successfully. Output file: {output_file}")
        except ffmpeg.Error as e:
            print(f"Error updating metadata: {e.stderr.decode()}")

    def process_single_video(self, file_path):
        print(f"working on: {file_path}")

        movie_info = self.extract_movie_info(file_path)
#        self.print_movie_info(movie_info)

        if "description" in movie_info["General"][0]:
            general_movie_description = movie_info["General"][0]["description"]
        else:
            general_movie_description = ""

        if "movie_name" in movie_info["General"][0]:
            general_movie_name = movie_info["General"][0]["movie_name"]
        else:
            general_movie_name = ""

        if "title" in movie_info["General"][0]:
            general_title = movie_info["General"][0]["title"]
        else:
            general_title = ""

        if "title" in movie_info["Video"][0]:
            video_title = movie_info["Video"][0]["title"]
        else:
            video_title = ""

        if "file_name" in movie_info["General"][0]:
            general_file_name = movie_info["General"][0]["file_name"]
        else:
            general_file_name = ""


        # check if the title contains S##E##
        for item in (general_movie_name, general_title, video_title, general_file_name):
            if item:
                result = self.parse_name_season_episode(item)
                season_num, episode_num = result['season'], result['episode']
                if season_num and episode_num:  # If we got valid results
                    print(f"found Season {season_num} and Episode {episode_num} in video file")
                    break  # Stop checking other items

        if 1081 <= int(movie_info["Video"][0]["height"]) <= 2160:
            height = 2160
        elif 721 <= int(movie_info["Video"][0]["height"]) <= 1080:
            height = 1080
        elif 481 <= int(movie_info["Video"][0]["height"]) <= 720:
            height = 720
        elif 1 <= int(movie_info["Video"][0]["height"]) <= 480:
            height = 480
        else:
            height = movie_info["Video"][0]["height"]

        v_format = movie_info["Video"][0]["format"]

        if "Audio" in movie_info.keys():
            a_format = movie_info["Audio"][0]["format"]
        else:
            print(f"WARNING, this file is missing audio")
            return

        dot_fname = re.sub(r"\s+", ".", self.series_data["name"])

        for season, season_data in self.series_data["seasons"].items():
            for episode, episode_details in season_data["episodes"].items():
#                print(f"season: {season}, episode: {episode}; season_num: {season_num}, episode_num: {episode_num}")
#                if self.match_episode(episode_details, season, episode):
                if self.match_episode(episode_details, general_movie_name, general_movie_name, video_title, season_num, episode_num):
#                    print(
#                        f"Match found - Season: {season}"
#                        f", Episode: {episode}"
#                        f"\nTitle: {general_movie_name}"
#                        f"\nDescription: {general_movie_description}"
#                    )
                    print("Available attributes:")
                    for key, value in episode_details.items():
                        print(f"- {key}: {value}")
                    print("\n")

                    ffmpeg_version = self.get_ffmpeg_version()
                    if "FFmpeg not found" in ffmpeg_version or "Could not parse" in ffmpeg_version:
                        print(ffmpeg_version)
                    else:
                        print(f"FFmpeg version: {ffmpeg_version}")
#                        self.update_metadata(input_file, output_file, ffmpeg_version)

                    new_metadata = {
                        'title': episode_details['name'],
                        'description': episode_details['overview'],
                        'writing_application': f'ffmpeg {ffmpeg_version}',
                        }
#                    self.set_mkv_title(file_path, episode_details['name'])
#                    self.set_mkv_tag(file_path, "DESCRIPTION", episode_details['overview'])

                    # Copy and rename the file
                    directory_path, src_file_name = os.path.split(file_path)
                    src_fname_wout_ext, src_extension = os.path.splitext(src_file_name)
                    new_filename = (
                        f"{dot_fname}"
                        f".S{season:02d}E{episode:02d}"
                        f".{height}p"
                        f".{v_format.lower()}"
                        f".{a_format.lower()}"
                        f"{src_extension}"
                    )
                    dest_path = os.path.join(directory_path, new_filename)
                    # old name, new name
#                    os.rename(file_path, dest_path)
                    self.update_metadata(file_path, dest_path, new_metadata)
                    print(f"File copied and renamed: {dest_path}\n")
                    return  # Stop after first match

        print(f"***\nNo match found - {movie_name}\n{description}\n***\n")

    #    def match_episode(self, movie_name, description, episode_details):
    #        episode_name = episode_details.get('name', '').lower()
    #        episode_overview = episode_details.get('overview', '').lower()
    #        movie_name = movie_name.lower()
    #        description = description.lower()
    #        return (movie_name in episode_name or movie_name in episode_overview or
    #                description in episode_name or description in episode_overview)

    def run(self):
        try:
            test_auth = self.auth_tmdb()
            print(f"Testing auth first: {test_auth}")
            self.gather_series_data()
            self.process_video_files()
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1


def main():
    parser = argparse.ArgumentParser(
        description="Process video files and match with TMDB data"
    )
    parser.add_argument("source_dir", help="Source directory containing video files")
    parser.add_argument("tv_series", help="Name of the TV series to search for")
    args = parser.parse_args()

    tmdb_api = TMDBApi(args.source_dir, args.tv_series)
    exit_code = tmdb_api.run()
    if exit_code == 0:
        print("Main completed successfully.")
    else:
        print("Main failed to complete.")


if __name__ == "__main__":
    main()
