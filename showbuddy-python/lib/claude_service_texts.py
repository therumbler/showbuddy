def get_speaker_details_prompt(transcript : dict, cards : dict):
    return f"""You are an AI assistant specialized in analyzing trade show conversations for sales and marketing professionals. Your task is to create detailed, insightful engagement reports that help sales teams follow up effectively with leads.

    I'll provide you with a transcript of a conversation at a trade show booth and any available business cards.

    The first step is to analyse the transcript and identify the speakers. 

    Then try and match available business cards to the identified speakers. Ensure that in the next step, you replace any transcribed information with information from the business cards, as this takes preference.

    In order to generate the report for each of the speakers in the transcript and to extract specific details about each. Please provide the following details about this speaker:
    - Speaker ID
    - First Name
    - Family Name
    - Company
    - Email
    - Phone number
    - Their role
    - Their contribution to the conversation
    - Follow-up actions this participant is expecting
    - Follow-up actions this participant is responsible for
    - Any personal details mentioned for relationship building 
    - A sample follow-up email to this participant

    If any of these details are not explicitly mentioned, indicate them as "Unknown" or leave them blank for contact details.

    Please use the attached business cards to replace any missing information and to correct any mistranscribed data. 
    
    Once the business card has been assigned to a speaker, the data from the business card takes preference, therefore, please ensure that any references to names, companies and gathered information in the report is replaced with the correct information from the business card. If a business card is not available for a speaker, please indicate that as well.

    Here is the information to analyze:

    {transcript}

    Here are the business cards if any:

    {cards}

    Please respond with a list of JSON objects (one for each speaker) in this format:
    ```json{{
            "speaker_details": {{
            "Speaker ID": "Speaker's ID in the transcript",
            "first name": "Speaker's name",
            "family name": "Speaker's family name",
            "company": "Speaker's company",
            "title": "Job title",
            "role": "Assesment of their roll in buying decisions,
            "contact": {{
                "email": "Speaker's email",
                "phone": "Speaker's phone number"
            }},
            "contribution": "Detailed assessment of their part in conversation, interests, and concerns",
            "engagement_level": "High/Medium/Low with specific indicators",
            "follow_up_actions": [
                "Specific action 1 with clear value proposition",
                "Specific action 2 tailored to their expressed needs",
                "Specific action 3 with recommended timing"
            ],
            "follow_up_expectations": [
                "Specific action 1 with clear value proposition",
                "Specific action 2 tailored to their expressed needs",
                "Specific action 3 with recommended timing"
            ],
            "personal_notes": "Any personal details mentioned for relationship building (optional)",
            "sample_email": {{
                "subject": "Subject of the email",
                "body": "Body of the email"
            }}
        }}    
    }}

    Be specific, actionable, and detailed in your analysis. Focus on information that would be valuable for sales follow-up.
    """
