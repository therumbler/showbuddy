import re
import lib.claude_service_texts as claude_service_texts
import json
import httpx
import os
import logging
import asyncio


# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ClaudeService:
    """
    Service for using Anthropic's Claude AI for summary generation and analysis
    """

    def __init__(self, ANTHROPIC_API_KEY):
        self.api_key = ANTHROPIC_API_KEY

    async def prompt_claude(self, prompt):
        """Prompt Claude"""
        logger.info(f"Prompting Claude...")
        try:
            # Call Claude API
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 2048,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.3
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Error from Claude API: {response.text}")
                    return None
                
                claude_response = response.json()
                content = claude_response["content"][0]["text"]
                print (content)
                # Parse the JSON response from Claude
                try:
                    # Try to extract JSON from the response
                    # First, look for JSON block in markdown
                    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1)
                    else:
                        # If no markdown JSON block, try to extract the whole content as JSON
                        logger.warning("No JSON block found in Claude response, trying to parse the whole content as JSON.")
                        json_str = content
                        
                    report_data = json.loads(json_str)
                    return {"Report Data" : report_data}
                except (json.JSONDecodeError, AttributeError) as e:
                    logger.error(f"Failed to parse Claude response as JSON: {e}")
        except Exception as e:
            logger.error(f"Error generating report with Claude: {str(e)}")
            return None


    def extract_simple_transcript(self, transcript):
        """
        Extracts a simplified transcript from the detailed JSON transcript.
        The simplified transcript contains a list of utterances with speaker and text.
        """
        logger.info(f"Simplifying Transcript")
        try:
            simplified_transcript = []
            for utterance in transcript.get("utterances", []):
                simplified_transcript.append({
                "speaker": utterance.get("speaker", "unknown"),
                "text": utterance.get("text", "")
            })
            return {"Transcript:" : simplified_transcript}
        except Exception as e:
            logger.error(f"Error extracting simple transcript: {str(e)}")
            return []

    async def generate_report(self, session_id, transcript_file, card_file):
        """Generate a report using Claude"""
        logger.info(f"Generating Report")
        # Prepare the prompt

        transcript_bytes = await transcript_file.read()
        transcript = json.loads(transcript_bytes)

        cards_bytes = await card_file.read()
        cards = json.loads(cards_bytes)



        simplified_transcript = self.extract_simple_transcript(transcript)
        prompt = claude_service_texts.get_speaker_details_prompt(simplified_transcript, cards)

        report_data = await self.prompt_claude(prompt)
        
        
        # If the response is not valid, return an empty dictionary
        if not report_data:
            return {}
        
        # Process the report data
        report_data["session_id"] = session_id
        return report_data
    


async def main():
    logging.basicConfig(level=logging.INFO)
    api_key = os.environ["ANTHROPIC_API_KEY"]
    session_id = "your_session_id_here"
    
    transcript_path = "/Users/tsepomontsi/projects/showbuddy/showbuddy-data/transcripts/829fa7d4-d829-40b3-8fe5-ad44d4e5afb8.json"
    card_path = "/Users/tsepomontsi/projects/showbuddy/tests/integration/files/b_cards.json"
    analytics_service = ClaudeService(api_key)

    with open(transcript_path, "r") as transcript_file:
        transcript_text = transcript_file.read()
        transcript_dict = json.loads(transcript_text)
        with open (card_path, "r") as card_file:
            card_text = card_file.read()
            card_dict = json.loads(card_text)
        
            results = await analytics_service.generate_report(session_id, transcript_dict, card_dict)
        logger.info(results)


if __name__ == "__main__":
    asyncio.run(main())
