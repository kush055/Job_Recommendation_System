import ollama

def generate_response(prompt: str, model: str = "mistral") -> str:
    """
    Sends a prompt to the Ollama server using the specified LLM model and returns the response.

    Args:
        prompt (str): The prompt/question to send to the LLM.
        model (str): The name of the model to use (default is 'mistral').

    Returns:
        str: The LLM-generated response text.
    """
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"[LLM Error] {str(e)}"
