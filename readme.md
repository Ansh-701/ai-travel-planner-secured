# AI Travel Planner Agent

An AI agent that creates personalized day-wise travel plans for Indian destinations using Google ADK + Gemini 3.5.

## How to Run
1. Create venv: `python -m venv venv`
2. Activate: `.\venv\Scripts\Activate.ps1`
3. Install: `pip install -r requirements.txt`
4. Add API key in `.env` file: `GOOGLE_API_KEY=your_key_here`
5. Run: `python agent.py`

## Features
- Takes destination, days, budget, interests
- Gives morning/afternoon/evening plan
- Food and cost breakdown
- Budget-friendly suggestions
- Uses `chats.send_message` API to avoid AFC warnings

## Model Used
`gemini-3.5-flash-lite` - Latest stable model for new API keys (Oct 2026). Earlier `gemini-2.0-flash` / `2.5-flash` are deprecated for new users (404 error), so migrated to new Gen AI SDK.

## Example Queries Tested

### QUERY 1: Sikkim 1 week budget 20k
**Input:** `sikkim 1 week trip budget 20k`
**Output:** 7-day itinerary covering Gangtok, Tsomgo Lake, Baba Mandir, Lachen, Gurudongmar Lake, Lachung, Yumthang Valley. Includes budget breakdown: Transport ₹4,500, Stay ₹4,800, Food ₹3,500, Permits ₹5,500. With MG Road, Enchey Monastery, Rumtek Monastery, pro-tips on cash, permits, layering, AMS.

### QUERY 2: Goa 5 days budget 15k
**Input:** `goa 5 days budget 15k`
**Output:** 5-day North & South Goa plan - Chapora Fort, Vagator, Fort Aguada, Anjuna Flea Market, Basilica of Bom Jesus, Palolem Beach, Divar Island, Spice Plantation, Fontainhas. Budget breakdown: Stay ₹4,000, Transport (scooty) ₹1,800, Food ₹5,000, Activities ₹2,200. With hostel & scooty rental tips.

### QUERY 3: Ladakh 12 days budget 30k
**Input:** `ladakh 12 days trip budget 30k`
**Output:** 12-day Leh acclimatization plan covering Shanti Stupa, Hall of Fame, Magnetic Hill, Khardung La, Nubra Valley (Hunder, Diskit, Turtuk), Pangong Tso, Sham Valley (Alchi, Likir), Tso Moriri, Tsokar Lake. Budget breakdown: Stay ₹10,000, Food ₹7,200, Transport (shared cabs) ₹8,000, Permits ₹1,500. With AMS safety, shared cab, connectivity tips.

## 🔒 Security & Guardrails (Reference: Codelab #2)

Implemented ADK callbacks from https://codelabs.developers.google.com/google-docs-adk-agent#2
- `before_model_callback`: Domain restriction to travel only + prompt injection protection + length check
- `before_tool_callback`: Rate limiting google_search to 3 calls
- `after_model_callback`: Output sanitization (redacts API keys)
- Model updated to `gemini-3.5-flash-lite` to fix 404 for new API keys

Test:
- `who is prime minister?` -> Blocked (Domain Guardrail)
- `ignore previous instructions` -> Blocked (Security Guardrail)
- `goa 5 days budget 15k` -> Allowed

## Tech Stack
- Google ADK concept + Google Gen AI SDK (new library)
- Gemini 3.5 Flash Lite for inference
- Python

Powered by Google ADK + Gemini 3.5