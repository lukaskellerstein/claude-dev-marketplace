# LLM Plugin Specification

## Plugin Overview

**Name**: `llm-plugin`  
**Version**: `1.0.0`  
**Description**: Comprehensive LLM toolkit for training, fine-tuning, deployment, and inference using PyTorch, HuggingFace, Unsloth, vLLM, and Ollama.

## Core Capabilities

### Model Operations

- **Training**: Full model training from scratch with distributed support
- **Fine-tuning**: LoRA, QLoRA, PEFT, full fine-tuning
- **RLHF/DPO**: Reinforcement learning from human feedback, Direct Preference Optimization
- **Quantization**: INT8, INT4, GPTQ, AWQ, BitsAndBytes
- **Deployment**: vLLM serving, Ollama local deployment, TensorRT optimization

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
- **Other Models**: Phi, Qwen, Yi, Gemma, DeepSeek, StarCoder

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
├── hooks/
│   └── hooks.json
└── mcp-servers/
    └── config.json
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
  "mcpServers": "./mcp-servers/config.json"
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
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
return 0
else
echo "Warning: No GPU detected, training will be slow"
echo "Consider using cloud GPUs or smaller models"
return 1
fi
}

# Setup Python environment

setup_environment() {
if [ ! -d "venv" ]; then
echo "Creating virtual environment..."
python -m venv venv
fi
source venv/bin/activate

    echo "Installing required packages..."
    pip install -q torch transformers datasets accelerate peft trl

    if [ "$METHOD" == "qlora" ] || [ "$METHOD" == "lora" ]; then
        echo "Installing Unsloth for 2x faster training..."
        pip install -q "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
    fi

    if [ "$METHOD" == "rlhf" ] || [ "$METHOD" == "dpo" ]; then
        echo "Installing TRL for RLHF/DPO..."
        pip install -q trl
    fi

}

# Check GPU and setup environment

GPU_AVAILABLE=$(check_gpu)
setup_environment

case $METHOD in
full)
echo "Starting full model training..."
echo "Model: $MODEL"
echo "Dataset: $DATASET"
echo "This will invoke the training-specialist agent" # Agent will handle the actual training implementation
;;
lora)
echo "Starting LoRA fine-tuning..."
echo "Model: $MODEL"
echo "Dataset: $DATASET"
echo "LoRA configuration: r=16, alpha=16" # Invoke finetuning-expert agent
;;
qlora)
echo "Starting QLoRA fine-tuning with 4-bit quantization..."
echo "Model: $MODEL"
echo "Dataset: $DATASET" # Invoke finetuning-expert agent with QLoRA context
;;
dpo)
echo "Starting Direct Preference Optimization..."
echo "Model: $MODEL"
echo "Preference Dataset: $DATASET" # Invoke training-specialist with DPO context
;;
rlhf)
echo "Starting RLHF training..."
echo "Model: $MODEL"
echo "Dataset: $DATASET" # Invoke training-specialist with RLHF context
;;
continued)
echo "Starting continued pre-training..."
echo "Base Model: $MODEL"
echo "New Dataset: $DATASET" # Invoke training-specialist with continued training context
;;
\*)
echo "Usage: /train [full|lora|qlora|dpo|rlhf|continued] [model] [dataset]"
echo ""
echo "Examples:"
echo " /train lora llama2-7b alpaca"
echo " /train qlora mistral-7b custom_dataset.jsonl"
echo " /train dpo llama2-7b preferences.json"
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

if [ -z "$TECHNIQUE" ] || [ -z "$BASE_MODEL" ] || [ -z "$DATASET" ]; then
echo "Usage: /finetune [technique] [base_model] [dataset] [output_dir]"
echo ""
echo "Techniques: lora, qlora, prefix, ia3, adapters"
echo "Example: /finetune lora llama2-7b dataset.jsonl ./output"
exit 1
fi

echo "Fine-tuning configuration:"
echo "Technique: $TECHNIQUE"
echo "Base Model: $BASE_MODEL"
echo "Dataset: $DATASET"
echo "Output: $OUTPUT_DIR"

# Create output directory

mkdir -p $OUTPUT_DIR

# Check dataset exists

if [ ! -f "$DATASET" ]; then
echo "Error: Dataset file not found: $DATASET"
exit 1
fi

case $TECHNIQUE in
lora)
echo "Configuring LoRA fine-tuning..."
echo "Default settings: r=16, alpha=32, dropout=0.05"
echo "Target modules: q_proj, v_proj, k_proj, o_proj" # Invoke finetuning-expert agent
;;
qlora)
echo "Configuring QLoRA with 4-bit quantization..."
echo "Using nf4 quantization with double quantization"
echo "Computing in bfloat16 for stability" # Invoke finetuning-expert agent with QLoRA
;;
prefix)
echo "Configuring prefix tuning..."
echo "Prefix length: 20 tokens" # Invoke finetuning-expert agent with prefix tuning
;;
ia3)
echo "Configuring IA3 fine-tuning..."
echo "Scaling vectors for efficient adaptation" # Invoke finetuning-expert agent with IA3
;;
adapters)
echo "Configuring adapter layers..."
echo "Bottleneck dimension: 64" # Invoke finetuning-expert agent with adapters
;;
\*)
echo "Unknown technique: $TECHNIQUE"
exit 1
;;
esac
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
- `local` - Simple local serving with transformers

!`
#!/bin/bash

PLATFORM=$1
MODEL=$2
PORT=${3:-8000}
OPTIONS=$4

if [ -z "$PLATFORM" ] || [ -z "$MODEL" ]; then
echo "Usage: /serve [platform] [model] [port]"
echo ""
echo "Platforms: vllm, ollama, hf-inference, tensorrt, local"
echo "Example: /serve vllm ./my-model 8000"
exit 1
fi

case $PLATFORM in
vllm)
echo "Starting vLLM server..."
echo "Model: $MODEL"
echo "Port: $PORT"
echo "Configuration:"
echo " - Tensor parallel: auto"
echo " - GPU memory utilization: 90%"
echo " - Max model length: 4096"
echo ""
echo "Starting server with:"
echo "python -m vllm.entrypoints.openai.api_server \\"
echo " --model $MODEL \\"
echo " --port $PORT \\"
echo " --max-model-len 4096 \\"
echo " --gpu-memory-utilization 0.9" # Invoke deployment-engineer agent for vLLM
;;
ollama)
echo "Deploying with Ollama..."
echo "Model: $MODEL"
echo ""
echo "Steps:"
echo "1. Creating Modelfile..."
echo "2. Building model..."
echo "3. Starting Ollama server..." # Invoke deployment-engineer agent for Ollama
;;
hf-inference)
echo "Setting up HuggingFace inference endpoint..."
echo "Model: $MODEL"
echo "This will deploy to HuggingFace's infrastructure" # Invoke deployment-engineer agent for HF
;;
tensorrt)
echo "Optimizing with TensorRT..."
echo "Model: $MODEL"
echo "Building optimized engine for current GPU" # Invoke optimization-expert agent
;;
local)
echo "Starting local server with transformers..."
echo "Model: $MODEL"
echo "Port: $PORT" # Simple local serving
;;
\*)
echo "Unknown platform: $PLATFORM"
exit 1
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

`/evaluate [model] [benchmark] [options]`

## Benchmarks

- `perplexity` - Calculate perplexity on dataset
- `mmlu` - Massive Multitask Language Understanding
- `humaneval` - Code generation benchmark
- `gsm8k` - Grade school math problems
- `truthfulqa` - Truthfulness evaluation
- `custom` - Custom evaluation dataset

!`
#!/bin/bash

MODEL=$1
BENCHMARK=$2
OPTIONS=$3

if [ -z "$MODEL" ] || [ -z "$BENCHMARK" ]; then
echo "Usage: /evaluate [model] [benchmark] [options]"
echo ""
echo "Benchmarks: perplexity, mmlu, humaneval, gsm8k, truthfulqa, custom"
echo "Example: /evaluate llama2-7b mmlu"
exit 1
fi

echo "Evaluating model: $MODEL"
echo "Benchmark: $BENCHMARK"

# Check if model exists

if [ ! -d "$MODEL" ] && [ ! -f "$MODEL" ]; then
echo "Warning: Model path not found. Assuming HuggingFace model ID."
fi

case $BENCHMARK in
perplexity)
echo "Calculating perplexity..."
echo "This measures how well the model predicts text" # Invoke evaluation-analyst agent
;;
mmlu)
echo "Running MMLU benchmark..."
echo "Testing on 57 subjects across STEM, humanities, and more" # Invoke evaluation-analyst agent with MMLU
;;
humaneval)
echo "Running HumanEval code generation benchmark..."
echo "Testing ability to generate correct Python functions" # Invoke evaluation-analyst agent with HumanEval
;;
gsm8k)
echo "Running GSM8K math benchmark..."
echo "Testing grade school math problem solving" # Invoke evaluation-analyst agent with GSM8K
;;
truthfulqa)
echo "Running TruthfulQA benchmark..."
echo "Testing truthfulness and accuracy" # Invoke evaluation-analyst agent with TruthfulQA
;;
custom)
echo "Running custom evaluation..."
echo "Please specify dataset path in options" # Invoke evaluation-analyst with custom dataset
;;
\*)
echo "Unknown benchmark: $BENCHMARK"
exit 1
;;
esac

echo ""
echo "Evaluation will generate a detailed report with:"
echo "- Performance metrics"
echo "- Comparison to baseline"
echo "- Recommendations for improvement"
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
- `gguf` - GGUF format for Ollama/llama.cpp

!`
#!/bin/bash

METHOD=$1
MODEL=$2
OUTPUT=$3

if [ -z "$METHOD" ] || [ -z "$MODEL" ] || [ -z "$OUTPUT" ]; then
echo "Usage: /quantize [method] [model] [output]"
echo ""
echo "Methods: int8, int4, gptq, awq, bnb, gguf"
echo "Example: /quantize gptq llama2-7b ./llama2-7b-gptq"
exit 1
fi

echo "Quantizing model..."
echo "Method: $METHOD"
echo "Input: $MODEL"
echo "Output: $OUTPUT"

# Check model exists

if [ ! -d "$MODEL" ] && [ ! -f "$MODEL" ]; then
echo "Warning: Model path not found. Will attempt to download from HuggingFace."
fi

# Create output directory

mkdir -p $OUTPUT

case $METHOD in
int8)
echo "Applying INT8 quantization..."
echo "Expected size reduction: ~50%"
echo "Performance impact: Minimal" # Invoke optimization-expert agent
;;
int4)
echo "Applying INT4 quantization..."
echo "Expected size reduction: ~75%"
echo "Performance impact: Minor" # Invoke optimization-expert agent
;;
gptq)
echo "Applying GPTQ quantization..."
echo "Using calibration dataset for optimal quantization"
echo "Expected size reduction: ~75%"
echo "Performance: Near original quality" # Invoke optimization-expert agent with GPTQ
;;
awq)
echo "Applying AWQ quantization..."
echo "Activation-aware quantization for better quality"
echo "Expected size reduction: ~70%" # Invoke optimization-expert agent with AWQ
;;
bnb)
echo "Applying BitsAndBytes quantization..."
echo "8-bit or 4-bit with minimal quality loss" # Invoke optimization-expert agent with BnB
;;
gguf)
echo "Converting to GGUF format..."
echo "Compatible with Ollama and llama.cpp"
echo "Multiple quantization levels available" # Invoke optimization-expert agent for GGUF
;;
\*)
echo "Unknown method: $METHOD"
exit 1
;;
esac

echo ""
echo "Quantization complete. Model saved to: $OUTPUT"
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

`/dataset [action] [source] [output]`

## Actions

- `prepare` - Prepare dataset for training
- `convert` - Convert between formats
- `analyze` - Analyze dataset statistics
- `clean` - Clean and filter dataset
- `augment` - Augment with synthetic data
- `split` - Split into train/val/test

## Formats

- `alpaca` - Alpaca instruction format
- `chatml` - ChatML format
- `jsonl` - JSON Lines format
- `sharegpt` - ShareGPT conversation format

!`
#!/bin/bash

ACTION=$1
SOURCE=$2
OUTPUT=$3

if [ -z "$ACTION" ] || [ -z "$SOURCE" ]; then
echo "Usage: /dataset [action] [source] [output]"
echo ""
echo "Actions: prepare, convert, analyze, clean, augment, split"
echo "Example: /dataset prepare raw_data.json training_data.jsonl"
exit 1
fi

echo "Dataset operation: $ACTION"
echo "Source: $SOURCE"
[ ! -z "$OUTPUT" ] && echo "Output: $OUTPUT"

# Check source exists

if [ ! -f "$SOURCE" ] && [ "$ACTION" != "analyze" ]; then
echo "Error: Source file not found: $SOURCE"
exit 1
fi

case $ACTION in
prepare)
echo "Preparing dataset for training..."
echo "Steps:"
echo "1. Loading data"
echo "2. Formatting for training"
echo "3. Tokenization check"
echo "4. Validation" # Invoke dataset-curator agent
;;
convert)
echo "Converting dataset format..."
echo "Detecting source format..."
echo "Target format: ${OUTPUT##_.}" # Invoke dataset-curator agent for conversion
;;
analyze)
echo "Analyzing dataset..."
echo "Calculating statistics:"
echo "- Number of examples"
echo "- Token distribution"
echo "- Quality metrics" # Invoke dataset-curator for analysis
;;
clean)
echo "Cleaning dataset..."
echo "- Removing duplicates"
echo "- Filtering by length"
echo "- Removing invalid entries" # Invoke dataset-curator for cleaning
;;
augment)
echo "Augmenting dataset..."
echo "Methods: paraphrase, back-translation, synthesis" # Invoke dataset-curator for augmentation
;;
split)
echo "Splitting dataset..."
echo "Default: 80% train, 10% val, 10% test" # Invoke dataset-curator for splitting
;;
_)
echo "Unknown action: $ACTION"
exit 1
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

Expert in training large language models with PyTorch and HuggingFace, including distributed training and optimization techniques.

## Full Model Training

### Complete Training Pipeline

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    EarlyStoppingCallback
)
import torch
from datasets import load_dataset
from accelerate import Accelerator
import wandb

class LLMTrainer:
    def __init__(self, model_name: str, dataset_name: str, output_dir: str = "./output"):
        """Initialize trainer with model and dataset"""
        self.accelerator = Accelerator(
            mixed_precision='bf16',  # Use bfloat16 for stable training
            gradient_accumulation_steps=4,
            log_with="wandb",  # Use Weights & Biases for logging
            project_dir=output_dir
        )

        # Initialize wandb for experiment tracking
        if self.accelerator.is_main_process:
            wandb.init(
                project="llm-training",
                config={
                    "model": model_name,
                    "dataset": dataset_name,
                    "mixed_precision": "bf16",
                    "gradient_accumulation": 4
                }
            )

        # Load model with optimization
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            use_cache=False,  # Disable KV cache for training
            attn_implementation="flash_attention_2" if self.check_flash_attn() else "eager"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            use_fast=True,
            trust_remote_code=True
        )

        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.dataset_name = dataset_name
        self.output_dir = output_dir

    def check_flash_attn(self):
        """Check if Flash Attention 2 is available"""
        try:
            import flash_attn
            return True
        except ImportError:
            print("Flash Attention not available, using standard attention")
            return False

    def prepare_dataset(self):
        """Load and prepare dataset for training"""
        # Load dataset
        dataset = load_dataset(self.dataset_name, split="train")

        # Split into train/validation
        split_dataset = dataset.train_test_split(test_size=0.05, seed=42)

        def tokenize_function(examples):
            # Tokenize with proper truncation and padding
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding="max_length",
                max_length=2048,
                return_special_tokens_mask=True
            )

        # Tokenize dataset
        tokenized_dataset = split_dataset.map(
            tokenize_function,
            batched=True,
            num_proc=4,
            remove_columns=dataset.column_names,
            desc="Tokenizing dataset"
        )

        return tokenized_dataset

    def setup_training_args(self, num_epochs: int = 3):
        """Configure training arguments"""
        return TrainingArguments(
            output_dir=self.output_dir,
            overwrite_output_dir=True,

            # Training hyperparameters
            num_train_epochs=num_epochs,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            gradient_accumulation_steps=4,
            eval_accumulation_steps=4,

            # Learning rate schedule
            learning_rate=2e-5,
            lr_scheduler_type="cosine",
            warmup_steps=500,

            # Optimization
            optim="adamw_torch_fused",  # Fused AdamW for speed
            adam_beta1=0.9,
            adam_beta2=0.95,
            adam_epsilon=1e-8,
            weight_decay=0.01,
            max_grad_norm=1.0,

            # Evaluation and saving
            evaluation_strategy="steps",
            eval_steps=500,
            save_strategy="steps",
            save_steps=1000,
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,

            # Performance optimization
            bf16=True,
            tf32=True,  # Enable TF32 on Ampere GPUs
            gradient_checkpointing=True,
            gradient_checkpointing_kwargs={"use_reentrant": False},
            group_by_length=True,
            length_column_name="length",
            ddp_find_unused_parameters=False if torch.cuda.device_count() > 1 else None,

            # Logging
            logging_dir=f"{self.output_dir}/logs",
            logging_strategy="steps",
            logging_steps=10,
            report_to=["wandb", "tensorboard"],

            # Other
            dataloader_num_workers=4,
            dataloader_pin_memory=True,
            skip_memory_metrics=False,
            push_to_hub=False,
        )

    def train(self):
        """Execute training"""
        # Prepare dataset
        dataset = self.prepare_dataset()

        # Setup training arguments
        training_args = self.setup_training_args()

        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset["train"],
            eval_dataset=dataset["test"],
            tokenizer=self.tokenizer,
            data_collator=DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False,  # Causal LM, not masked LM
                pad_to_multiple_of=8  # Efficient padding
            ),
            callbacks=[
                EarlyStoppingCallback(
                    early_stopping_patience=3,
                    early_stopping_threshold=0.001
                )
            ]
        )

        # Enable gradient checkpointing
        if training_args.gradient_checkpointing:
            self.model.gradient_checkpointing_enable()

        # Start training
        print("Starting training...")
        train_result = trainer.train()

        # Save final model
        print("Saving model...")
        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)

        # Save training metrics
        with open(f"{self.output_dir}/training_metrics.txt", "w") as f:
            f.write(str(train_result.metrics))

        return train_result
```
````

### Distributed Training with DeepSpeed

```python
# deepspeed_config.json
deepspeed_config = {
    "train_batch_size": "auto",
    "gradient_accumulation_steps": "auto",
    "gradient_clipping": 1.0,
    "zero_optimization": {
        "stage": 2,  # ZeRO-2 for balanced memory/speed
        "offload_optimizer": {
            "device": "cpu",
            "pin_memory": True
        },
        "allgather_partitions": True,
        "allgather_bucket_size": 5e8,
        "overlap_comm": True,
        "reduce_scatter": True,
        "reduce_bucket_size": 5e8,
        "contiguous_gradients": True
    },
    "bf16": {
        "enabled": True
    },
    "optimizer": {
        "type": "AdamW",
        "params": {
            "lr": "auto",
            "betas": [0.9, 0.95],
            "eps": 1e-8,
            "weight_decay": "auto"
        }
    },
    "scheduler": {
        "type": "WarmupCosineLR",
        "params": {
            "warmup_min_lr": 0,
            "warmup_max_lr": "auto",
            "warmup_num_steps": "auto",
            "total_num_steps": "auto"
        }
    }
}

# Use with trainer
training_args.deepspeed = "deepspeed_config.json"
```

### DPO Training

```python
from trl import DPOTrainer

def train_dpo(model_name: str, dataset_name: str):
    """Train with Direct Preference Optimization"""

    # Load model and reference model
    model = AutoModelForCausalLM.from_pretrained(model_name)
    ref_model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Load preference dataset
    dataset = load_dataset(dataset_name)

    # DPO training arguments
    training_args = TrainingArguments(
        output_dir="./dpo_output",
        num_train_epochs=1,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=1e-6,
        warmup_ratio=0.1,
        bf16=True,
        gradient_checkpointing=True,
        evaluation_strategy="steps",
        eval_steps=500,
        save_strategy="steps",
        save_steps=1000,
        logging_steps=10,
    )

    # Initialize DPO trainer
    dpo_trainer = DPOTrainer(
        model=model,
        ref_model=ref_model,
        args=training_args,
        beta=0.1,  # KL penalty coefficient
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        tokenizer=tokenizer,
        max_length=512,
        max_prompt_length=256,
    )

    # Train
    dpo_trainer.train()

    # Save
    dpo_trainer.save_model("./dpo_final")
```

## Best Practices

1. **Start with smaller models**: Test pipeline with 125M-1B parameter models first
2. **Monitor metrics closely**: Watch for loss spikes, gradient explosions
3. **Use mixed precision**: BF16 is more stable than FP16 for training
4. **Save checkpoints frequently**: Every 1000 steps or less
5. **Implement gradient checkpointing**: Essential for large models
6. **Use efficient data loading**: Multiple workers, pin memory
7. **Profile training**: Identify bottlenecks with PyTorch profiler
8. **Track experiments**: Use Weights & Biases or TensorBoard
9. **Validate frequently**: Catch issues early with validation loss
10. **Have rollback plan**: Keep best checkpoints, be ready to resume

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

Expert in parameter-efficient fine-tuning methods using PEFT, Unsloth, and advanced techniques.

## LoRA Fine-tuning with Unsloth

### Fast LoRA Implementation
```python
from unsloth import FastLanguageModel
import torch
from transformers import TrainingArguments
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
from datasets import load_dataset

class LoRAFineTuner:
    def __init__(self, model_name: str, max_seq_length: int = 2048):
        """Initialize with Unsloth for 2x faster training"""

        # Load 4-bit quantized model for QLoRA
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=max_seq_length,
            dtype=None,  # Auto-detect optimal dtype
            load_in_4bit=True,  # Use 4-bit quantization
        )

        self.max_seq_length = max_seq_length

    def prepare_model_for_training(self, r: int = 16, target_modules: list = None):
        """Apply LoRA adapters with optimal configuration"""

        if target_modules is None:
            # Default to attention + MLP layers for maximum impact
            target_modules = [
                "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
                "gate_proj", "up_proj", "down_proj",      # MLP
            ]

        # Apply LoRA with Unsloth optimizations
        self.model = FastLanguageModel.get_peft_model(
            self.model,
            r=r,  # LoRA rank
            target_modules=target_modules,
            lora_alpha=r,  # Usually set equal to r
            lora_dropout=0.05,  # Small dropout for regularization
            bias="none",  # Don't train biases
            use_gradient_checkpointing="unsloth",  # Unsloth's optimized checkpointing
            random_state=42,
            use_rslora=False,  # Use standard LoRA (RSLoRA is experimental)
            loftq_config=None,  # LoftQ for better initialization (optional)
        )

        # Print trainable parameters
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in self.model.parameters())
        print(f"Trainable parameters: {trainable_params:,} ({100 * trainable_params / total_params:.2f}%)")

    def prepare_dataset(self, dataset_name: str, format_type: str = "alpaca"):
        """Prepare dataset in appropriate format"""

        dataset = load_dataset(dataset_name)

        if format_type == "alpaca":
            # Alpaca instruction format
            alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input}

### Response:
{output}"""

            def format_alpaca(examples):
                instructions = examples["instruction"]
                inputs = examples.get("input", [""] * len(instructions))
                outputs = examples["output"]

                texts = []
                for instruction, input_text, output in zip(instructions, inputs, outputs):
                    text = alpaca_prompt.format(
                        instruction=instruction,
                        input=input_text if input_text else "",
                        output=output
                    )
                    texts.append(text)

                return {"text": texts}

        elif format_type == "chat":
            # Chat format
            def format_chat(examples):
                texts = []
                for conversation in examples["conversations"]:
                    text = ""
                    for message in conversation:
                        role = message["from"]
                        content = message["value"]
                        if role == "human":
                            text += f"User: {content}\n"
                        else:
                            text += f"Assistant: {content}\n"
                    texts.append(text)

                return {"text": texts}

        # Apply formatting
        format_func = format_alpaca if format_type == "alpaca" else format_chat
        dataset = dataset.map(format_func, batched=True, num_proc=4)

        return dataset

    def train(self,
              dataset_name: str,
              output_dir: str = "./lora_model",
              num_epochs: int = 3,
              batch_size: int = 4,
              learning_rate: float = 2e-4):
        """Execute LoRA fine-tuning"""

        # Prepare model with LoRA
        self.prepare_model_for_training()

        # Prepare dataset
        dataset = self.prepare_dataset(dataset_name)

        # Training arguments optimized for LoRA
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            warmup_steps=100,
            learning_rate=learning_rate,

            # Optimization settings
            optim="adamw_8bit",  # 8-bit Adam for memory efficiency
            weight_decay=0.01,
            lr_scheduler_type="cosine",

            # Mixed precision
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),

            # Logging
            logging_steps=10,
            logging_first_step=True,

            # Evaluation
            evaluation_strategy="steps" if "validation" in dataset else "no",
            eval_steps=100 if "validation" in dataset else None,

            # Saving
            save_strategy="steps",
            save_steps=500,
            save_total_limit=2,
            load_best_model_at_end=True if "validation" in dataset else False,

            # Performance
            gradient_checkpointing=True,
            gradient_checkpointing_kwargs={"use_reentrant": False},
            group_by_length=True,

            # Other
            report_to="tensorboard",
            seed=42,
        )

        # Initialize SFT trainer
        trainer = SFTTrainer(
            model=self.model,
            tokenizer=self.tokenizer,
            train_dataset=dataset["train"],
            eval_dataset=dataset.get("validation", None),
            dataset_text_field="text",
            max_seq_length=self.max_seq_length,
            dataset_num_proc=4,
            packing=False,  # Can enable for short sequences
            args=training_args,
        )

        # Train
        print("Starting LoRA fine-tuning...")
        trainer.train()

        # Save LoRA adapters
        print(f"Saving LoRA adapters to {output_dir}")
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)

        # Option to merge and save full model
        # self.model.save_pretrained_merged(f"{output_dir}_merged", self.tokenizer)

        return trainer.state.log_history
````

### QLoRA with Advanced Quantization

```python
from transformers import BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

def create_qlora_model(model_name: str):
    """Create QLoRA model with 4-bit quantization"""

    # Configure 4-bit quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,  # Double quantization
        bnb_4bit_quant_type="nf4",  # NormalFloat4 quantization
        bnb_4bit_compute_dtype=torch.bfloat16,  # Compute in bfloat16
    )

    # Load model with quantization
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        attn_implementation="flash_attention_2" if is_flash_attn_available() else "eager"
    )

    # Prepare for k-bit training
    model = prepare_model_for_kbit_training(model)

    # Configure LoRA
    peft_config = LoraConfig(
        r=64,  # Higher rank for QLoRA
        lora_alpha=16,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj", "lm_head"
        ],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        inference_mode=False,
    )

    # Apply LoRA
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    return model
```

### Advanced Fine-tuning Techniques

#### Merged Adapter Training

```python
def merge_and_continue_training(base_model_path: str,
                                lora_adapter_path: str,
                                new_dataset: str):
    """Merge LoRA adapter and continue training"""

    # Load base model and adapter
    model = AutoModelForCausalLM.from_pretrained(base_model_path)
    model = PeftModel.from_pretrained(model, lora_adapter_path)

    # Merge adapter into base model
    model = model.merge_and_unload()

    # Apply new LoRA for continued training
    new_peft_config = LoraConfig(
        r=8,  # Smaller rank for fine-tuning
        lora_alpha=8,
        target_modules=["q_proj", "v_proj"],  # Fewer targets
        lora_dropout=0.1,
    )

    model = get_peft_model(model, new_peft_config)

    # Continue training on new dataset
    # ... training code ...
```

#### Multi-Task LoRA

```python
def create_multi_task_lora(model_name: str, tasks: dict):
    """Create multiple LoRA adapters for different tasks"""

    model = AutoModelForCausalLM.from_pretrained(model_name)

    for task_name, task_config in tasks.items():
        # Create task-specific LoRA config
        peft_config = LoraConfig(
            r=task_config["rank"],
            lora_alpha=task_config["alpha"],
            target_modules=task_config["targets"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        )

        # Add adapter for this task
        model.add_adapter(task_name, peft_config)

    # Train each adapter
    for task_name in tasks:
        model.set_adapter(task_name)
        # ... task-specific training ...
```

## Best Practices

1. **Start with LoRA rank 8-16**: Increase only if needed
2. **Use QLoRA for large models**: Enables fine-tuning 70B+ models on single GPU
3. **Target all linear layers**: Better results than just attention
4. **Monitor gradient norms**: Detect training instabilities
5. **Save adapters separately**: Much smaller than full models
6. **Test before merging**: Ensure quality before creating full model
7. **Use Unsloth for speed**: 2x faster training with same quality
8. **Implement early stopping**: Prevent overfitting
9. **Validate on held-out data**: Ensure generalization
10. **Document hyperparameters**: Track what works for reproducibility

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

Expert in deploying LLMs for production inference with vLLM, Ollama, TensorRT, and optimization techniques.

## vLLM High-Performance Deployment

### Production vLLM Server
```python
from vllm import LLM, SamplingParams
from vllm.entrypoints.openai import api_server
import ray
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

class vLLMDeployment:
    def __init__(self, model_path: str, gpu_memory_utilization: float = 0.9):
        """Initialize vLLM with production optimizations"""

        # Detect available GPUs
        import torch
        num_gpus = torch.cuda.device_count()

        # Initialize vLLM with optimal settings
        self.llm = LLM(
            model=model_path,

            # Parallelism settings
            tensor_parallel_size=num_gpus if num_gpus > 1 else 1,
            pipeline_parallel_size=1,

            # Memory settings
            gpu_memory_utilization=gpu_memory_utilization,
            swap_space=4,  # GB of CPU swap space for overflow

            # Model settings
            max_model_len=4096,
            dtype="auto",  # Auto-detect best dtype

            # Optimization settings
            enforce_eager=False,  # Use CUDA graphs for speed
            enable_prefix_caching=True,  # Cache common prefixes
            enable_chunked_prefill=False,  # Disable for lower latency

            # Quantization (if model supports it)
            quantization="awq" if self.check_awq_support(model_path) else None,

            # Scheduling
            max_num_batched_tokens=8192,
            max_num_seqs=256,

            # Logging
            disable_log_stats=False,
            disable_log_requests=False,
        )

        self.model_path = model_path

    def check_awq_support(self, model_path: str) -> bool:
        """Check if model has AWQ quantization"""
        import os
        config_path = os.path.join(model_path, "config.json")
        if os.path.exists(config_path):
            import json
            with open(config_path) as f:
                config = json.load(f)
                return config.get("quantization_config", {}).get("quant_method") == "awq"
        return False

    async def generate(self,
                       prompts: list,
                       temperature: float = 0.7,
                       max_tokens: int = 512,
                       top_p: float = 0.9,
                       **kwargs):
        """Batch generation with vLLM"""

        sampling_params = SamplingParams(
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            repetition_penalty=kwargs.get("repetition_penalty", 1.1),
            frequency_penalty=kwargs.get("frequency_penalty", 0.0),
            presence_penalty=kwargs.get("presence_penalty", 0.0),
            stop=kwargs.get("stop", None),
            skip_special_tokens=kwargs.get("skip_special_tokens", True),
        )

        # Generate with vLLM's efficient batching
        outputs = self.llm.generate(prompts, sampling_params)

        # Extract generated text
        results = []
        for output in outputs:
            text = output.outputs[0].text
            results.append({
                "generated_text": text,
                "finish_reason": output.outputs[0].finish_reason,
                "prompt_tokens": len(output.prompt_token_ids),
                "completion_tokens": len(output.outputs[0].token_ids),
            })

        return results

    def create_openai_compatible_server(self, port: int = 8000):
        """Create OpenAI-compatible API server"""

        # Server startup script
        server_script = f"""
#!/bin/bash

# Start vLLM OpenAI-compatible server
python -m vllm.entrypoints.openai.api_server \\
    --model {self.model_path} \\
    --port {port} \\
    --host 0.0.0.0 \\
    --gpu-memory-utilization {self.llm.llm_engine.gpu_memory_utilization} \\
    --max-model-len {self.llm.llm_engine.max_model_len} \\
    --enable-prefix-caching \\
    --served-model-name "model" \\
    --api-key "$VLLM_API_KEY"
"""

        # Save startup script
        with open("start_vllm_server.sh", "w") as f:
            f.write(server_script)

        print(f"Server script created. Run: bash start_vllm_server.sh")
        print(f"API will be available at: http://localhost:{port}/v1")

        return server_script
````

### Production Configuration

```yaml
# vllm_production.yaml
model:
  name: "meta-llama/Llama-2-70b-chat-hf"
  dtype: "auto"
  max_model_len: 4096
  download_dir: "/models"

parallel:
  tensor_parallel_size: 4 # For 4 GPUs
  pipeline_parallel_size: 1

memory:
  gpu_memory_utilization: 0.95
  swap_space: 8 # GB

optimization:
  enable_prefix_caching: true
  enable_chunked_prefill: false
  use_v2_block_manager: true

serving:
  host: "0.0.0.0"
  port: 8000
  uvicorn_log_level: "info"
  api_key: "${VLLM_API_KEY}"

monitoring:
  prometheus_port: 9090
  collect_stats: true
```

## Ollama Local Deployment

### Ollama Model Manager

```python
import subprocess
import requests
import json
import os

class OllamaDeployment:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"

    def is_running(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False

    def start_ollama(self):
        """Start Ollama service"""
        if not self.is_running():
            subprocess.Popen(["ollama", "serve"],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print("Starting Ollama service...")
            # Wait for service to be ready
            import time
            for _ in range(30):
                if self.is_running():
                    print("Ollama service started successfully")
                    return
                time.sleep(1)
            raise Exception("Failed to start Ollama service")

    def create_from_gguf(self,
                        gguf_path: str,
                        model_name: str,
                        system_prompt: str = None,
                        parameters: dict = None):
        """Create Ollama model from GGUF file"""

        # Create Modelfile
        modelfile_content = f'FROM {gguf_path}\n\n'

        if system_prompt:
            modelfile_content += f'SYSTEM """{system_prompt}"""\n\n'

        if parameters:
            for key, value in parameters.items():
                modelfile_content += f'PARAMETER {key} {value}\n'

        # Add template for chat models
        modelfile_content += '''
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
"""

PARAMETER stop <|im_start|>
PARAMETER stop <|im_end|>
'''

        # Save Modelfile
        modelfile_path = f"{model_name}.Modelfile"
        with open(modelfile_path, "w") as f:
            f.write(modelfile_content)

        # Create model
        result = subprocess.run(
            ["ollama", "create", model_name, "-f", modelfile_path],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"Successfully created model: {model_name}")
            os.remove(modelfile_path)
            return True
        else:
            print(f"Error creating model: {result.stderr}")
            return False

    def deploy_model(self, model_name: str):
        """Deploy and test model"""

        # Pull model if it's from registry
        if "/" in model_name and not os.path.exists(model_name):
            print(f"Pulling model: {model_name}")
            subprocess.run(["ollama", "pull", model_name])

        # Run model
        result = subprocess.run(
            ["ollama", "run", model_name, "Hello, how are you?"],
            capture_output=True,
            text=True
        )

        print(f"Model response: {result.stdout}")

        return result.returncode == 0

    def create_api_endpoint(self, model_name: str):
        """Create API endpoint for model"""

        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel

        app = FastAPI()

        class GenerateRequest(BaseModel):
            prompt: str
            temperature: float = 0.7
            max_tokens: int = 512
            stream: bool = False

        @app.post("/generate")
        async def generate(request: GenerateRequest):
            try:
                response = requests.post(
                    f"{self.api_url}/generate",
                    json={
                        "model": model_name,
                        "prompt": request.prompt,
                        "stream": request.stream,
                        "options": {
                            "temperature": request.temperature,
                            "num_predict": request.max_tokens
                        }
                    }
                )

                if request.stream:
                    # Handle streaming response
                    def stream_response():
                        for line in response.iter_lines():
                            if line:
                                yield json.loads(line)
                    return stream_response()
                else:
                    return response.json()

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        return app
```

## Production Optimization

### Load Balancing Multiple Instances

```python
from typing import List
import asyncio
import aiohttp
from collections import defaultdict

class LoadBalancedDeployment:
    def __init__(self, endpoints: List[str]):
        self.endpoints = endpoints
        self.healthy_endpoints = set(endpoints)
        self.request_counts = defaultdict(int)
        self.response_times = defaultdict(list)

    async def health_check(self):
        """Periodic health checking of endpoints"""
        while True:
            for endpoint in self.endpoints:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            f"{endpoint}/health",
                            timeout=aiohttp.ClientTimeout(total=5)
                        ) as response:
                            if response.status == 200:
                                self.healthy_endpoints.add(endpoint)
                            else:
                                self.healthy_endpoints.discard(endpoint)
                except:
                    self.healthy_endpoints.discard(endpoint)

            await asyncio.sleep(30)  # Check every 30 seconds

    def get_best_endpoint(self) -> str:
        """Select best endpoint using least connections"""
        if not self.healthy_endpoints:
            raise Exception("No healthy endpoints available")

        # Find endpoint with least active requests
        best_endpoint = min(
            self.healthy_endpoints,
            key=lambda e: self.request_counts[e]
        )

        return best_endpoint

    async def generate(self, prompt: str, **kwargs):
        """Generate with automatic failover"""
        endpoint = self.get_best_endpoint()
        self.request_counts[endpoint] += 1

        try:
            start_time = asyncio.get_event_loop().time()

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{endpoint}/v1/completions",
                    json={
                        "model": "model",
                        "prompt": prompt,
                        **kwargs
                    }
                ) as response:
                    result = await response.json()

            # Track response time
            response_time = asyncio.get_event_loop().time() - start_time
            self.response_times[endpoint].append(response_time)

            return result

        except Exception as e:
            # Mark endpoint as unhealthy and retry with different one
            self.healthy_endpoints.discard(endpoint)
            if self.healthy_endpoints:
                return await self.generate(prompt, **kwargs)
            raise e
        finally:
            self.request_counts[endpoint] -= 1
```

### Docker Deployment

```dockerfile
# Dockerfile for vLLM deployment
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install vLLM and dependencies
RUN pip install --no-cache-dir \
    vllm \
    torch \
    transformers \
    fastapi \
    uvicorn

# Copy model (or download at runtime)
COPY ./model /model

# Copy server script
COPY start_server.py /app/start_server.py

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start server
CMD ["python", "/app/start_server.py", "--model-path", "/model", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-server
  template:
    metadata:
      labels:
        app: llm-server
    spec:
      containers:
        - name: vllm
          image: vllm/vllm-openai:latest
          ports:
            - containerPort: 8000
          env:
            - name: MODEL_NAME
              value: "/models/llama-2-7b"
            - name: GPU_MEMORY_UTILIZATION
              value: "0.9"
          resources:
            limits:
              nvidia.com/gpu: 1
            requests:
              memory: "16Gi"
              cpu: "4"
          volumeMounts:
            - name: model-volume
              mountPath: /models
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 60
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 5
      volumes:
        - name: model-volume
          persistentVolumeClaim:
            claimName: model-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: llm-service
spec:
  selector:
    app: llm-server
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer
```

## Best Practices

1. **Use vLLM for production**: Best throughput and latency
2. **Enable prefix caching**: Significant speedup for common prefixes
3. **Implement health checks**: Detect and handle failures
4. **Use load balancing**: Distribute requests across instances
5. **Monitor GPU memory**: Prevent OOM errors
6. **Implement request queuing**: Handle burst traffic
7. **Use quantization**: Reduce memory and increase speed
8. **Set up monitoring**: Track latency, throughput, errors
9. **Implement caching**: Cache common responses
10. **Plan for scaling**: Horizontal scaling for increased load

````

### Additional agents (dataset-curator, optimization-expert, evaluation-analyst) would continue...

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

## Activation Triggers
- GPU memory usage > 90%
- OOM errors detected
- Training speed below expected
- Multi-GPU imbalance detected
- Temperature > 80°C

## Automatic Interventions

### Memory Optimization
```python
# Automatic memory clearing
torch.cuda.empty_cache()

# Enable gradient checkpointing if memory critical
if gpu_memory_usage > 0.9:
    model.gradient_checkpointing_enable()

# Reduce batch size dynamically
if oom_detected:
    batch_size = max(1, batch_size // 2)
    print(f"Reduced batch size to {batch_size}")
````

### Multi-GPU Optimization

- Detect GPU imbalance
- Redistribute model layers
- Balance data loading
- Optimize communication

### Performance Monitoring

```bash
# GPU utilization check
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv

# Power and temperature
nvidia-smi --query-gpu=power.draw,temperature.gpu --format=csv
```

## Optimization Strategies

1. **Mixed Precision**: Automatically enable bf16/fp16
2. **Flash Attention**: Switch to Flash Attention when available
3. **Gradient Accumulation**: Increase for larger effective batch
4. **CPU Offloading**: Move optimizer states to CPU
5. **Tensor Parallelism**: Split model across GPUs

## Alerts

- Memory usage > 95%: Critical warning
- Temperature > 85°C: Thermal throttling risk
- Utilization < 50%: Underutilization warning

````

### memory-management.md

```markdown
---
name: memory-management
description: Manages memory efficiently during model operations
allowed-tools: Monitor, Optimize, Clear
---

# Memory Management Skill

Prevents OOM errors and optimizes memory usage automatically.

## Activation Triggers
- Before model loading
- After each training epoch
- On OOM detection
- When switching models
- Memory usage > threshold

## Automatic Actions

### Memory Monitoring
```python
def get_memory_stats():
    return {
        'allocated': torch.cuda.memory_allocated() / 1024**3,  # GB
        'reserved': torch.cuda.memory_reserved() / 1024**3,
        'free': torch.cuda.mem_get_info()[0] / 1024**3,
        'total': torch.cuda.mem_get_info()[1] / 1024**3
    }
````

### Preventive Measures

1. **Pre-allocation Check**: Verify memory before operations
2. **Automatic Cleanup**: Clear cache periodically
3. **Batch Size Adjustment**: Dynamic sizing based on available memory
4. **Model Sharding**: Split large models automatically

### Recovery Actions

On OOM:

1. Clear CUDA cache
2. Reduce batch size
3. Enable gradient checkpointing
4. Offload to CPU if needed
5. Restart with optimized settings

## Memory Optimization Techniques

- Replace standard attention with Flash Attention
- Use 8-bit optimizers
- Enable gradient checkpointing
- Implement activation checkpointing
- Use mixed precision training

## Thresholds

- Warning: 85% memory usage
- Critical: 95% memory usage
- Action: 90% memory usage

````

### hyperparameter-tuning.md

```markdown
---
name: hyperparameter-tuning
description: Automatically suggests and validates hyperparameters
allowed-tools: Analyze, Suggest, Track
---

# Hyperparameter Tuning Skill

Optimizes training hyperparameters based on model and dataset characteristics.

## Activation Triggers
- Starting new training
- Poor convergence detected
- Validation loss increasing
- Training plateau detected
- Gradient explosion/vanishing

## Automatic Suggestions

### Learning Rate
```python
def suggest_learning_rate(model_params, batch_size, model_type):
    # Base learning rates by model size
    base_lr = {
        "small": 5e-4,   # <1B params
        "medium": 2e-4,  # 1-10B params
        "large": 1e-4,   # 10-30B params
        "xlarge": 5e-5   # >30B params
    }

    # Adjust for batch size (linear scaling rule)
    lr = base_lr[model_type] * (batch_size / 32)

    # Cap maximum learning rate
    return min(lr, 1e-3)
````

### Batch Size Optimization

- Start with largest that fits in memory
- Use gradient accumulation for effective larger batches
- Monitor gradient noise scale

### Scheduler Selection

- **Cosine**: Default for most cases
- **Linear**: Good for fine-tuning
- **Polynomial**: Smooth decay
- **OneCycleLR**: For super-convergence

## Monitoring Metrics

- Loss curve smoothness
- Gradient norm trends
- Learning rate vs loss correlation
- Weight update magnitudes

## Auto-Adjustments

- Reduce LR on plateau
- Early stopping on overfitting
- Gradient clipping on explosion
- Warmup adjustment based on stability

````

### model-selection.md

```markdown
---
name: model-selection
description: Helps select appropriate models for tasks
allowed-tools: Analyze, Compare, Recommend
---

# Model Selection Skill

Recommends optimal models based on requirements and constraints.

## Activation Triggers
- User asks for model recommendation
- Starting new project
- Resource constraints specified
- Task requirements defined

## Selection Criteria

### By Task Type
```yaml
text_generation:
  quality_focused:
    - llama-3-70b
    - mixtral-8x22b
    - gpt-j-6b
  balanced:
    - llama-2-13b
    - mistral-7b
    - yi-34b
  speed_focused:
    - llama-2-7b
    - phi-2
    - gemma-2b

code_generation:
  - codellama-34b
  - deepseek-coder-33b
  - starcoder-15b
  - codegen-16B

math_reasoning:
  - deepseek-math-7b
  - llemma-34b
  - minerva-62b
````

### By Hardware

```yaml
consumer_gpu: # 8-12GB VRAM
  full_precision:
    - phi-2
    - gemma-2b
    - llama-2-7b (barely)
  quantized:
    - llama-2-13b-qlora
    - mistral-7b-gptq
    - yi-34b-int4

datacenter_gpu: # 24-80GB VRAM
  full_precision:
    - llama-2-70b (80GB)
    - llama-2-13b (24GB)
    - mixtral-8x7b (48GB)
  optimized:
    - llama-2-70b-int8 (40GB)
    - mixtral-8x7b-awq (24GB)
```

## Recommendations

### Decision Tree

1. Define task requirements
2. Check hardware constraints
3. Consider quality vs speed tradeoff
4. Evaluate licensing requirements
5. Test with sample data

### Optimization Suggestions

- Use quantization for larger models
- Consider LoRA fine-tuning instead of full
- Try smaller specialized models
- Implement caching for repeated queries

## Model Comparison Metrics

- Perplexity scores
- Task-specific benchmarks
- Inference speed (tokens/sec)
- Memory requirements
- License restrictions

````

## Hooks Configuration

```json
{
  "hooks": {
    "SessionStart": {
      "enabled": true,
      "actions": [
        {
          "type": "command",
          "command": "echo 'LLM Plugin loaded. Checking GPU availability...'"
        },
        {
          "type": "skill",
          "name": "gpu-optimization",
          "action": "check_gpus"
        }
      ]
    },
    "pre-training": {
      "enabled": true,
      "pattern": "/train*",
      "actions": [
        {
          "type": "skill",
          "name": "gpu-optimization",
          "action": "optimize_settings"
        },
        {
          "type": "skill",
          "name": "hyperparameter-tuning",
          "action": "suggest_params"
        },
        {
          "type": "skill",
          "name": "memory-management",
          "action": "check_available"
        }
      ]
    },
    "during-training": {
      "enabled": true,
      "trigger": "epoch_end",
      "actions": [
        {
          "type": "skill",
          "name": "memory-management",
          "action": "clear_cache"
        },
        {
          "type": "command",
          "command": "echo 'Epoch complete. Clearing cache...'"
        }
      ]
    },
    "on-oom": {
      "enabled": true,
      "trigger": "oom_error",
      "actions": [
        {
          "type": "skill",
          "name": "memory-management",
          "action": "emergency_cleanup"
        },
        {
          "type": "skill",
          "name": "gpu-optimization",
          "action": "reduce_memory_usage"
        }
      ]
    },
    "post-training": {
      "enabled": true,
      "pattern": "/train*",
      "trigger": "completion",
      "actions": [
        {
          "type": "command",
          "command": "echo 'Training complete. Running evaluation...'"
        },
        {
          "type": "skill",
          "name": "model-selection",
          "action": "suggest_next_steps"
        }
      ]
    }
  }
}
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
        "WANDB_API_KEY": "${WANDB_API_KEY}",
        "TENSORBOARD_PORT": "6006"
      }
    },
    {
      "name": "model-registry",
      "description": "Manages model versions and metadata",
      "command": "python",
      "args": ["./mcp-servers/model_registry.py"],
      "env": {
        "REGISTRY_PATH": "./models",
        "HF_TOKEN": "${HF_TOKEN}"
      }
    },
    {
      "name": "gpu-manager",
      "description": "GPU allocation and monitoring",
      "command": "python",
      "args": ["./mcp-servers/gpu_manager.py"]
    },
    {
      "name": "inference-server",
      "description": "Model inference endpoint",
      "command": "python",
      "args": ["./mcp-servers/inference_server.py"],
      "env": {
        "DEFAULT_MODEL": "llama-2-7b",
        "PORT": "8080"
      }
    }
  ]
}
```

## Usage Examples

### Fine-tuning with LoRA

```bash
# User command
/finetune lora llama2-7b dataset.jsonl ./my-model

# Plugin flow:
1. Command validates inputs
2. Checks GPU availability (gpu-optimization skill)
3. Suggests hyperparameters (hyperparameter-tuning skill)
4. Invokes finetuning-expert agent
5. Agent:
   - Loads model with Unsloth
   - Applies LoRA adapters (r=16)
   - Trains with optimized settings
   - Saves adapters
6. training-monitor MCP server tracks progress
7. Post-training evaluation runs automatically
```

### Deploying with vLLM

```bash
# User command
/serve vllm ./my-model 8000

# Plugin flow:
1. Command checks model format
2. deployment-engineer agent invoked
3. Agent:
   - Initializes vLLM with optimal settings
   - Detects GPU count for tensor parallelism
   - Enables prefix caching
   - Creates OpenAI-compatible endpoint
4. inference-server MCP starts
5. Health checks enabled
6. Ready for production traffic
```

### Model Evaluation

```bash
# User command
/evaluate llama2-7b mmlu

# Plugin flow:
1. Command loads model
2. evaluation-analyst agent invoked
3. Agent:
   - Loads MMLU benchmark
   - Runs evaluation across 57 subjects
   - Calculates accuracy scores
   - Generates detailed report
4. Results saved and displayed
5. Recommendations provided
```

### Quantization for Deployment

```bash
# User command
/quantize gptq llama2-13b ./llama2-13b-gptq

# Plugin flow:
1. Command validates model path
2. optimization-expert agent invoked
3. Agent:
   - Loads calibration dataset
   - Applies GPTQ quantization
   - Tests quantized model
   - Saves optimized model
4. Size reduction: ~75%
5. Speed improvement measured
```

## Performance Benchmarks

### Training Speed

- **LoRA with Unsloth**: 2x faster than standard
- **QLoRA**: Enables 70B model fine-tuning on 24GB GPU
- **Multi-GPU**: Near-linear scaling up to 8 GPUs

### Inference Performance

- **vLLM**: 10-20x throughput vs naive implementation
- **Quantized models**: 2-4x speedup with <3% quality loss
- **Ollama**: Fast local inference with GGUF

### Memory Efficiency

- **QLoRA**: 75% memory reduction
- **Gradient checkpointing**: 30% memory savings
- **Flash Attention**: 10x memory efficiency for long contexts

## Troubleshooting

### Common Issues

**CUDA Out of Memory**

- Skills automatically reduce batch size
- Enable gradient checkpointing
- Use QLoRA instead of full fine-tuning

**Slow Training**

- Check GPU utilization with nvidia-smi
- Ensure Flash Attention is enabled
- Verify data loading isn't bottleneck

**Poor Model Quality**

- Check learning rate (may be too high)
- Increase training epochs
- Verify dataset quality

**Deployment Issues**

- Ensure model format compatibility
- Check available ports
- Verify GPU drivers updated

## Best Practices Summary

1. **Always start with smaller models** for testing
2. **Use QLoRA for large models** on limited hardware
3. **Monitor GPU metrics** throughout training
4. **Save checkpoints frequently** during training
5. **Test quantized models** before production
6. **Use vLLM for production** deployments
7. **Implement health checks** and monitoring
8. **Document model versions** and parameters
9. **Validate on held-out data** before deployment
10. **Plan for scaling** from day one

## Future Enhancements

1. **AutoML Integration**: Hyperparameter search
2. **Model Merging**: Combine multiple LoRA adapters
3. **Continuous Learning**: Online learning from production
4. **Edge Deployment**: Mobile and embedded optimization
5. **Multi-Modal Support**: Vision-language models
6. **Federated Learning**: Privacy-preserving training
7. **Model Compression**: Beyond quantization

## Contributing

To contribute:

1. Follow existing patterns
2. Add comprehensive documentation
3. Include working code examples
4. Test on multiple GPU configurations
5. Submit PR with benchmarks

## License

MIT License - See LICENSE file for details
