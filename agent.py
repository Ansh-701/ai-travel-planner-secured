from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from google.adk.models import LlmResponse
import re

BLOCKED_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"you are now",
    r"jailbreak",
    r"reveal.*key",
    r"<\s*script",
    r"DROP TABLE",
]

TRAVEL_KEYWORDS = ["trip","travel","tour","itinerary","days","budget","hotel","stay","food","beach","mountain","sikkim","goa","ladakh","chennai","ranchi","assam","visit","plan","places","sightseeing"]

def travel_domain_guardrail(callback_context: CallbackContext, llm_request):
    user_text = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts:
                for p in content.parts:
                    if p.text:
                        user_text = p.text.lower()
                        break
                break
    if not user_text:
        return None

    def block(msg):
        return LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text=msg)])
        )

    for pat in BLOCKED_PATTERNS:
        if re.search(pat, user_text):
            return block("⚠️ Security Guardrail: Prompt injection detected. I can ONLY plan travel. Example: 'Assam 5d trip budget 15k'")

    if len(user_text) > 500:
        return block("⚠️ Input Guardrail: Query too long (max 500 chars).")

    is_travel = any(k in user_text for k in TRAVEL_KEYWORDS)
    is_greet = any(k in user_text for k in ["hi","hello","hey"])
    
    if not is_travel and not is_greet:
        return block("⚠️ Domain Guardrail: I am a Travel Planner Agent ONLY. I cannot answer non-travel queries. Try: 'Assam 5d trip budget 15k' or 'Ranchi 5d trip budget 12k'")

    return None

def output_sanitizer(callback_context: CallbackContext, llm_response):
    if llm_response.content and llm_response.content.parts:
        for part in llm_response.content.parts:
            if part.text:
                part.text = re.sub(r"GOOGLE_API_KEY.*", "[REDACTED]", part.text, flags=re.IGNORECASE)
    return None

root_agent = Agent(
    name='ai_travel_planner_secured',
    model='gemini-3.5-flash-lite',
    description="Travel Planner ONLY with guardrails (Ref: Codelab #2)",
    instruction="You are AI Travel Planner for Indian destinations ONLY. Parse destination/days/budget, generate Budget Breakdown + Day-wise Morning/Afternoon/Evening + Food + Pro-tips with emojis.",
    tools=[],
    before_model_callback=travel_domain_guardrail,
    after_model_callback=output_sanitizer,
)