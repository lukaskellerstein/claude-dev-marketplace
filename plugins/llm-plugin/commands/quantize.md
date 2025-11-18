---
description: Quantize models for efficient deployment
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

## Arguments

- `$ARGUMENTS` will contain: `[method] [model] [output]`

## Implementation

Parse arguments and invoke the **optimization-expert** agent with method-specific context.

**Example flow:**

1. Parse method, model, output from $ARGUMENTS
2. Validate model path or HuggingFace model ID
3. Create output directory
4. Invoke **optimization-expert** agent with quantization method:
   - For 'int8': ~50% size reduction, minimal performance impact
   - For 'int4': ~75% size reduction, minor performance impact
   - For 'gptq': ~75% size reduction with calibration dataset
   - For 'awq': ~70% size reduction, activation-aware
   - For 'bnb': BitsAndBytes 8-bit or 4-bit quantization
   - For 'gguf': Convert to GGUF format for Ollama/llama.cpp

**Output:**

Quantized model saved to specified output directory with:
- Model size comparison
- Expected performance characteristics
- Usage instructions

**Examples:**

```bash
/quantize gptq llama2-7b ./llama2-7b-gptq
/quantize awq mistral-7b ./mistral-7b-awq
/quantize gguf phi-2 ./phi-2.gguf
```
