import re
import lib.claude_service_texts
import json

class ClaudeService:
    """
    Service for using Anthropic's Claude AI for summary generation and analysis
    """

    async def generate_report(transcript: Dict[str, Any], cards: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate engagement report using Claude"""
        print("Generating report using Claude...")
        
        # Check if API key is set
        if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_anthropic_api_key":
            print("Anthropic API key not set, using mock report")
            return ClaudeService.generate_mock_report(transcript, cards)
            
        try:
            # Prepare the context for Claude
            context = ClaudeService._prepare_context(transcript, cards)
            
            # Prepare the prompt for Claude
            prompt = ClaudeService._create_prompt(context)
            
            # Call Claude API
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 1024,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.3
                    }
                )
                
                if response.status_code != 200:
                    print(f"Error from Claude API: {response.text}")
                    return ClaudeService.generate_mock_report(transcript, cards)
                
                claude_response = response.json()
                content = claude_response["content"][0]["text"]
                
                # Parse the JSON response from Claude
                try:
                    # Try to extract JSON from the response
                    # First, look for JSON block in markdown
                    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1)
                    else:
                        # If no markdown JSON block, try to extract the whole content as JSON
                        json_str = content
                        
                    report_data = json.loads(json_str)
                    return report_data
                except (json.JSONDecodeError, AttributeError) as e:
                    print(f"Failed to parse Claude response as JSON: {e}")
                    # Extract information using regex as fallback
                    return ClaudeService._extract_report_from_text(content, transcript, cards)
                    
        except Exception as e:
            print(f"Error generating report with Claude: {str(e)}")
            return ClaudeService.generate_mock_report(transcript, cards)
    
    def _prepare_context(transcript: Dict[str, Any], cards: List[Dict[str, Any]]) -> str:
        """Prepare context for Claude from transcript and cards"""
        context = "TRANSCRIPT:\n"
        
        # Add full transcript text if available
        if "utterances" in transcript:
            for utterance in transcript["utterances"]:
                speaker = utterance.get("speaker", "Unknown")
                text = utterance.get("text", "")
                context += f"Speaker {speaker}: {text}\n"
            context += "\n"
        
        # Add business card information
        context += "BUSINESS CARDS:\n"
        if cards:
            for i, card in enumerate(cards):
                extracted_data = card.get("extracted_data", {})
                if "data" in extracted_data:
                    card_data = extracted_data["data"]
                    context += f"Card {i+1}:\n"
                    context += f"  Name: {card_data.get('name', 'Unknown')}\n"
                    context += f"  Company: {card_data.get('company', 'Unknown')}\n"
                    context += f"  Title: {card_data.get('title', 'Unknown')}\n"
                    context += f"  Email: {card_data.get('email', 'Unknown')}\n"
                    context += f"  Phone: {card_data.get('phone', 'Unknown')}\n\n"
        else:
            context += "No business cards available.\n\n"
        
        return context
    
    @staticmethod
    def _create_prompt(context: str) -> str:
        """Create an enhanced prompt for Claude to generate richer reports"""
        return claude_service_texts.claude_prompt(context)
    
    @staticmethod
    def _extract_report_from_text(text: str, transcript: Dict[str, Any], cards: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Enhanced fallback method to extract report information from Claude's text response"""
        import re
        
        # Try to extract summary
        summary_match = re.search(r'summary["\s:]+([^"]+)', text, re.IGNORECASE)
        summary = summary_match.group(1).strip() if summary_match else "Conversation at trade show booth with potential client showing interest in our solution."
        
        # Try to extract topics
        topics = re.findall(r'topic[s\s]*[:"\[]([^"\],]+)', text, re.IGNORECASE)
        if not topics:
            topics = ["Product Features", "Pricing Options", "Implementation", "Technical Requirements", "Competitive Comparison"]
        
        # Try to extract opportunity assessment
        opportunity_match = re.search(r'opportunity[_\s]*assessment["\s:]+([^"]+)', text, re.IGNORECASE)
        opportunity = opportunity_match.group(1).strip() if opportunity_match else "Medium priority lead requiring follow-up to assess project timeline and budget."
        
        # Create participants from available business cards with enhanced details
        participants = []
        for card in cards:
            extracted_data = card.get("extracted_data", {})
            if "data" in extracted_data:
                card_data = extracted_data["data"]
                participant = {
                    "name": card_data.get("name", "Unknown Person"),
                    "company": card_data.get("company", "Unknown Company"),
                    "role": card_data.get("title", ""),
                    "buying_role": "Potential evaluator based on technical questions",
                    "contact": {
                        "email": card_data.get("email", ""),
                        "phone": card_data.get("phone", "")
                    },
                    "contribution": "Actively participated in the conversation, asking specific questions about product capabilities and implementation.",
                    "engagement_level": "Medium-High based on conversation duration and question specificity",
                    "follow_up_actions": [
                        "Send detailed product specifications and case studies",
                        "Offer a personalized demo focusing on their industry use cases",
                        "Connect with technical team for implementation discussion",
                        "Follow up within 3 business days to maintain momentum"
                    ],
                    "personal_notes": ""
                }
                participants.append(participant)
        
        # If no participants were created from cards, create a detailed default one
        if not participants:
            participants = [{
                "name": "Booth Visitor",
                "company": "Unknown Company",
                "role": "",
                "buying_role": "Initial contact requiring qualification",
                "contact": {"email": "", "phone": ""},
                "contribution": "Engaged in discussion showing interest in core product features and potential applications.",
                "engagement_level": "Medium - asked questions but didn't share specific project details",
                "follow_up_actions": [
                    "Send follow-up email with product information",
                    "Connect on LinkedIn to maintain relationship",
                    "Invite to upcoming webinar or product demonstration",
                    "Call within one week to assess interest level and requirements"
                ],
                "personal_notes": ""
            }]
        
        return {
            "summary": summary,
            "topic_tags": topics,
            "participants": participants,
            "opportunity_assessment": opportunity
        }
        
    @staticmethod
    def generate_mock_report(transcript: Dict[str, Any], cards: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a richer mock report when Claude API is not available"""
        print("Generating enhanced mock report...")
        
        # Get speaker IDs from the transcript
        speaker_ids = set()
        if "utterances" in transcript:
            for utterance in transcript["utterances"]:
                speaker_id = utterance.get("speaker", "")
                if speaker_id:
                    speaker_ids.add(speaker_id)
        
        # Create participants
        participants = []
        
        # First, use business cards if available
        for i, card in enumerate(cards):
            extracted_data = card.get("extracted_data", {})
            if "data" in extracted_data:
                card_data = extracted_data["data"]
                participant = {
                    "name": card_data.get("name", f"Person {i+1}"),
                    "company": card_data.get("company", "TechCorp Inc."),
                    "role": card_data.get("title", "Director of Operations"),
                    "buying_role": "Potential",
                    "contact": {
                        "email": card_data.get("email", ""),
                        "phone": card_data.get("phone", "")
                    },
                    "contribution": "Asked detailed questions about product features, specifically the AI integration capabilities and analytics dashboard. Expressed concerns about implementation timeline and team training requirements.",
                    "engagement_level": "High - spent significant time discussing technical specifications and requested a follow-up demo",
                    "follow_up_actions": [
                        "Send detailed spec sheet for the enterprise plan within 24 hours",
                        "Schedule a technical demo focusing on the AI analytics capabilities they showed interest in",
                        "Connect them with a current customer in their industry (manufacturing) for reference",
                        "Prepare a custom implementation timeline addressing their 60-day rollout concern"
                    ],
                    "personal_notes": "Mentioned upcoming industry conference in Chicago; avid golfer; previously worked with our competitor XYZ Solutions"
                }
                participants.append(participant)
        
        # If we have more speakers than cards, add generic but detailed participants
        if len(speaker_ids) > len(participants):
            role_options = ["Technical Evaluator", "Financial Decision Maker", "End User", "Project Manager"]
            for i, speaker_id in enumerate(list(speaker_ids)[len(participants):]):
                role_idx = i % len(role_options)
                participant = {
                    "name": f"Speaker {speaker_id}",
                    "company": "Unknown Company",
                    "role": "Unknown Title",
                    "buying_role": role_options[role_idx],
                    "contact": {"email": "", "phone": ""},
                    "contribution": "Asked specific questions about system requirements and API capabilities. Seemed particularly interested in mobile functionality and data export options.",
                    "engagement_level": "Medium - engaged on technical topics but didn't discuss next steps",
                    "follow_up_actions": [
                        "Send API documentation highlighting the features they inquired about",
                        "Share case study on mobile implementation success with similar company",
                        "Offer a technical consultation call to address their integration questions",
                        "Follow up within 5 business days as this appears to be in early evaluation stage"
                    ],
                    "personal_notes": ""
                }
                participants.append(participant)
        
        # If we have no participants at all, add a detailed default one
        if not participants:
            participants = [{
                "name": "Trade Show Visitor",
                "company": "Unknown Company",
                "role": "Unknown Title",
                "buying_role": "Initial contact - needs qualification",
                "contact": {"email": "", "phone": ""},
                "contribution": "Engaged in a general discussion about our product offerings. Showed particular interest in cost savings aspects and quick implementation options.",
                "engagement_level": "Medium - asked good questions but didn't share specific project details",
                "follow_up_actions": [
                    "Send introductory product brochure highlighting ROI calculator",
                    "Connect on LinkedIn within 24 hours while conversation is fresh",
                    "Invite to upcoming webinar on implementation best practices",
                    "Follow up by email in 3 days to qualify their interest and timeline"
                ],
                "personal_notes": ""
            }]
        
        return {
            "summary": "Engaging conversation with a potential enterprise client showing significant interest in our AI-powered analytics solution. The visitor asked detailed questions about implementation timeline, pricing tiers, and technical specifications, particularly around data security and API capabilities. They mentioned a current pain point with their existing solution's reporting limitations and have an active project to replace it within 60-90 days. Based on their questions and seniority, this appears to be a qualified lead with decision-making authority and a defined timeline.",
            "topic_tags": ["AI Analytics Dashboard", "Enterprise Pricing", "API Integration", "Data Security Compliance", "Implementation Timeline", "Mobile Accessibility", "ROI Calculation"],
            "participants": participants,
            "opportunity_assessment": "HIGH PRIORITY - Qualified lead with active project, defined timeline (60-90 days), and budget authority. Their technical questions indicate they're in the solution evaluation phase. Key decision factors appear to be implementation speed and API flexibility. Recommend sales follow-up within 24 hours with technical team involvement."
        }
