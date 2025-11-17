---
description: Train or fine-tune language models
allowed-tools: Bash, Read, Write, Task
---

# Train Command

Train and fine-tune large language models with various techniques.

## Usage

`/train [method] [model] [dataset] [options]`

## Methods

- `full` - Full model training
- `lora` - LoRA fine-tuning
- `qlora` - QLoRA (4-bit) fine-tuning
- `dpo` - Direct Preference Optimization
- `rlhf` - Reinforcement Learning from Human Feedback
- `continued` - Continued pre-training

## Models

- `llama2-7b`, `llama2-13b`, `llama2-70b`
- `llama3-8b`, `llama3-70b`
- `mistral-7b`, `mixtral-8x7b`
- `phi-2`, `phi-3`
- `custom` - Custom model path

## Arguments

- `$ARGUMENTS` will contain: `[method] [model] [dataset] [options]`

## Implementation

Parse the arguments and invoke the appropriate training-specialist or finetuning-expert agent based on the method.

**Example flow:**

1. Parse method from $ARGUMENTS
2. Validate GPU availability
3. For methods 'lora', 'qlora' -> invoke **finetuning-expert** agent
4. For methods 'full', 'dpo', 'rlhf', 'continued' -> invoke **training-specialist** agent
5. Agent handles all training implementation

**GPU Check:**

First check if GPU is available:

```bash
if command -v nvidia-smi &> /dev/null; then
  echo "GPU detected"
  nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
else
  echo "Warning: No GPU detected, training will be slow"
fi
```

**Examples:**

```bash
/train lora llama2-7b alpaca
/train qlora mistral-7b custom_dataset.jsonl
/train dpo llama2-7b preferences.json
```
