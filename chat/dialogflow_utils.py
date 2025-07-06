import uuid
import os
from google.cloud import dialogflow_v2 as dialogflow
from django.conf import settings

def detect_intent_text(session_id: str, text: str, language_code: str = None):
    """
    Sends `text` to Dialogflow and returns the response text.
    session_id: a unique identifier per user/chat session; using chat.id or user.id is fine.
    """
    if language_code is None:
        language_code = settings.DIALOGFLOW_LANGUAGE_CODE

    project_id = settings.DIALOGFLOW_PROJECT_ID
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
    except Exception as e:
        # Log error appropriately
        raise

    # The reply text(s) from Dialogflow; typically first message
    if response.query_result.fulfillment_messages:
        # Depending on your Dialogflow setup, messages might have text fields:
        for msg in response.query_result.fulfillment_messages:
            if msg.text and msg.text.text:
                # return first non-empty
                return msg.text.text[0]
    # Fallback to plain text field:
    return response.query_result.fulfillment_text
