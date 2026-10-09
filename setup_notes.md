
This repo should become a helper for filling out expense reports in Concur.

The idea is to have people clone this repo, open it in VS Code, and then start a copilot agent, which uses the browser to fill in the reports. This will not only be a collection of skills because apart from skills we also need to make sure that there existtools for converting invoices from PDF to text.

Components we need:
- Agent skills which tell agents how to handle
  - Facts about expenses, taxes, etc.
  - How to interact with the Concur system via web browser
- Simple python script/shell script or similar which the agent can call to convert PDF to text so it can read and extract relevant information from invoices.
- Setup script (e.g. in Python) which ensures that a necessary pdf conversion tool is available to the agent or alternatively installs it if missing.
- Information infrastructure
  - A document where the user enters personal info such as address or name. Simple markdown is fine and agent-friendly. Provide templates for this in the repo
  - A document for company specific regulations, e.g. limits
  - A receipts folder convention: for example, receipts/inbox/ → receipts/processed/ so the agent knows what's new.
  - A log file where the agent can record actions taken and any issues encountered.


Apart from that the usual:
- README with instructions
- AGENTS markdown file
- .gitignore