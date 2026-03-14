"""Verify status_display is used in template and view builds it."""
import os
base = os.path.dirname(os.path.abspath(__file__))
os.chdir(base)
results = []

# Check template uses status_display
with open(os.path.join(base, "backend", "templates", "projects.html")) as f:
    content = f.read()
if "hasattr" in content:
    results.append("FAIL: template still contains hasattr")
elif "row.status_display" not in content:
    results.append("FAIL: template does not use row.status_display")
else:
    results.append("PASS: template uses row.status_display, no hasattr")

# Check view builds status_display
with open(os.path.join(base, "backend", "app", "main.py")) as f:
    main_content = f.read()
if "status_display" not in main_content or "hasattr(p.status" not in main_content:
    results.append("FAIL: view does not set status_display")
else:
    results.append("PASS: view sets status_display from hasattr(p.status)")

# Write to workspace so we can read it
out = os.path.join(base, "verify_result.txt")
with open(out, "w") as f:
    f.write("\n".join(results))
