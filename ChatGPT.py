import requests

def send_message_to_gpt(message, api_key):
    """
    Send a message object to OpenAI's GPT-4 API endpoint.
    
    Parameters:
    message (dict): A dictionary containing the message data.
    api_key (str): Your OpenAI API key.
    
    Returns:
    response (requests.Response): The response from the API call.
    """
    api_url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-4",
        "messages": [message]
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    return response

# Example usage:
if __name__ == "__main__":
    api_key = "your_openai_api_key_here"
    message = {
        "role": "user",
        "content": "Hello, GPT-4!"
    }
    
    response = send_message_to_gpt(message, api_key)
    
    if response.status_code == 200:
        print("Response from GPT-4:", response.json())
    else:
        print("Error:", response.status_code, response.text)
