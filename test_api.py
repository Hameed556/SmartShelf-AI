import requests
import os

def test_api():
    url = "http://127.0.0.1:8000/verify"
    
    # Check if we have a test image
    test_image_path = "test_image.jpg"
    
    if not os.path.exists(test_image_path):
        print("No test image found. Please:")
        print("1. Place a test image named 'test_image.jpg' in this directory")
        print("2. Or use the Swagger UI at http://127.0.0.1:8000/docs")
        return
    
    # Prepare the form data
    files = {
        'image': ('test_image.jpg', open(test_image_path, 'rb'), 'image/jpeg')
    }
    
    data = {
        'expected_expiry': '12/2025',
        'product_category': 'food'
    }
    
    try:
        print("Testing API endpoint...")
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Test Successful!")
            print("Response:")
            print(f"  Extracted Expiry: {result.get('extracted_expiry')}")
            print(f"  Expiry Match: {result.get('expiry_match')}")
            print(f"  Image Classification: {result.get('image_classification')}")
            print(f"  Is Duplicate: {result.get('is_duplicate')}")
            print(f"  Confidence Score: {result.get('confidence_score')}")
            print(f"  Decision: {result.get('decision')}")
            print(f"  Rationale: {result.get('rationale')}")
        else:
            print(f"❌ API Test Failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        print("\nMake sure your server is running with:")
        print("cd near_expiry_platform/app && uvicorn main:app --reload")

if __name__ == "__main__":
    test_api() 