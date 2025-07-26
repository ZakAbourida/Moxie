from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

# Enums
class UserRole(str, Enum):
    COACH = "coach"
    ATHLETE = "athlete"

class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class GoalType(str, Enum):
    PERFORMANCE = "performance"
    TECHNICAL = "technical"
    PHYSICAL = "physical"
    HEALTH = "health"
    OTHER = "other"

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class GoalStatus(str, Enum):
    ACTIVE = "active"
    ACHIEVED = "achieved"
    FAILED = "failed"
    ABANDONED = "abandoned"
    POSTPONED = "postponed"

class ProgramStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELED = "canceled"

class SessionType(str, Enum):
    GYM = "gym"
    TECHNIQUE = "technique"
    SPEED = "speed"
    ENDURANCE = "endurance"
    REST = "rest"
    OTHER = "other"

class SessionStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    DONE = "done"
    CANCELED = "canceled"

class ExerciseCategory(str, Enum):
    LEGS = "legs"
    PUSH = "push"
    PULL = "pull"
    CORE = "core"
    OLYMPIC = "olympic"
    MOBILITY = "mobility"
    OTHER = "other"

# Base Models
class BaseDBModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# User Models
class User(BaseDBModel):
    role: UserRole
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str

class UserCreate(BaseModel):
    role: UserRole
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    id: str
    role: UserRole
    email: str
    first_name: str
    last_name: str
    created_at: datetime

# Injury Model
class Injury(BaseModel):
    date: datetime
    type: str
    notes: Optional[str] = None

# Athlete Models
class Athlete(BaseDBModel):
    first_name: str
    last_name: str
    birth_date: Optional[datetime] = None
    sex: Optional[Sex] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    specialties: List[str] = []
    sector: Optional[str] = None
    photo_url: Optional[str] = None
    category: Optional[str] = None
    coach_name: Optional[str] = None
    club: Optional[str] = None
    notes: Optional[str] = None
    health_status: Optional[str] = None
    strengths: List[str] = []
    weaknesses: List[str] = []
    injuries: List[Injury] = []
    allergies_limitations: List[str] = []
    user_id: Optional[str] = None  # FK to User when athlete has login

class AthleteCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[datetime] = None
    sex: Optional[Sex] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    specialties: List[str] = []
    sector: Optional[str] = None
    photo_url: Optional[str] = None
    category: Optional[str] = None
    coach_name: Optional[str] = None
    club: Optional[str] = None
    notes: Optional[str] = None
    health_status: Optional[str] = None
    strengths: List[str] = []
    weaknesses: List[str] = []
    injuries: List[Injury] = []
    allergies_limitations: List[str] = []

class AthleteUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    sex: Optional[Sex] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    specialties: Optional[List[str]] = None
    sector: Optional[str] = None
    photo_url: Optional[str] = None
    category: Optional[str] = None
    coach_name: Optional[str] = None
    club: Optional[str] = None
    notes: Optional[str] = None
    health_status: Optional[str] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    injuries: Optional[List[Injury]] = None
    allergies_limitations: Optional[List[str]] = None

# Personal Record Models
class PersonalRecord(BaseDBModel):
    athlete_id: str
    discipline: str
    value: str
    date: datetime
    notes: Optional[str] = None

class PersonalRecordCreate(BaseModel):
    athlete_id: str
    discipline: str
    value: str
    date: datetime
    notes: Optional[str] = None

# Goal Models
class Goal(BaseDBModel):
    athlete_id: str
    name: str
    type: GoalType
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    priority: Priority
    initial_value: Optional[str] = None
    target_value: Optional[str] = None
    current_value: Optional[str] = None
    status: GoalStatus = GoalStatus.ACTIVE

class GoalCreate(BaseModel):
    athlete_id: str
    name: str
    type: GoalType
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    priority: Priority
    initial_value: Optional[str] = None
    target_value: Optional[str] = None
    current_value: Optional[str] = None

class GoalUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[GoalType] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    priority: Optional[Priority] = None
    initial_value: Optional[str] = None
    target_value: Optional[str] = None
    current_value: Optional[str] = None
    status: Optional[GoalStatus] = None

# Program Models
class Program(BaseDBModel):
    athlete_id: str
    goal_id: Optional[str] = None
    name: str
    start_date: datetime
    end_date: datetime
    weekly_frequency: int
    structure_text: Optional[str] = None
    status: ProgramStatus = ProgramStatus.DRAFT
    notes: Optional[str] = None

class ProgramCreate(BaseModel):
    athlete_id: str
    goal_id: Optional[str] = None
    name: str
    start_date: datetime
    end_date: datetime
    weekly_frequency: int
    structure_text: Optional[str] = None
    notes: Optional[str] = None

class ProgramUpdate(BaseModel):
    goal_id: Optional[str] = None
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    weekly_frequency: Optional[int] = None
    structure_text: Optional[str] = None
    status: Optional[ProgramStatus] = None
    notes: Optional[str] = None

# Session Models
class Session(BaseDBModel):
    program_id: str
    athlete_id: str
    title: str
    type: SessionType
    start: datetime
    end: datetime
    intensity: Optional[int] = None  # 1-10 scale
    tags: List[str] = []
    status: SessionStatus = SessionStatus.DRAFT
    notes: Optional[str] = None
    rpe: Optional[int] = None  # Rate of Perceived Exertion 1-10
    duration_min: Optional[int] = None

class SessionCreate(BaseModel):
    program_id: str
    athlete_id: str
    title: str
    type: SessionType
    start: datetime
    end: datetime
    intensity: Optional[int] = None
    tags: List[str] = []
    notes: Optional[str] = None

class SessionUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[SessionType] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    intensity: Optional[int] = None
    tags: Optional[List[str]] = None
    status: Optional[SessionStatus] = None
    notes: Optional[str] = None
    rpe: Optional[int] = None
    duration_min: Optional[int] = None

# Exercise Models
class Exercise(BaseDBModel):
    name: str
    category: ExerciseCategory
    muscles: List[str] = []
    description: Optional[str] = None
    video_url: Optional[str] = None

class ExerciseCreate(BaseModel):
    name: str
    category: ExerciseCategory
    muscles: List[str] = []
    description: Optional[str] = None
    video_url: Optional[str] = None

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[ExerciseCategory] = None
    muscles: Optional[List[str]] = None
    description: Optional[str] = None
    video_url: Optional[str] = None

# Session Exercise Models
class SessionExercise(BaseDBModel):
    session_id: str
    exercise_id: str
    order: int
    sets: int
    reps: int
    load_kg: Optional[float] = None
    tempo: Optional[str] = None
    rest_sec: Optional[int] = None
    notes: Optional[str] = None

class SessionExerciseCreate(BaseModel):
    session_id: str
    exercise_id: str
    order: int
    sets: int
    reps: int
    load_kg: Optional[float] = None
    tempo: Optional[str] = None
    rest_sec: Optional[int] = None
    notes: Optional[str] = None

# Physical Assessment Models
class PhysicalAssessment(BaseDBModel):
    athlete_id: str
    date: datetime
    strength_max: Optional[int] = None
    strength_endurance: Optional[int] = None
    strength_explosive: Optional[int] = None
    speed_linear: Optional[int] = None
    agility: Optional[int] = None
    power: Optional[int] = None
    mobility: Optional[int] = None
    endurance_aerobic: Optional[int] = None
    endurance_lactate: Optional[int] = None
    icm: Optional[int] = None
    notes: Optional[str] = None

class PhysicalAssessmentCreate(BaseModel):
    athlete_id: str
    date: datetime
    strength_max: Optional[int] = None
    strength_endurance: Optional[int] = None
    strength_explosive: Optional[int] = None
    speed_linear: Optional[int] = None
    agility: Optional[int] = None
    power: Optional[int] = None
    mobility: Optional[int] = None
    endurance_aerobic: Optional[int] = None
    endurance_lactate: Optional[int] = None
    icm: Optional[int] = None
    notes: Optional[str] = None

# Event Models
class Event(BaseDBModel):
    name: str
    place: Optional[str] = None
    date: datetime
    notes: Optional[str] = None

class EventCreate(BaseModel):
    name: str
    place: Optional[str] = None
    date: datetime
    notes: Optional[str] = None

class EventEntry(BaseDBModel):
    event_id: str
    athlete_id: str
    discipline: str
    result_value: Optional[str] = None
    placing: Optional[int] = None
    is_pb: bool = False

class EventEntryCreate(BaseModel):
    event_id: str
    athlete_id: str
    discipline: str
    result_value: Optional[str] = None
    placing: Optional[int] = None
    is_pb: bool = False

# Session Template Models
class SessionTemplate(BaseDBModel):
    name: str
    type: SessionType
    description: Optional[str] = None
    duration_min: int
    intensity: Optional[int] = None
    tags: List[str] = []
    exercises: List[Dict[str, Any]] = []  # Will store exercise templates

class SessionTemplateCreate(BaseModel):
    name: str
    type: SessionType
    description: Optional[str] = None
    duration_min: int
    intensity: Optional[int] = None
    tags: List[str] = []
    exercises: List[Dict[str, Any]] = []

# Authentication Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Analytics Models
class AthleteOverview(BaseModel):
    weekly_volume: int
    intensity_avg: float
    sessions_count_by_type: Dict[str, int]
    next_events: List[Event]

class AssessmentSeries(BaseModel):
    dates: List[str]
    strength_max: List[Optional[int]]
    strength_endurance: List[Optional[int]]
    strength_explosive: List[Optional[int]]
    speed_linear: List[Optional[int]]
    agility: List[Optional[int]]
    power: List[Optional[int]]
    mobility: List[Optional[int]]
    endurance_aerobic: List[Optional[int]]
    endurance_lactate: List[Optional[int]]
    icm: List[Optional[int]]