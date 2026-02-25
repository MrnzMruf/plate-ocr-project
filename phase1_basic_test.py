# phase1_basic_test.py
# Phase 1: Basic local API test (no queue yet)
# We sent image via multipart POST and checked JSON response with 'plaque' field
# Used to debug 405 errors and python-multipart issues

import requests

# Local API endpoint we were testing (generic name here)
API_URL = "http://localhost:5050/plaque"  # in real test: 192.168.1.162:5050/plaque

def test_upload_image(image_path):
    try:
        with open(image_path, "rb") as f:
            files = {"file": (image_path.split("/")[-1], f, "image/jpeg")}
            response = requests.post(API_URL, files=files, timeout=10)

        print(f"Status Code: {response.status_code}")
        print("Response:", response.text)

        if response.status_code == 200:
            data = response.json()
            print("Detected plate:", data.get("plaque", "Not found"))
        else:
            print("Error details:", response.reason)

    except Exception as e:
        print("Request failed:", str(e))


if __name__ == "__main__":
    # Replace with your test image path
    test_upload_image("sample_plate.jpg")
