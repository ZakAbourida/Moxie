import asyncio
from datetime import datetime, timedelta
from database import db_manager, COLLECTIONS
from auth import get_password_hash
from models import (
    UserRole, Sex, GoalType, Priority, GoalStatus, 
    ProgramStatus, SessionType, SessionStatus, ExerciseCategory
)
import uuid

async def create_seed_data():
    """Create seed data for the application."""
    print("🌱 Creating seed data...")
    
    # Create coach user
    coach_id = str(uuid.uuid4())
    coach_data = {
        "id": coach_id,
        "role": UserRole.COACH.value,
        "email": "coach@example.com",
        "hashed_password": get_password_hash("Password123!"),
        "first_name": "Coach",
        "last_name": "Johnson"
    }
    
    await db_manager.create_document(COLLECTIONS['users'], coach_data)
    print("✅ Created coach user: coach@example.com / Password123!")
    
    # Create 3 sample athletes
    athletes_data = [
        {
            "id": str(uuid.uuid4()),
            "first_name": "Sarah",
            "last_name": "Miller",
            "birth_date": datetime(2001, 3, 15),
            "sex": Sex.FEMALE.value,
            "height_cm": 170.0,
            "weight_kg": 58.0,
            "specialties": ["100m", "200m", "Long Jump"],
            "sector": "Track & Field",
            "category": "Senior",
            "coach_name": "Coach Johnson",
            "club": "Athletics Club",
            "health_status": "Excellent",
            "strengths": ["Speed", "Explosive power", "Technique"],
            "weaknesses": ["Endurance", "Start reaction"],
            "allergies_limitations": ["Pollen allergy"],
            "notes": "Promising young sprinter with excellent technique"
        },
        {
            "id": str(uuid.uuid4()),
            "first_name": "Marcus",
            "last_name": "Thompson",
            "birth_date": datetime(1998, 7, 22),
            "sex": Sex.MALE.value,
            "height_cm": 185.0,
            "weight_kg": 110.0,
            "specialties": ["Discus", "Shot Put"],
            "sector": "Field Events",
            "category": "Elite",
            "coach_name": "Coach Johnson",
            "club": "Athletics Club",
            "health_status": "Good",
            "strengths": ["Raw power", "Technique", "Mental focus"],
            "weaknesses": ["Mobility", "Recovery"],
            "allergies_limitations": [],
            "injuries": [
                {
                    "date": datetime(2023, 8, 15),
                    "type": "Shoulder strain",
                    "notes": "Minor strain during training, fully recovered"
                }
            ],
            "notes": "Strong thrower with consistent performance"
        },
        {
            "id": str(uuid.uuid4()),
            "first_name": "Elena",
            "last_name": "Rodriguez",
            "birth_date": datetime(2000, 11, 8),
            "sex": Sex.FEMALE.value,
            "height_cm": 165.0,
            "weight_kg": 52.0,
            "specialties": ["800m", "1500m"],
            "sector": "Middle Distance",
            "category": "Senior",
            "coach_name": "Coach Johnson",
            "club": "Athletics Club",
            "health_status": "Excellent",
            "strengths": ["Endurance", "Race tactics", "Mental toughness"],
            "weaknesses": ["Speed", "Kick finish"],
            "allergies_limitations": ["Lactose intolerance"],
            "notes": "Tactical runner with great endurance base"
        }
    ]
    
    created_athletes = []
    for athlete_data in athletes_data:
        athlete = await db_manager.create_document(COLLECTIONS['athletes'], athlete_data)
        created_athletes.append(athlete)
        print(f"✅ Created athlete: {athlete_data['first_name']} {athlete_data['last_name']}")
    
    # Create sample goals for each athlete
    goals_data = [
        # Sarah's goals
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[0]['id'],
            "name": "Sub-11 seconds in 100m",
            "type": GoalType.PERFORMANCE.value,
            "description": "Break the 11-second barrier in 100m sprint",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=180),
            "priority": Priority.HIGH.value,
            "initial_value": "11.24",
            "target_value": "10.99",
            "current_value": "11.18",
            "status": GoalStatus.ACTIVE.value
        },
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[0]['id'],
            "name": "Improve start technique",
            "type": GoalType.TECHNICAL.value,
            "description": "Focus on reaction time and block starts",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=90),
            "priority": Priority.MEDIUM.value,
            "status": GoalStatus.ACTIVE.value
        },
        # Marcus's goals
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[1]['id'],  
            "name": "65m+ discus throw",
            "type": GoalType.PERFORMANCE.value,
            "description": "Achieve personal best of 65+ meters in discus",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=120),
            "priority": Priority.HIGH.value,
            "initial_value": "62.5m",
            "target_value": "65.0m",
            "current_value": "63.2m",
            "status": GoalStatus.ACTIVE.value
        },
        # Elena's goals
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[2]['id'],
            "name": "Sub-2:10 in 800m",
            "type": GoalType.PERFORMANCE.value,
            "description": "Break 2:10 barrier in 800m",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=150),
            "priority": Priority.HIGH.value,
            "initial_value": "2:12.45",
            "target_value": "2:09.99",
            "current_value": "2:11.20",
            "status": GoalStatus.ACTIVE.value
        }
    ]
    
    created_goals = []
    for goal_data in goals_data:
        goal = await db_manager.create_document(COLLECTIONS['goals'], goal_data)
        created_goals.append(goal)
    print(f"✅ Created {len(goals_data)} goals")
    
    # Create training programs
    programs_data = [
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[0]['id'],
            "goal_id": created_goals[0]['id'],
            "name": "Sprint Speed Development",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=90),
            "weekly_frequency": 4,
            "structure_text": "Mon: Speed work, Wed: Technique, Fri: Power, Sat: Competition prep",
            "status": ProgramStatus.ACTIVE.value,
            "notes": "Focus on acceleration and maximum speed development"
        },
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[1]['id'],
            "goal_id": created_goals[2]['id'],
            "name": "Throwing Power Program",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=120),
            "weekly_frequency": 5,
            "structure_text": "Mon: Strength, Tue: Technique, Thu: Power, Fri: Throws, Sat: Recovery",
            "status": ProgramStatus.ACTIVE.value,
            "notes": "Periodized program for discus throwing development"
        },
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[2]['id'],
            "goal_id": created_goals[3]['id'],
            "name": "Middle Distance Base",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=100),
            "weekly_frequency": 6,
            "structure_text": "Daily training with varied intensities and recovery",
            "status": ProgramStatus.ACTIVE.value,
            "notes": "Base building phase for 800m specialization"
        }
    ]
    
    created_programs = []
    for program_data in programs_data:
        program = await db_manager.create_document(COLLECTIONS['programs'], program_data)
        created_programs.append(program)
    print(f"✅ Created {len(programs_data)} training programs")
    
    # Create sample exercises
    exercises_data = [
        {
            "id": str(uuid.uuid4()),
            "name": "Block Starts",
            "category": ExerciseCategory.OTHER.value,
            "muscles": ["Quadriceps", "Glutes", "Calves"],
            "description": "Sprint start from starting blocks",
            "video_url": None
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Flying Sprints",
            "category": ExerciseCategory.OTHER.value,
            "muscles": ["Full body"],
            "description": "Maximum speed sprints with build-up",
            "video_url": None
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Discus Throws",
            "category": ExerciseCategory.OTHER.value,
            "muscles": ["Core", "Shoulders", "Legs"],
            "description": "Full discus throwing technique",
            "video_url": None
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Medicine Ball Throws",
            "category": ExerciseCategory.CORE.value,
            "muscles": ["Core", "Shoulders", "Arms"],
            "description": "Explosive medicine ball throwing exercises",
            "video_url": None
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Tempo Runs",
            "category": ExerciseCategory.OTHER.value,
            "muscles": ["Full body cardiovascular"],
            "description": "Controlled pace running for endurance",
            "video_url": None
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Squats",
            "category": ExerciseCategory.LEGS.value,
            "muscles": ["Quadriceps", "Glutes", "Hamstrings"],
            "description": "Back squats for leg strength",
            "video_url": None
        }
    ]
    
    created_exercises = []
    for exercise_data in exercises_data:
        exercise = await db_manager.create_document(COLLECTIONS['exercises'], exercise_data)
        created_exercises.append(exercise)
    print(f"✅ Created {len(exercises_data)} exercises")
    
    # Create sample sessions for the next week
    sessions_data = []
    base_date = datetime.now()
    
    # Sarah's sessions
    sessions_data.extend([
        {
            "id": str(uuid.uuid4()),
            "program_id": created_programs[0]['id'],
            "athlete_id": created_athletes[0]['id'],
            "title": "Speed Development",
            "type": SessionType.SPEED.value,
            "start": base_date + timedelta(days=1, hours=16),
            "end": base_date + timedelta(days=1, hours=17, minutes=30),
            "intensity": 8,
            "tags": ["sprint", "acceleration"],
            "status": SessionStatus.SCHEDULED.value,
            "notes": "Focus on 30m acceleration"
        },
        {
            "id": str(uuid.uuid4()),
            "program_id": created_programs[0]['id'],
            "athlete_id": created_athletes[0]['id'],
            "title": "Technique Session",
            "type": SessionType.TECHNIQUE.value,
            "start": base_date + timedelta(days=3, hours=15),
            "end": base_date + timedelta(days=3, hours=16, minutes=30),
            "intensity": 6,
            "tags": ["technique", "starts"],
            "status": SessionStatus.SCHEDULED.value,
            "notes": "Block start practice"
        }
    ])
    
    # Marcus's sessions  
    sessions_data.extend([
        {
            "id": str(uuid.uuid4()),
            "program_id": created_programs[1]['id'],
            "athlete_id": created_athletes[1]['id'],
            "title": "Strength Training",
            "type": SessionType.GYM.value,
            "start": base_date + timedelta(days=1, hours=10),
            "end": base_date + timedelta(days=1, hours=11, minutes=30),
            "intensity": 7,
            "tags": ["strength", "power"],
            "status": SessionStatus.SCHEDULED.value,
            "notes": "Focus on explosive movements"
        },
        {
            "id": str(uuid.uuid4()),
            "program_id": created_programs[1]['id'],
            "athlete_id": created_athletes[1]['id'],
            "title": "Throwing Practice",
            "type": SessionType.TECHNIQUE.value,
            "start": base_date + timedelta(days=2, hours=16),
            "end": base_date + timedelta(days=2, hours=18),
            "intensity": 8,
            "tags": ["discus", "technique"],
            "status": SessionStatus.SCHEDULED.value,
            "notes": "Full throwing session"
        }
    ])
    
    # Elena's sessions
    sessions_data.extend([
        {
            "id": str(uuid.uuid4()),
            "program_id": created_programs[2]['id'],
            "athlete_id": created_athletes[2]['id'],
            "title": "Tempo Run",
            "type": SessionType.ENDURANCE.value,
            "start": base_date + timedelta(days=1, hours=7),
            "end": base_date + timedelta(days=1, hours=8, minutes=15),
            "intensity": 5,
            "tags": ["tempo", "aerobic"],
            "status": SessionStatus.SCHEDULED.value,
            "notes": "6km tempo at threshold pace"
        },
        {
            "id": str(uuid.uuid4()),
            "program_id": created_programs[2]['id'],
            "athlete_id": created_athletes[2]['id'],
            "title": "Track Intervals",
            "type": SessionType.SPEED.value,
            "start": base_date + timedelta(days=4, hours=17),
            "end": base_date + timedelta(days=4, hours=18, minutes=30),
            "intensity": 9,
            "tags": ["intervals", "lactate"],
            "status": SessionStatus.SCHEDULED.value,
            "notes": "400m repeats at race pace"
        }
    ])
    
    for session_data in sessions_data:
        await db_manager.create_document(COLLECTIONS['sessions'], session_data)
    print(f"✅ Created {len(sessions_data)} training sessions")
    
    # Create sample physical assessments
    assessments_data = [
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[0]['id'],
            "date": datetime.now() - timedelta(days=30),
            "strength_max": 7,
            "strength_endurance": 6,
            "strength_explosive": 9,
            "speed_linear": 9,
            "agility": 8,
            "power": 9,
            "mobility": 7,
            "endurance_aerobic": 5,
            "endurance_lactate": 6,
            "icm": 8,
            "notes": "Strong in power and speed metrics"
        },
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[1]['id'],
            "date": datetime.now() - timedelta(days=25),
            "strength_max": 9,
            "strength_endurance": 7,
            "strength_explosive": 8,
            "speed_linear": 6,
            "agility": 5,
            "power": 9,
            "mobility": 5,
            "endurance_aerobic": 4,
            "endurance_lactate": 5,
            "icm": 7,
            "notes": "Excellent strength and power, needs mobility work"
        },
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[2]['id'],
            "date": datetime.now() - timedelta(days=20),
            "strength_max": 6,
            "strength_endurance": 8,
            "strength_explosive": 6,
            "speed_linear": 7,
            "agility": 7,
            "power": 6,
            "mobility": 8,
            "endurance_aerobic": 9,
            "endurance_lactate": 9,
            "icm": 8,
            "notes": "Outstanding endurance profile"
        }
    ]
    
    for assessment_data in assessments_data:
        await db_manager.create_document(COLLECTIONS['physical_assessments'], assessment_data)
    print(f"✅ Created {len(assessments_data)} physical assessments")
    
    # Create sample personal records
    records_data = [
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[0]['id'],
            "discipline": "100m",
            "value": "11.18",
            "date": datetime.now() - timedelta(days=15),
            "notes": "Season best with tailwind 1.2m/s"
        },
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[0]['id'],
            "discipline": "200m",
            "value": "23.45",
            "date": datetime.now() - timedelta(days=45),
            "notes": "Personal best from regional championships"
        },
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[1]['id'],
            "discipline": "Discus",
            "value": "63.2m",
            "date": datetime.now() - timedelta(days=10),
            "notes": "Recent personal best"
        },
        {
            "id": str(uuid.uuid4()),
            "athlete_id": created_athletes[2]['id'],
            "discipline": "800m",
            "value": "2:11.20",
            "date": datetime.now() - timedelta(days=8),
            "notes": "Strong negative split race"
        }
    ]
    
    for record_data in records_data:
        await db_manager.create_document(COLLECTIONS['personal_records'], record_data)
    print(f"✅ Created {len(records_data)} personal records")
    
    # Create sample session templates
    templates_data = [
        {
            "id": str(uuid.uuid4()),
            "name": "Speed Development",
            "type": SessionType.SPEED.value,
            "description": "Sprint training focused on acceleration and max speed",
            "duration_min": 90,
            "intensity": 8,
            "tags": ["sprint", "acceleration", "speed"],
            "exercises": [
                {"name": "Dynamic Warm-up", "sets": 1, "reps": 1, "notes": "10min mobility and activation"},
                {"name": "Block Starts", "sets": 6, "reps": 1, "rest_sec": 180, "notes": "30m acceleration"},
                {"name": "Flying Sprints", "sets": 4, "reps": 1, "rest_sec": 240, "notes": "20m fly zone"},
            ]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Strength Training",
            "type": SessionType.GYM.value,
            "description": "General strength development session",
            "duration_min": 75,
            "intensity": 7,
            "tags": ["strength", "gym", "power"],
            "exercises": [
                {"name": "Squats", "sets": 4, "reps": 6, "load_kg": 100, "rest_sec": 180},
                {"name": "Medicine Ball Throws", "sets": 3, "reps": 8, "rest_sec": 120},
            ]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Endurance Base",
            "type": SessionType.ENDURANCE.value,
            "description": "Aerobic base building session",
            "duration_min": 60,
            "intensity": 5,
            "tags": ["endurance", "aerobic", "base"],
            "exercises": [
                {"name": "Tempo Runs", "sets": 1, "reps": 1, "notes": "45min steady state"},
            ]
        }
    ]
    
    for template_data in templates_data:
        await db_manager.create_document(COLLECTIONS['session_templates'], template_data)
    print(f"✅ Created {len(templates_data)} session templates")
    
    print("🎉 Seed data creation completed successfully!")
    print("\nLogin credentials:")
    print("📧 Email: coach@example.com")
    print("🔑 Password: Password123!")

if __name__ == "__main__":
    asyncio.run(create_seed_data())