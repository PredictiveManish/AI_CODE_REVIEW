import ast
import os


def extract_code_elements(repo_path):
    code_data = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()

                    tree = ast.parse(code)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            code_data.append({
                                "type": "Function",
                                "name": node.name,
                                "file": file_path,
                                "code": ast.get_source_segment(code, node)
                            })

                        elif isinstance(node, ast.ClassDef):
                            code_data.append({
                                "type": "Class",
                                "name": node.name,
                                "file": file_path,
                                "code": ast.get_source_segment(code, node)
                            })

                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")

    return code_data