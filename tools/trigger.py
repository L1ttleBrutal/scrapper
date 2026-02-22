import scraper
import analyzer
import time
from datetime import datetime
import os

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), '..', 'progress.md')

def orchestrate():
    msg = f"\n--- Pipeline Triggered: {datetime.now().isoformat()} ---"
    try:
        with open(PROGRESS_FILE, 'a') as f:
            f.write(msg)
    except:
        pass
    print(msg)
    
    print("1. Running Scraper...")
    success = scraper.fetch_data()
    if success:
        print("2. Running Analyzer...")
        analyzer.analyze()
        print("Pipeline execution complete.")
    else:
        print("Pipeline aborted due to scraper failure.")

if __name__ == "__main__":
    orchestrate()
