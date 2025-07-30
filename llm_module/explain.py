import subprocess
import json
from django.template.loader import render_to_string

# Path to your resume_summary.txt template (ensure this file exists in your templates folder)
TEMPLATE_PATH = 'llm_module/prompts/resume_summary.txt'

def call_ollama_with_prompt(prompt: str, model='mistral', temperature=0.4) -> str:
    """
    Sends a prompt to the Ollama LLM running Mistral and returns the response.
    """
    try:
        result = subprocess.run(
            [
                'ollama', 'run', model,
                '--temperature', str(temperature),
                '--prompt', prompt
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error during Ollama call:", e.stderr)
        return "LLM processing failed."


def explain_resume_with_llm(resume_text: str, job_roles: list[str]) -> list[dict]:
    """
    Builds a prompt using the resume text and job roles, sends it to the LLM, and parses recommendations.
    """
    job_roles_text = "\n".join(job_roles[:100])  # Avoid overloading tokens

    # Load and render the template
    prompt = render_to_string(TEMPLATE_PATH, {
        'resume_text': resume_text,
        'job_roles': job_roles_text
    })

    # Get response from LLM
    response = call_ollama_with_prompt(prompt)

    try:
        recommendations = json.loads(response)
    except json.JSONDecodeError:
        print("LLM response not in valid JSON format.")
        recommendations = [{"job_title": "No result", "reason": response}]

    return recommendations
