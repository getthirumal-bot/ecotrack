"""Test that projects template renders without UndefinedError for hasattr."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

result = []
try:
    from backend.app.main import templates
    result.append("import OK")
    if "hasattr" not in templates.env.globals:
        result.append("FAIL: hasattr not in globals")
    else:
        result.append("hasattr in globals OK")
    # Render the exact fragment from projects.html that was failing
    from jinja2 import Template
    tpl = "{{ row.p.status.value if row.p.status and hasattr(row.p.status, 'value') else row.p.status }}"
    t = templates.env.from_string(tpl)
    class Status:
        value = "active"
    class P:
        status = Status()
        name = "Test"
        id = "1"
    class Row:
        p = P()
    out = t.render(row=Row())
    result.append("render OK: " + out)
except Exception as e:
    result.append("ERROR: " + type(e).__name__ + ": " + str(e))

out_path = r"C:\Users\itadmin\.cursor\projects\psf-Home-Desktop-Ashram-Processes-Nursery\test_result.txt"
with open(out_path, "w") as f:
    f.write("\n".join(result))
