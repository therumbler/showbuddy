import httpx
import logging
import asyncio
import os


from datetime import datetime
logger = logging.getLogger(__name__)    
class SpreadlyService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def upload_card(self, session_id: str, image_path: str):
        """Upload a business card image"""

        # Process card in background
        # asyncio.run(self._process_card(session_id, image_path))
        task = await asyncio.create_task(self._process_card(session_id, image_path))
        return {"status": "card_uploaded", "file_path": image_path}

    async def _process_card(self, session_id: str, image_path: str):
        """Process business card using Spreadly.io"""
        print(f"Processing card for session {session_id}...")
        
        try:
            # Make API request to Spreadly.io
            # Set headers with Bearer token and Content-Type
            headers = {
                'Authorization': f'Bearer {self.api_key}',
            }

            if not os.path.exists(image_path):
                print(f"Error: File {image_path} does not exist.")
                return

            try:
                files = {
                    'front': ('image.png', open(image_path, 'rb')),
                }
            except Exception as e:
                print(f"Error opening file {image_path}: {str(e)}")
                return

            # Make the POST request with requests
            async with httpx.AsyncClient() as client:
                response = await client.post('https://spreadly.app/api/v1/business-card-scans', headers=headers, files=files)
            
            if response.status_code != 200:
                print(f"Card processing failed: {response.text}")
                return
            
            try:
                card_data = response.json()
            except ValueError:
                print(f"Card processing failed: Invalid JSON response")
                return
            
            file_creation_time = datetime.fromtimestamp(os.stat(image_path).st_mtime).isoformat()
            card_data["reseponse_type"] = "card_data"
            card_data["file_creation_time"] = file_creation_time
            card_data["image_path"] = image_path
            card_data["session_id"] = session_id
            
            print(f"Card processing completed for session {session_id}")
            logger.info("Retrieved card data: %r", card_data)
            return card_data

            
        except Exception as e:
            logger.exception(f"Error processing card: {str(e)}")

async def main():
    session_id = "your_session_id_here"
    image_path0 = "/Users/tsepomontsi/scratch/showbuddy/tests/integration/files/business_card_0.png"
    image_path1 = "/Users/tsepomontsi/scratch/showbuddy/tests/integration/files/business_card_1.png"
  
    spreadly_service = SpreadlyService(api_key=api_key)
    
    await spreadly_service.upload_card(session_id, image_path0)
    await spreadly_service.upload_card(session_id, image_path1)

if __name__ == "__main__":
    asyncio.run(main())
