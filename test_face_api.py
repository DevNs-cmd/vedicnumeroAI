import requests

# Test the face reading endpoint
url = "http://127.0.0.1:8000/api/face-read"
files = {'file': ('AI face.png', open('AI face.png', 'rb'), 'image/png')}

try:
    response = requests.post(url, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

