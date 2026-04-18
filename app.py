import gradio as gr
import re

def transform_v6_to_v7(code):
    """
    web3.py v6 -> v7 automated migration logic
    """
    if not code or not code.strip():
        return "Enter some code...?"

    # --- 1. Parameter and method renaming (camelCase -> snake_case) ---
    exact_map = [
        (r'\bWebsocketProviderV2\b', 'WebSocketProvider'),
        (r'\bWebsocketProvider\b', 'LegacyWebSocketProvider'),
        (r'\b(\w+)\.persistent_websocket\(', r'\1('),
        (r'\bws\.process_subscriptions\b', 'socket.process_subscriptions'),
        (r'\bfromBlock\b', 'from_block'),
        (r'\btoBlock\b', 'to_block'),
        (r'\bblockHash\b', 'block_hash'),
        (r'\bmiddlewares\b', 'middleware'),
        (r'\bencodeABI\b', 'encode_abi'),
        (r'\bCallOverride\b', 'StateOverride'),
    ]

    # --- 2. Exception class replacement ---
    exception_map = {
        r'\bValueError\b': 'Web3ValueError',
        r'\bTypeError\b': 'Web3TypeError',
        r'\bAttributeError\b': 'Web3AttributeError',
        r'\bAssertionError\b': 'Web3AssertionError',
    }

    new_code = code

    # Execute exact string/regex replacements
    for old, new in exact_map:
        new_code = re.sub(old, new, new_code)

    # Execute exception replacement
    for old, new in exception_map.items():
        new_code = re.sub(old, new, new_code)

    # --- 3. Middleware Refactoring ---
    middleware_map = {
        r'\bpythonic_middleware\b': 'PythonicMiddleware',
        r'\bgeth_poa_middleware\b': 'ExtraDataToPOAMiddleware',
        r'\bname_to_address_middleware\b': 'ENSNameToAddressMiddleware',
        r'\bconstruct_sign_and_send_raw_middleware\b': 'SignAndSendRawMiddlewareBuilder.build',
    }
    for old, new in middleware_map.items():
        new_code = re.sub(old, new, new_code)

    # --- 4. Auto-import missing dependencies ---
    if "Web3ValueError" in new_code and "from web3.exceptions" not in new_code:
        new_code = "from web3.exceptions import Web3ValueError, Web3TypeError, Web3AttributeError\n" + new_code
    
    if "PythonicMiddleware" in new_code and "from web3.middleware" not in new_code:
        new_code = "from web3.middleware import PythonicMiddleware\n" + new_code
        
    if "SignAndSendRawMiddlewareBuilder" in new_code and "from web3.middleware" not in new_code:
        new_code = "from web3.middleware import SignAndSendRawMiddlewareBuilder\n" + new_code

    # --- 5. Deprecations and Removals Warnings ---
    warnings = []
    removed_middlewares = [
        "abi_middleware", "simple_cache_middleware", "latest_block_based_cache_middleware",
        "time_based_cache_middleware", "fixture_middleware", "result_generator_middleware",
        "http_retry_request_middleware", "normalize_request_parameters"
    ]
    
    for rm in removed_middlewares:
        if rm in new_code:
            warnings.append(f"# WARNING: {rm} has been removed in v7.")
            
    if "EthPM" in new_code or "ethpm" in new_code:
        warnings.append("# WARNING: EthPM module has been removed in v7.")
    if "geth.miner" in new_code:
        warnings.append("# WARNING: geth.miner namespace has been removed in v7.")
    if "geth.personal" in new_code:
        warnings.append("# WARNING: geth.personal namespace has been removed in v7.")

    if warnings:
        new_code = "\n".join(warnings) + "\n\n" + new_code

    return new_code

# --- Gradio UI ---
# Fixed the theme error by using the default Soft theme parameters
theme = gr.themes.Soft()

with gr.Blocks(theme=theme, title="Web3Py V7 Transmuter") as demo:
    gr.Markdown("""
    # 🧪 Web3Py V7 Transmuter
    ### Quickly migrate legacy Python Web3 code to V7 specification

    ---
    **🤖 Notice for AI Intervention:**
    While this tool automates syntax migrations, complex logical refactoring cannot always be statically resolved. **For asynchronous function promotions that cannot be determined in the script, or custom middleware class rewriting, please cooperate with a Codemod AI agent for logical refactoring.**
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            # Used gr.Code instead of gr.Textbox for syntax highlighting on the input
            input_area = gr.Code(
                label="📥 V6 Legacy Code (Before)", 
                language="python",
                lines=18
            )
        with gr.Column(scale=1):
            output_area = gr.Code(
                label="📤 V7 Refactored Code (After)", 
                language="python",
                lines=18
            )
            
    with gr.Row():
        clear_btn = gr.Button("Clear")
        submit_btn = gr.Button("🚀 Start 1-Click Transformation", variant="primary")

    submit_btn.click(fn=transform_v6_to_v7, inputs=input_area, outputs=output_area)
    clear_btn.click(lambda: [None, None], outputs=[input_area, output_area])

    gr.Examples(
        label="Test Cases (Click to populate)",
        examples=[
            ["# Example 1: Variable Name & Exception Replacement\ndef get_logs():\n    try:\n        return w3.eth.get_logs(fromBlock=1, toBlock='latest')\n    except ValueError:\n        return None"],
            ["# Example 2: Middleware Refactoring\nw3.middleware_onion.add(pythonic_middleware)"],
            ["# Example 3: WebSocket Upgrade\nw3.ws.process_subscriptions()"],
            ["# Example 4: v7 Deprecations\nw3.middleware_onion.add(abi_middleware)\nimport ethpm\nfrom web3 import WebsocketProviderV2\nAsyncWeb3.persistent_websocket(WebsocketProviderV2('...'))"]
        ],
        inputs=input_area
    )

if __name__ == "__main__":
    demo.launch()
