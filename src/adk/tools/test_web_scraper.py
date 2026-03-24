from web_scraper import read_webpage

def main():

    urls_to_test = [
        "https://www.gov.uk/child-benefit/eligibility",
        "https://www.gov.uk/child-benefit-child-lives-with-someone-else",
        "https://www.gov.uk/child-benefit-for-children-in-hospital-or-care",
        # A bad URL just to visually confirm the safety check works
        "https://www.wikipedia.org/wiki/Child_benefit" 
    ]

    print("=== GOV.UK Web Scraper Sanity Check ===")
    
    for url in urls_to_test:
        print(f"\n[TARGET]: {url}")
        
        # Call the tool exactly as the LLM would
        result = read_webpage(url)
        
        if "error" in result:
            print(f"❌ [BLOCKED/FAILED]: {result['error']}")
        else:
            content = result.get("content", "")
            print(f"✅ [SUCCESS]: Extracted {len(content)} characters.")
            print("-" * 60)
            print(content)
            print("-" * 60)
            input("Press any key to test the next page.")

if __name__ == "__main__":
    main()