# 🧪 Web3Py V7 Transmuter

**Web3Py V7 Transmuter** is an automated migration engine designed to eliminate the friction of upgrading legacy `web3.py` v6 codebases to the new v7 specification. 

By combining **deterministic codemods** with **AI-assisted safety checks**, this tool automates over 80% of the mechanical refactoring required for a production-grade upgrade.

## ✨ Key Features

- **Deterministic Refactoring**: Automates the conversion of `camelCase` parameters to `snake_case` (e.g., `fromBlock` → `from_block`).
- **Class-Based Middleware Migration**: Rewrites functional middleware calls to the new v7 class-based model.
- **Exception Refactoring**: Automatically replaces standard Python exceptions with specialized `Web3Exception` classes and fixes required imports.
- **Safety Warning System**: Detects and warns about deprecated or removed modules such as `EthPM` and the `geth.miner` namespace.
- **WebSocket Interface Upgrade**: Updates `WebSocketProvider` instantiation and subscription handling logic.

## 🔗 Live Demo
Experience the interactive migration tool on Hugging Face Spaces: 
**https://huggingface.co/spaces/kikl/Web3Py-V7-Transmuter**

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.10+

### Local Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/rawetrip/web3py-v7-transmuter.git]
