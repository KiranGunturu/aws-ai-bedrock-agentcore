# 01 — AgentCore Overview

![Architecture](images/architecture.png)

> Editable source: [`images/agentcore-architecture.drawio`](images/agentcore-architecture.drawio)

**Why AgentCore?** Managed, secure infrastructure to run agents in production with any framework (here, Strands) and any model — no building hosting, auth, memory, or tools yourself.

| Component | Why |
|---|---|
| **AgentCore Runtime** | Serverless hosting for the agent, with session isolation and long-running support. |
| **AgentCore Gateway** | Turns your APIs and Lambdas into MCP tools the agent can call. |
| **AgentCore Policy** | Enforces rules on what the agent's tool calls are allowed to do. |
| **AgentCore Identity** | Handles inbound user auth and outbound credentials to tools for the agent. |
| **AgentCore Memory** | Keeps short-term chat context and long-term user facts across sessions. |
| **AgentCore Browser** | A managed, isolated browser so the agent can work on external websites. |
| **Bedrock LLM** | The model (Claude) that reasons and decides which tools to use. |
| **Knowledge Base** | Retrieval over your documents, for grounded answers. |
| **Amazon Cognito** | OAuth2 login for customers; issues the tokens AgentCore Identity validates. |
| **SSM Parameter Store** | Central config (IDs, endpoints) for the UI, with no hardcoding. |
| **API Gateway + Lambda** | The backend order and product APIs, exposed as tools. |
| **DynamoDB / S3** | Where orders and products live, and where documents are stored. |

---

**Previous:** [00 — Setup](../00-setup/README.md)
