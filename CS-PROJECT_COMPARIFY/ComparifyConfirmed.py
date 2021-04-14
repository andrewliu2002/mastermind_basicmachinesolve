
import base64
import datetime
from urllib.parse import urlencode
import spotipy

import requests

client_id = "2b9242f011934954bb7a66ac8b61724f"
client_secret = "ded1c38950114386b878d0a3735e5b3c"

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_trackList(self,playlist_id):
        headers = self.get_resource_header()
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        r = requests.get(endpoint, headers = headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()

    def base_search(self, query_params): # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()
    
    def search(self, query=None, operator=None, operator_query=None, search_type= None ):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        #print(query_params)
        return self.base_search(query_params)

class ClientInteract():
    def get_playlist(self):
        playlistTemp = input("Submit your UNIQUE playlist name: ")
        return playlistTemp
    def question(self):
        questionTemp = input("")


class Compare():
    def compare_list(playlistOne, playlistTwo):
        playlistThree = playlistOne + playlistTwo
        playlistFour = []
        playlistThree.sort()
        i = 1
        for i in range(len(playlistThree)):
            if playlistThree[i-1]==playlistThree[i]:
                playlistFour.append(playlistThree[i-1])
                i = i + 1
        return playlistFour
    def notin_playlist(playlistOne, playlistTwo):
        tempOne = list(set(playlistOne) - set(playlistTwo))
        tempTwo = list(set(playlistTwo)- set(playlistOne))
        tempThree = tempOne + tempTwo
        tempThree.sort()
        return tempThree
        #temp = list(set(playlistOne) - set(playlistTwo))
        #temp = playlistOne + playlistTwo
        #temp.sort()
        #return temp     
        
class Searching():
    playlist = None
    actualPlaylist = None
    def finderPlaylist(playlist):
        Comparify = SpotifyAPI(client_id, client_secret)
        search = Comparify.search(playlist, search_type="playlist")
        nested_nested_dict = search['playlists']['items']
        nested_dict = nested_nested_dict[0]
        #regular_dict = nested_dict["external_urls"]
        return(nested_dict["id"])
    def finderTrack(actualPlaylist):
        testing = actualPlaylist["items"]
        #print(testing)
        i = 0
        finalList = []
        for i in range(len(testing)):
            newTrack = testing[i]['track']
            newName = newTrack['name']
            newArtist = ((newTrack["artists"])[0])["name"]
            tempText = (newName + " by " + newArtist)
            finalList.append(tempText)
        return finalList

def main():
    Comparify = SpotifyAPI(client_id, client_secret)
    ClientInput = ClientInteract()
    playlist_one = ClientInput.get_playlist()
    playlist_two = ClientInput.get_playlist()
    key_one = Searching.finderPlaylist(playlist_one)
    key_two = Searching.finderPlaylist(playlist_two)
    temp_playlist_one = Comparify.get_trackList(key_one)
    temp_playlist_two = Comparify.get_trackList(key_two)
    final_tracklist_one = Searching.finderTrack(temp_playlist_one)
    final_tracklist_two = Searching.finderTrack(temp_playlist_two)
    #yurd = Compare.compare_list(final_tracklist_one,final_tracklist_two)
    yurd = Compare.notin_playlist(final_tracklist_one,final_tracklist_two)
    print(yurd)
main()





