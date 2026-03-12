import re

def get_short_model_name(model_string: str) -> str:
    """
    Quick and dirty way to get a human-readable model name with no regex.
    So "bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0" -> "claude-sonnet-4-5"
    """
    base_name = model_string.split("/")[-1].split(".")[-1]
    clean_parts = []

    for part in base_name.split("-"):
        # Stop if we hit an 8-digit date (e.g., 20250929)
        if len(part) == 8 and part.isdigit():
            break

        # Stop if we hit a version tag (starts with 'v' followed by a number, e.g., v1:0)
        if part.startswith("v") and part[1:2].isdigit():
            break

        clean_parts.append(part)
    # Stitch it back together
    return "-".join(clean_parts)

def extract_prompt_version(prompt_name: str) -> str:
    match = re.search(r"v\d+(?:\.\d+)?", str(prompt_name))
    return match.group(0) if match else "v?"

def get_nice_prompt_name(prompt_string: str, prompt_mapping: dict) -> str:
    if not isinstance(prompt_string, str):
        return "Unknown"
    file_name = prompt_string.split("/")[-1]
    return (file_name, prompt_mapping.get(file_name, "Other Prompt"))
