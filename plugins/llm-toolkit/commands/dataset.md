---
description: Manage and prepare datasets for training
allowed-tools: Read, Write, Task
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

## Arguments

- `$ARGUMENTS` will contain: `[action] [source] [output]`

## Implementation

Parse arguments and invoke the **dataset-curator** agent with action-specific context.

**Example flow:**

1. Parse action, source, output from $ARGUMENTS
2. Validate source file exists (except for 'analyze')
3. Invoke **dataset-curator** agent with action context:
   - For 'prepare': Load, format, tokenize, validate
   - For 'convert': Detect source format and convert to target
   - For 'analyze': Calculate statistics (num examples, token distribution, quality metrics)
   - For 'clean': Remove duplicates, filter by length, remove invalid entries
   - For 'augment': Use paraphrase, back-translation, or synthesis
   - For 'split': Split into train/val/test (default: 80/10/10)

**Output:**

The agent will:
- Process the dataset according to the action
- Save results to output path
- Display summary statistics
- Provide recommendations for training

**Examples:**

```bash
/dataset prepare raw_data.json training_data.jsonl
/dataset convert alpaca_data.json sharegpt_format.jsonl
/dataset analyze training_data.jsonl
/dataset clean noisy_data.jsonl clean_data.jsonl
/dataset split full_dataset.jsonl train_val_test/
```
