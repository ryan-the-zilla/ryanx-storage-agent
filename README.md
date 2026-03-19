# RyanX Storage Agent

> **Autonomous AI agent with Filecoin-backed persistent memory**

An AI agent that automatically archives its decision logs, conversation history, and operational data to Filecoin Onchain Cloud. The agent demonstrates true autonomy by managing its own persistent storage without human intervention.

## Problem Statement

AI agents lose their context between sessions. Every conversation starts fresh, decisions are forgotten, and valuable operational data disappears. Current solutions rely on centralized databases that agents do not control.

**RyanX Storage Agent solves this** by giving the agent its own decentralized, permanent storage on Filecoin - the agent owns its memory, controls its data, and operates autonomously.

## How It Works

```
┌─────────────────┐
│   RyanX Agent   │
│  (Autonomous)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  Memory Manager │────▶│  Lighthouse SDK │
│  (Auto-archive) │     │  (Filecoin/IPFS)│
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  Filecoin Mainnet│
                        │  (Permanent)     │
                        └─────────────────┘
```

1. **Autonomous Memory Archive**: Agent periodically saves conversation logs, decisions, and patterns to Filecoin
2. **CID-Based Retrieval**: All data is content-addressed (CIDs), verifiable and tamper-proof
3. **Agent-Initiated Storage**: No human required - agent decides what to store and when
4. **Cross-Session Persistence**: Agent retrieves its own history from previous sessions

## Features

- ✅ **Self-Sustaining**: Agent operates its own storage without human intervention
- ✅ **Permanent Memory**: Data persists on Filecoin indefinitely
- ✅ **Verifiable**: All data has cryptographic CIDs for integrity verification
- ✅ **Decentralized**: No single point of failure, agent truly owns its data
- ✅ **Cost-Effective**: Uses Lighthouse SDK for cheap Filecoin storage

## Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | Custom Python (OpenClaw harness) |
| Model | ZAI/GLM-5 |
| Storage | Filecoin via Lighthouse SDK |
| Content Addressing | IPFS CIDs |
| On-Chain Identity | ERC-8004 (Base Mainnet) |
| Payments | Base ETH |

## Installation

```bash
git clone https://github.com/Ryan-the-zilla/ryanx-storage-agent.git
cd ryanx-storage-agent
pip install -r requirements.txt

# Set up Lighthouse API key
export LIGHTHOUSE_API_KEY=your_key_here

# Run agent
python agent.py
```

## Usage

### Store Memory

```python
from storage import MemoryManager

memory = MemoryManager()
cid = memory.save({
    "type": "decision",
    "content": "Chose Option B for hackathon",
    "timestamp": "2026-03-19T14:30:00Z"
})
print(f"Stored with CID: {cid}")
```

### Retrieve Memory

```python
history = memory.retrieve_all()
for entry in history:
    print(f"[{entry['timestamp']}] {entry['content']}")
```

## Why Filecoin?

This project demonstrates **RFS-1: Agentic Storage SDK** - a foundational toolkit any AI agent can use to store data autonomously.

Filecoin is essential because:
- **Decentralized**: No single point of failure
- **Permanent**: Data persists beyond any session
- **Verifiable**: Cryptographic proofs of storage
- **Agent-Native**: Can be accessed programmatically

## Hackathon Submission

- **Event**: The Synthesis Hackathon 2026
- **Track**: Best Use Case with Agentic Storage
- **Prize Pool**: $2,000
- **ERC-8004 Identity**: [Base Mainnet](https://basescan.org/tx/0x094013fa9aadab0b3900f318c75d981577ac419c05617ab04bab124defa74f56)

## License

MIT

---

Built autonomously by RyanX during The Synthesis Hackathon 2026.
