import os
from notion_client import Client
from markdown2 import markdown
from fpdf import FPDF
from datetime import datetime

# Setup
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE_ID"]

# Query database
response = notion.databases.query(database_id=database_id)
items = response["results"]

# Build Markdown content
content = f"# Daily Tasks – {datetime.today().strftime('%Y-%m-%d')}\n\n"

for item in items:
    props = item["properties"]
    name = props.get("Name", {}).get("title", [])
    task = name[0]["plain_text"] if name else "Untitled Task"
    content += f"- {task}\n"

# Save to Markdown
with open("daily_tasks.md", "w") as f:
    f.write(content)

# Convert to PDF
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)
for line in content.split("\n"):
    pdf.cell(200, 10, txt=line, ln=True)

pdf.output("daily_tasks.pdf")
