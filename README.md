# Song-To-MP3-Downloader

This Python script can:
```bash
- Download a song from Spotify or YouTube link.
- Download songs from a Spotify or YouTube playlist.
```

## Package Installation Instructions:

### Spotify
This is a Python library for the Spotify Web API. To install it, you can use pip,
```bash
pip install spotipy
```

### Pytube
This is a library to work with YouTube videos. To install it, you can use pip,
```bash
pip install pytube
```

### Googleapiclient
This is part of the Google API client library. To install it, you can use pip,
```bash
pip install google-api-python-client
```

## Obtaining API Credentials:
To interact with the Spotify and YouTube APIs, you need to obtain the necessary API credentials.
Here are the steps to get the credentials:

### Spotify API Credentials
1. Go to the Spotify Developer Dashboard: https://developer.spotify.com/dashboard/applications
2. Login or create a new Spotify account if you don't have one.
3. Click on the "Create an App" button.
4. Fill out the necessary information for your application (name, description, etc.).
5. Once your app is created, you'll see your Client ID and Client Secret. Keep these credentials safe, as they are used to authenticate your app with the Spotify API.

### YouTube API Key
1. Go to the Google Developers Console: https://console.developers.google.com/
2. Create a new project by clicking on the project dropdown and selecting "New Project."
3. Give your project a name and select the appropriate organization and billing account if prompted.
4. Once the project is created, go to "APIs & Services" > "Library" from the left-hand sidebar.
5. Search for "YouTube Data API v3" and click on it.
6. Click the "Enable" button to enable the API for your project.
7. After enabling the API, go to "APIs & Services" > "Credentials" from the left-hand sidebar.
8. Click on the "Create Credentials" button and select "API Key."
9. Your API key will be generated. Make sure to restrict the usage of the key to prevent unauthorized access. For example, you can restrict the key to only allow usage from your server's IP address.
10. Keep your YouTube API key safe and do not share it publicly.

## Important Note:
Remember to store these credentials securely and avoid sharing them in public repositories or websites, as they grant access to your respective developer accounts and data. Once you have obtained the Spotify API credentials and YouTube API key, you can use them in the script to make authenticated requests to these APIs.
