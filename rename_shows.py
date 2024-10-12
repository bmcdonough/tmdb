#!/usr/bin/env python3
import json
import os
import re
import requests
import urllib.parse
import argparse
from dotenv import load_dotenv
from pymediainfo import MediaInfo
import shutil

class TMDBApi:
    def __init__(self, source_dir, dest_dir, tv_series):
        self.load_env()
        self.tmdb_token = os.getenv('TMDB_ACCESS_TOKEN')
        if not self.tmdb_token:
            raise ValueError("Missing TMDB_ACCESS_TOKEN in environment variables")
        self.source_dir = source_dir
        self.dest_dir = dest_dir
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
            "Authorization": f"Bearer {self.tmdb_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            return response_json['status_message']
        else:
            return json.loads(response.text)

    def search_tmdb_tv(self, search_string: str):
        encoded_string = urllib.parse.quote(search_string)
        query = f"{encoded_string}&include_adult=false&language=en-US&page=1"
        url = f"https://api.themoviedb.org/3/search/tv?query={query}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.tmdb_token}"
        }
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def get_series_details(self, series_id: str):
        url = f"https://api.themoviedb.org/3/tv/{series_id}?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.tmdb_token}"
        }
        response = requests.get(url, headers=headers)
        json_dict = json.loads(response.text)
        return {key: json_dict[key] for key in sorted(json_dict.keys())}

    def get_season_details(self, series_id: str, season_num: int):
        url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_num}?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.tmdb_token}"
        }
        response = requests.get(url, headers=headers)
        json_dict = json.loads(response.text)
        return {key: json_dict[key] for key in sorted(json_dict.keys())}

    def get_episode_details(self, series_id: str, season: int, episode: int):
        url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season}/episode/{episode}?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.tmdb_token}"
        }
        response = requests.get(url, headers=headers)
        json_dict = json.loads(response.text)
        return {key: json_dict[key] for key in sorted(json_dict.keys())}

    def gather_series_data(self):
        search_results = self.search_tmdb_tv(self.tv_series)
        if not search_results['results']:
            raise ValueError(f"No results found for TV series: {self.tv_series}")

        series_id = search_results['results'][0]['id']
        series_details = self.get_series_details(series_id)
        self.series_data = {
            'id': series_id,
            'name': series_details['name'],
            'seasons': {}
        }

        for season in range(1, series_details['number_of_seasons'] + 1):
            season_details = self.get_season_details(series_id, season)
            self.series_data['seasons'][season] = {
                'episodes': {}
            }
            for episode in season_details['episodes']:
                episode_details = self.get_episode_details(series_id, season, episode['episode_number'])
                self.series_data['seasons'][season]['episodes'][episode['episode_number']] = episode_details

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
                for key, value in track.items():
                    print(f"    {key}: {value}")
            print()  # Add a newline for better readability

    def process_single_video(self, file_path):
        movie_info = self.extract_movie_info(file_path)
#        self.print_movie_info(movie_info)
        movie_name = movie_info['General'][0]['movie_name']
        description = movie_info['General'][0]['description']
        height = movie_info['Video'][0]['height']
        v_format = movie_info['Video'][0]['format']
        a_format = movie_info['Audio'][0]['format']
        dot_fname = re.sub(r'\s+', '.', self.series_data['name'])

        for season, season_data in self.series_data['seasons'].items():
            for episode, episode_details in season_data['episodes'].items():
                if self.match_episode(movie_name, description, episode_details):
                    print(f"Match found for {file_path}")
                    print(f"Season: {season}, Episode: {episode}, Title: {movie_name}")
#                    print("Available attributes:")
#                    for key, value in episode_details.items():
#                        print(f"- {key}: {value}")
#                    print("\n")
                    
                    # Copy and rename the file
                    src_fname, src_extension = os.path.splitext(os.path.basename(file_path))
                    new_filename = f"{dot_fname}.S{season:02d}E{episode:02d}.{height}p.{v_format}.{a_format}{src_extension}"
                    dest_path = os.path.join(self.dest_dir, new_filename)
                    shutil.copy2(file_path, dest_path)
                    print(f"File copied and renamed: {dest_path}\n")
                    return  # Stop after first match

        print(f"No match found for {file_path}: {movie_name}\n")

    def match_episode(self, movie_name, description, episode_details):
        episode_name = episode_details.get('name', '').lower()
        episode_overview = episode_details.get('overview', '').lower()
        movie_name = movie_name.lower()
        description = description.lower()

        return (movie_name in episode_name or movie_name in episode_overview or
                description in episode_name or description in episode_overview)

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
    parser = argparse.ArgumentParser(description="Process video files and match with TMDB data")
    parser.add_argument("source_dir", help="Source directory containing video files")
    parser.add_argument("dest_dir", help="Destination directory for processed files")
    parser.add_argument("tv_series", help="Name of the TV series to search for")
    args = parser.parse_args()

    tmdb_api = TMDBApi(args.source_dir, args.dest_dir, args.tv_series)
    exit_code = tmdb_api.run()
    if exit_code == 0:
        print("Main completed successfully.")
    else:
        print("Main failed to complete.")

if __name__ == "__main__":
    main()