#!/usr/bin/env python3
"""
Test script for the Child Benefit Eligibility Agent.

This script demonstrates how to interact with the agent and tests various scenarios.
"""

import asyncio
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from agent import root_agent


async def test_basic_flow():
    """Test a basic eligibility flow."""
    print("=" * 80)
    print("TEST: Basic Eligibility Flow")
    print("=" * 80)

    session_service = InMemorySessionService()
    session = session_service.create_session()

    # Start the conversation
    print("\n[User]: Am I eligible for Child Benefit?")
    response = await root_agent.send_message(
        "Am I eligible for Child Benefit?",
        session=session
    )
    print(f"[Agent]: {response.data.text}\n")

    # Follow-up based on questions asked
    print("[User]: My child is 14 years old")
    response = await root_agent.send_message(
        "My child is 14 years old",
        session=session
    )
    print(f"[Agent]: {response.data.text}\n")


async def test_edge_case_hospital():
    """Test hospital stay edge case."""
    print("=" * 80)
    print("TEST: Hospital Stay Edge Case")
    print("=" * 80)

    session_service = InMemorySessionService()
    session = session_service.create_session()

    print("\n[User]: Can I still claim if my child has been in hospital for 10 weeks?")
    response = await root_agent.send_message(
        "Can I still claim if my child has been in hospital for 10 weeks?",
        session=session
    )
    print(f"[Agent]: {response.data.text}\n")


async def test_education_requirement():
    """Test education requirements for 16-19 year olds."""
    print("=" * 80)
    print("TEST: Education Requirements (16-19 year olds)")
    print("=" * 80)

    session_service = InMemorySessionService()
    session = session_service.create_session()

    print("\n[User]: My 17-year-old is doing A-levels. Can I claim Child Benefit?")
    response = await root_agent.send_message(
        "My 17-year-old is doing A-levels. Can I claim Child Benefit?",
        session=session
    )
    print(f"[Agent]: {response.data.text}\n")


async def test_residency_requirements():
    """Test residency requirements."""
    print("=" * 80)
    print("TEST: Residency Requirements")
    print("=" * 80)

    session_service = InMemorySessionService()
    session = session_service.create_session()

    print("\n[User]: I have pre-settled status. What do I need to qualify for Child Benefit?")
    response = await root_agent.send_message(
        "I have pre-settled status. What do I need to qualify for Child Benefit?",
        session=session
    )
    print(f"[Agent]: {response.data.text}\n")


async def test_constants_query():
    """Test querying constants from the specification."""
    print("=" * 80)
    print("TEST: Constants Query")
    print("=" * 80)

    session_service = InMemorySessionService()
    session = session_service.create_session()

    print("\n[User]: What is the maximum age for Child Benefit?")
    response = await root_agent.send_message(
        "What is the maximum age for Child Benefit?",
        session=session
    )
    print(f"[Agent]: {response.data.text}\n")


async def test_specification_info():
    """Test getting specification metadata."""
    print("=" * 80)
    print("TEST: Specification Information")
    print("=" * 80)

    session_service = InMemorySessionService()
    session = session_service.create_session()

    print("\n[User]: What version of the eligibility rules are you using?")
    response = await root_agent.send_message(
        "What version of the eligibility rules are you using?",
        session=session
    )
    print(f"[Agent]: {response.data.text}\n")


async def interactive_mode():
    """Run in interactive mode for manual testing."""
    print("=" * 80)
    print("INTERACTIVE MODE - Child Benefit Eligibility Agent")
    print("=" * 80)
    print("Type 'quit' or 'exit' to end the session")
    print()

    session_service = InMemorySessionService()
    session = session_service.create_session()

    while True:
        try:
            user_input = input("[You]: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            response = await root_agent.send_message(
                user_input,
                session=session
            )
            print(f"[Agent]: {response.data.text}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"[Error]: {e}\n")


async def main():
    """Run all tests."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        await interactive_mode()
    else:
        # Run automated tests
        await test_basic_flow()
        await test_edge_case_hospital()
        await test_education_requirement()
        await test_residency_requirements()
        await test_constants_query()
        await test_specification_info()

        print("=" * 80)
        print("All tests completed!")
        print("=" * 80)
        print("\nRun with 'python test_agent.py interactive' for interactive mode")


if __name__ == "__main__":
    asyncio.run(main())
