# Goal

Create a marketplace that contains all plugins described in section "My plugins". You are expert on Claude code plugins, you mastered all components of plugins ("subagents", "skills", "commands", "hooks" ... etc.). You can judge with experience, what components to use for each use-case/plugin, and you can optimize for success. 

Each plugin has a area of interest. Cover them all. 

In case you will decide that for some plugin make sense to use some MCP server, use them, but make sure the MCP server really exist and read a documentation about him first. Do not make anything up. I am providing for you list of some MCP servers that would make sense to me to be used, but the final judgement is on you. Here: `/home/lukas/Projects/Github/lukaskellerstein/claude-dev-marketplace/MCP_SERVERS_LIST.md`

## Documentation

All documentation is to your disposal in folder `docs`.

## Examples

You can access the OFFICIAL anthropic's examples, take an inspiration there, as the examples are created by authors of the claude code.

- `/home/lukas/Projects/Github/anthropic/claude-code/plugins`
- `/home/lukas/Projects/Github/anthropic/skills`


## My Plugins

`Architecture-plugin` = Microservices design, communication, and orchestration. Cloud patterns. Monolithic architecture. 3 layer architecture = UI -> API -> DB. Message brokers, event sourcing.

---

`Frontend-plugin` = Javascript, Typescript, React, shadcn-ui, Radix UI, Tailwind CSS, CSS/SCSS, Responsive design

`Backend-plugin` = REST, GraphQL, grpc, Websocket, Message Broker (NATS, RabbitMQ, Redis pub/sub, Kafka)

`Database-plugin` = PostgreSQL, Supabase, Qdrant, Elastick-search, MongoDB, Redis, MinIO (S3)

---

`cicd-plugin` = Github actions, pipelines, automated deployment, and release management

`infra-plugin` = Google Cloud, Kubernetes, Docker, Terraform, Helm

---

`llm-plugin` = Pytorch, HuggingFace (datasets, transformers, trl, peft), Unsloth, vLLM, Ollama, Models - GPT-OSS, Llama4 ... etc.

`aiagent-plugin` = Claude Agent SDK, Codex SDK, Lanchain + Langgraph, Microsoft Agent Framework, Workflows - Temporal.io

---

`Documentation-plugin` = Documentation generation, review, and scoring

`Security-plugin` = Security auditing, vulnerability scanning, and fixes

`Performance-plugin` = Performance monitoring, profiling, and optimization

`Test-plugin` = Test generation, coverage analysis, and quality assurance
