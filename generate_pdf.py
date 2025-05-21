import os
from notion_client import Client
from fpdf import FPDF
from datetime import datetime

# Get token and database ID from environment
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

# Set up Notion client
notion = Client(auth=NOTION_TOKEN)

# Query database
response = notion.databases.query(database_id=DATABASE_ID)
results = response.get("results", [])

# Prepare content
today = datetime.today().strftime("%Y-%m-%d")
content = f"Daily Tasks – {today}\n\n"

for item in results:
    title_prop = item["properties"].get("Name", {}).get("title", [])
    title = title_prop[0]["plain_text"] if title_prop else "Untitled Task"
    content += f"- {title}\n"

# Generate PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
for line in content.strip().split("\n"):
    pdf.cell(200, 10, txt=line, ln=True)

pdf.output("daily_tasks.pdf")
