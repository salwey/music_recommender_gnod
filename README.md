# music_recommender_gnod

## Ironhack project: Web Scraping, APIs, Clustering

**Goal:** Take a song and artist provided by the user, if this song is found within the Billboard Top 100 return another song from this top 100, if it is not found. We use spotipy API to gather audio features to suggest a similar song based on a list of tracks we have applied a clustering to and built a machine learning model from so we can apply the model to the users song's audio features and with that find a song to recommend from the same cluster within our list.


music_recommender.ipynb : jupyter notebook for the project, sections: Billboard 100 - (get list of 100 tracks by web scraping Billboard Top 100)
                                                                      Spotipy (get large list of tracks with audio features, gets a unique list of artists from 5 playlists and gets 10 songs for each artist ~3500 tracks info)
                                                                      Clustering - building model to cluster our tracks based the tracks audio features
                                                                      Song recommendationeratorizer - applies model to user selected track and returns recommendation
music_recommenderizer.py : python file, seperating out the model building and track gathering and leaving the user program to get song recommendations
my_model.p : pickle of our model so we can load into python program
my_scaler.p : pickle of scaler transformation which we apply prior to applying the model to audio features of users provided track
top_100.csv : the top songs and artists from Billboard 100
tracks.csv : list of tracks collected using spotipy
tracks_clustered.csv : same list of tracks collected using spotipy but with column to identify the cluster it belongs to
