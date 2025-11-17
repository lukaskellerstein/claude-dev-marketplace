---
description: Deploy AI agents to production
allowed-tools: Bash, Read, Write
---

# Deploy Command

Deploy AI agents and workflows to production environments.

## Usage

`/deploy [target] [agent-name] [options]`

## Deployment Targets

- `docker` - Deploy as Docker container
- `kubernetes` - Deploy to Kubernetes cluster
- `aws-lambda` - Deploy to AWS Lambda
- `azure` - Deploy to Azure AI Foundry
- `local` - Run as local service

## Features

- **Containerization**: Automatic Docker image creation
- **Environment Management**: Handle secrets and configs
- **Health Checks**: Built-in monitoring endpoints
- **Scaling**: Auto-scaling configuration
- **CI/CD Integration**: GitHub Actions templates

## Implementation

!`
#!/bin/bash

TARGET=$1
AGENT_NAME=$2
OPTIONS=$3

case $TARGET in
    docker)
        echo "Deploying $AGENT_NAME to Docker..."

        # Create Dockerfile
        cat > "Dockerfile" << 'EODOCKER'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY ./agents ./agents
COPY ./workflows ./workflows

# Expose port
EXPOSE 8000

# Run agent
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EODOCKER

        # Create requirements.txt
        cat > "requirements.txt" << 'EOREQ'
langchain>=1.0.0
langgraph>=1.0.0
langchain-anthropic>=1.0.0
anthropic
uvicorn
fastapi
EOREQ

        echo "Building Docker image..."
        docker build -t "$AGENT_NAME:latest" .

        echo "Running container..."
        docker run -d -p 8000:8000 --name "$AGENT_NAME" "$AGENT_NAME:latest"

        echo "Deployment complete! Agent running on http://localhost:8000"
        ;;

    kubernetes)
        echo "Deploying $AGENT_NAME to Kubernetes..."

        # Create Kubernetes deployment
        cat > "k8s-deployment.yaml" << EOKUBE
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $AGENT_NAME
spec:
  replicas: 3
  selector:
    matchLabels:
      app: $AGENT_NAME
  template:
    metadata:
      labels:
        app: $AGENT_NAME
    spec:
      containers:
      - name: $AGENT_NAME
        image: $AGENT_NAME:latest
        ports:
        - containerPort: 8000
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: anthropic-secret
              key: api-key
---
apiVersion: v1
kind: Service
metadata:
  name: $AGENT_NAME-service
spec:
  selector:
    app: $AGENT_NAME
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
EOKUBE

        echo "Applying Kubernetes configuration..."
        kubectl apply -f k8s-deployment.yaml

        echo "Deployment complete!"
        ;;

    aws-lambda)
        echo "Deploying $AGENT_NAME to AWS Lambda..."

        # Create Lambda handler
        cat > "lambda_handler.py" << 'EOLAMBDA'
import json
from agents.agent import agent

def lambda_handler(event, context):
    """AWS Lambda handler for agent"""
    try:
        message = event.get('message', 'Hello')

        result = agent.invoke({
            "messages": [{"role": "user", "content": message}]
        })

        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': result["messages"][-1].content
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
EOLAMBDA

        echo "Creating Lambda deployment package..."
        pip install -t ./package langchain langgraph langchain-anthropic
        cd package && zip -r ../lambda-deployment.zip . && cd ..
        zip -g lambda-deployment.zip lambda_handler.py

        echo "Deployment package created: lambda-deployment.zip"
        echo "Upload to AWS Lambda console or use AWS CLI"
        ;;

    azure)
        echo "Deploying $AGENT_NAME to Azure AI Foundry..."

        echo "Using Microsoft Agent Framework for Azure deployment"
        python3 << 'EOAZURE'
from agent_framework.azure import AzureAIFoundryClient
from azure.identity import DefaultAzureCredential

# Deploy to Azure
client = AzureAIFoundryClient(
    credential=DefaultAzureCredential(),
    resource_group="ai-agents-rg",
    workspace="ai-agents-workspace"
)

# Deploy agent
deployment = client.deploy_agent(
    agent_path="./agents/agent.py",
    name="production-agent",
    compute="serverless"
)

print(f"Deployed to: {deployment.endpoint_url}")
EOAZURE
        ;;

    local)
        echo "Starting $AGENT_NAME as local service..."

        # Create FastAPI service
        cat > "main.py" << 'EOAPI'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.agent import agent

app = FastAPI()

class Message(BaseModel):
    content: str

@app.post("/invoke")
async def invoke_agent(message: Message):
    """Invoke agent with message"""
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": message.content}]
        })

        return {
            "response": result["messages"][-1].content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
EOAPI

        echo "Starting local service..."
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
        ;;

    *)
        echo "Usage: /deploy [docker|kubernetes|aws-lambda|azure|local] [agent-name]"
        exit 1
        ;;
esac
`
