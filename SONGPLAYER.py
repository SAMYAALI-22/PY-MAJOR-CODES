import cv2
import requests
from deepface import DeepFace
import matplotlib.pyplot as plt

def img_to_song(image_location,
                 api_url='https://open.spotify.com/track/0eCajpR75pDW0r64U6hP2x',
                 api_key="<b18477f8d1msh99ca1ea1e0921a3p102572jsn7c10c937a796>",
                 api_host="spotify81.p.rapidapi.com",
                 offset=0,
                 limit=10,
                 numberOfTopResults=5):
    # Read image
    img = cv2.imread("C:\\Users\\SAMYA ALI\\OneDrive\\Desktop\\sample.jpg")

    # Analyze the image for emotions
    result = DeepFace.analyze(img, actions=['emotion'])

    # Extract the emotion with the highest percentage
    query = str(max(zip(result[0]['emotion'].values(),
                         result[0]['emotion'].keys()))[1])

    # Prepare the request to the Spotify API
    querystring = {"q": f"{query}", "type": "multi",
                   "offset": str(offset), "limit": str(limit),
                   "numberOfTopResults": str(numberOfTopResults)}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }

    # Send the request
    response = requests.get(api_url, headers=headers, params=querystring)

    # Check for successful response
    if response.status_code == 200:
        output = []
        for i in range(min(limit, len(response.json()['tracks']))):
            output.append(f"""Song name: {response.json()['tracks'][i]['data']['name']}
Album name: {response.json()['tracks'][i]['data']['albumOfTrack']['name']}\n""")
        return output
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

if __name__ == "__main__":
    # Display the image
    loc = '("C:\\Users\\SAMYA ALI\\OneDrive\\Desktop\\sample.jpg")'  # Use your actual image path
    img = cv2.imread(loc)
    plt.imshow(img[:, :, ::-1])
    plt.axis('off')  # Hide axes
    plt.show()

    # Call the function
    api_key = "<b18477f8d1msh99ca1ea1e0921a3p102572jsn7c10c937a796>"  # Replace with your actual API key
    songs = img_to_song(loc, api_key=api_key)
    
    # Print results
    if songs:
        for song in songs:
            print(song)
    else:
        print("No songs found or there was an error.")
