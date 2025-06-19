import os
from crewai import Crew, Agent, Task
from dotenv import load_dotenv
import yaml
from typing import List
from tools.custom_tool import TwitterPostTool # Import the tool

load_dotenv()

def load_agents(config_path="config/agents.yaml") -> List[Agent]:
    with open(config_path, 'r') as file:
        agents_config = yaml.safe_load(file)
    agents = []
    # Load the Twitter posting tool here so it's available when creating the agent
    twitter_tool = TwitterPostTool()
    for name, config in agents_config.items():
        tools = []
        if 'tools' in config:
            for tool_name_config in config['tools']:
                tool_name = tool_name_config if isinstance(tool_name_config, str) else tool_name_config.get('name')
                if tool_name == 'SerperDevTool':
                    from crewai_tools import SerperDevTool
                    tools.append(SerperDevTool())
                elif tool_name == 'ScrapeWebsiteTool':
                    from crewai_tools import ScrapeWebsiteTool
                    tools.append(ScrapeWebsiteTool())
                elif tool_name == 'WebsiteSearchTool':
                    from crewai_tools import WebsiteSearchTool
                    tools.append(WebsiteSearchTool(config={}))
                elif tool_name == 'TwitterPostTool':
                    tools.append(twitter_tool) # Use the instantiated tool
                # Add other tools as needed
        agent = Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=config.get('verbose', False),
            allow_delegation=config.get('allow_delegation', True),
            tools=tools,
            llm=config.get('llm') # Ensure LLM config is passed
        )
        agents.append(agent)
    return agents

def load_tasks(agents: List[Agent], subject: str, config_path="config/tasks.yaml") -> List[Task]:
    with open(config_path, 'r') as file:
        tasks_config = yaml.safe_load(file)
    tasks = []
    for name, config in tasks_config.items():
        agent_name = config['agent']
        agent = next((a for a in agents if a.role.lower().replace(" ", "_") == agent_name.lower().replace(" ", "_")), None)
        if agent:
            task = Task(
                description=config['description'].replace('${subject}', subject),
                agent=agent,
                output_to_stdout=config.get('output_to_stdout', False),
                expected_output=config.get('expected_output', "Results.")
            )
            tasks.append(task)
        else:
            print(f"Warning: Agent '{agent_name}' not found for task '{name}'.")
    return tasks

def run_crew(subject: str):
    agents = load_agents()
    tasks = load_tasks(agents, subject)

    twitter_poster = next((a for a in agents if a.role == "Twitter Poster"), None)
    if not twitter_poster:
        print("Warning: Twitter Poster agent not found.")
        return {}

    review_task = next((t for t in tasks if t.agent.role == "Content Reviewer"), None)
    reviewed_twitter_content = None
    if review_task and hasattr(review_task, 'output') and review_task.output is not None:
        output_lines = review_task.output.split('\n')
        for line in output_lines:
            if "Revised Twitter Post:" in line:
                reviewed_twitter_content = line.split("Revised Twitter Post:")[1].strip()
                break
        if not reviewed_twitter_content:
            for line in output_lines:
                if "Twitter Post:" in line:
                    reviewed_twitter_content = line.split("Twitter Post:")[1].strip()
                    break
        if not reviewed_twitter_content:
            for line in output_lines:
                if "Revised Twitter Post" in line:
                    found_label = False
                    for sub_line in output_lines[output_lines.index(line) + 1:]:
                        if sub_line.strip():
                            reviewed_twitter_content = sub_line.strip()
                            found_label = True
                            break
                    if found_label:
                        break
        if not reviewed_twitter_content:
            for line in output_lines:
                if "Twitter Post" in line:
                    found_label = False
                    for sub_line in output_lines[output_lines.index(line) + 1:]:
                        if sub_line.strip():
                            reviewed_twitter_content = sub_line.strip()
                            found_label = True
                            break
                    if found_label:
                        break


    if not reviewed_twitter_content:
        reviewed_twitter_content = "No reviewed Twitter content available (Review task output was None)."

    post_to_twitter_task = Task(
        description=f"Post the following content to Twitter using the TwitterPostTool and then confirm the Tweet ID: '{reviewed_twitter_content}'",
        agent=twitter_poster,
        output_to_stdout=True,
        expected_output="Confirmation of the tweet being posted with the Tweet ID."
    )
    tasks.append(post_to_twitter_task)

    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True,
    )

    final_output = crew.kickoff()
    print("\n\n✅ Final Output:")
    print(final_output)

    tweet_status = "Not confirmed" # Initialize
    for task in crew.tasks:
        if task.agent.role == "Twitter Poster" and hasattr(task, 'output') and task.output:
            tweet_status = task.output
            break

    return {
        "final_output": final_output,
        "blog_content": next((t.output for t in crew.tasks if t.agent.role == "Content Creator" and hasattr(t, 'output') and t.output), "No blog content"),
        "social_media_posts": next((t.output for t in crew.tasks if t.agent.role == "Chief Content Officer" and hasattr(t, 'output') and t.output), "No social media posts"),
        "reviewed_content": next((t.output for t in crew.tasks if t.agent.role == "Content Reviewer" and hasattr(t, 'output') and t.output), "No reviewed content"),
        "tweet_status": tweet_status
    }
