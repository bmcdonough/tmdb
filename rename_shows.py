#!/usr/bin/env python3
import json
import os
import requests
import urllib.parse
from dotenv import load_dotenv

def auth_tmdb(tmdb_token: str):
    url = "https://api.themoviedb.org/3/authentication"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        return response_json['status_message']
    else:
        return json.loads(response.text)

def search_tmdb_tv(tmdb_token: str, search_string: str):
    encoded_string = urllib.parse.quote(search_string)
    query = f"{encoded_string}&include_adult=false&language=en-US&page=1"
    url = f"https://api.themoviedb.org/3/search/tv?query={query}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_token}"
    }
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def get_series_details(tmdb_token: str, series_id: str):
    url = f"https://api.themoviedb.org/3/tv/{series_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_token}"
    }
    response = requests.get(url, headers=headers)
    json_dict = json.loads(response.text)
    # Sort the dictionary by keys
    sorted_dict = {key: json_dict[key] for key in sorted(json_dict.keys())}
    return sorted_dict

def get_season_details(tmdb_token: str, series_id: str, season_num: int):
    url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_num}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_token}"
    }
    response = requests.get(url, headers=headers)
    json_dict = json.loads(response.text)
    # Sort the dictionary by keys
    sorted_dict = {key: json_dict[key] for key in sorted(json_dict.keys())}
    return sorted_dict

def get_episode_details(tmdb_token: str, series_id: str, season: int, episode: int):
    url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season}/episode/{episode}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_token}"
    }
    response = requests.get(url, headers=headers)
    json_dict = json.loads(response.text)
    # Sort the dictionary by keys
    sorted_dict = {key: json_dict[key] for key in sorted(json_dict.keys())}
    return sorted_dict

def add_season(tv_series, season_number, details):
    tv_series['seasons'][season_number].update(details)
    return tv_series


def main():
    try:
        # Check if .env file exists
        if os.path.isfile(".env"):
            # Load environment variables from the .env file
            load_dotenv()
        else:
            print("Missing .env file")
            return 1 # Indicate error
    except Exception as e:
        print(f"Error condition: {e}")
        return 1  # Indicate error

    if os.getenv('TMDB_ACCESS_TOKEN'):
        test_auth = auth_tmdb(os.getenv('TMDB_ACCESS_TOKEN'))
        print(f"testing auth first: {test_auth}")
    else:
        print(f"missing env TMDB_ACCESS_TOKEN")

    search_string = input("Please enter a search string: ")
    search_results = search_tmdb_tv(os.getenv('TMDB_ACCESS_TOKEN'), search_string)

    # use the ID from the first result
    tv_series_id = search_results['results'][0]['id']
    series_details = get_series_details(os.getenv('TMDB_ACCESS_TOKEN'), tv_series_id)
        
    for season in range(series_details['number_of_seasons']):
        # add 1 to season for API
        season_details = get_season_details(os.getenv('TMDB_ACCESS_TOKEN'), tv_series_id, season + 1)
        # overwriting with season_details, strips 'episode_count'
        series_details['seasons'][season] = season_details
        print(f"Season: {series_details['seasons'][season]['season_number']}, Episodes: {len(series_details['seasons'][season]['episodes'])}")
    return 0


if __name__ == "__main__":
  exit_code = main()
  if exit_code == 0:
    print("Main completed successfully.")
  else:
    print("Main failed to complete.")