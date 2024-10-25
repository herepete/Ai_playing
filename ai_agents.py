#!/usr/bin/python3.11

import openai
import os
os.system('clear')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Function to determine the most appropriate agent to respond
def select_agent(agents, user_input):
    if "joke" in user_input.lower():
        return "Joke Creator"
    elif "fact" in user_input.lower() or "verify" in user_input.lower():
        return "Fact Checker"
    else:
        return "Creative Thinker"

# Function for the agent to respond based on instructions
def agent_respond(agent, context):
    try:
        # Make the call to the OpenAI API with clear and explicit structure
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": agent["instructions"]},
                *context
            ],
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to create an agent
def create_agent(name, role, instructions):
    return {"name": name, "role": role, "instructions": instructions}

# Create agents
agent_1 = create_agent("Fact Checker", "assistant", "You are a detailed fact-checker. Provide accurate and concise responses.")
agent_2 = create_agent("Creative Thinker", "assistant", "You are a creative agent that provides out-of-the-box thinking.")
agent_3 = create_agent("Joke Creator", "assistant", "You are a joke creator. Provide funny jokes when asked.")

# List of agents
agents = [agent_1, agent_2, agent_3]

# Initial explanation to the user
print("Welcome! We have three agents here to assist you:")
print("1. Fact Checker: This agent helps with verifying information, providing accurate answers, and fact-checking.")
print("2. Creative Thinker: This agent helps with brainstorming ideas, creative problem-solving, and thinking outside the box.")
print("3. Joke Creator: This agent helps you by creating jokes and providing humor.")
print("Feel free to ask any questions, and our most suitable agent will assist you.")

# Run an interactive conversation loop
while True:
    # Ask user for input
    user_input = input("\nWhat do you need help with today?\nYou: ")
    
    # Break loop if user wants to quit
    if user_input.lower() in ["quit", "exit"]:
        print("Ending the conversation.")
        break

    # Determine the most appropriate agent based on user input
    selected_agent_name = select_agent(agents, user_input)
    selected_agent = next(agent for agent in agents if agent["name"] == selected_agent_name)
    
    # Reset messages to contain only the most recent user input for new prompts
    messages = [{"role": "user", "content": user_input}]

    # Run the selected agent to process the current context
    response = agent_respond(selected_agent, messages)
    if response:
        messages.append({"role": "assistant", "content": f"{selected_agent['name']} response: {response}"})
        print(f"{selected_agent['name']} response: {response}")
    else:
        print(f"No response from {selected_agent['name']}.")

