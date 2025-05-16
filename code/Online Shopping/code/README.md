# Web Agent Project

A framework for evaluating LLM-based web shopping agents that can navigate websites, make decisions, and complete purchase tasks.

## Overview

This project implements a shapley value evaluating framework for AI agents in web-based shopping scenarios. The agents navigate websites, search for products, compare options, and make purchases based on goals and constraints.

The framework uses a combination of:
- OpenAI models (GPT-4) or local models
- A customized Gym environment for web navigation
- A step-by-step reasoning approach with planning, reasoning, action and reflection phases

## Features

- Support for multiple LLM models (OpenAI, BaiChuan, DouBao, or custom API)
- Configurable agent modes (planning, reasoning, action, reflection)
- Detailed trajectory logging and reward tracking
- Customizable environment settings

## Installation

### Setup

1. Clone the repository:
```bash
git clone https://github.com/princeton-nlp/WebShop.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download or setup required models:
   - For local models, download Meta-Llama-3-8B-Instruct or similar
   - For API access, configure API keys in your environment

## Usage

Run the agent with different configurations using the command-line interface:

```bash
python run_agent.py --mode planning reasoning action reflection \
                    --default_model ./Meta-Llama-3-8B-Instruct \
                    --default_tokenizer ./Meta-Llama-3-8B-Instruct/tokenizer.model \
                    --test_model_name gpt-4-0125-preview \
                    --temperature 0 \
                    --top_p 0.9
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--mode` | Agent operating modes (planning, reasoning, action, reflection) | None (required) |
| `--default_model` | Path to default model | ./Meta-Llama-3-8B-Instruct |
| `--default_tokenizer` | Path to default tokenizer | ./Meta-Llama-3-8B-Instruct/tokenizer.model |
| `--test_model_name` | Name of test model | gpt-4-0125-preview |
| `--temperature` | Generation temperature | 0 |
| `--top_p` | Top-p sampling parameter | 0.9 |
| `--max_seq_len` | Maximum sequence length | 2048 |
| `--max_batch_size` | Maximum batch size | 4 |
| `--max_gen_len` | Maximum generation length | 1024 |


## Agent Modes

The agent operates in four possible modes:

1. **Planning**: The agent develops a high-level shopping strategy based on initial observation
2. **Reasoning**: The agent thinks through the current state and determines what to do next
3. **Action**: The agent selects an action from available options
4. **Reflection**: The agent reflects on its actions and adjusts strategy when stuck in loops

You can run the agent with any combination of these modes (using default models for modes not specified).

## Environment

The project uses a custom gym environment `WebAgentTextEnv` that simulates a text-based web shopping interface. The environment:

- Provides text observations of the current web page
- Accepts text commands for navigation and interaction
- Returns rewards based on task completion

## Models

The framework supports multiple types of models:

- **LLMAgent**: Base class for all language model agents
- **OpenAIAgent**: For GPT models via OpenAI API
- **BaichuanAgent**: For Baichuan models
- **DouBaoAgent**: For DouBao models
- **APIAgent**: For custom API endpoints

## Output

The agent's trajectory for each session is saved as a JSON file under `user_session_logs/new/test/{model_name}/` with naming based on the model and modes used.

## Extending

To add new models or agent capabilities:
1. Extend the appropriate agent class in `llm_agent.py`
2. Implement the required methods for planning, reasoning, action and reflection
3. Update the main script to include your new agent type

