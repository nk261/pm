from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import json
import asyncio

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Import Gemini integration
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Create the main app without a prefix
app = FastAPI(title="Autonomous AI Project Manager", description="AI system that completely replaces human project managers")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class ProjectRequirements(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    business_context: str
    success_criteria: str
    constraints: str
    stakeholders: str
    timeline_preference: str
    budget_range: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectObjective(BaseModel):
    objective: str
    specific: str
    measurable: str
    achievable: str
    relevant: str
    time_bound: str

class WBSTask(BaseModel):
    id: str
    name: str
    description: str
    level: int
    parent_id: Optional[str] = None
    estimated_hours: int
    dependencies: List[str] = []
    assigned_role: str
    priority: str

class ResourceEstimate(BaseModel):
    role: str
    hours_required: int
    skill_level: str
    cost_estimate: Optional[float] = None

class RiskItem(BaseModel):
    risk: str
    probability: str
    impact: str
    mitigation_strategy: str
    owner: str

class ProjectPlan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_requirements_id: str
    objectives: List[ProjectObjective]
    wbs_tasks: List[WBSTask]
    timeline_weeks: int
    resource_estimates: List[ResourceEstimate]
    risk_analysis: List[RiskItem]
    success_metrics: List[str]
    next_steps: List[str]
    confidence_score: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectRequirementsCreate(BaseModel):
    title: str
    description: str
    business_context: str
    success_criteria: str
    constraints: str
    stakeholders: str
    timeline_preference: str
    budget_range: Optional[str] = None

# Initialize Gemini Chat
def get_gemini_chat():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")
    
    return LlmChat(
        api_key=api_key,
        session_id=f"planning_agent_{uuid.uuid4()}",
        system_message="""You are an expert AI Project Manager with 20+ years of experience in project planning and management. 
        Your role is to analyze project requirements and generate comprehensive, professional project plans that completely replace human PM capabilities.
        
        You excel at:
        - Converting vague requirements into SMART objectives
        - Creating detailed Work Breakdown Structures (WBS)
        - Estimating realistic timelines and resources
        - Identifying risks and mitigation strategies
        - Defining success metrics and KPIs
        
        Always provide structured, actionable project plans that demonstrate superior analysis compared to human project managers."""
    ).with_model("gemini", "gemini-2.0-flash").with_max_tokens(8000)

async def generate_project_plan(requirements: ProjectRequirements) -> Dict[str, Any]:
    """AI Planning Agent - Core function that replaces human project planning"""
    
    chat = get_gemini_chat()
    
    planning_prompt = f"""
    AUTONOMOUS PROJECT PLANNING REQUEST

    PROJECT DETAILS:
    - Title: {requirements.title}
    - Description: {requirements.description}
    - Business Context: {requirements.business_context}
    - Success Criteria: {requirements.success_criteria}
    - Constraints: {requirements.constraints}
    - Stakeholders: {requirements.stakeholders}
    - Timeline Preference: {requirements.timeline_preference}
    - Budget Range: {requirements.budget_range or 'Not specified'}

    GENERATE A COMPREHENSIVE PROJECT PLAN WITH THE FOLLOWING STRUCTURE:

    Please respond with a valid JSON object containing:

    {{
        "objectives": [
            {{
                "objective": "Main objective statement",
                "specific": "Specific details",
                "measurable": "How success will be measured",
                "achievable": "Why this is achievable",
                "relevant": "Business relevance",
                "time_bound": "Timeline commitment"
            }}
        ],
        "wbs_tasks": [
            {{
                "id": "task_1",
                "name": "Task Name",
                "description": "Detailed task description",
                "level": 1,
                "parent_id": null,
                "estimated_hours": 40,
                "dependencies": [],
                "assigned_role": "Role responsible",
                "priority": "High/Medium/Low"
            }}
        ],
        "timeline_weeks": 12,
        "resource_estimates": [
            {{
                "role": "Project Manager",
                "hours_required": 200,
                "skill_level": "Senior",
                "cost_estimate": 25000
            }}
        ],
        "risk_analysis": [
            {{
                "risk": "Risk description",
                "probability": "High/Medium/Low",
                "impact": "High/Medium/Low", 
                "mitigation_strategy": "How to mitigate",
                "owner": "Who owns this risk"
            }}
        ],
        "success_metrics": ["Metric 1", "Metric 2"],
        "next_steps": ["Step 1", "Step 2"],
        "confidence_score": 0.85
    }}

    IMPORTANT: Return ONLY the JSON object, no additional text or formatting.
    """

    try:
        user_message = UserMessage(text=planning_prompt)
        response = await chat.send_message(user_message)
        
        # Parse the JSON response
        response_text = response.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:-3]
        elif response_text.startswith('```'):
            response_text = response_text[3:-3]
            
        plan_data = json.loads(response_text)
        return plan_data
        
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON from Gemini response: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate valid project plan")
    except Exception as e:
        logging.error(f"Error generating project plan: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate project plan")

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Autonomous AI Project Manager - Planning Agent Ready"}

@api_router.post("/project-requirements", response_model=ProjectRequirements)
async def create_project_requirements(input: ProjectRequirementsCreate):
    """Submit project requirements for AI analysis"""
    requirements_dict = input.dict()
    requirements_obj = ProjectRequirements(**requirements_dict)
    await db.project_requirements.insert_one(requirements_obj.dict())
    return requirements_obj

@api_router.get("/project-requirements/{requirements_id}", response_model=ProjectRequirements)
async def get_project_requirements(requirements_id: str):
    """Get project requirements by ID"""
    requirements = await db.project_requirements.find_one({"id": requirements_id})
    if not requirements:
        raise HTTPException(status_code=404, detail="Project requirements not found")
    return ProjectRequirements(**requirements)

@api_router.post("/generate-plan/{requirements_id}")
async def generate_plan(requirements_id: str):
    """AI Planning Agent - Generate comprehensive project plan"""
    
    # Get project requirements
    requirements_doc = await db.project_requirements.find_one({"id": requirements_id})
    if not requirements_doc:
        raise HTTPException(status_code=404, detail="Project requirements not found")
    
    requirements = ProjectRequirements(**requirements_doc)
    
    # Generate AI-powered project plan
    try:
        plan_data = await generate_project_plan(requirements)
        
        # Create project plan object
        project_plan = ProjectPlan(
            project_requirements_id=requirements_id,
            objectives=[ProjectObjective(**obj) for obj in plan_data["objectives"]],
            wbs_tasks=[WBSTask(**task) for task in plan_data["wbs_tasks"]],
            timeline_weeks=plan_data["timeline_weeks"],
            resource_estimates=[ResourceEstimate(**res) for res in plan_data["resource_estimates"]],
            risk_analysis=[RiskItem(**risk) for risk in plan_data["risk_analysis"]],
            success_metrics=plan_data["success_metrics"],
            next_steps=plan_data["next_steps"],
            confidence_score=plan_data["confidence_score"]
        )
        
        # Save to database
        await db.project_plans.insert_one(project_plan.dict())
        
        return project_plan
        
    except Exception as e:
        logging.error(f"Error in generate_plan: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate project plan: {str(e)}")

@api_router.get("/project-plan/{plan_id}")
async def get_project_plan(plan_id: str):
    """Get generated project plan by ID"""
    plan = await db.project_plans.find_one({"id": plan_id})
    if not plan:
        raise HTTPException(status_code=404, detail="Project plan not found")
    return plan

@api_router.get("/project-plans")
async def get_all_project_plans():
    """Get all generated project plans"""
    plans = await db.project_plans.find().to_list(100)
    return plans

@api_router.get("/project-requirements")
async def get_all_project_requirements():
    """Get all project requirements"""
    requirements = await db.project_requirements.find().to_list(100)
    # Convert ObjectId to string for JSON serialization
    for req in requirements:
        if '_id' in req:
            del req['_id']
    return requirements

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
