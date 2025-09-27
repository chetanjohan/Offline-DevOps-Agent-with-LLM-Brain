import importlib
import traceback

print("Importing src.llm.llm")
try:
    m = importlib.import_module("src.llm.llm")
    print("Imported OK, symbols:", [s for s in dir(m) if not s.startswith("_")])
    try:
        print("Calling generate_text (expected to fail if llama_cpp or model missing)")
        out = m.generate_text("Hello from smoke test", max_tokens=5)
        print("generate_text output:", out)
    except Exception as e:
        print("generate_text raised:", type(e).__name__, e)
        traceback.print_exc()
except Exception as e:
    print("Import failed:", type(e).__name__, e)
    traceback.print_exc()
