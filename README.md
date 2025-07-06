# <center>ASTRA✨ — Always Adapting, Always Ahead</center>

> ***It isn’t just a*** **MCP server** **— ASTRA** **✨** ***is your ever-evolving toolkit and digital companion.***  
> Today it…  
> 
> * 🗺️ **Plans trips**  
> * 🌦️ **Checks the weather**  
> * 📧 **Reads your emails**  
> * 🗓️ **Schedules tasks & meetings** from your inbox  
> * ✅ **Reminds you of new to-dos**  
> 
> …and ***tomorrow***, it’ll do **even more!** 🎉  

---

![ASTRA Logo](assets/ASTRA_1.png)

**ASTRA**  
<small><em>(Assistant for <u>Scheduling</u>, <u>Travel</u>, <u>Routines</u>, and <u>Automation</u>)</em></small>  

> **What’s under the hood?**  
> ASTRA uses the **Model Context Protocol** to expose 🤖 _modular “tools”_—each one just a Python function in `tools/`—so **Claude Desktop** (or any MCP-aware client) can auto-discover and fire them off.

---

## ⭐ Features

- **Trip Planning & Itineraries**  
  🏖️ Day-by-day plans that blend weather forecasts with top attractions—no more “where to go today?” panic.

- **Real-Time Weather**  
  🌡️ Get a 5-day forecast: temps, humidity, wind, rain/snow, sunrise/sunset—so you pack like a pro.

- **WhatsApp Messaging**  
  📱 Instant click-to-chat URLs from your own contacts list and custom messages—because typing is overrated.

- **Todoist Integration**  
  📋 Create, read, update, & delete tasks in your “Meetings,” “Shopping,” or “Reminders” projects—task-ninja mode activated.

- **Email Intelligence**  
  ✉️ Scan Gmail for meetings, interviews, verifications, subscriptions, deliveries—extract body text, links, attachments & invites (yes, ICS files too!).

- **…and Growing**  
  🛠️ New skills and automations roll out continuously. Suggest a tool, and ASTRA might just build it next week!

---

## ⚡ Getting Started

1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt

2. **Configure your environment**
   Copy `.env.example` → `.env` and fill in your API keys & credentials.

3. **Run the server**

   ```bash
   python main.py
   ```

   Or via MCP-CLI:

   ```bash
   uv run --with mcp[cli] mcp run main.py
   ```

4. **Hook up Claude Desktop**

   * Open **Claude Desktop** Preferences → **Tools**.
   * Add `http://localhost:8000` as an MCP server.
   * Watch ASTRA’s toolbox appear—no reboot required.

---

## 🔧 Tool Workflow

1. **Define** a new tool in `tools/your_tool.py`
2. **Decorate** it in `main.py` with `@app.tool()`
3. **Restart** ASTRA: `python main.py`
4. **Invoke** it from Claude Desktop (or any MCP-enabled client)

> **Pro tip:**
> Got a crazy idea? Build it, plug it in, and tell ASTRA to “just do it.” It’s your tireless AI sidekick—minus the coffee breaks. ☕🚫

Enjoy your new digital wingman—ASTRA’s got your back, day and night! 🌟

```
```
