import os

CHATBASE_API_KEY = "vfrjmha5mhvovc4hi793ii5meo1m8g2m"
CHATBASE_CHATBOT_ID = "i_fFtvM3aNyCVCBrW0dyj"
# Optionally set defaults or raise if missing:
# if not CHATBASE_API_KEY or not CHATBASE_CHATBOT_ID:
#     raise RuntimeError("CHATBASE_API_KEY and CHATBASE_CHATBOT_ID must be set")

import uuid
import requests
from django.conf import settings

CHAT_ENDPOINT = "https://www.chatbase.co/api/v1/chat"

class ChatbaseError(Exception):
    pass

def call_chatbase(messages, conversation_id=None, stream=False, temperature=0.0, model=None):
    """
    Send messages array to Chatbase and return the response JSON.
    
    Args:
      messages: list of {"role": "user" or "assistant", "content": str}
      conversation_id: str or None. If None, a new UUID is generated.
      stream: bool — whether to request streaming response.
      temperature: float — sampling temperature.
      model: str or None — override model set in Chatbase dashboard.
    
    Returns:
      dict: parsed JSON response from Chatbase, e.g., {"text": "..."} or streamed chunks if streaming.
    
    Raises:
      ChatbaseError on non-200 or parse errors.
    """
    api_key = CHATBASE_API_KEY
    chatbot_id = CHATBASE_CHATBOT_ID
    print(conversation_id)
    if conversation_id is None:
        # Generate a new unique conversation ID
        conversation_id = str(uuid.uuid4())

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "messages": messages,
        "chatbotId": chatbot_id,
        "conversationId": conversation_id,
        "stream": stream,
        "temperature": temperature,
    }
    if model:
        body["model"] = model

    resp = requests.post(CHAT_ENDPOINT, headers=headers, json=body)

    if not resp.ok:
        # Try to get error message from JSON
        try:
            err = resp.json().get("message", resp.text)
        except ValueError:
            err = resp.text
        raise ChatbaseError(f"Chatbase API error: {resp.status_code}: {err}")

    # For non-streaming, Chatbase returns JSON with e.g., {"text": "..."}
    print(conversation_id)
    return {
        "conversation_id": conversation_id,
        "response": resp.json()['text']
    }

def get_chatbase_conversations(
    conversation_id,
    start_date=None,
    end_date=None,
    page=1,
    size=10,
    filtered_sources=None
):
    """
    Fetch conversations from Chatbase for the configured chatbot.

    Args:
      start_date (str or datetime.date, optional): “YYYY-MM-DD” format or date object.
      end_date (str or datetime.date, optional): “YYYY-MM-DD” format or date object.
      page (int, optional): Page number for pagination (default 1).
      size (int, optional): Number of items per page (max 100; default 10).
      filtered_sources (list[str] or None): List of sources to filter, e.g. ["API","WhatsApp"].

    Returns:
      dict: Parsed JSON response containing “data” array of conversations.
    
    Raises:
      ChatbaseError: on non-200 responses or invalid parameters.
    """
    api_key = CHATBASE_API_KEY
    chatbot_id = CHATBASE_CHATBOT_ID
    if not api_key or not chatbot_id:
        raise ChatbaseError("CHATBASE_API_KEY and CHATBASE_CHATBOT_ID must be set")
    
    url = "https://www.chatbase.co/api/v1/get-conversations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
    }

    params = {"chatbotId": chatbot_id, "page": str(page), "size": str(size)}
    # Validate and format dates
    def fmt_date(d):
        if isinstance(d, str):
            # Expect "YYYY-MM-DD"
            try:
                datetime.strptime(d, "%Y-%m-%d")
            except ValueError:
                raise ChatbaseError(f"Invalid date format: {d}. Expected YYYY-MM-DD.")
            return d
        elif hasattr(d, "strftime"):
            return d.strftime("%Y-%m-%d")
        else:
            raise ChatbaseError(f"Invalid date type: {d!r}.")
    if start_date:
        params["startDate"] = fmt_date(start_date)
    if end_date:
        params["endDate"] = fmt_date(end_date)
    if filtered_sources:
        if not isinstance(filtered_sources, (list, tuple)):
            raise ChatbaseError("filtered_sources must be a list of strings")
        # Join with commas, e.g., "API,WhatsApp"
        params["filteredSources"] = ",".join(filtered_sources)

    resp = requests.get(url, headers=headers, params=params, timeout=10)
    res = []
    for data in resp.json()['data']:
        if data['id'] == conversation_id:
            res.append(data)
    if resp.status_code != 200:
        try:
            err = resp.json().get("message", resp.text)
        except ValueError:
            err = resp.text
        raise ChatbaseError(f"Chatbase get-conversations error {resp.status_code}: {err}")
    # Expected response: {"data": [ { "id":..., "created_at":..., "messages":[...], ... }, ... ] }
    return res