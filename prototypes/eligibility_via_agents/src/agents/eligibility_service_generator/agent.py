from dotenv import load_dotenv
from strands import Agent, tool
import requests
from bs4 import BeautifulSoup
from strands.models import BedrockModel
import os
from pathlib import Path
import shutil

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
        
        base_dir = Path(f"src/agents/{safe_service_name}")
        
        # Phase 1: Prompts
        if artifact_type == 1:
            target_dir = base_dir / "eligibility_checker"
            file_name = "system_prompt.md"
        elif artifact_type == 2:
            target_dir = base_dir / "implications_checker"
            file_name = "system_prompt.md"
            
        # Phase 1: A2A Agent Cards
        elif artifact_type == 3:
            target_dir = base_dir / "eligibility_checker"
            file_name = "agent.json"
        elif artifact_type == 4:
            target_dir = base_dir / "implications_checker"
            file_name = "agent.json"
                
        # Phase 3: Strands Python Implementations
        elif artifact_type == 5:
            target_dir = base_dir / "eligibility_checker"
            file_name = "agent.py"
        elif artifact_type == 6:
            target_dir = base_dir / "implications_checker"
            file_name = "agent.py"

        # Phase 3: Tests
        elif artifact_type == 7:
            target_dir = Path("tests/scenario")
            file_name = f"{safe_service_name}.py"
        elif artifact_type == 8:
            target_dir = Path("tests")
            file_name = f"test_{safe_service_name}.py"
        else:
            return f"Error: Invalid artifact_type {artifact_type}. Must be a number between 1 and 8"
            
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

def delete_service_artifacts(service_name: str) -> str:
    """Deletes all generated files and directories for a given eligibility service."""
    safe_service_name = service_name.lower().replace(" ", "_")
    
    # Define the 3 target paths
    service_agent_dir = Path(f"src/agents/{safe_service_name}")
    scenario_test_file = Path(f"tests/scenario/{safe_service_name}.py")
    pytest_file = Path(f"tests/test_{safe_service_name}.py")
    
    deleted_items = []
    
    # 1. Nuke the entire agent directory (prompts, cards, and strands agents)
    if service_agent_dir.exists() and service_agent_dir.is_dir():
        shutil.rmtree(service_agent_dir)
        deleted_items.append(f"Directory: {service_agent_dir}")
        
    # 2. Delete the scenario builder class
    if scenario_test_file.exists():
        scenario_test_file.unlink()
        deleted_items.append(f"File: {scenario_test_file}")
        
    # 3. Delete the Pytest suite
    if pytest_file.exists():
        pytest_file.unlink()
        deleted_items.append(f"File: {pytest_file}")
        
    if not deleted_items:
        return f"No artifacts found for '{service_name}' to delete. They may have already been removed."
        
    return f"Successfully aborted and cleaned up artifacts for '{service_name}':\n- " + "\n- ".join(deleted_items)
    
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
    print("🤖 Agent: Hello! I am your QA & Agent Generation Architect.")
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