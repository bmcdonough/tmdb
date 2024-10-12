#!/usr/bin/env python3
import json
import os
import requests
import urllib.parse
import argparse
from dotenv import load_dotenv
from pymediainfo import MediaInfo
import re

class TMDBApi:
    def __init__(self, source_dir, dest_dir):
        self.load_env()
        self.tmdb_token = os.getenv('TMDB_ACCESS_TOKEN')
        if not self.tmdb_token:
            raise ValueError("Missing TMDB_ACCESS_TOKEN in environment variables")
        self.source_dir = source_dir
        self.dest_dir = dest_dir

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
#        movie_name = os.path.splitext(os.path.basename(file_path))[0]
#        description = ""
        for track in media_info.tracks:
            if track.track_type == "General":
                description = track.description or ""
                movie_name = track.movie_name or ""
                break
        return movie_name, description

    def process_single_video(self, file_path):
        movie_name, description = self.extract_movie_info(file_path)
#        search_results = self.search_tmdb_tv(movie_name)
        search_results = self.search_tmdb_tv("sanford and son")
        
        if search_results['results']:
            series_id = search_results['results'][0]['id']
            series_details = self.get_series_details(series_id)
            
            for season in range(1, series_details['number_of_seasons'] + 1):
                season_details = self.get_season_details(series_id, season)
                for episode in season_details['episodes']:
                    episode_details = self.get_episode_details(series_id, season, episode['episode_number'])
                    if self.match_episode(movie_name, description, episode_details):
                        print(f"Match found for {movie_name}:")
                        print(f"Season: {season}, Episode: {episode['episode_number']}")
                        print("Available attributes:")
                        for key, value in episode_details.items():
                            print(f"- {key}: {value}")
                        print("\n")

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
            self.process_video_files()
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1

def main():
    parser = argparse.ArgumentParser(description="Process video files and match with TMDB data")
    parser.add_argument("source_dir", help="Source directory containing video files")
    parser.add_argument("dest_dir", help="Destination directory for processed files")
    args = parser.parse_args()

    tmdb_api = TMDBApi(args.source_dir, args.dest_dir)
    exit_code = tmdb_api.run()
    if exit_code == 0:
        print("Main completed successfully.")
    else:
        print("Main failed to complete.")

if __name__ == "__main__":
    main()