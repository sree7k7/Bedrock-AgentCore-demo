from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

# initialize the AgentCore App
app = BedrockAgentCoreApp(

)

# Create a basic agent brain using the strands framework
# agent = Agent()

# Create a basic agent brain using the strands framework
# You need to specify a model for the agent to use
agent = Agent(
    # model="anthropic.claude-3-5-sonnet-20240620-v1:0",
    # system_prompt="You are a helpful AI assistant."
)


# Define the entrypoint - this is the function that 
# AgentCore Runtime will call when it receives a request. 

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    
    #Get the user's prompt from the payload
    user_message = payload.get("prompt", "Hello! How can i help you today?")

    # Send the Prompt to the agent brain. add the past history
    result = agent(user_message)

    # return the agent's response
    return {"result": result.message}

if __name__ == "__main__":
    print("Agent is running on localhost:8080")
    app.run()

