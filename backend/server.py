from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, Request, Response
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

# Import our models and utilities
from models import *
from auth import (
    get_current_user, get_current_coach, get_current_athlete,
    verify_password, get_password_hash, create_access_token,
    AuthError
)
from database import db_manager, COLLECTIONS

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="Athletica API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()

# Configure CORS
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


# AUTHENTICATION ENDPOINTS
@api_router.post("/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """Register a new user (coach only for now)."""
    # Check if user already exists
    existing_user = await db_manager.find_one(COLLECTIONS['users'], {"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.dict()
    user_dict.pop('password')
    user_dict['hashed_password'] = hashed_password
    
    # Create user model instance to get the ID
    user = User(**user_dict)
    
    # Save to database
    created_user = await db_manager.create_document(COLLECTIONS['users'], user.dict())
    
    return UserResponse(**created_user)


@api_router.post("/auth/login", response_model=Token)
async def login(response: Response, login_data: LoginRequest):
    """Login user."""
    # Find user by email
    user_doc = await db_manager.find_one(COLLECTIONS['users'], {"email": login_data.email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user_doc['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": user_doc['id'],
            "email": user_doc['email'],
            "role": user_doc['role']
        }
    )
    
    # Set httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=30 * 24 * 60 * 60,  # 30 days
        samesite="lax"
    )
    
    return Token(access_token=access_token, token_type="bearer")


@api_router.post("/auth/logout")
async def logout(response: Response):
    """Logout user."""
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}


@api_router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: TokenData = Depends(get_current_user)):
    """Get current user info."""
    user_doc = await db_manager.get_document(COLLECTIONS['users'], current_user.user_id)
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user_doc)


# ATHLETE ENDPOINTS
@api_router.get("/athletes", response_model=List[Athlete])
async def get_athletes(
    name: Optional[str] = None,
    sector: Optional[str] = None,
    current_user: TokenData = Depends(get_current_coach)
):
    """Get all athletes with optional filtering."""
    query = {}
    if name:
        query["$or"] = [
            {"first_name": {"$regex": name, "$options": "i"}},
            {"last_name": {"$regex": name, "$options": "i"}}
        ]
    if sector:
        query["sector"] = sector
    
    athletes = await db_manager.find_documents(COLLECTIONS['athletes'], query)
    return [Athlete(**athlete) for athlete in athletes]


@api_router.get("/athletes/{athlete_id}", response_model=Athlete)
async def get_athlete(athlete_id: str, current_user: TokenData = Depends(get_current_user)):
    """Get athlete by ID."""
    athlete = await db_manager.get_document(COLLECTIONS['athletes'], athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    
    return Athlete(**athlete)


@api_router.post("/athletes", response_model=Athlete)
async def create_athlete(athlete_data: AthleteCreate, current_user: TokenData = Depends(get_current_coach)):
    """Create a new athlete."""
    athlete = Athlete(**athlete_data.dict())
    created_athlete = await db_manager.create_document(COLLECTIONS['athletes'], athlete.dict())
    return Athlete(**created_athlete)


@api_router.put("/athletes/{athlete_id}", response_model=Athlete)
async def update_athlete(
    athlete_id: str, 
    athlete_data: AthleteUpdate, 
    current_user: TokenData = Depends(get_current_coach)
):
    """Update an athlete."""
    # Get existing athlete
    existing_athlete = await db_manager.get_document(COLLECTIONS['athletes'], athlete_id)
    if not existing_athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    
    # Update only provided fields
    update_data = {k: v for k, v in athlete_data.dict().items() if v is not None}
    
    updated_athlete = await db_manager.update_document(COLLECTIONS['athletes'], athlete_id, update_data)
    return Athlete(**updated_athlete)


@api_router.delete("/athletes/{athlete_id}")
async def delete_athlete(athlete_id: str, current_user: TokenData = Depends(get_current_coach)):
    """Delete an athlete."""
    success = await db_manager.delete_document(COLLECTIONS['athletes'], athlete_id)
    if not success:
        raise HTTPException(status_code=404, detail="Athlete not found")
    
    return {"message": "Athlete deleted successfully"}


# GOALS ENDPOINTS
@api_router.get("/goals", response_model=List[Goal])
async def get_goals(athlete_id: Optional[str] = None, current_user: TokenData = Depends(get_current_user)):
    """Get goals, optionally filtered by athlete."""
    query = {}
    if athlete_id:
        query["athlete_id"] = athlete_id
    
    goals = await db_manager.find_documents(COLLECTIONS['goals'], query)
    return [Goal(**goal) for goal in goals]


@api_router.post("/goals", response_model=Goal)
async def create_goal(goal_data: GoalCreate, current_user: TokenData = Depends(get_current_coach)):
    """Create a new goal."""
    goal = Goal(**goal_data.dict())
    created_goal = await db_manager.create_document(COLLECTIONS['goals'], goal.dict())
    return Goal(**created_goal)


@api_router.put("/goals/{goal_id}", response_model=Goal)
async def update_goal(
    goal_id: str, 
    goal_data: GoalUpdate, 
    current_user: TokenData = Depends(get_current_coach)
):
    """Update a goal."""
    update_data = {k: v for k, v in goal_data.dict().items() if v is not None}
    updated_goal = await db_manager.update_document(COLLECTIONS['goals'], goal_id, update_data)
    
    if not updated_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return Goal(**updated_goal)


@api_router.delete("/goals/{goal_id}")
async def delete_goal(goal_id: str, current_user: TokenData = Depends(get_current_coach)):
    """Delete a goal."""
    success = await db_manager.delete_document(COLLECTIONS['goals'], goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return {"message": "Goal deleted successfully"}


# PROGRAMS ENDPOINTS
@api_router.get("/programs", response_model=List[Program])
async def get_programs(athlete_id: Optional[str] = None, current_user: TokenData = Depends(get_current_user)):
    """Get programs, optionally filtered by athlete."""
    query = {}
    if athlete_id:
        query["athlete_id"] = athlete_id
    
    programs = await db_manager.find_documents(COLLECTIONS['programs'], query)
    return [Program(**program) for program in programs]


@api_router.post("/programs", response_model=Program)
async def create_program(program_data: ProgramCreate, current_user: TokenData = Depends(get_current_coach)):
    """Create a new program."""
    program = Program(**program_data.dict())
    created_program = await db_manager.create_document(COLLECTIONS['programs'], program.dict())
    return Program(**created_program)


@api_router.put("/programs/{program_id}", response_model=Program)
async def update_program(
    program_id: str, 
    program_data: ProgramUpdate, 
    current_user: TokenData = Depends(get_current_coach)
):
    """Update a program."""
    update_data = {k: v for k, v in program_data.dict().items() if v is not None}
    updated_program = await db_manager.update_document(COLLECTIONS['programs'], program_id, update_data)
    
    if not updated_program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    return Program(**updated_program)


@api_router.delete("/programs/{program_id}")
async def delete_program(program_id: str, current_user: TokenData = Depends(get_current_coach)):
    """Delete a program."""
    success = await db_manager.delete_document(COLLECTIONS['programs'], program_id)
    if not success:
        raise HTTPException(status_code=404, detail="Program not found")
    
    return {"message": "Program deleted successfully"}


# SESSIONS ENDPOINTS
@api_router.get("/sessions", response_model=List[Session])
async def get_sessions(
    athlete_id: Optional[str] = None,
    program_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: TokenData = Depends(get_current_user)
):
    """Get sessions with optional filtering."""
    query = {}
    if athlete_id:
        query["athlete_id"] = athlete_id
    if program_id:
        query["program_id"] = program_id
    if start_date and end_date:
        query["start"] = {"$gte": start_date, "$lte": end_date}
    
    sessions = await db_manager.find_documents(COLLECTIONS['sessions'], query)
    return [Session(**session) for session in sessions]


@api_router.post("/sessions", response_model=Session)
async def create_session(session_data: SessionCreate, current_user: TokenData = Depends(get_current_coach)):
    """Create a new session."""
    session = Session(**session_data.dict())
    created_session = await db_manager.create_document(COLLECTIONS['sessions'], session.dict())
    return Session(**created_session)


@api_router.put("/sessions/{session_id}", response_model=Session)
async def update_session(
    session_id: str, 
    session_data: SessionUpdate, 
    current_user: TokenData = Depends(get_current_user)
):
    """Update a session."""
    update_data = {k: v for k, v in session_data.dict().items() if v is not None}
    updated_session = await db_manager.update_document(COLLECTIONS['sessions'], session_id, update_data)
    
    if not updated_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return Session(**updated_session)


@api_router.delete("/sessions/{session_id}")
async def delete_session(session_id: str, current_user: TokenData = Depends(get_current_coach)):
    """Delete a session."""
    success = await db_manager.delete_document(COLLECTIONS['sessions'], session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session deleted successfully"}


# EXERCISES ENDPOINTS
@api_router.get("/exercises", response_model=List[Exercise])
async def get_exercises(category: Optional[ExerciseCategory] = None, current_user: TokenData = Depends(get_current_user)):
    """Get all exercises, optionally filtered by category."""
    query = {}
    if category:
        query["category"] = category.value
    
    exercises = await db_manager.find_documents(COLLECTIONS['exercises'], query)
    return [Exercise(**exercise) for exercise in exercises]


@api_router.post("/exercises", response_model=Exercise)
async def create_exercise(exercise_data: ExerciseCreate, current_user: TokenData = Depends(get_current_coach)):
    """Create a new exercise."""
    exercise = Exercise(**exercise_data.dict())
    created_exercise = await db_manager.create_document(COLLECTIONS['exercises'], exercise.dict())
    return Exercise(**created_exercise)


@api_router.put("/exercises/{exercise_id}", response_model=Exercise)
async def update_exercise(
    exercise_id: str, 
    exercise_data: ExerciseUpdate, 
    current_user: TokenData = Depends(get_current_coach)
):
    """Update an exercise."""
    update_data = {k: v for k, v in exercise_data.dict().items() if v is not None}
    updated_exercise = await db_manager.update_document(COLLECTIONS['exercises'], exercise_id, update_data)
    
    if not updated_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    return Exercise(**updated_exercise)


@api_router.delete("/exercises/{exercise_id}")
async def delete_exercise(exercise_id: str, current_user: TokenData = Depends(get_current_coach)):
    """Delete an exercise."""
    success = await db_manager.delete_document(COLLECTIONS['exercises'], exercise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    return {"message": "Exercise deleted successfully"}


# PHYSICAL ASSESSMENTS ENDPOINTS
@api_router.get("/assessments", response_model=List[PhysicalAssessment])
async def get_assessments(athlete_id: Optional[str] = None, current_user: TokenData = Depends(get_current_user)):
    """Get physical assessments, optionally filtered by athlete."""
    query = {}
    if athlete_id:
        query["athlete_id"] = athlete_id
    
    assessments = await db_manager.find_documents(COLLECTIONS['physical_assessments'], query)
    return [PhysicalAssessment(**assessment) for assessment in assessments]


@api_router.post("/assessments", response_model=PhysicalAssessment)
async def create_assessment(assessment_data: PhysicalAssessmentCreate, current_user: TokenData = Depends(get_current_coach)):
    """Create a new physical assessment."""
    assessment = PhysicalAssessment(**assessment_data.dict())
    created_assessment = await db_manager.create_document(COLLECTIONS['physical_assessments'], assessment.dict())
    return PhysicalAssessment(**created_assessment)


@api_router.put("/assessments/{assessment_id}", response_model=PhysicalAssessment)
async def update_assessment(
    assessment_id: str,
    assessment_data: PhysicalAssessmentCreate,
    current_user: TokenData = Depends(get_current_coach)
):
    """Update a physical assessment."""
    update_data = {k: v for k, v in assessment_data.dict().items() if v is not None}
    updated_assessment = await db_manager.update_document(COLLECTIONS['physical_assessments'], assessment_id, update_data)
    
    if not updated_assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    return PhysicalAssessment(**updated_assessment)


@api_router.delete("/assessments/{assessment_id}")
async def delete_assessment(assessment_id: str, current_user: TokenData = Depends(get_current_coach)):
    """Delete a physical assessment."""
    success = await db_manager.delete_document(COLLECTIONS['physical_assessments'], assessment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    return {"message": "Assessment deleted successfully"}


# PERSONAL RECORDS ENDPOINTS
@api_router.get("/records", response_model=List[PersonalRecord])
async def get_records(athlete_id: Optional[str] = None, current_user: TokenData = Depends(get_current_user)):
    """Get personal records, optionally filtered by athlete."""
    query = {}
    if athlete_id:
        query["athlete_id"] = athlete_id
    
    records = await db_manager.find_documents(COLLECTIONS['personal_records'], query)
    return [PersonalRecord(**record) for record in records]


@api_router.post("/records", response_model=PersonalRecord)
async def create_record(record_data: PersonalRecordCreate, current_user: TokenData = Depends(get_current_coach)):
    """Create a new personal record."""
    record = PersonalRecord(**record_data.dict())
    created_record = await db_manager.create_document(COLLECTIONS['personal_records'], record.dict())
    return PersonalRecord(**created_record)


@api_router.delete("/records/{record_id}")
async def delete_record(record_id: str, current_user: TokenData = Depends(get_current_coach)):
    """Delete a personal record."""
    success = await db_manager.delete_document(COLLECTIONS['personal_records'], record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return {"message": "Record deleted successfully"}


# SESSION TEMPLATES ENDPOINTS
@api_router.get("/templates/sessions", response_model=List[SessionTemplate])
async def get_session_templates(current_user: TokenData = Depends(get_current_user)):
    """Get all session templates."""
    templates = await db_manager.get_documents(COLLECTIONS['session_templates'])
    return [SessionTemplate(**template) for template in templates]


@api_router.post("/templates/sessions", response_model=SessionTemplate)
async def create_session_template(template_data: SessionTemplateCreate, current_user: TokenData = Depends(get_current_coach)):
    """Create a new session template."""
    template = SessionTemplate(**template_data.dict())
    created_template = await db_manager.create_document(COLLECTIONS['session_templates'], template.dict())
    return SessionTemplate(**created_template)


@api_router.delete("/templates/sessions/{template_id}")
async def delete_session_template(template_id: str, current_user: TokenData = Depends(get_current_coach)):
    """Delete a session template."""
    success = await db_manager.delete_document(COLLECTIONS['session_templates'], template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return {"message": "Template deleted successfully"}


# ANALYTICS ENDPOINTS
@api_router.get("/analytics/athlete/{athlete_id}/overview", response_model=AthleteOverview)
async def get_athlete_overview(athlete_id: str, current_user: TokenData = Depends(get_current_user)):
    """Get athlete overview analytics."""
    # Get sessions for the last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    recent_sessions = await db_manager.find_documents(
        COLLECTIONS['sessions'],
        {
            "athlete_id": athlete_id,
            "start": {"$gte": week_ago},
            "status": SessionStatus.DONE.value
        }
    )
    
    # Calculate metrics
    weekly_volume = len(recent_sessions)
    intensity_avg = sum(session.get('intensity', 0) for session in recent_sessions) / len(recent_sessions) if recent_sessions else 0
    
    # Count sessions by type
    sessions_count_by_type = {}
    for session in recent_sessions:
        session_type = session.get('type', 'other')
        sessions_count_by_type[session_type] = sessions_count_by_type.get(session_type, 0) + 1
    
    # Get upcoming events (placeholder - would need Event model integration)
    next_events = []
    
    return AthleteOverview(
        weekly_volume=weekly_volume,
        intensity_avg=round(intensity_avg, 1),
        sessions_count_by_type=sessions_count_by_type,
        next_events=next_events
    )


@api_router.get("/analytics/athlete/{athlete_id}/assessments", response_model=AssessmentSeries)
async def get_athlete_assessments(athlete_id: str, current_user: TokenData = Depends(get_current_user)):
    """Get athlete assessment series for charts."""
    assessments = await db_manager.find_documents(
        COLLECTIONS['physical_assessments'],
        {"athlete_id": athlete_id}
    )
    
    # Sort by date
    assessments.sort(key=lambda x: x['date'])
    
    dates = [assessment['date'].strftime('%Y-%m-%d') for assessment in assessments]
    
    return AssessmentSeries(
        dates=dates,
        strength_max=[assessment.get('strength_max') for assessment in assessments],
        strength_endurance=[assessment.get('strength_endurance') for assessment in assessments],
        strength_explosive=[assessment.get('strength_explosive') for assessment in assessments],
        speed_linear=[assessment.get('speed_linear') for assessment in assessments],
        agility=[assessment.get('agility') for assessment in assessments],
        power=[assessment.get('power') for assessment in assessments],
        mobility=[assessment.get('mobility') for assessment in assessments],
        endurance_aerobic=[assessment.get('endurance_aerobic') for assessment in assessments],
        endurance_lactate=[assessment.get('endurance_lactate') for assessment in assessments],
        icm=[assessment.get('icm') for assessment in assessments]
    )


# Root endpoint for health check
@api_router.get("/")
async def root():
    return {"message": "Athletica API v1.0.0", "status": "healthy"}


# Include the router in the main app
app.include_router(api_router)


@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connections on shutdown."""
    pass  # Motor handles connection cleanup automatically
