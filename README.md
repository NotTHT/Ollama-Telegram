# Telegram AI bot using Ollama

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-white?logo=ollama&logoColor=black)](https://ollama.com/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-0088cc?logo=telegram&logoColor=white)](https://core.telegram.org/bots)

Powered by **Ollama** and **python-telegram-bot**

---

## ✨ Features

- **Local Processing:** Your data stays on your machine. No cloud API subscriptions required.
- **Persistent History:** Automatically saves conversation history per user.
- **Configurable:** Easily swap models, adjust context windows, or change history depth.
- **Type Awareness:** Displays a "typing..." status while the AI is thinking.
---
### Setup

1. Install Ollama from [ollama.com/download](https://ollama.com/download).
2. Pull a model using `ollama pull <model_name>`.
    - For example: `ollama pull gemma3`
3. Pip install
    ```bash
    pip install -r requirements.txt
    ```
4. Rename **.env.copy** to **.env**
    ```bash
    mv .env.copy .env
    ```
5. Fill in your Telegram bot token in *.env*

---
### Checklist:
1. The **.env** file has the right bot token. Run `/newbot` at: [t.me/botfather](https://t.me/botfather)
2. The **.env** file has a model that you have downloaded *(check with `ollama ls`)*
---
6. Run **bot.py**
    ```bash
    python bot.py
    ```


## Environment Variables

You can customize the behavior by editing the `.env` file:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | Your unique Bot API token. | **Required** |
| `OLLAMA_MODEL` | The model name (must be downloaded). | `smollm2` |
| `MAX_HISTORY` | Number of messages to remember for context. | `10` |
| `CONTEXT_WINDOW` | The `num_ctx` passed to Ollama. | `2048` |
| `KEEP_ALIVE` | How long to keep the model in memory. | `-1` (infinite) |

---