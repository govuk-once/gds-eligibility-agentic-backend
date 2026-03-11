from dotenv import load_dotenv
from strands import Agent, tool
import requests
from bs4 import BeautifulSoup
from strands.models import BedrockModel
import os
from pathlib import Path

load_dotenv()

@tool
def fetch_eligibility_criteria(url: str) -> str:
    """
    Fetches and extracts the text content from the provided UK Gov criteria URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract main content area (standard for gov.uk)
        content = soup.find('main', id='content')
        return content.get_text(separator='\n', strip=True) if content else soup.get_text(separator='\n', strip=True)
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

@tool    
def save_artifact_to_file(service_name: str, artifact_type: int, file_content: str, append: bool = False) -> str:
    """
    Saves the generated artifact code to the strictly defined project directories.
    Overwrites the file if it already exists during iterative refinement.
    
    Args:
        service_name: The snake_case name of the eligibility service (e.g., 'skilled_worker_visa').
        artifact_type: The integer ID of the artifact (1 for Tool Logic, 2 for Scenario, 3 for Pytest Suite).
        file_content: The raw Python code to be saved.
        append: If True, appends to the existing file instead of overwriting. Crucial for chunking large files.
    """
    try:
        # Sanitize service name to be safe for filenames
        safe_service_name = service_name.lower().replace(" ", "_").replace("-", "_")
        
        # Route to the exact directories requested
        if artifact_type == 1:
            target_dir = Path(f"src/mcp_server/tools/{safe_service_name}")
            file_name = "eligibility_checker.py"
        elif artifact_type == 2:
            target_dir = Path("tests/scenario")
            file_name = f"{safe_service_name}.py"
        elif artifact_type == 3:
            target_dir = Path("tests")
            file_name = f"test_{safe_service_name}.py"
        else:
            return f"Error: Invalid artifact_type {artifact_type}. Must be 1, 2, or 3."
            
        # Create directories if they don't exist
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / file_name

        mode = "a" if append else "w"
        
        # Write the file (overwrites existing files on refinement passes)
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(file_content)
            
        return f"Success: Saved Artifact {artifact_type} to {file_path}"
    except Exception as e:
        return f"Error saving file: {str(e)}"
    
@tool
def delete_service_artifacts(service_name: str) -> str:
    """
    Deletes all generated artifact files for a specific eligibility service.
    Use this if the user wants to abandon or cancel the codification process.
    
    Args:
        service_name: The snake_case name of the eligibility service (e.g., 'skilled_worker_visa').
    """
    try:
        # Sanitize service name to match the save tool logic
        safe_service_name = service_name.lower().replace(" ", "_").replace("-", "_")
        
        # Define the exact file paths
        paths_to_delete = [
            Path("src/mcp_server/tools") / f"{safe_service_name}.py",
            Path("tests/scenario") / f"{safe_service_name}.py",
            Path("tests") / f"test_{safe_service_name}.py"
        ]
        
        deleted_files: list[str] = []
        for file_path in paths_to_delete:
            if file_path.exists():
                file_path.unlink()
                deleted_files.append(str(file_path))
                
        if deleted_files:
            return f"Success: Deleted the following files:\n" + "\n".join(deleted_files)
        else:
            return f"No files found to delete for service '{service_name}'."
            
    except Exception as e:
        return f"Error deleting files: {str(e)}"
    
def load_system_prompt() -> str:
    """Reads the system prompt from a markdown file."""

    filepath: str = "src/agents/eligibility_service_generator/system_prompt.md"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: {filepath} not found. Please create it in the same directory.")
        exit(1)

# 2. Initialize the Strands Agent
code_generator_agent = Agent(
    model=BedrockModel(
        model_id=os.getenv("ELIGIBILITY_GENERATOR_AGENT_AWS_BEDROCK_MODEL_ID", ""),
        region_name="eu-west-2"
    ),
    tools=[
        fetch_eligibility_criteria, 
        save_artifact_to_file,
        delete_service_artifacts
    ],
    system_prompt=load_system_prompt()
)

# 4. The Interactive Generation Loop
if __name__ == "__main__":
    print("🤖 Agent: Hello! I am your QA & Code Generation Architect.")
    print("🤖 Agent: Please provide the URL for the eligibility criteria you want to convert, and we'll start Phase 1.")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'stop']:
                print("\n🤖 Agent: Shutting down generator. Goodbye!")
                break
                
            response = code_generator_agent(user_input)
            print(f"\n🤖 Agent:\n{response}")
            
        except KeyboardInterrupt:
            print("\n🤖 Agent: Process interrupted. Goodbye!")
            break