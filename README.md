# 🧠 Apache Jira Web Scraper & LLM Corpus Builder

This project builds a **data scraping and transformation pipeline** that extracts public issue data from **Apache’s Jira** instance and converts it into a **clean JSONL corpus** suitable for **Large Language Model (LLM) training**.

---

## 🚀 Overview

The system scrapes issue metadata, descriptions, and comments from selected Apache projects (e.g., `HADOOP`, `SPARK`, `KAFKA`) and transforms them into a structured JSONL dataset.  
It handles network failures, rate limits, malformed data, and supports **checkpoint-based recovery**.

---

## 🧩 Architecture

jira-llm-corpus/
├── main.py
├── config.yaml
├── requirements.txt
├── scraper/
│ ├── client.py # Handles Jira REST API calls + retries
│ ├── pagination.py # JQL pagination + checkpointing
│ ├── models.py # Pydantic data models for Jira JSON
│ └── extractor.py # Iterates through projects & issues
├── transformer/
│ ├── cleaner.py # Converts HTML to plain text
│ ├── tasks.py # Summarization, classification, QnA via LLM
│ └── writer.py # Streams JSONL output
├── utils/
│ ├── logger.py # Custom logger
│ └── checkpoint.py # Save/load scraping progress
├── checkpoints/ # Resume progress storage
└── corpus/ # Final LLM-ready dataset

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/jira-llm-corpus.git
cd jira-llm-corpus
2. Create and Activate Virtual Environment
🪟 On Windows PowerShell
powershell
Copy code
python -m venv .venv
.venv\Scripts\activate
🐧 On macOS / Linux
bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Set Your OpenAI API Key
🪟 Windows PowerShell
powershell
Copy code
$env:OPENAI_API_KEY = "sk-your_actual_api_key_here"
🐧 macOS / Linux
bash
Copy code
export OPENAI_API_KEY="sk-your_actual_api_key_here"
▶️ Run the Pipeline
bash
Copy code
python main.py
✅ It will:

Scrape issues from Apache Jira projects (based on config.yaml)

Clean and transform them into training-ready JSONL

Apply LLM-based summarization and classification

Save outputs to corpus/

🧠 Example Corpus Entry
json
Copy code
{
  "issue_key": "HADOOP-8",
  "project": "HADOOP",
  "title": "NDFS DataNode advertises localhost as its address",
  "status": "Closed",
  "priority": "Major",
  "reporter": "Peter Sandström",
  "created": "2005-07-24T23:46:18.000+0000",
  "updated": "2015-05-18T04:15:07.000+0000",
  "comments": [
    "fixes the problem by connecting to the NameNode and using the address that the local socket is bound to instead of calling getLocalHost()",
    "if the namenode is down, the socket creation fails and datanode won't launch"
  ],
  "derived": {
    "summary": "Fixes DataNode advertisement bug where localhost is incorrectly used.",
    "classification": "Networking / Configuration",
    "qa": {
      "question": "Why was localhost being advertised?",
      "answer": "Because getLocalHost() returned a loopback address; fix uses actual bound socket IP."
    }
  }
}
🧾 License
This project is licensed under the MIT License — feel free to use, modify, and extend it.

💡 Notes
The scraper respects public Jira access limits.

It auto-resumes from the last saved checkpoint in case of failure.

Supports easy extension to other issue trackers.