import json
import ast
import traceback

notebook_path = "c:/Users/thela/OneDrive/Desktop/personal projets/multi domain projects/Clean-SupplyChain-Finance/backend/ai-ml/notebooks/Data_Prep_and_Feature_Extraction_Colab.ipynb"

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    print("Notebook parsed successfully.")
    
    # Check Cell 9 (Log-Signatures)
    cell_9_source = "".join(nb['cells'][9]['source'])
    # Filter out jupyter magic commands (!pip etc)
    clean_source_9 = "\n".join([line for line in cell_9_source.split('\n') if not line.strip().startswith('!')])
    ast.parse(clean_source_9)
    print("Cell 9 (Log-Signatures): Syntax OK")
    
    # Check Cell 11 (Topological Fraud)
    cell_11_source = "".join(nb['cells'][11]['source'])
    clean_source_11 = "\n".join([line for line in cell_11_source.split('\n') if not line.strip().startswith('!')])
    ast.parse(clean_source_11)
    print("Cell 11 (Topological Fraud): Syntax OK")
    
except Exception as e:
    print(traceback.format_exc())
    print("TEST FAILED")
