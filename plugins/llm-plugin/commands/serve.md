---
description: Deploy and serve models for inference
---

# Serve Command

Deploy models using vLLM, Ollama, or HuggingFace inference endpoints.

## Usage

`/serve [platform] [model] [port]`

## Platforms

- `vllm` - High-performance batch inference
- `ollama` - Local deployment with Ollama
- `hf-inference` - HuggingFace inference endpoint
- `tensorrt` - NVIDIA TensorRT optimization
- `local` - Simple local serving with transformers

## Arguments

- `$ARGUMENTS` will contain: `[platform] [model] [port]`
- Port defaults to 8000 if not specified

## Implementation

Parse arguments and invoke the **deployment-engineer** agent with platform-specific context.

**Example flow:**

1. Parse platform, model, port from $ARGUMENTS (default port=8000)
2. Check if model path exists or is a HuggingFace model ID
3. Invoke **deployment-engineer** agent with platform context:
   - For 'vllm': Deploy with vLLM optimizations (tensor parallel, prefix caching)
   - For 'ollama': Create Modelfile and deploy with Ollama
   - For 'hf-inference': Set up HuggingFace inference endpoint
   - For 'tensorrt': Build TensorRT engine for current GPU
   - For 'local': Simple transformers-based server

**Examples:**

```bash
/serve vllm ./my-model 8000
/serve ollama llama2-7b
/serve hf-inference meta-llama/Llama-2-7b-chat-hf
```
