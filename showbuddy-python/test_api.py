#!/usr/bin/env python3
"""
Test script for ShowBuddy API endpoints
"""

import asyncio
import logging
import json
import os
import sys
from pathlib import Path
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Base URL - adjust if needed
API_BASE_URL = "http://localhost:8000"

# Test data paths
TEST_FILES_DIR = Path("../tests/integration/files")
BUSINESS_CARD_PATH = TEST_FILES_DIR / "business_card_tsepo_monatea.png"
AUDIO_FILE_PATH = TEST_FILES_DIR / "dialog.m4a"

async def test_api():
    """Run tests for all API endpoints"""
    missing_key_count = 0
    
    # Check for environment variables
    if not os.environ.get("SPREADLY_API_KEY"):
        logger.warning("⚠️ SPREADLY_API_KEY not set. Card tests will fail.")
        missing_key_count += 1
        
    if not os.environ.get("ASSEMBLYAI_API_KEY"):
        logger.warning("⚠️ ASSEMBLYAI_API_KEY not set. Transcription tests will fail.")
        missing_key_count += 1
        
    if not os.environ.get("ANTHROPIC_API_KEY"):
        logger.warning("⚠️ ANTHROPIC_API_KEY not set. Analysis tests will fail.")
        missing_key_count += 1
    
    if missing_key_count > 0:
        logger.warning(f"⚠️ {missing_key_count} API key(s) missing. Some tests will fail.")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Test 1: Check API is running
        logger.info("Test 1: Checking if API is running...")
        try:
            response = await client.get(f"{API_BASE_URL}/")
            if response.status_code == 200:
                logger.info("✅ API is running")
                logger.info(f"Response: {response.json()}")
            else:
                logger.error(f"❌ API check failed: {response.status_code}")
                return
        except Exception as e:
            logger.error(f"❌ API check failed: {e}")
            logger.error("Is the API server running? Start with 'make run-local'")
            return

        # Test 2: Create a new session
        logger.info("\nTest 2: Creating a new session...")
        try:
            response = await client.post(f"{API_BASE_URL}/api/sessions")
            if response.status_code == 200:
                session_data = response.json()
                session_id = session_data.get("session_id")
                if session_id:
                    logger.info(f"✅ Session created: {session_id}")
                else:
                    logger.error("❌ No session_id in response")
                    return
            else:
                logger.error(f"❌ Session creation failed: {response.status_code}")
                return
        except Exception as e:
            logger.error(f"❌ Session creation failed: {e}")
            return

        # Test 3: Upload a business card
        logger.info(f"\nTest 3: Uploading business card for session {session_id}...")
        try:
            if not BUSINESS_CARD_PATH.exists():
                logger.error(f"❌ Business card file not found: {BUSINESS_CARD_PATH}")
                return
                
            with open(BUSINESS_CARD_PATH, "rb") as f:
                card_image = f.read()
                
            files = {"image_file": ("business_card.png", card_image, "image/png")}
            response = await client.post(
                f"{API_BASE_URL}/api/sessions/{session_id}/cards",
                files=files
            )
            
            if response.status_code == 200:
                logger.info("✅ Business card uploaded successfully")
                logger.info(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                logger.error(f"❌ Business card upload failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"❌ Business card upload failed: {e}")

        # Test 4: Get cards for the session
        logger.info(f"\nTest 4: Getting cards for session {session_id}...")
        try:
            response = await client.get(f"{API_BASE_URL}/api/sessions/{session_id}/cards")
            if response.status_code == 200:
                cards_data = response.json()
                logger.info("✅ Cards retrieved successfully")
                logger.info(f"Response: {json.dumps(cards_data, indent=2)}")
            else:
                logger.error(f"❌ Get cards failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"❌ Get cards failed: {e}")

        # Test 5: Upload audio for transcription
        logger.info(f"\nTest 5: Uploading audio for session {session_id}...")
        try:
            if not AUDIO_FILE_PATH.exists():
                logger.error(f"❌ Audio file not found: {AUDIO_FILE_PATH}")
                return
                
            with open(AUDIO_FILE_PATH, "rb") as f:
                audio_data = f.read()
                
            files = {"audio_file": ("dialog.m4a", audio_data, "audio/m4a")}
            response = await client.post(
                f"{API_BASE_URL}/api/sessions/{session_id}/audio",
                files=files
            )
            
            if response.status_code == 200:
                logger.info("✅ Audio uploaded and transcribed successfully")
                logger.info("Response: (truncated due to size)")
            else:
                logger.error(f"❌ Audio transcription failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"❌ Audio transcription failed: {e}")

        # Test 6: Get transcript for the session
        logger.info(f"\nTest 6: Getting transcript for session {session_id}...")
        try:
            response = await client.get(f"{API_BASE_URL}/api/sessions/{session_id}/transcript")
            if response.status_code == 200:
                transcript_data = response.json()
                logger.info("✅ Transcript retrieved successfully")
                logger.info("Response: (truncated due to size)")
            else:
                logger.error(f"❌ Get transcript failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"❌ Get transcript failed: {e}")

        # Test 7: Run analysis
        logger.info(f"\nTest 7: Running analysis for session {session_id}...")
        try:
            response = await client.post(f"{API_BASE_URL}/api/sessions/{session_id}/analysis")
            if response.status_code == 200:
                analysis_data = response.json()
                logger.info("✅ Analysis completed successfully")
                logger.info(f"Response: {json.dumps(analysis_data, indent=2)}")
            else:
                logger.error(f"❌ Analysis failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")

        # Test 8: Get report
        logger.info(f"\nTest 8: Getting report for session {session_id}...")
        try:
            response = await client.get(f"{API_BASE_URL}/api/sessions/{session_id}/report")
            if response.status_code == 200:
                report_data = response.json()
                logger.info("✅ Report retrieved successfully")
                logger.info(f"Response: {json.dumps(report_data, indent=2)}")
            else:
                logger.error(f"❌ Get report failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except Exception as e:
            logger.error(f"❌ Get report failed: {e}")

        logger.info("\n✅ All API tests completed")

if __name__ == "__main__":
    # Make the script executable
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(f"Usage: python {sys.argv[0]}")
        print("  Tests the ShowBuddy API endpoints")
        print("\nEnvironment variables required:")
        print("  SPREADLY_API_KEY - For business card scanning")
        print("  ASSEMBLYAI_API_KEY - For audio transcription")
        print("  ANTHROPIC_API_KEY - For report generation")
        sys.exit(0)
        
    # Run the tests
    asyncio.run(test_api())