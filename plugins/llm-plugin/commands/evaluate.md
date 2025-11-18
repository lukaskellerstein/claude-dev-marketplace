---
description: Evaluate model performance and benchmarks
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

## Arguments

- `$ARGUMENTS` will contain: `[model] [benchmark] [options]`

## Implementation

Parse arguments and invoke the **evaluation-analyst** agent with benchmark-specific context.

**Example flow:**

1. Parse model, benchmark, options from $ARGUMENTS
2. Check if model exists or is a HuggingFace model ID
3. Invoke **evaluation-analyst** agent with benchmark context:
   - For 'perplexity': Calculate perplexity on specified dataset
   - For 'mmlu': Run MMLU benchmark across 57 subjects
   - For 'humaneval': Test code generation capabilities
   - For 'gsm8k': Test grade school math problem solving
   - For 'truthfulqa': Test truthfulness and accuracy
   - For 'custom': Use custom evaluation dataset from options

**Output:**

The agent will generate a detailed report with:
- Performance metrics
- Comparison to baseline
- Recommendations for improvement

**Examples:**

```bash
/evaluate llama2-7b mmlu
/evaluate ./my-model perplexity
/evaluate mistral-7b humaneval
```
