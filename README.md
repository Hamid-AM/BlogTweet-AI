## Overview

**Content Forge** is an automated content generation pipeline powered by **CrewAI**. This project orchestrates a team of specialized AI agents to collaboratively research a given subject, analyze findings, draft a comprehensive blog post, adapt content for social media, rigorously review it, and finally, publish tweets directly to Twitter. The primary goal is to streamline the entire content creation process, from initial research to final social media distribution.

## Features

  * **Intelligent Research:** Agents equipped with web search and scraping tools gather relevant information and identify trends.
  * **Data Analysis & Structuring:** Transforms raw research data into structured insights and clear outlines for content creation.
  * **Blog Post Generation:** Crafts well-structured, long-form blog posts on any specified topic.
  * **Social Media Adaptation:** Converts blog content into engaging and platform-specific social media posts (currently focused on Twitter).
  * **Content Review:** Ensures all generated content meets quality standards, checking for grammar, clarity, tone, and consistency.
  * **Automated Twitter Publishing:** Posts reviewed content directly to Twitter using a custom-built tool.

## How It Works (The Agent Team)

The project leverages a crew of distinct AI agents, each with a specialized role:

1.  **Market Analyst:**

      * **Role:** The "Researcher."
      * **Goal:** Find relevant information and trends about the subject using web search and scraping tools.

2.  **Data Analyst:**

      * **Role:** The "Organizer & Insight Extractor."
      * **Goal:** Synthesize raw research into key insights, trends, and a structured outline for the content.

3.  **Content Creator:**

      * **Role:** The "Writer."
      * **Goal:** Write a long-form, polished blog post based on the provided insights and outline.

4.  **Chief Content Officer:**

      * **Role:** The "Social Media Strategist."
      * **Goal:** Convert the blog post into engaging social media posts, specifically focusing on Twitter content.

5.  **Content Reviewer:**

      * **Role:** The "Quality Controller."
      * **Goal:** Review the blog post and social media content for grammar, clarity, tone, and structural consistency.

6.  **Twitter Poster:**

      * **Role:** The "Publisher."
      * **Goal:** Effectively share reviewed social media content on Twitter using the custom `TwitterPostTool`.

## Setup and Installation

### Prerequisites

  * Python 3.12+ (It's recommended to use the same Python version your `venv` was created with).
  * API keys for your chosen Large Language Model (LLM) provider (e.g., OpenAI, Anthropic, Google Gemini).
  * Twitter Developer Account and API credentials (Consumer Key, Consumer Secret, Bearer Token, Access Token, Access Token Secret).

### Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Hamid-AM/BlogTweet-AI.git # Adjust if your repo name is different
    cd BlogTweet-AI/edu
    ```

2.  **Create a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage dependencies.

    ```bash
    python3 -m venv venv
    ```

3.  **Activate the Virtual Environment:**

      * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
      * On Windows (Command Prompt):
        ```bash
        venv\Scripts\activate.bat
        ```
      * On Windows (PowerShell):
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```

    You should see `(venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

4.  **Install Dependencies:**
    Install all required Python packages. If you have a `requirements.txt` file, use it. Otherwise, install them manually:

    ```bash
    pip install crewai python-dotenv pyyaml tweepy crewai-tools
    ```

    *(If you used `uv` for your venv setup, you might use `uv pip install ...` instead of `pip install ...`)*

5.  **Configure Environment Variables (.env file):**
    Create a file named `.env` in the root of your `edu` project directory (where `main.py` is located). Add your LLM and Twitter API credentials to this file:

    ```dotenv
    # LLM API Key (Example for OpenAI)
    OPENAI_API_KEY=your_openai_api_key_here
    # Or for others, e.g., GOOGLE_API_KEY=your_google_api_key

    # Twitter API Keys
    TWITTER_API_KEY=your_consumer_key_here
    TWITTER_API_SECRET=your_consumer_secret_here
    TWITTER_BEARER_TOKEN=your_bearer_token_here
    TWITTER_ACCESS_TOKEN=your_access_token_here
    TWITTER_ACCESS_SECRET=your_access_token_secret_here
    ```

    **Important:** Do not commit your `.env` file to version control (e.g., Git) as it contains sensitive information.

## Usage

To run the content generation pipeline, execute the `main.py` script from your project's `edu` directory and provide the subject as an argument.

```bash
cd edu # Ensure you are in the edu directory
python main.py "The Future of AI in Healthcare"
```

Replace `"The Future of AI in Healthcare"` with your desired blog post subject.

The crew will then begin its process, and you'll see verbose output in your terminal as agents perform their tasks. Upon completion, the final generated content (including blog post snippets and tweet status) will be printed.

## Project Structure

```
.
├── config/
│   ├── agents.yaml           # Defines AI agent roles, goals, and backstories
│   └── tasks.yaml            # Defines the sequential tasks for the agents
├── src/
│   └── edu/
│       ├── __init__.py
│       ├── crew.py           # Contains the CrewAI setup, agent, and task loading logic
│       ├── main.py           # Entry point for running the project
│       └── tools/
│           ├── __init__.py
│           └── custom_tool.py  # Custom TwitterPostTool implementation
├── venv/                     # Python virtual environment (ignored by Git)
├── .env                      # Environment variables (ignored by Git)
└── README.md                 # This file
