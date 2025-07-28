import requests
import os

def test_google_vision():
    """Test if Google Vision is working"""
    
    # Test image path (you'll need to provide a real image)
    image_path = "test_image.png"  # Replace with your actual image
    
    if not os.path.exists(image_path):
        print("❌ Test image not found. Please provide a test image named 'test_image.png'")
        return
    
    url = "http://127.0.0.1:8000/verify"
    
    with open(image_path, "rb") as f:
        files = {"image": f}
        data = {
            "expected_expiry": "01/2025",
            "product_category": "food"
        }
        
        print("🚀 Testing Google Vision API...")
        print("📤 Sending request to:", url)
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response:")
            print(f"   OCR Text: {result.get('ocr_text', 'N/A')}")
            print(f"   Extracted Expiry: {result.get('extracted_expiry', 'N/A')}")
            print(f"   Note: {result.get('note', 'N/A')}")
            print(f"   Confidence Score: {result.get('confidence_score', 'N/A')}")
            
            # Check if Google Vision is being used
            if "Google Vision" in result.get('note', ''):
                print("🎉 Google Vision is ACTIVE!")
            else:
                print("⚠️  Google Vision may not be active")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    test_google_vision() 