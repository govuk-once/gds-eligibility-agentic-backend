import pytest
import subprocess
import time
import httpx

@pytest.fixture(scope="session", autouse=True)
def start_registry_server():
    """Boots the global Agent Registry server before any tests run."""
    print("\n[conftest] Starting Registry Server on port 7999...")
    process = subprocess.Popen(["python", "src/agents/eligibility_orchestrator/registry.py"])
    
    # Poll the server until it's ready (timeout after 10 seconds)
    for _ in range(10):
        try:
            response = httpx.get("http://localhost:7999/catalog")
            if response.status_code == 200:
                print("[conftest] Registry Server is up!")
                break
        except httpx.RequestError:
            time.sleep(1)
    else:
        process.terminate()
        raise RuntimeError("Registry server failed to start in time.")
        
    yield  # Hand control over to the Pytest suite
    
    # Teardown: Kill the server when all tests are done
    print("\n[conftest] Shutting down Registry Server...")
    process.terminate()
    process.wait()