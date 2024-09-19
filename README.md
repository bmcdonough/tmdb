# summary
script to rename shows using the API of The Movie Database (TMDB)
## attribution
![alt text](https://www.themoviedb.org/assets/2/v4/logos/v2/blue_long_2-9665a76b1ae401a510ec1e0ca40ddcb3b0cfe45f1d51b77a308fea0845885648.svg "The Movie Database")
## create .env
- create **.env** file with the following contents, populated from your personal account:  [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)
```shell
TMDB_API_KEY = "your api key here"
TMDB_ACCESS_TOKEN = "your api access token here"
```
## use
### requirements
```shell
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
### run
```shell
python3 rename_shows.py
Please enter a search string: sanford and son
```