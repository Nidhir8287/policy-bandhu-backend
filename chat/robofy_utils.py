import os

ACCOUNT_ID = "mj7sfsk/YesG/rZjbBvBlg=="
WEBSITE_ID = "zluvggo0UQUqVL9PmNjsUw=="
api_key = "3214fc1ff0dd444a8cc3e608c34eab63"
# Optionally set defaults or raise if missing:
# if not CHATBASE_API_KEY or not CHATBASE_CHATBOT_ID:
#     raise RuntimeError("CHATBASE_API_KEY and CHATBASE_CHATBOT_ID must be set")

import uuid
import requests
from django.conf import settings

CHAT_ENDPOINT = "https://3ipk7r0ux8.execute-api.us-west-2.amazonaws.com/Prod"

class RobofyError(Exception):
    pass

def call_robofy(messages, SessionId=""):
    """
    Send messages array to Robofy and return the response JSON.
    
    Args:
      messages: list of {"role": "user" or "assistant", "content": str}
      SessionId: str or None. If None, a new UUID is generated.
      stream: bool — whether to request streaming response.
      temperature: float — sampling temperature.
      model: str or None — override model set in Robofy dashboard.
    
    Returns:
      dict: parsed JSON response from Robofy, e.g., {"text": "..."} or streamed chunks if streaming.
    
    Raises:
      RobofyError on non-200 or parse errors.
    """
    account_id = ACCOUNT_ID
    website_id = WEBSITE_ID

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "AccountId": account_id,
        "QuestionQuery": messages,
        "SessionId": SessionId,
        "SourceMode": "0",
        "URL": "https://policybandhu.info",
        "WebsiteId": website_id,
    }

    resp = requests.post(CHAT_ENDPOINT, headers=headers, json=body)
    if not resp.ok:
        # Try to get error message from JSON
        try:
            err = resp.json().get("message", resp.text)
        except ValueError:
            err = resp.text
        raise RobofyError(f"Robofy API error: {resp.status_code}: {err}")

    # For non-streaming, Robofy returns JSON with e.g., {"text": "..."}
    return {
        "SessionId": resp.json()['Data']['SessionId'],
        "response": resp.json()['Data']['BotAnswer']
    }

def get_robofy_conversations(
    SessionId,
    start_date=None,
    end_date=None,
    page=1,
    size=10,
    filtered_sources=None
):
    """
    Fetch conversations from Robofy for the configured chatbot.

    Args:
      start_date (str or datetime.date, optional): “YYYY-MM-DD” format or date object.
      end_date (str or datetime.date, optional): “YYYY-MM-DD” format or date object.
      page (int, optional): Page number for pagination (default 1).
      size (int, optional): Number of items per page (max 100; default 10).
      filtered_sources (list[str] or None): List of sources to filter, e.g. ["API","WhatsApp"].

    Returns:
      dict: Parsed JSON response containing “data” array of conversations.
    
    Raises:
      RobofyError: on non-200 responses or invalid parameters.
    """
    account_id = ACCOUNT_ID
    website_id = WEBSITE_ID
    if not api_key or not chatbot_id:
        raise RobofyError("CHATBASE_API_KEY and CHATBASE_CHATBOT_ID must be set")
    
    url = CHAT_ENDPOINT
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
                raise RobofyError(f"Invalid date format: {d}. Expected YYYY-MM-DD.")
            return d
        elif hasattr(d, "strftime"):
            return d.strftime("%Y-%m-%d")
        else:
            raise RobofyError(f"Invalid date type: {d!r}.")
    if start_date:
        params["startDate"] = fmt_date(start_date)
    if end_date:
        params["endDate"] = fmt_date(end_date)
    if filtered_sources:
        if not isinstance(filtered_sources, (list, tuple)):
            raise RobofyError("filtered_sources must be a list of strings")
        # Join with commas, e.g., "API,WhatsApp"
        params["filteredSources"] = ",".join(filtered_sources)

    resp = requests.get(url, headers=headers, params=params, timeout=10)
    res = []
    for data in resp.json()['data']:
        if data['id'] == SessionId:
            res.append(data)
    if resp.status_code != 200:
        try:
            err = resp.json().get("message", resp.text)
        except ValueError:
            err = resp.text
        raise RobofyError(f"Robofy get-conversations error {resp.status_code}: {err}")
    # Expected response: {"data": [ { "id":..., "created_at":..., "messages":[...], ... }, ... ] }
    return res