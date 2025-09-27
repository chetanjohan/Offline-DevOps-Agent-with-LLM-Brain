import sys
import os
import importlib
import traceback

# Ensure repo root is on sys.path so `src` packages import correctly
repo_root = os.getcwd()
sys.path.insert(0, repo_root)
print('repo_root added to sys.path:', repo_root)

try:
    m = importlib.import_module('src.llm.llm')
    print('Imported OK, symbols:', [s for s in dir(m) if not s.startswith('_')])
    try:
        print('Calling generate_text (may raise ImportError if llama_cpp or model is missing)')
        out = m.generate_text('Hello from smoke2', max_tokens=5)
        print('generate_text output:', out)
    except Exception as e:
        print('generate_text raised:', type(e).__name__, e)
        traceback.print_exc()
except Exception as e:
    print('Import failed:', type(e).__name__, e)
    traceback.print_exc()
