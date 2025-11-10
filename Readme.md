# Bedrock AgentCore Stateful Agent

### Purpose:
To write, package, and deploy basic AI agent to the AWS cloud using the AgentCore Runtime
 - AI agent deployment locally on machine
 - AI agent deployment in cloud

### Prerequsites
- AWS account with permissions for Bedrock AgentCore
- Python 3
- AWS [CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Docker

### Implementation
1. Create a project folder and a virtual environment

```
mkdir agentcore-quickstart #project folder
cd agentcore-quickstart
python3 -m venv .venv # create virtual environment
source .venv/bin/activate # activate the environment
```

> **Note**: Windows, use ```.venv\Scripts\activate```

→ Install AWS libraries
```
pip install --upgrade pip
pip install bedrock-agentcore strands-agents bedrock-agentcore-starter-toolkit

```
📖 Why you're doing this:
*bedrock-agentcore*: This is the main SDK that lets your python code talk to AgentCore services.
*strands-agents*: This is an open-source framework for building AI agents in few line of code.
*bedrock-agentcore-starter-toolkit*: This is a utility that makes it much easier to deploy your agent to the ```AgentCore Runtime```.
2. Agent Code and libraries

```
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

# initialize the AgentCore App
app = BedrockAgentCoreApp()

# Create a basic agent brain using the strands framework
# It will choose the default model 
# agent = Agent()

# Define the entrypoint - this is the function that AgentCore Runtime will call when it receives a request. 

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    
    #Get the user's prompt from the payload
    user_message = payload.get("prompt", "Hello!")

    # Send the Prompt to the agent brain.
    result = agent(user_message)

    # return the agent's response
    return {"result": result.message}

if __name__ == "__main__":
    print("Agent is running on localhost:8080")
    app.run()

```
→ Keep two/split terminals.
  Execute the following command to run your agent from script:
```python my_agent.py```

  In second terminal, execute the curl command to talk to agent.

```
curl -X POST http://localhost:8080/invocations \
-H "Content-Type: application/json" \
-d '{"prompt": "Hello!"}'
```
### output
You should get a successful json response back, something like: 
```
{"result": {"role": "assistant", "content": [{"text": "Hello! It's nice to meet you"}]}}%  
```

3. ###### 🚀 Deploy to Amazon AgentCore Runtime

Now, you are handing your agent's code over to AWS cloud, and the ```Runtime``` service is taking control of hosting agent.

Execute the below cmd. To package and deploy the agent.
```
agentcore configure -e my_agent.py
```
info: go with default options for now. After, cmd will generate config file: ```.bedrock_agentcore.yaml```

To launch the agent, execute the cmd;

```
agentcore launch
```
After you'll be seeing the AWS services such as: ```AWS Codebuild```, ```Amazon ECR```, ```Amazon Bedrock```.

After success:
This means your agent is no longer on your laptop. It is live and running in AWS on AgentCore Runtime.

> Tip: If you have docker running on your system. Use command: agentcore launch --local-build. The starter toolkit will build the container image locally with docker instead of using AWSCodebuild. Then the image is uploaded to AWS ECR.

To invoke/call your live agent:
```
agentcore invoke '{"prompt": "Hello"}'
```
Output:
```
{"result": {"role": "assistant", "content": [{"text": "Hello! How are you doing today?"}]}}
```

![Agent Output](pics/Screenshot%202025-11-09%20174340.png)
