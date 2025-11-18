---
description: Fine-tune models with advanced techniques
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

## Arguments

- `$ARGUMENTS` will contain: `[technique] [base_model] [dataset] [output_dir]`

## Implementation

Parse arguments and invoke the **finetuning-expert** agent with appropriate context based on technique.

**Example flow:**

1. Parse technique, base_model, dataset, output_dir from $ARGUMENTS
2. Validate that dataset exists
3. Create output directory if needed
4. Invoke **finetuning-expert** agent with technique-specific context:
   - For 'lora': LoRA with default settings (r=16, alpha=32)
   - For 'qlora': 4-bit quantization with double quantization
   - For 'prefix': Prefix tuning with 20 token prefix length
   - For 'ia3': IA3 with scaling vectors
   - For 'adapters': Adapter layers with bottleneck dim=64

**Examples:**

```bash
/finetune lora llama2-7b dataset.jsonl ./output
/finetune qlora mistral-7b custom_data.jsonl ./models/finetuned
/finetune prefix phi-2 instructions.jsonl ./prefix-model
```
