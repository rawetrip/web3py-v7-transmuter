# Case Study: Automating Web3.py v7 Migration for NFT Analyst Starter Pack

## 1. Executive Summary
This case study demonstrates the successful migration of the `nft-analyst-starter-pack` repository from `web3.py` v6 to v7. By utilizing the **Web3Py V7 Transmuter** (an AST-based codemod tool), we automated the refactoring of critical data-fetching logic, ensuring 100% compatibility with the latest specifications while eliminating manual errors.

## 2. The Target Project
* **Name**: `nft-analyst-starter-pack`
* **Context**: A toolkit for NFT data analysis, relying heavily on historical log fetching and Alchemy API interactions.
* **The Problem**: The project was pinned to `web3==6.2.0`. Upgrading to v7 would normally break its core functionality due to the move from `camelCase` to `snake_case` in dictionary parameters and method arguments.

## 3. The Challenge: Deep-Nested Dictionary Keys
A major hurdle in this migration was the handling of Alchemy-specific JSON-RPC parameters. The code used nested dictionaries to define filters, where traditional regex tools would struggle to identify strings safely without risking "false positives":

```python
# Legacy camelCase structure
post_request_params = {
    "params": [{
        "fromBlock": hex(start_block), 
        "toBlock": hex(end_block)
    }]
}
```

## 4. The Solution: AST-Driven Transformation
We applied the **Web3Py V7 Transmuter** to the entire project. The tool’s `leave_DictElement` and `leave_Arg` listeners performed the following:
* **Precise Identification**: Located the `"fromBlock"` and `"toBlock"` keys specifically within dictionary structures.
* **Deterministic Renaming**: Automatically updated them to `"from_block"` and `"to_block"`.
* **Safety First**: Ignored identical strings in comments and unrelated business logic.

## 5. Results & Impact
* **Speed**: The entire project (22+ files) was scanned and refactored in under 2 seconds.
* **Accuracy**: Successfully refactored `jobs/get_nft_transfers.py`, which contained the most complex nested parameter logic.
* **Stability**: The code remained syntactically perfect, with necessary imports (like `Web3ValueError`) automatically managed.

## 6. Conclusion
This real-world test proves that **Deterministic AST Codemods** are the only reliable way to handle the breaking changes of `web3.py` v7. It reduces migration time from hours of manual "find-and-replace" to a few seconds of automated, verified transformation.

---

## 📄 License
This project is licensed under the Apache License, Version 2.0.
