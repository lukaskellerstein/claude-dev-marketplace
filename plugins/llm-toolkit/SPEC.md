# LLM Plugin Specification

## Plugin Overview

**Name**: `llm-plugin`  
**Version**: `1.0.0`  
**Description**: Comprehensive LLM toolkit for training, fine-tuning, deployment, and inference using PyTorch, HuggingFace, Unsloth, vLLM, and Ollama.

## Core Capabilities

### Model Operations

- **Training**: Full model training from scratch
- **Fine-tuning**: LoRA, QLoRA, full fine-tuning
- **RLHF/DPO**: Reinforcement learning from human feedback
- **Quantization**: INT8, INT4, GPTQ, AWQ
- **Deployment**: vLLM serving, Ollama local deployment

### Supported Frameworks

- **PyTorch**: Core deep learning framework
- **HuggingFace**: Transformers, Datasets, Accelerate, PEFT, TRL
- **Unsloth**: 2x faster training with memory optimization
- **vLLM**: High-throughput inference serving
- **Ollama**: Local model deployment and management

### Model Support

- **Llama Family**: Llama 2, Llama 3, Code Llama, Alpaca
- **Mistral/Mixtral**: 7B, 8x7B, 8x22B
- **GPT Models**: GPT-J, GPT-NeoX, GPT2
- **Other Models**: Phi, Qwen, Yi, Gemma, DeepSeek

## Plugin Structure

```
llm-plugin/
├── manifest.json
├── commands/
│   ├── train.md              # Training command
│   ├── finetune.md          # Fine-tuning command
│   ├── serve.md             # Model serving
│   ├── evaluate.md          # Model evaluation
│   ├── quantize.md          # Quantization command
│   └── dataset.md           # Dataset management
├── agents/
│   ├── training-specialist.md
│   ├── finetuning-expert.md
│   ├── deployment-engineer.md
│   ├── dataset-curator.md
│   ├── optimization-expert.md
│   └── evaluation-analyst.md
├── skills/
│   ├── gpu-optimization.md
│   ├── memory-management.md
│   ├── hyperparameter-tuning.md
│   └── model-selection.md
├── mcp-servers/
│   └── config.json
└── output-styles/
    ├── training-report.md
    ├── benchmark-results.md
    └── model-card.md
```

## Manifest Configuration

```json
{
  "name": "llm-plugin",
  "version": "1.0.0",
  "description": "Comprehensive LLM toolkit for training, fine-tuning, and deployment",
  "author": {
    "name": "Claude Code Team",
    "email": "team@claude.code",
    "url": "https://github.com/claude-code/llm-plugin"
  },
  "keywords": [
    "llm",
    "pytorch",
    "huggingface",
    "transformers",
    "unsloth",
    "vllm",
    "ollama",
    "training",
    "finetuning",
    "lora",
    "qlora",
    "rlhf",
    "dpo",
    "llama",
    "mistral",
    "gpt"
  ],
  "commands": [
    "./commands/train.md",
    "./commands/finetune.md",
    "./commands/serve.md",
    "./commands/evaluate.md",
    "./commands/quantize.md",
    "./commands/dataset.md"
  ],
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./mcp-servers/config.json",
  "outputStyles": "./output-styles/"
}
```

## Commands

### `/train` Command

```markdown
---
description: Train or fine-tune language models
allowed-tools: Bash, Read, Write, Execute
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

## Implementation

!`
#!/bin/bash

METHOD=$1
MODEL=$2
DATASET=$3
OPTIONS=$4

# Check for GPU availability

check_gpu() {
if command -v nvidia-smi &> /dev/null; then
echo "GPU detected:"
nvidia-smi --query-gpu=name,memory.total --format=csv
return 0
else
echo "Warning: No GPU detected, training will be slow"
return 1
fi
}

# Setup Python environment

setup_environment() {
if [ ! -d "venv" ]; then
python -m venv venv
fi
source venv/bin/activate

    # Install required packages
    pip install -q torch transformers datasets accelerate peft trl

    if [ "$METHOD" == "qlora" ] || [ "$METHOD" == "lora" ]; then
        pip install -q unsloth
    fi

}

GPU_AVAILABLE=$(check_gpu)
setup_environment

case $METHOD in
full)
echo "Starting full model training..."
echo "Model: $MODEL"
echo "Dataset: $DATASET" # Invoke training-specialist agent
;;
lora|qlora)
echo "Starting ${METHOD^^} fine-tuning..."
echo "Model: $MODEL"
echo "Dataset: $DATASET" # Invoke finetuning-expert agent
;;
dpo|rlhf)
echo "Starting $METHOD training..." # Invoke training-specialist with RLHF context
;;
continued)
echo "Starting continued pre-training..." # Invoke training-specialist with continued training context
;;
\*)
echo "Usage: /train [full|lora|qlora|dpo|rlhf|continued] [model] [dataset]"
exit 1
;;
esac
`
```

### `/finetune` Command

```markdown
---
description: Fine-tune models with advanced techniques
allowed-tools: Bash, Read, Write, Execute
---

# Finetune Command

Fine-tune LLMs with LoRA, QLoRA, and other parameter-efficient methods.

## Usage

`/finetune [technique] [base_model] [dataset] [output_dir]`

## Techniques

- `lora` - Low-Rank Adaptation
- `qlora` - Quantized LoRA (4-bit)
- `prefix` - Prefix tuning
- `ia3` - Infused Adapter by Inhibiting and Amplifying
- `adapters` - Adapter layers

!`
#!/bin/bash

TECHNIQUE=$1
BASE_MODEL=$2
DATASET=$3
OUTPUT_DIR=${4:-"./models/finetuned"}

echo "Fine-tuning configuration:"
echo "Technique: $TECHNIQUE"
echo "Base Model: $BASE_MODEL"
echo "Dataset: $DATASET"
echo "Output: $OUTPUT_DIR"

# Create output directory

mkdir -p $OUTPUT_DIR

case $TECHNIQUE in
lora)
echo "Configuring LoRA fine-tuning..." # r=16, alpha=32, target all linear layers
;;
qlora)
echo "Configuring QLoRA with 4-bit quantization..." # 4-bit quantization with nf4
;;
prefix)
echo "Configuring prefix tuning..."
;;
ia3)
echo "Configuring IA3 fine-tuning..."
;;
adapters)
echo "Configuring adapter layers..."
;;
esac

# Invoke finetuning-expert agent with configuration

`
```

### `/serve` Command

```markdown
---
description: Deploy and serve models for inference
allowed-tools: Bash, Execute, Monitor
---

# Serve Command

Deploy models using vLLM, Ollama, or HuggingFace inference endpoints.

## Usage

`/serve [platform] [model] [options]`

## Platforms

- `vllm` - High-performance batch inference
- `ollama` - Local deployment with Ollama
- `hf-inference` - HuggingFace inference endpoint
- `tensorrt` - NVIDIA TensorRT optimization

!`
#!/bin/bash

PLATFORM=$1
MODEL=$2
PORT=${3:-8000}

case $PLATFORM in
vllm)
echo "Starting vLLM server..."
echo "Model: $MODEL"
echo "Port: $PORT" # python -m vllm.entrypoints.openai.api_server \
 # --model $MODEL \
 # --port $PORT \
 # --max-model-len 4096
;;
ollama)
echo "Deploying with Ollama..." # ollama run $MODEL
;;
hf-inference)
echo "Setting up HuggingFace inference endpoint..."
;;
tensorrt)
echo "Optimizing with TensorRT..."
;;
esac
`
```

### `/evaluate` Command

```markdown
---
description: Evaluate model performance and benchmarks
allowed-tools: Read, Execute, Analyze
---

# Evaluate Command

Run comprehensive model evaluation and benchmarking.

## Usage

`/evaluate [model] [benchmark] [metrics]`

## Benchmarks

- `mmlu` - Massive Multitask Language Understanding
- `humaneval` - Code generation benchmark
- `gsm8k` - Grade school math problems
- `truthfulqa` - Truthfulness evaluation
- `custom` - Custom evaluation dataset

## Metrics

- `perplexity` - Language modeling quality
- `accuracy` - Task-specific accuracy
- `bleu` - Translation quality
- `rouge` - Summarization quality

!`
#!/bin/bash

MODEL=$1
BENCHMARK=$2
METRICS=${3:-"all"}

echo "Evaluating model: $MODEL"
echo "Benchmark: $BENCHMARK"
echo "Metrics: $METRICS"

# Invoke evaluation-analyst agent

`
```

### `/quantize` Command

```markdown
---
description: Quantize models for efficient deployment
allowed-tools: Read, Write, Execute
---

# Quantize Command

Quantize models to reduce size and improve inference speed.

## Usage

`/quantize [method] [model] [output]`

## Methods

- `int8` - 8-bit integer quantization
- `int4` - 4-bit integer quantization
- `gptq` - GPTQ quantization
- `awq` - Activation-aware Weight Quantization
- `bnb` - BitsAndBytes quantization

!`
#!/bin/bash

METHOD=$1
MODEL=$2
OUTPUT=$3

echo "Quantizing model..."
echo "Method: $METHOD"
echo "Input: $MODEL"
echo "Output: $OUTPUT"

case $METHOD in
int8)
echo "Applying INT8 quantization..."
;;
int4)
echo "Applying INT4 quantization..."
;;
gptq)
echo "Applying GPTQ quantization..."
;;
awq)
echo "Applying AWQ quantization..."
;;
bnb)
echo "Applying BitsAndBytes quantization..."
;;
esac
`
```

### `/dataset` Command

```markdown
---
description: Manage and prepare datasets for training
allowed-tools: Read, Write, Process
---

# Dataset Command

Prepare, process, and manage datasets for LLM training.

## Usage

`/dataset [action] [source] [format]`

## Actions

- `prepare` - Prepare dataset for training
- `convert` - Convert between formats
- `analyze` - Analyze dataset statistics
- `clean` - Clean and filter dataset
- `augment` - Augment with synthetic data

## Formats

- `alpaca` - Alpaca instruction format
- `chatml` - ChatML format
- `jsonl` - JSON Lines format
- `parquet` - Parquet format

!`
#!/bin/bash

ACTION=$1
SOURCE=$2
FORMAT=${3:-"jsonl"}

echo "Dataset operation: $ACTION"
echo "Source: $SOURCE"
echo "Format: $FORMAT"

case $ACTION in
prepare)
echo "Preparing dataset..." # Invoke dataset-curator agent
;;
convert)
echo "Converting dataset format..."
;;
analyze)
echo "Analyzing dataset..."
;;
clean)
echo "Cleaning dataset..."
;;
augment)
echo "Augmenting dataset..."
;;
esac
`
```

## Agents

### training-specialist.md

````markdown
---
name: training-specialist
description: Expert in training LLMs from scratch and continued pre-training
tools: Read, Write, Execute, Monitor
model: opus
---

# Training Specialist

Expert in training large language models with PyTorch and HuggingFace.

## Full Model Training

### Training Configuration

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
import torch
from datasets import load_dataset
from accelerate import Accelerator

class LLMTrainer:
    def __init__(self, model_name: str, dataset_name: str):
        self.accelerator = Accelerator(
            mixed_precision='bf16',  # Use bfloat16 for training
            gradient_accumulation_steps=4,
            cpu=False
        )

        # Load model and tokenizer
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            use_cache=False,  # Disable KV cache for training
            attn_implementation="flash_attention_2"  # Use FlashAttention 2
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            use_fast=True
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def prepare_dataset(self, dataset_name: str):
        # Load and tokenize dataset
        dataset = load_dataset(dataset_name)

        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                padding="max_length",
                truncation=True,
                max_length=2048,
                return_tensors="pt"
            )

        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            num_proc=4,
            remove_columns=dataset["train"].column_names
        )

        return tokenized_dataset

    def setup_training_args(self):
        return TrainingArguments(
            output_dir="./output",
            overwrite_output_dir=True,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            gradient_accumulation_steps=4,
            eval_accumulation_steps=4,
            warmup_steps=500,
            learning_rate=2e-5,
            logging_steps=10,
            save_steps=1000,
            eval_steps=500,
            save_total_limit=3,
            save_strategy="steps",
            evaluation_strategy="steps",
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            bf16=True,
            tf32=True,  # Enable TF32 on Ampere GPUs
            gradient_checkpointing=True,
            group_by_length=True,
            ddp_find_unused_parameters=False,
            report_to=["tensorboard"],
            dataloader_num_workers=4,
        )

    def train(self):
        dataset = self.prepare_dataset(self.dataset_name)
        training_args = self.setup_training_args()

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset["train"],
            eval_dataset=dataset["validation"],
            tokenizer=self.tokenizer,
            data_collator=DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False
            ),
        )

        # Start training
        trainer.train()

        # Save final model
        trainer.save_model("./final_model")
        self.tokenizer.save_pretrained("./final_model")
```
````

### Distributed Training with DeepSpeed

```python
# DeepSpeed Configuration
deepspeed_config = {
    "zero_optimization": {
        "stage": 2,  # ZeRO Stage 2
        "offload_optimizer": {
            "device": "cpu",
            "pin_memory": True
        },
        "allgather_partitions": True,
        "allgather_bucket_size": 2e8,
        "overlap_comm": True,
        "reduce_scatter": True,
        "reduce_bucket_size": 2e8,
        "contiguous_gradients": True
    },
    "bf16": {
        "enabled": True
    },
    "gradient_accumulation_steps": 4,
    "gradient_clipping": 1.0,
    "train_batch_size": "auto",
    "train_micro_batch_size_per_gpu": 2,
    "wall_clock_breakdown": False
}
```

### Continued Pre-training

```python
def continued_pretraining(base_model: str, new_data: str):
    """
    Continue pre-training an existing model on new data
    """
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.bfloat16
    )

    # Adjust learning rate for continued training
    training_args = TrainingArguments(
        learning_rate=5e-6,  # Lower LR for continued training
        warmup_ratio=0.03,
        num_train_epochs=1,
        save_strategy="epoch",
        # ... other args
    )

    # Continue training on new domain
    trainer.train(resume_from_checkpoint=True)
```

## Training Optimization Techniques

### Gradient Checkpointing

```python
# Enable gradient checkpointing to save memory
model.gradient_checkpointing_enable()
model.config.use_cache = False  # Incompatible with checkpointing
```

### Mixed Precision Training

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    optimizer.zero_grad()

    with autocast(dtype=torch.bfloat16):
        outputs = model(**batch)
        loss = outputs.loss

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## Best Practices

1. **Learning Rate Schedule**: Use cosine or linear warmup
2. **Gradient Clipping**: Prevent exploding gradients
3. **Weight Decay**: 0.01 for regularization
4. **Batch Size**: Maximize GPU utilization
5. **Checkpointing**: Save regularly to prevent loss
6. **Monitoring**: Track loss, learning rate, gradients

````

### finetuning-expert.md

```markdown
---
name: finetuning-expert
description: Specialist in LoRA, QLoRA, and parameter-efficient fine-tuning
tools: Read, Write, Execute, Optimize
model: sonnet
---

# Fine-tuning Expert

Expert in parameter-efficient fine-tuning methods using PEFT and Unsloth.

## LoRA Fine-tuning with Unsloth

```python
from unsloth import FastLanguageModel
import torch
from transformers import TrainingArguments
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
from datasets import load_dataset

class LoRAFineTuner:
    def __init__(self, model_name: str, max_seq_length: int = 2048):
        # Load model with Unsloth for 2x faster training
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=max_seq_length,
            dtype=None,  # Auto-detect
            load_in_4bit=True,  # Use 4bit for QLoRA
        )

    def prepare_model_for_training(self):
        # Apply LoRA adapters
        self.model = FastLanguageModel.get_peft_model(
            self.model,
            r=16,  # LoRA rank
            target_modules=[
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj",
            ],
            lora_alpha=16,
            lora_dropout=0.05,
            bias="none",
            use_gradient_checkpointing="unsloth",  # Unsloth's optimized checkpointing
            random_state=42,
            use_rslora=False,  # Rank stabilized LoRA
            loftq_config=None,  # LoftQ initialization
        )

    def prepare_dataset(self, dataset_name: str):
        """
        Prepare dataset in Alpaca format
        """
        dataset = load_dataset(dataset_name)

        # Alpaca prompt template
        alpaca_prompt = """### Instruction:
{}

### Input:
{}

### Response:
{}"""

        def formatting_prompts_func(examples):
            instructions = examples["instruction"]
            inputs = examples["input"]
            outputs = examples["output"]
            texts = []

            for instruction, input, output in zip(instructions, inputs, outputs):
                text = alpaca_prompt.format(instruction, input, output)
                texts.append(text)

            return {"text": texts}

        dataset = dataset.map(
            formatting_prompts_func,
            batched=True,
        )

        return dataset

    def train(self, dataset_name: str, output_dir: str = "./lora_model"):
        self.prepare_model_for_training()
        dataset = self.prepare_dataset(dataset_name)

        trainer = SFTTrainer(
            model=self.model,
            tokenizer=self.tokenizer,
            train_dataset=dataset["train"],
            dataset_text_field="text",
            max_seq_length=2048,
            dataset_num_proc=2,
            packing=False,  # Can set to True for short sequences
            args=TrainingArguments(
                per_device_train_batch_size=2,
                gradient_accumulation_steps=4,
                warmup_steps=5,
                max_steps=60,  # Or num_train_epochs
                learning_rate=2e-4,
                fp16=not torch.cuda.is_bf16_supported(),
                bf16=torch.cuda.is_bf16_supported(),
                logging_steps=1,
                optim="adamw_8bit",
                weight_decay=0.01,
                lr_scheduler_type="linear",
                seed=42,
                output_dir=output_dir,
                save_strategy="steps",
                save_steps=10,
                save_total_limit=2,
            ),
        )

        # Train
        trainer.train()

        # Save LoRA adapters
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)

        # Merge and save full model (optional)
        # self.model.save_pretrained_merged(f"{output_dir}_merged", tokenizer)
````

## QLoRA with 4-bit Quantization

```python
from transformers import BitsAndBytesConfig
import bitsandbytes as bnb

def create_qlora_config():
    """
    Create QLoRA configuration with 4-bit quantization
    """
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,  # Double quantization
        bnb_4bit_quant_type="nf4",  # NormalFloat4
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    return bnb_config

class QLoRATrainer:
    def __init__(self, model_name: str):
        bnb_config = create_qlora_config()

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

    def prepare_for_training(self):
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

        # Prepare model for k-bit training
        self.model = prepare_model_for_kbit_training(self.model)

        # LoRA configuration
        peft_config = LoraConfig(
            r=64,
            lora_alpha=16,
            target_modules=[
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj", "lm_head"
            ],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )

        self.model = get_peft_model(self.model, peft_config)

        # Print trainable parameters
        self.model.print_trainable_parameters()
```

## Advanced Fine-tuning Techniques

### DPO (Direct Preference Optimization)

```python
from trl import DPOTrainer

class DPOFineTuner:
    def __init__(self, model_name: str):
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.ref_model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def train_dpo(self, dataset):
        dpo_trainer = DPOTrainer(
            self.model,
            self.ref_model,
            args=TrainingArguments(
                per_device_train_batch_size=4,
                learning_rate=1e-6,
                num_train_epochs=1,
                gradient_accumulation_steps=2,
                save_strategy="epoch",
                logging_steps=10,
            ),
            beta=0.1,  # KL penalty coefficient
            train_dataset=dataset["train"],
            eval_dataset=dataset["test"],
            tokenizer=self.tokenizer,
        )

        dpo_trainer.train()
```

### RLHF with PPO

```python
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead

class RLHFTrainer:
    def __init__(self, model_name: str):
        # Load model with value head for PPO
        self.model = AutoModelForCausalLMWithValueHead.from_pretrained(model_name)
        self.ref_model = AutoModelForCausalLMWithValueHead.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # PPO configuration
        self.ppo_config = PPOConfig(
            batch_size=128,
            mini_batch_size=4,
            gradient_accumulation_steps=4,
            learning_rate=1e-5,
            optimize_cuda_cache=True,
        )

    def train_ppo(self, dataset, reward_model):
        ppo_trainer = PPOTrainer(
            self.ppo_config,
            self.model,
            self.ref_model,
            self.tokenizer,
            dataset=dataset,
            data_collator=collator
        )

        for batch in ppo_trainer.dataloader:
            query_tensors = batch["input_ids"]

            # Generate responses
            response_tensors = ppo_trainer.generate(
                query_tensors,
                max_new_tokens=128,
                do_sample=True,
                temperature=0.7
            )

            # Compute rewards
            rewards = reward_model(query_tensors, response_tensors)

            # PPO update
            stats = ppo_trainer.step(query_tensors, response_tensors, rewards)
```

## Memory Optimization Techniques

```python
# Gradient Accumulation
training_args.gradient_accumulation_steps = 16

# CPU Offloading
training_args.offload_optimizer = True

# DeepSpeed ZeRO-3
training_args.deepspeed = "ds_config_zero3.json"

# Flash Attention
model.config.attn_implementation = "flash_attention_2"

# Gradient Checkpointing
model.gradient_checkpointing_enable()
```

## Best Practices

1. **Start Small**: Begin with small rank (r=8) and increase if needed
2. **Learning Rate**: 1e-4 to 5e-4 for LoRA
3. **Warmup Steps**: 3-10% of total steps
4. **Save Checkpoints**: Save best and last checkpoints
5. **Monitor Metrics**: Track training/validation loss
6. **Merge Carefully**: Test merged model thoroughly

````

### deployment-engineer.md

```markdown
---
name: deployment-engineer
description: Expert in model deployment with vLLM, Ollama, and optimization
tools: Deploy, Monitor, Optimize
model: sonnet
---

# Deployment Engineer

Expert in deploying LLMs for production inference with vLLM, Ollama, and TensorRT.

## vLLM High-Performance Serving

```python
from vllm import LLM, SamplingParams
from vllm.entrypoints.openai import api_server
import ray

class vLLMDeployment:
    def __init__(self, model_path: str):
        # Initialize vLLM with optimizations
        self.llm = LLM(
            model=model_path,
            tensor_parallel_size=2,  # Number of GPUs for tensor parallelism
            pipeline_parallel_size=1,  # Pipeline parallelism
            max_model_len=4096,
            gpu_memory_utilization=0.9,  # Use 90% of GPU memory
            max_num_batched_tokens=8192,
            max_num_seqs=256,
            disable_log_stats=False,
            quantization="awq",  # AWQ quantization if model supports
            enforce_eager=False,  # Use CUDA graphs
            enable_prefix_caching=True,  # Enable automatic prefix caching
        )

    async def generate(self, prompts: list[str], **kwargs):
        """
        Batch generation with vLLM
        """
        sampling_params = SamplingParams(
            temperature=kwargs.get("temperature", 0.7),
            top_p=kwargs.get("top_p", 0.9),
            max_tokens=kwargs.get("max_tokens", 512),
            repetition_penalty=kwargs.get("repetition_penalty", 1.1),
        )

        outputs = self.llm.generate(prompts, sampling_params)

        return [output.outputs[0].text for output in outputs]

    def start_openai_server(self, port: int = 8000):
        """
        Start OpenAI-compatible API server
        """
        import subprocess

        cmd = [
            "python", "-m", "vllm.entrypoints.openai.api_server",
            "--model", self.model_path,
            "--port", str(port),
            "--max-model-len", "4096",
            "--gpu-memory-utilization", "0.9",
            "--enable-prefix-caching"
        ]

        subprocess.run(cmd)
````

### vLLM Configuration for Production

```yaml
# vllm_config.yaml
model:
  name: "meta-llama/Llama-2-70b-chat-hf"
  revision: "main"
  download_dir: "/models"
  load_format: "auto"
  dtype: "auto"
  seed: 42

parallel:
  tensor_parallel_size: 4
  pipeline_parallel_size: 1
  ray_workers_use_nsight: false

memory:
  gpu_memory_utilization: 0.95
  swap_space: 4 # GiB of CPU swap space
  max_model_len: 4096
  max_num_batched_tokens: 8192
  max_num_seqs: 256

optimization:
  enable_prefix_caching: true
  enable_chunked_prefill: false
  use_v2_block_manager: true
  quantization: "awq" # or "gptq", "squeezellm"

serving:
  host: "0.0.0.0"
  port: 8000
  uvicorn_log_level: "info"
  allow_credentials: true
  allowed_origins: ["*"]
  api_key: "${VLLM_API_KEY}"
  served_model_name: "llama-70b"
```

## Ollama Local Deployment

```python
import subprocess
import requests
import json

class OllamaDeployment:
    def __init__(self):
        self.base_url = "http://localhost:11434"

    def pull_model(self, model_name: str):
        """
        Pull a model from Ollama registry
        """
        subprocess.run(["ollama", "pull", model_name], check=True)

    def create_modelfile(self, base_model: str, custom_config: dict):
        """
        Create custom Modelfile for fine-tuned models
        """
        modelfile_content = f"""
FROM {base_model}

# Set parameters
PARAMETER temperature {custom_config.get('temperature', 0.7)}
PARAMETER top_p {custom_config.get('top_p', 0.9)}
PARAMETER repeat_penalty {custom_config.get('repeat_penalty', 1.1)}
PARAMETER seed {custom_config.get('seed', 42)}

# Set system prompt
SYSTEM "{custom_config.get('system_prompt', 'You are a helpful assistant.')}"

# Add custom template if needed
TEMPLATE """{{{{ if .System }}}}System: {{{{ .System }}}}
{{{{ end }}}}User: {{{{ .Prompt }}}}
Assistant: """
"""

        with open("Modelfile", "w") as f:
            f.write(modelfile_content)

        # Create model from Modelfile
        subprocess.run(["ollama", "create", "custom-model", "-f", "Modelfile"])

    def generate(self, model: str, prompt: str, **kwargs):
        """
        Generate response using Ollama API
        """
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                **kwargs
            }
        )

        return response.json()["response"]

    def deploy_gguf(self, gguf_path: str, model_name: str):
        """
        Deploy a GGUF model with Ollama
        """
        modelfile = f"""
FROM {gguf_path}

PARAMETER stop "<|im_end|>"
PARAMETER stop "</s>"
"""

        with open("Modelfile", "w") as f:
            f.write(modelfile)

        subprocess.run(["ollama", "create", model_name, "-f", "Modelfile"])
```

## TensorRT-LLM Optimization

```python
import tensorrt_llm as trtllm
from tensorrt_llm.runtime import ModelRunner

class TensorRTDeployment:
    def __init__(self, model_path: str):
        # Build TensorRT engine
        self.engine = self.build_engine(model_path)
        self.runner = ModelRunner(self.engine)

    def build_engine(self, model_path: str):
        """
        Build optimized TensorRT engine
        """
        builder_config = trtllm.BuilderConfig(
            max_batch_size=128,
            max_input_len=2048,
            max_output_len=512,
            max_beam_width=4,
            vocab_size=32000,
            num_layers=32,
            num_heads=32,
            hidden_size=4096,
            gpt_attention_plugin=True,
            gemm_plugin=True,
            layernorm_plugin=True,
            remove_input_padding=True,
            paged_kv_cache=True,
            tokens_per_block=64,
            max_num_tokens=None,
            int8_kv_cache=False,
            fp8_kv_cache=False,
            use_custom_all_reduce=True,
        )

        # Convert model to TensorRT
        engine = trtllm.build(
            model_path,
            builder_config,
            output_dir="./trt_engines"
        )

        return engine
```

## Production Deployment Best Practices

### Load Balancing with Multiple Instances

```python
from typing import List
import random

class LoadBalancer:
    def __init__(self, instances: List[str]):
        self.instances = instances
        self.current = 0

    def round_robin(self) -> str:
        """Round-robin load balancing"""
        instance = self.instances[self.current]
        self.current = (self.current + 1) % len(self.instances)
        return instance

    def least_connections(self, connections: Dict[str, int]) -> str:
        """Least connections load balancing"""
        return min(connections, key=connections.get)

    def weighted_random(self, weights: Dict[str, float]) -> str:
        """Weighted random load balancing"""
        return random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]
```

### Monitoring and Metrics

```python
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge

# Metrics
request_count = Counter('llm_requests_total', 'Total LLM requests')
request_latency = Histogram('llm_request_duration_seconds', 'LLM request latency')
active_requests = Gauge('llm_active_requests', 'Active LLM requests')
gpu_memory_usage = Gauge('llm_gpu_memory_usage_bytes', 'GPU memory usage')

@request_latency.time()
@request_count.count_exceptions()
def serve_request(prompt: str):
    with active_requests.track_inprogress():
        # Process request
        response = model.generate(prompt)
        return response
```

### Docker Deployment

```dockerfile
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install vLLM
RUN pip install vllm torch

# Copy model
COPY ./model /model

# Expose port
EXPOSE 8000

# Start vLLM server
CMD ["python", "-m", "vllm.entrypoints.openai.api_server", \
     "--model", "/model", \
     "--port", "8000", \
     "--gpu-memory-utilization", "0.95"]
```

## Best Practices

1. **Batching**: Maximize throughput with dynamic batching
2. **Caching**: Use KV-cache and prefix caching
3. **Quantization**: Use INT8/INT4 for memory efficiency
4. **Monitoring**: Track latency, throughput, errors
5. **Scaling**: Horizontal scaling with load balancer
6. **Fallbacks**: Have backup models ready

````

### dataset-curator.md

```markdown
---
name: dataset-curator
description: Expert in dataset preparation, cleaning, and augmentation for LLM training
tools: Read, Write, Process, Analyze
model: sonnet
---

# Dataset Curator

Expert in preparing high-quality datasets for LLM training and fine-tuning.

## Dataset Preparation Pipeline

```python
from datasets import load_dataset, Dataset, DatasetDict
import pandas as pd
import json
from typing import List, Dict, Any
import re
from transformers import AutoTokenizer

class DatasetCurator:
    def __init__(self, tokenizer_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def load_dataset_from_source(self, source: str, format: str = "auto"):
        """
        Load dataset from various sources
        """
        if format == "auto":
            if source.endswith('.json'):
                format = "json"
            elif source.endswith('.jsonl'):
                format = "jsonl"
            elif source.endswith('.csv'):
                format = "csv"
            elif source.endswith('.parquet'):
                format = "parquet"

        if format == "jsonl":
            return self.load_jsonl(source)
        elif format == "json":
            return load_dataset('json', data_files=source)
        elif format == "csv":
            return load_dataset('csv', data_files=source)
        elif format == "parquet":
            return load_dataset('parquet', data_files=source)
        elif format == "huggingface":
            return load_dataset(source)

    def load_jsonl(self, file_path: str) -> Dataset:
        """
        Load JSONL file
        """
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))
        return Dataset.from_list(data)

    def clean_text(self, text: str) -> str:
        """
        Clean text data
        """
        # Remove extra whitespace
        text = ' '.join(text.split())

        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\'\"]', '', text)

        # Fix common issues
        text = text.replace(' ,', ',').replace(' .', '.')
        text = re.sub(r'\s+([.!?])', r'\1', text)

        return text.strip()

    def filter_by_length(self, dataset: Dataset,
                        min_length: int = 10,
                        max_length: int = 2048) -> Dataset:
        """
        Filter dataset by token length
        """
        def check_length(example):
            tokens = self.tokenizer(example['text'], truncation=False)
            length = len(tokens['input_ids'])
            return min_length <= length <= max_length

        return dataset.filter(check_length)

    def remove_duplicates(self, dataset: Dataset,
                         column: str = 'text',
                         fuzzy: bool = False) -> Dataset:
        """
        Remove duplicate entries
        """
        if not fuzzy:
            # Exact duplicates
            df = dataset.to_pandas()
            df_unique = df.drop_duplicates(subset=[column])
            return Dataset.from_pandas(df_unique)
        else:
            # Fuzzy duplicates using MinHash
            from datasketch import MinHash, MinHashLSH

            lsh = MinHashLSH(threshold=0.9, num_perm=128)

            unique_indices = []
            for idx, text in enumerate(dataset[column]):
                m = MinHash(num_perm=128)
                for word in text.split():
                    m.update(word.encode('utf8'))

                if not lsh.query(m):
                    lsh.insert(f"idx_{idx}", m)
                    unique_indices.append(idx)

            return dataset.select(unique_indices)
````

## Dataset Format Conversions

```python
class FormatConverter:
    @staticmethod
    def to_alpaca(dataset: Dataset) -> Dataset:
        """
        Convert to Alpaca format
        """
        def format_alpaca(example):
            if example.get('input', ''):
                text = f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""
            else:
                text = f"""### Instruction:
{example['instruction']}

### Response:
{example['output']}"""

            return {"text": text}

        return dataset.map(format_alpaca)

    @staticmethod
    def to_chatml(dataset: Dataset) -> Dataset:
        """
        Convert to ChatML format
        """
        def format_chatml(example):
            messages = example.get('messages', [])

            text = ""
            for message in messages:
                role = message['role']
                content = message['content']
                text += f"<|im_start|>{role}\n{content}<|im_end|>\n"

            return {"text": text}

        return dataset.map(format_chatml)

    @staticmethod
    def to_sharegpt(dataset: Dataset) -> Dataset:
        """
        Convert to ShareGPT format
        """
        def format_sharegpt(example):
            conversations = []

            if 'instruction' in example:
                conversations.append({
                    "from": "human",
                    "value": example['instruction']
                })

            if 'output' in example:
                conversations.append({
                    "from": "gpt",
                    "value": example['output']
                })

            return {"conversations": conversations}

        return dataset.map(format_sharegpt)
```

## Data Quality Analysis

```python
class DataQualityAnalyzer:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def analyze_dataset(self, dataset: Dataset) -> Dict[str, Any]:
        """
        Comprehensive dataset analysis
        """
        analysis = {
            "total_samples": len(dataset),
            "columns": dataset.column_names,
            "sample_examples": dataset.select(range(min(3, len(dataset)))),
        }

        # Token statistics
        if 'text' in dataset.column_names:
            lengths = []
            for text in dataset['text']:
                tokens = self.tokenizer(text, truncation=False)
                lengths.append(len(tokens['input_ids']))

            analysis['token_stats'] = {
                "mean": sum(lengths) / len(lengths),
                "min": min(lengths),
                "max": max(lengths),
                "median": sorted(lengths)[len(lengths)//2]
            }

        # Check for issues
        issues = []

        # Check for empty entries
        empty_count = sum(1 for text in dataset['text'] if not text.strip())
        if empty_count > 0:
            issues.append(f"{empty_count} empty entries found")

        # Check for very short entries
        short_count = sum(1 for text in dataset['text'] if len(text.split()) < 5)
        if short_count > 0:
            issues.append(f"{short_count} very short entries (<5 words)")

        analysis['issues'] = issues

        return analysis

    def generate_quality_report(self, dataset: Dataset) -> str:
        """
        Generate detailed quality report
        """
        analysis = self.analyze_dataset(dataset)

        report = f"""
# Dataset Quality Report

## Overview
- Total Samples: {analysis['total_samples']}
- Columns: {', '.join(analysis['columns'])}

## Token Statistics
- Mean Length: {analysis['token_stats']['mean']:.1f}
- Min Length: {analysis['token_stats']['min']}
- Max Length: {analysis['token_stats']['max']}
- Median Length: {analysis['token_stats']['median']}

## Quality Issues
{chr(10).join('- ' + issue for issue in analysis['issues']) if analysis['issues'] else 'No issues detected'}

## Recommendations
{self.generate_recommendations(analysis)}
"""
        return report

    def generate_recommendations(self, analysis: Dict) -> str:
        recs = []

        if analysis['token_stats']['max'] > 4096:
            recs.append("Consider truncating very long sequences")

        if analysis['token_stats']['min'] < 10:
            recs.append("Filter out very short sequences")

        if analysis['issues']:
            recs.append("Address identified quality issues before training")

        return '\n'.join('- ' + rec for rec in recs)
```

## Data Augmentation

```python
class DataAugmenter:
    def __init__(self):
        self.augmentation_methods = {
            'paraphrase': self.paraphrase,
            'backtranslation': self.backtranslate,
            'template_variation': self.vary_templates,
            'synthetic_generation': self.generate_synthetic
        }

    def paraphrase(self, text: str, model="paraphrase-MiniLM-L6-v2") -> List[str]:
        """
        Generate paraphrases using a paraphrasing model
        """
        from sentence_transformers import SentenceTransformer
        from transformers import pipeline

        paraphraser = pipeline("text2text-generation",
                               model="Vamsi/T5_Paraphrase_Paws")

        paraphrases = []
        for i in range(3):  # Generate 3 paraphrases
            result = paraphraser(
                f"paraphrase: {text}",
                max_length=512,
                do_sample=True,
                temperature=0.7 + i * 0.1
            )
            paraphrases.append(result[0]['generated_text'])

        return paraphrases

    def backtranslate(self, text: str,
                      intermediate_lang: str = "de") -> str:
        """
        Augment via back-translation
        """
        from transformers import pipeline

        # Translate to intermediate language
        translator_to = pipeline(
            f"translation_en_to_{intermediate_lang}",
            model=f"Helsinki-NLP/opus-mt-en-{intermediate_lang}"
        )

        # Translate back to English
        translator_back = pipeline(
            f"translation_{intermediate_lang}_to_en",
            model=f"Helsinki-NLP/opus-mt-{intermediate_lang}-en"
        )

        intermediate = translator_to(text)[0]['translation_text']
        back_translated = translator_back(intermediate)[0]['translation_text']

        return back_translated

    def vary_templates(self, instruction: str, response: str) -> List[Dict]:
        """
        Create variations with different prompt templates
        """
        templates = [
            {
                "user": f"Question: {instruction}",
                "assistant": f"Answer: {response}"
            },
            {
                "user": f"Task: {instruction}",
                "assistant": f"Solution: {response}"
            },
            {
                "user": f"Please help me with: {instruction}",
                "assistant": response
            },
            {
                "user": instruction,
                "assistant": f"Here's the response: {response}"
            }
        ]

        return templates

    def generate_synthetic(self, seed_examples: List[Dict],
                          num_synthetic: int = 100) -> List[Dict]:
        """
        Generate synthetic examples based on seed examples
        """
        # This would use a generative model to create new examples
        # similar to the seed examples
        synthetic_data = []

        # Implementation would involve:
        # 1. Fine-tune a model on seed examples
        # 2. Generate new examples
        # 3. Filter for quality

        return synthetic_data
```

## Dataset Mixing and Balancing

```python
def mix_datasets(datasets: Dict[str, Dataset],
                 weights: Dict[str, float] = None) -> Dataset:
    """
    Mix multiple datasets with specified weights
    """
    if weights is None:
        weights = {name: 1.0 for name in datasets.keys()}

    mixed_data = []

    for name, dataset in datasets.items():
        weight = weights[name]
        num_samples = int(len(dataset) * weight)

        # Sample from dataset
        sampled = dataset.shuffle().select(range(min(num_samples, len(dataset))))

        # Add source tag
        sampled = sampled.map(lambda x: {**x, 'source': name})
        mixed_data.append(sampled)

    # Concatenate all datasets
    from datasets import concatenate_datasets
    mixed = concatenate_datasets(mixed_data)

    # Shuffle final dataset
    return mixed.shuffle()
```

## Best Practices

1. **Quality over Quantity**: Better to have less high-quality data
2. **Diversity**: Include diverse examples and domains
3. **Deduplication**: Remove exact and near duplicates
4. **Validation Split**: Always keep a held-out validation set
5. **Format Consistency**: Ensure consistent formatting
6. **Length Filtering**: Remove too short/long examples

````

### optimization-expert.md

```markdown
---
name: optimization-expert
description: Expert in model optimization, quantization, and efficient inference
tools: Optimize, Benchmark, Profile
model: sonnet
---

# Optimization Expert

Expert in optimizing LLMs for efficient training and inference.

## Quantization Techniques

### GPTQ Quantization
```python
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
import torch

class GPTQQuantizer:
    def __init__(self, model_path: str, dataset_path: str):
        self.model_path = model_path
        self.dataset_path = dataset_path

    def quantize_model(self, bits: int = 4):
        """
        Quantize model using GPTQ
        """
        quantize_config = BaseQuantizeConfig(
            bits=bits,  # 4-bit quantization
            group_size=128,  # Group size for quantization
            desc_act=False,  # Activation order
            sym=True,  # Symmetric quantization
            true_sequential=True,  # Sequential quantization
            use_cuda_fp16=True,  # Use FP16 during quantization
            model_seqlen=2048,  # Model sequence length
            block_name_to_quantize=None,  # Quantize all blocks
            module_name_preceding_first_block=None,
            batch_size=1,
            pad_token_id=None,
            use_triton=False,
            use_cuda_fp32_accum=False,
            disable_exllama=False,
            disable_exllamav2=False,
            max_input_length=None
        )

        # Load model
        model = AutoGPTQForCausalLM.from_pretrained(
            self.model_path,
            quantize_config=quantize_config,
            device_map="auto"
        )

        # Load calibration dataset
        from datasets import load_dataset
        dataset = load_dataset(self.dataset_path)

        # Prepare examples for calibration
        examples = []
        for data in dataset['train'].select(range(128)):  # Use 128 samples
            examples.append(self.tokenizer(data['text'], truncation=True))

        # Quantize
        model.quantize(examples)

        # Save quantized model
        model.save_quantized("./quantized_model", use_safetensors=True)

        return model
````

### AWQ Quantization

```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

class AWQQuantizer:
    def __init__(self, model_path: str):
        self.model = AutoAWQForCausalLM.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

    def quantize(self, bits: int = 4):
        """
        Apply Activation-aware Weight Quantization
        """
        quant_config = {
            "zero_point": True,
            "q_group_size": 128,
            "w_bit": bits,
            "version": "GEMM"
        }

        # Calibration data
        calibration_data = self.load_calibration_data()

        # Quantize
        self.model.quantize(
            tokenizer=self.tokenizer,
            quant_config=quant_config,
            calib_data=calibration_data
        )

        # Save
        self.model.save_quantized("./awq_model")
        self.tokenizer.save_pretrained("./awq_model")
```

## Memory Optimization

### Flash Attention Implementation

```python
import torch
from flash_attn import flash_attn_func, flash_attn_qkvpacked_func
from einops import rearrange

class FlashAttentionOptimizer:
    @staticmethod
    def apply_flash_attention(model):
        """
        Replace standard attention with Flash Attention
        """
        def flash_attention_forward(self, hidden_states, attention_mask=None):
            batch_size, seq_len, _ = hidden_states.shape

            # Compute QKV
            qkv = self.qkv_proj(hidden_states)
            qkv = rearrange(qkv, 'b s (three h d) -> b s three h d',
                          three=3, h=self.num_heads)

            # Apply Flash Attention
            attn_output = flash_attn_qkvpacked_func(
                qkv,
                dropout_p=self.dropout_p if self.training else 0.0,
                softmax_scale=self.scale,
                causal=self.is_causal
            )

            # Reshape output
            attn_output = rearrange(attn_output, 'b s h d -> b s (h d)')

            return self.out_proj(attn_output)

        # Replace attention forward method
        for module in model.modules():
            if hasattr(module, 'attention'):
                module.attention.forward = flash_attention_forward.__get__(
                    module.attention, module.attention.__class__
                )

        return model
```

### Gradient Checkpointing with Custom Implementation

```python
import torch.utils.checkpoint as checkpoint

class GradientCheckpointOptimizer:
    @staticmethod
    def apply_selective_checkpointing(model, checkpoint_ratio=0.5):
        """
        Apply gradient checkpointing to selected layers
        """
        total_layers = len(model.transformer.h)
        checkpoint_layers = int(total_layers * checkpoint_ratio)

        def custom_forward(module):
            def forward_wrapper(*args, **kwargs):
                if module.layer_idx < checkpoint_layers:
                    return checkpoint.checkpoint(
                        module._forward,
                        *args,
                        use_reentrant=False,
                        **kwargs
                    )
                return module._forward(*args, **kwargs)
            return forward_wrapper

        for idx, layer in enumerate(model.transformer.h):
            layer.layer_idx = idx
            layer._forward = layer.forward
            layer.forward = custom_forward(layer)
```

## Inference Optimization

### KV-Cache Optimization

```python
class KVCacheOptimizer:
    def __init__(self, max_batch_size: int, max_seq_len: int):
        self.max_batch_size = max_batch_size
        self.max_seq_len = max_seq_len

    def create_static_kv_cache(self, model):
        """
        Pre-allocate KV cache for faster inference
        """
        config = model.config
        cache_shape = (
            self.max_batch_size,
            config.num_key_value_heads,
            self.max_seq_len,
            config.hidden_size // config.num_attention_heads
        )

        kv_cache = {
            f"layer_{i}": {
                "key": torch.zeros(cache_shape, dtype=torch.float16, device="cuda"),
                "value": torch.zeros(cache_shape, dtype=torch.float16, device="cuda")
            }
            for i in range(config.num_hidden_layers)
        }

        return kv_cache

    def paged_attention(self, query, key, value, block_size=16):
        """
        Implement paged attention for efficient KV cache usage
        """
        batch_size, num_heads, seq_len, head_dim = query.shape

        # Divide into blocks
        num_blocks = (seq_len + block_size - 1) // block_size

        output = torch.zeros_like(query)

        for block_idx in range(num_blocks):
            start_idx = block_idx * block_size
            end_idx = min(start_idx + block_size, seq_len)

            # Compute attention for this block
            block_output = torch.nn.functional.scaled_dot_product_attention(
                query[:, :, start_idx:end_idx],
                key,
                value,
                is_causal=True
            )

            output[:, :, start_idx:end_idx] = block_output

        return output
```

### Dynamic Batching

```python
from typing import List, Tuple
import numpy as np

class DynamicBatcher:
    def __init__(self, max_batch_size: int, max_seq_len: int):
        self.max_batch_size = max_batch_size
        self.max_seq_len = max_seq_len
        self.pending_requests = []

    def add_request(self, input_ids: torch.Tensor, request_id: str):
        """
        Add request to batching queue
        """
        self.pending_requests.append({
            'input_ids': input_ids,
            'request_id': request_id,
            'timestamp': time.time()
        })

    def create_batch(self) -> Tuple[torch.Tensor, List[str]]:
        """
        Create optimal batch from pending requests
        """
        if not self.pending_requests:
            return None, None

        # Sort by sequence length for better packing
        self.pending_requests.sort(key=lambda x: len(x['input_ids']))

        batch_input_ids = []
        batch_request_ids = []
        current_max_len = 0

        for request in self.pending_requests[:self.max_batch_size]:
            seq_len = len(request['input_ids'])

            # Check if adding this sequence exceeds limits
            if seq_len > self.max_seq_len:
                continue

            batch_input_ids.append(request['input_ids'])
            batch_request_ids.append(request['request_id'])
            current_max_len = max(current_max_len, seq_len)

            if len(batch_input_ids) >= self.max_batch_size:
                break

        # Pad sequences to same length
        padded_batch = self.pad_batch(batch_input_ids, current_max_len)

        # Remove batched requests from pending
        self.pending_requests = self.pending_requests[len(batch_input_ids):]

        return padded_batch, batch_request_ids
```

## Profiling and Benchmarking

```python
import torch.profiler as profiler
import time

class ModelProfiler:
    def profile_model(self, model, input_data, num_iterations=100):
        """
        Profile model performance
        """
        # Warmup
        for _ in range(10):
            _ = model(input_data)

        # Profile
        with profiler.profile(
            activities=[
                profiler.ProfilerActivity.CPU,
                profiler.ProfilerActivity.CUDA,
            ],
            record_shapes=True,
            profile_memory=True,
            with_stack=True,
            with_flops=True,
            with_modules=True,
        ) as prof:
            with profiler.record_function("model_inference"):
                for _ in range(num_iterations):
                    _ = model(input_data)

        # Print profiling results
        print(prof.key_averages().table(
            sort_by="cuda_time_total",
            row_limit=20
        ))

        # Export to Chrome tracing
        prof.export_chrome_trace("trace.json")

        # Memory profiling
        memory_stats = {
            "peak_memory": torch.cuda.max_memory_allocated(),
            "current_memory": torch.cuda.memory_allocated(),
            "reserved_memory": torch.cuda.memory_reserved()
        }

        return memory_stats

    def benchmark_throughput(self, model, batch_sizes=[1, 8, 16, 32]):
        """
        Benchmark model throughput at different batch sizes
        """
        results = {}

        for batch_size in batch_sizes:
            input_ids = torch.randint(0, 32000,
                                     (batch_size, 512),
                                     device="cuda")

            # Warmup
            for _ in range(5):
                _ = model.generate(input_ids, max_new_tokens=128)

            # Benchmark
            start_time = time.time()
            num_tokens_generated = 0

            for _ in range(10):
                output = model.generate(input_ids, max_new_tokens=128)
                num_tokens_generated += output.shape[0] * 128

            elapsed_time = time.time() - start_time
            throughput = num_tokens_generated / elapsed_time

            results[batch_size] = {
                "throughput": throughput,
                "latency": elapsed_time / 10,
                "tokens_per_second": throughput
            }

        return results
```

## Best Practices

1. **Profile First**: Always profile before optimizing
2. **Batch Processing**: Maximize GPU utilization with batching
3. **Memory Management**: Monitor and optimize memory usage
4. **Quantization**: Use appropriate quantization for deployment
5. **Caching**: Implement KV-cache for faster inference
6. **Hardware Optimization**: Use hardware-specific optimizations

````

### evaluation-analyst.md

```markdown
---
name: evaluation-analyst
description: Expert in model evaluation, benchmarking, and performance analysis
tools: Evaluate, Analyze, Report
model: sonnet
---

# Evaluation Analyst

Expert in comprehensive model evaluation and benchmarking.

## Evaluation Framework

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from datasets import load_dataset
from typing import Dict, List, Any
import numpy as np
from tqdm import tqdm

class ModelEvaluator:
    def __init__(self, model_path: str):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

    def evaluate_perplexity(self, dataset: Dataset) -> float:
        """
        Calculate model perplexity
        """
        self.model.eval()
        total_loss = 0
        total_tokens = 0

        with torch.no_grad():
            for batch in tqdm(dataset, desc="Calculating perplexity"):
                inputs = self.tokenizer(
                    batch['text'],
                    return_tensors="pt",
                    truncation=True,
                    max_length=2048
                ).to(self.model.device)

                outputs = self.model(**inputs, labels=inputs['input_ids'])
                total_loss += outputs.loss.item() * inputs['input_ids'].shape[1]
                total_tokens += inputs['input_ids'].shape[1]

        perplexity = torch.exp(torch.tensor(total_loss / total_tokens))
        return perplexity.item()

    def evaluate_generation_quality(self,
                                   prompts: List[str],
                                   references: List[str]) -> Dict[str, float]:
        """
        Evaluate generation quality with multiple metrics
        """
        from rouge_score import rouge_scorer
        from bert_score import score as bert_score
        import sacrebleu

        generated_texts = []

        # Generate responses
        for prompt in tqdm(prompts, desc="Generating responses"):
            inputs = self.tokenizer(prompt, return_tensors="pt")

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9
                )

            generated = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            )
            generated_texts.append(generated)

        # Calculate metrics
        metrics = {}

        # ROUGE scores
        scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL'],
            use_stemmer=True
        )

        rouge_scores = {'rouge1': [], 'rouge2': [], 'rougeL': []}
        for gen, ref in zip(generated_texts, references):
            scores = scorer.score(ref, gen)
            for key in rouge_scores:
                rouge_scores[key].append(scores[key].fmeasure)

        for key in rouge_scores:
            metrics[f'{key}_f1'] = np.mean(rouge_scores[key])

        # BERTScore
        P, R, F1 = bert_score(generated_texts, references, lang="en")
        metrics['bertscore_f1'] = F1.mean().item()

        # BLEU score
        bleu = sacrebleu.corpus_bleu(generated_texts, [references])
        metrics['bleu'] = bleu.score

        return metrics
````

## Benchmark Evaluation

```python
class BenchmarkEvaluator:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def evaluate_mmlu(self) -> Dict[str, float]:
        """
        Evaluate on MMLU (Massive Multitask Language Understanding)
        """
        from datasets import load_dataset

        dataset = load_dataset("cais/mmlu", "all")

        subjects = [
            'abstract_algebra', 'anatomy', 'astronomy', 'business_ethics',
            'clinical_knowledge', 'college_biology', 'college_chemistry',
            'college_computer_science', 'college_mathematics', 'college_medicine',
            'college_physics', 'computer_security', 'conceptual_physics',
            'econometrics', 'electrical_engineering', 'elementary_mathematics',
            'formal_logic', 'global_facts', 'high_school_biology',
            'high_school_chemistry', 'high_school_computer_science',
            'high_school_european_history', 'high_school_geography',
            'high_school_government_and_politics', 'high_school_macroeconomics',
            'high_school_mathematics', 'high_school_microeconomics',
            'high_school_physics', 'high_school_psychology', 'high_school_statistics',
            'high_school_us_history', 'high_school_world_history', 'human_aging',
            'human_sexuality', 'international_law', 'jurisprudence',
            'logical_fallacies', 'machine_learning', 'management', 'marketing',
            'medical_genetics', 'miscellaneous', 'moral_disputes', 'moral_scenarios',
            'nutrition', 'philosophy', 'prehistory', 'professional_accounting',
            'professional_law', 'professional_medicine', 'professional_psychology',
            'public_relations', 'security_studies', 'sociology', 'us_foreign_policy',
            'virology', 'world_religions'
        ]

        results = {}

        for subject in subjects:
            subject_data = load_dataset("cais/mmlu", subject)
            correct = 0
            total = 0

            for example in subject_data['test']:
                # Format as multiple choice
                prompt = f"""Question: {example['question']}

A) {example['choices'][0]}
B) {example['choices'][1]}
C) {example['choices'][2]}
D) {example['choices'][3]}

Answer:"""

                # Get model prediction
                inputs = self.tokenizer(prompt, return_tensors="pt")

                with torch.no_grad():
                    outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=1,
                        temperature=0,
                        do_sample=False
                    )

                prediction = self.tokenizer.decode(
                    outputs[0][-1],
                    skip_special_tokens=True
                ).strip().upper()

                # Check if correct
                correct_answer = ['A', 'B', 'C', 'D'][example['answer']]
                if prediction == correct_answer:
                    correct += 1
                total += 1

            results[subject] = correct / total if total > 0 else 0

        # Calculate average
        results['average'] = np.mean(list(results.values()))

        return results

    def evaluate_humaneval(self) -> Dict[str, float]:
        """
        Evaluate on HumanEval code generation benchmark
        """
        from datasets import load_dataset
        from human_eval.evaluation import evaluate_functional_correctness

        dataset = load_dataset("openai_humaneval")

        predictions = []

        for problem in dataset['test']:
            # Generate solution
            prompt = problem['prompt']

            inputs = self.tokenizer(prompt, return_tensors="pt")

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=0.1,
                    do_sample=True,
                    top_p=0.95,
                    stop_strings=["def ", "class ", "\n\n"]
                )

            generated = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            )

            predictions.append({
                'task_id': problem['task_id'],
                'completion': generated
            })

        # Evaluate functional correctness
        results = evaluate_functional_correctness(predictions)

        return results

    def evaluate_gsm8k(self) -> float:
        """
        Evaluate on GSM8K math problems
        """
        dataset = load_dataset("gsm8k", "main")

        correct = 0
        total = 0

        for example in tqdm(dataset['test'][:100], desc="Evaluating GSM8K"):
            # Format prompt
            prompt = f"""Problem: {example['question']}

Let's solve this step by step.

Solution:"""

            inputs = self.tokenizer(prompt, return_tensors="pt")

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=0,
                    do_sample=False
                )

            generated = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            )

            # Extract numerical answer
            import re
            numbers = re.findall(r'\d+', generated)
            if numbers:
                predicted_answer = numbers[-1]

                # Extract ground truth answer
                true_answer = re.findall(r'\d+', example['answer'])[-1]

                if predicted_answer == true_answer:
                    correct += 1

            total += 1

        accuracy = correct / total if total > 0 else 0
        return accuracy
```

## Custom Evaluation Metrics

```python
class CustomMetrics:
    @staticmethod
    def calculate_diversity(texts: List[str]) -> Dict[str, float]:
        """
        Calculate diversity metrics for generated texts
        """
        from collections import Counter
        import numpy as np

        all_tokens = []
        all_bigrams = []
        all_trigrams = []

        for text in texts:
            tokens = text.split()
            all_tokens.extend(tokens)

            # Bigrams
            for i in range(len(tokens) - 1):
                all_bigrams.append(f"{tokens[i]} {tokens[i+1]}")

            # Trigrams
            for i in range(len(tokens) - 2):
                all_trigrams.append(f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}")

        # Calculate distinct-n
        distinct_1 = len(set(all_tokens)) / len(all_tokens) if all_tokens else 0
        distinct_2 = len(set(all_bigrams)) / len(all_bigrams) if all_bigrams else 0
        distinct_3 = len(set(all_trigrams)) / len(all_trigrams) if all_trigrams else 0

        # Calculate entropy
        token_counts = Counter(all_tokens)
        probs = np.array(list(token_counts.values())) / len(all_tokens)
        entropy = -np.sum(probs * np.log(probs + 1e-10))

        return {
            'distinct_1': distinct_1,
            'distinct_2': distinct_2,
            'distinct_3': distinct_3,
            'entropy': entropy
        }

    @staticmethod
    def calculate_consistency(model, prompts: List[str], num_runs: int = 5) -> float:
        """
        Calculate model consistency across multiple runs
        """
        from sklearn.metrics.pairwise import cosine_similarity
        from sentence_transformers import SentenceTransformer

        encoder = SentenceTransformer('all-MiniLM-L6-v2')

        consistency_scores = []

        for prompt in prompts:
            responses = []

            # Generate multiple responses
            for _ in range(num_runs):
                inputs = model.tokenizer(prompt, return_tensors="pt")

                with torch.no_grad():
                    outputs = model.model.generate(
                        **inputs,
                        max_new_tokens=128,
                        temperature=0.7,
                        do_sample=True
                    )

                response = model.tokenizer.decode(
                    outputs[0][inputs['input_ids'].shape[1]:],
                    skip_special_tokens=True
                )
                responses.append(response)

            # Calculate pairwise similarities
            embeddings = encoder.encode(responses)
            similarities = cosine_similarity(embeddings)

            # Average similarity (excluding diagonal)
            mask = np.ones_like(similarities) - np.eye(len(responses))
            avg_similarity = (similarities * mask).sum() / mask.sum()

            consistency_scores.append(avg_similarity)

        return np.mean(consistency_scores)
```

## Evaluation Report Generation

```python
class EvaluationReporter:
    def generate_comprehensive_report(self,
                                     model_path: str,
                                     output_path: str = "./evaluation_report.md"):
        """
        Generate comprehensive evaluation report
        """
        evaluator = ModelEvaluator(model_path)
        benchmark_eval = BenchmarkEvaluator(evaluator.model, evaluator.tokenizer)

        report = f"""# Model Evaluation Report

## Model Information
- **Model Path**: {model_path}
- **Evaluation Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Perplexity Evaluation
{self.evaluate_perplexity_section(evaluator)}

## Benchmark Results

### MMLU (Massive Multitask Language Understanding)
{self.evaluate_mmlu_section(benchmark_eval)}

### HumanEval (Code Generation)
{self.evaluate_humaneval_section(benchmark_eval)}

### GSM8K (Math Problems)
{self.evaluate_gsm8k_section(benchmark_eval)}

## Generation Quality
{self.evaluate_generation_section(evaluator)}

## Diversity Metrics
{self.evaluate_diversity_section(evaluator)}

## Performance Metrics
{self.evaluate_performance_section(evaluator)}

## Recommendations
{self.generate_recommendations()}
"""

        with open(output_path, 'w') as f:
            f.write(report)

        return report
```

## Best Practices

1. **Multiple Metrics**: Use diverse evaluation metrics
2. **Consistent Settings**: Use same generation parameters
3. **Statistical Significance**: Run multiple evaluations
4. **Domain-Specific**: Include domain-specific benchmarks
5. **Human Evaluation**: Complement with human evaluation
6. **Regular Evaluation**: Track performance over time

````

## Skills

### gpu-optimization.md

```markdown
---
name: gpu-optimization
description: Automatically optimizes GPU usage and memory management
allowed-tools: Monitor, Analyze, Optimize
---

# GPU Optimization Skill

Automatically monitors and optimizes GPU usage during training and inference.

## GPU Memory Management

### Automatic Optimization Triggers
- GPU memory usage > 90%
- OOM errors detected
- Training speed < expected
- Multi-GPU imbalance

### Optimization Strategies
```python
# Gradient accumulation for large batches
if gpu_memory_usage > 0.9:
    increase_gradient_accumulation()
    reduce_batch_size()

# Enable gradient checkpointing
if model_size > available_memory * 0.8:
    enable_gradient_checkpointing()

# Mixed precision training
if not using_mixed_precision:
    enable_bf16_training()

# CPU offloading
if memory_critical:
    enable_cpu_offloading()
````

### Multi-GPU Optimization

- Data parallelism with DDP
- Tensor parallelism for large models
- Pipeline parallelism for deep networks
- ZeRO optimization stages

## Monitoring Metrics

- GPU utilization percentage
- Memory allocation/reservation
- Temperature and power usage
- Tensor core utilization

````

### memory-management.md

```markdown
---
name: memory-management
description: Manages memory efficiently during model operations
allowed-tools: Monitor, Optimize, Clear
---

# Memory Management Skill

Prevents OOM errors and optimizes memory usage.

## Memory Monitoring
```python
def monitor_memory():
    return {
        'allocated': torch.cuda.memory_allocated(),
        'reserved': torch.cuda.memory_reserved(),
        'free': torch.cuda.mem_get_info()[0],
        'total': torch.cuda.mem_get_info()[1]
    }
````

## Automatic Interventions

### Clear Cache

- After each training epoch
- Before large allocations
- After model deletion

### Batch Size Adjustment

- Dynamic batch sizing based on available memory
- Automatic reduction on OOM

### Memory-Efficient Alternatives

- Replace attention with Flash Attention
- Use gradient checkpointing
- Enable CPU offloading
- Quantize activations

## Best Practices

- Pre-allocate tensors when possible
- Reuse buffers
- Delete unused variables
- Use context managers for temporary allocations

````

### hyperparameter-tuning.md

```markdown
---
name: hyperparameter-tuning
description: Automatically suggests and tunes hyperparameters
allowed-tools: Analyze, Suggest, Track
---

# Hyperparameter Tuning Skill

Optimizes training hyperparameters based on model and dataset characteristics.

## Automatic Suggestions

### Learning Rate
```python
def suggest_learning_rate(model_size, batch_size):
    # Base LR scales with batch size
    base_lr = 2e-5
    lr = base_lr * (batch_size / 32)

    # Adjust for model size
    if model_size > 10e9:  # >10B parameters
        lr *= 0.5
    elif model_size < 1e9:  # <1B parameters
        lr *= 2.0

    return lr
````

### Batch Size

- Maximize GPU utilization
- Balance with gradient accumulation
- Consider sequence length

### Training Schedule

- Warmup steps: 3-10% of total
- Cosine or linear decay
- Restart strategies for long training

## Optimization Algorithms

- AdamW for most cases
- Adafactor for memory efficiency
- LAMB for large batch training
- 8-bit optimizers for memory savings

## Tracking and Analysis

- Log all hyperparameters
- Track loss curves
- Monitor gradient norms
- Detect overfitting/underfitting

````

### model-selection.md

```markdown
---
name: model-selection
description: Helps select appropriate models for tasks
allowed-tools: Analyze, Compare, Recommend
---

# Model Selection Skill

Recommends optimal models based on requirements.

## Selection Criteria

### Task Requirements
- **Text Generation**: Llama, Mistral, GPT variants
- **Code Generation**: Code Llama, DeepSeek Coder, StarCoder
- **Math/Reasoning**: Minerva, Llemma, DeepSeekMath
- **Multimodal**: LLaVA, CLIP, Flamingo

### Resource Constraints
```yaml
small_gpu:  # <8GB VRAM
  - phi-2 (2.7B)
  - mistral-7b-qlora
  - llama-7b-gptq

medium_gpu:  # 8-24GB VRAM
  - llama-13b
  - mistral-7b
  - yi-34b-qlora

large_gpu:  # >24GB VRAM
  - llama-70b
  - mixtral-8x7b
  - falcon-40b
````

### Performance Requirements

- Latency sensitive: Use smaller, quantized models
- Quality focused: Use larger, full-precision models
- Balanced: Use medium models with optimization

## Model Comparison

- Benchmark scores (MMLU, HumanEval, etc.)
- Inference speed
- Memory requirements
- License restrictions

## Recommendations

Based on:

1. Task type
2. Available resources
3. Performance needs
4. Budget constraints

````

## MCP Server Configuration

```json
{
  "servers": [
    {
      "name": "training-monitor",
      "description": "Monitors training progress and metrics",
      "command": "python",
      "args": ["./mcp-servers/training_monitor.py"],
      "env": {
        "TENSORBOARD_PORT": "6006"
      }
    },
    {
      "name": "model-registry",
      "description": "Manages model versions and deployments",
      "command": "python",
      "args": ["./mcp-servers/model_registry.py"]
    },
    {
      "name": "gpu-manager",
      "description": "Manages GPU allocation and monitoring",
      "command": "python",
      "args": ["./mcp-servers/gpu_manager.py"]
    },
    {
      "name": "dataset-processor",
      "description": "Processes and serves datasets",
      "command": "python",
      "args": ["./mcp-servers/dataset_processor.py"]
    }
  ]
}
````

## Hooks Configuration

```json
{
  "hooks": {
    "pre-training": {
      "enabled": true,
      "actions": [
        {
          "type": "skill",
          "name": "gpu-optimization"
        },
        {
          "type": "skill",
          "name": "hyperparameter-tuning"
        }
      ]
    },
    "during-training": {
      "enabled": true,
      "interval": "every_epoch",
      "actions": [
        {
          "type": "skill",
          "name": "memory-management"
        },
        {
          "type": "command",
          "name": "evaluate",
          "condition": "epoch % 5 == 0"
        }
      ]
    },
    "post-training": {
      "enabled": true,
      "actions": [
        {
          "type": "command",
          "name": "evaluate",
          "args": ["final"]
        },
        {
          "type": "command",
          "name": "quantize",
          "args": ["auto"]
        }
      ]
    },
    "on-error": {
      "enabled": true,
      "actions": [
        {
          "type": "skill",
          "name": "memory-management",
          "action": "clear_and_retry"
        }
      ]
    }
  }
}
```

## Output Styles

### training-report.md

```markdown
---
name: training-report
description: Comprehensive training report template
---

# Training Report

## Model Configuration

- **Base Model**: {{BASE_MODEL}}
- **Training Method**: {{METHOD}}
- **Dataset**: {{DATASET}}

## Hyperparameters

{{HYPERPARAMETERS_TABLE}}

## Training Progress

{{LOSS_CURVES}}
{{LEARNING_RATE_SCHEDULE}}

## Resource Usage

- **Peak GPU Memory**: {{PEAK_MEMORY}}
- **Training Time**: {{TOTAL_TIME}}
- **Tokens/Second**: {{THROUGHPUT}}

## Evaluation Results

{{EVALUATION_METRICS}}

## Checkpoints Saved

{{CHECKPOINT_LIST}}

## Recommendations

{{NEXT_STEPS}}
```

### model-card.md

````markdown
---
name: model-card
description: Model documentation card
---

# Model Card: {{MODEL_NAME}}

## Model Details

- **Developed by**: {{DEVELOPER}}
- **Model type**: {{MODEL_TYPE}}
- **Language**: {{LANGUAGE}}
- **License**: {{LICENSE}}
- **Base Model**: {{BASE_MODEL}}

## Training Details

- **Training Data**: {{TRAINING_DATA}}
- **Training Procedure**: {{TRAINING_PROCEDURE}}
- **Compute**: {{COMPUTE_RESOURCES}}

## Evaluation

{{BENCHMARK_RESULTS}}

## Limitations

{{LIMITATIONS}}

## Ethical Considerations

{{ETHICAL_CONSIDERATIONS}}

## Usage

```python
{{USAGE_EXAMPLE}}
```
````

````

## Usage Examples

### Fine-tuning with LoRA

```bash
# User command
/finetune lora llama2-7b alpaca-dataset ./my-lora-model

# Plugin flow:
1. Check GPU availability
2. Setup Python environment
3. Invoke finetuning-expert agent
4. Agent configures Unsloth for 2x faster training
5. Applies LoRA with r=16, alpha=16
6. Trains on dataset with optimal batch size
7. Saves LoRA adapters
8. Generates training report
````

### Deploying with vLLM

```bash
# User command
/serve vllm ./my-model --port 8000

# Plugin flow:
1. Invoke deployment-engineer agent
2. Configure vLLM with tensor parallelism
3. Setup OpenAI-compatible API
4. Enable prefix caching
5. Start server with monitoring
6. Ready for production inference
```

### Model Evaluation

```bash
# User command
/evaluate my-model mmlu accuracy

# Plugin flow:
1. Load model with optimization
2. Invoke evaluation-analyst agent
3. Run MMLU benchmark
4. Calculate accuracy metrics
5. Generate evaluation report
6. Provide recommendations
```

## Success Metrics

- **Training Speed**: 2x faster with Unsloth
- **Memory Efficiency**: 50% less VRAM with QLoRA
- **Inference Throughput**: >1000 tokens/second with vLLM
- **Evaluation Coverage**: All major benchmarks supported
- **Deployment Time**: <5 minutes from model to API

## Future Enhancements

1. **AutoML Integration**: Automatic hyperparameter search
2. **Distributed Training**: Multi-node training support
3. **Model Merging**: Combine multiple LoRA adapters
4. **Continuous Learning**: Online learning from feedback
5. **Edge Deployment**: Mobile and embedded optimization
