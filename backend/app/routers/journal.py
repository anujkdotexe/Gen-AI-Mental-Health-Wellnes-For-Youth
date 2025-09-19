from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_journal_entries():
    return {"message": "Journal endpoints coming soon"}

@router.post("/entries")
async def create_journal_entry():
    return {"message": "Create journal entry endpoint"}

@router.get("/ai-prompts")
async def get_ai_prompts():
    return [
        "What are three things you're grateful for today?",
        "Describe a moment when you felt proud of yourself.",
        "What's one challenge you're facing and how might you approach it?",
        "Write about a person who makes you feel supported.",
        "What's something new you learned about yourself recently?"
    ]