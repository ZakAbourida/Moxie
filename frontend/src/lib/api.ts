const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

export interface User {
  id: string;
  role: 'coach' | 'athlete';
  email: string;
  first_name: string;
  last_name: string;
  created_at: string;
}

export interface Athlete {
  id: string;
  first_name: string;
  last_name: string;
  birth_date?: string;
  sex?: 'male' | 'female' | 'other';
  height_cm?: number;
  weight_kg?: number;
  specialties: string[];
  sector?: string;
  photo_url?: string;
  category?: string;
  coach_name?: string;
  club?: string;
  notes?: string;
  health_status?: string;
  strengths: string[];
  weaknesses: string[];
  injuries: Array<{
    date: string;
    type: string;
    notes?: string;
  }>;
  allergies_limitations: string[];
  created_at: string;
  updated_at: string;
}

export interface Goal {
  id: string;
  athlete_id: string;
  name: string;
  type: 'performance' | 'technical' | 'physical' | 'health' | 'other';
  description?: string;
  start_date: string;
  end_date: string;
  priority: 'high' | 'medium' | 'low';
  initial_value?: string;
  target_value?: string;
  current_value?: string;
  status: 'active' | 'achieved' | 'failed' | 'abandoned' | 'postponed';
  created_at: string;
  updated_at: string;
}

export interface Program {
  id: string;
  athlete_id: string;
  goal_id?: string;
  name: string;
  start_date: string;
  end_date: string;
  weekly_frequency: number;
  structure_text?: string;
  status: 'draft' | 'active' | 'completed' | 'canceled';
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Session {
  id: string;
  program_id: string;
  athlete_id: string;
  title: string;
  type: 'gym' | 'technique' | 'speed' | 'endurance' | 'rest' | 'other';
  start: string;
  end: string;
  intensity?: number;
  tags: string[];
  status: 'draft' | 'scheduled' | 'done' | 'canceled';
  notes?: string;
  rpe?: number;
  duration_min?: number;
  created_at: string;
  updated_at: string;
}

export interface Exercise {
  id: string;
  name: string;
  category: 'legs' | 'push' | 'pull' | 'core' | 'olympic' | 'mobility' | 'other';
  muscles: string[];
  description?: string;
  video_url?: string;
  created_at: string;
  updated_at: string;
}

export interface PhysicalAssessment {
  id: string;
  athlete_id: string;
  date: string;
  strength_max?: number;
  strength_endurance?: number;
  strength_explosive?: number;
  speed_linear?: number;
  agility?: number; 
  power?: number;
  mobility?: number;
  endurance_aerobic?: number;
  endurance_lactate?: number;
  icm?: number;
  notes?: string;
  created_at: string;
}

export interface PersonalRecord {
  id: string;
  athlete_id: string;
  discipline: string;
  value: string;
  date: string;
  notes?: string;
  created_at: string;
}

export interface SessionTemplate {
  id: string;
  name: string;
  type: 'gym' | 'technique' | 'speed' | 'endurance' | 'rest' | 'other';
  description?: string;
  duration_min: number;
  intensity?: number;
  tags: string[];
  exercises: Array<{
    name: string;
    sets?: number;
    reps?: number;
    load_kg?: number;
    rest_sec?: number;
    notes?: string;
  }>;
  created_at: string;
}

export interface AthleteOverview {
  weekly_volume: number;
  intensity_avg: number;
  sessions_count_by_type: Record<string, number>;
  next_events: any[];
}

export interface AssessmentSeries {
  dates: string[];
  strength_max: (number | null)[];
  strength_endurance: (number | null)[];
  strength_explosive: (number | null)[];
  speed_linear: (number | null)[];
  agility: (number | null)[];
  power: (number | null)[];
  mobility: (number | null)[];
  endurance_aerobic: (number | null)[];
  endurance_lactate: (number | null)[];
  icm: (number | null)[];
}

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

class ApiService {
  private async request<T>(url: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_BASE}${url}`, {
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new ApiError(response.status, errorText);
    }

    return response.json();
  }

  // Authentication
  async login(email: string, password: string): Promise<{ access_token: string; token_type: string }> {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async logout(): Promise<void> {
    await this.request('/auth/logout', {
      method: 'POST',
    });
  }

  async getMe(): Promise<User> {
    return this.request('/auth/me');
  }

  // Athletes
  async getAthletes(filters?: { name?: string; sector?: string }): Promise<Athlete[]> {
    const params = new URLSearchParams();
    if (filters?.name) params.append('name', filters.name);
    if (filters?.sector) params.append('sector', filters.sector);
    
    const queryString = params.toString();
    return this.request(`/athletes${queryString ? `?${queryString}` : ''}`);
  }

  async getAthlete(id: string): Promise<Athlete> {
    return this.request(`/athletes/${id}`);
  }

  async createAthlete(athlete: Omit<Athlete, 'id' | 'created_at' | 'updated_at'>): Promise<Athlete> {
    return this.request('/athletes', {
      method: 'POST',
      body: JSON.stringify(athlete),
    });
  }

  async updateAthlete(id: string, athlete: Partial<Athlete>): Promise<Athlete> {
    return this.request(`/athletes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(athlete),
    });
  }

  async deleteAthlete(id: string): Promise<void> {
    await this.request(`/athletes/${id}`, {
      method: 'DELETE',
    });
  }

  // Goals
  async getGoals(athleteId?: string): Promise<Goal[]> {
    const params = athleteId ? `?athlete_id=${athleteId}` : '';
    return this.request(`/goals${params}`);
  }

  async createGoal(goal: Omit<Goal, 'id' | 'created_at' | 'updated_at'>): Promise<Goal> {
    return this.request('/goals', {
      method: 'POST',
      body: JSON.stringify(goal),
    });
  }

  async updateGoal(id: string, goal: Partial<Goal>): Promise<Goal> {
    return this.request(`/goals/${id}`, {
      method: 'PUT',
      body: JSON.stringify(goal),
    });
  }

  async deleteGoal(id: string): Promise<void> {
    await this.request(`/goals/${id}`, {
      method: 'DELETE',
    });
  }

  // Programs
  async getPrograms(athleteId?: string): Promise<Program[]> {
    const params = athleteId ? `?athlete_id=${athleteId}` : '';
    return this.request(`/programs${params}`);
  }

  async createProgram(program: Omit<Program, 'id' | 'created_at' | 'updated_at'>): Promise<Program> {
    return this.request('/programs', {
      method: 'POST',
      body: JSON.stringify(program),
    });
  }

  async updateProgram(id: string, program: Partial<Program>): Promise<Program> {
    return this.request(`/programs/${id}`, {
      method: 'PUT',
      body: JSON.stringify(program),
    });
  }

  async deleteProgram(id: string): Promise<void> {
    await this.request(`/programs/${id}`, {
      method: 'DELETE',
    });
  }

  // Sessions
  async getSessions(filters?: {
    athlete_id?: string;
    program_id?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<Session[]> {
    const params = new URLSearchParams();
    if (filters?.athlete_id) params.append('athlete_id', filters.athlete_id);
    if (filters?.program_id) params.append('program_id', filters.program_id);
    if (filters?.start_date) params.append('start_date', filters.start_date);
    if (filters?.end_date) params.append('end_date', filters.end_date);
    
    const queryString = params.toString();
    return this.request(`/sessions${queryString ? `?${queryString}` : ''}`);
  }

  async createSession(session: Omit<Session, 'id' | 'created_at' | 'updated_at'>): Promise<Session> {
    return this.request('/sessions', {
      method: 'POST',
      body: JSON.stringify(session),
    });
  }

  async updateSession(id: string, session: Partial<Session>): Promise<Session> {
    return this.request(`/sessions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(session),
    });
  }

  async deleteSession(id: string): Promise<void> {
    await this.request(`/sessions/${id}`, {
      method: 'DELETE',
    });
  }

  // Exercises
  async getExercises(category?: string): Promise<Exercise[]> {
    const params = category ? `?category=${category}` : '';
    return this.request(`/exercises${params}`);
  }

  async createExercise(exercise: Omit<Exercise, 'id' | 'created_at' | 'updated_at'>): Promise<Exercise> {
    return this.request('/exercises', {
      method: 'POST',
      body: JSON.stringify(exercise),
    });
  }

  async updateExercise(id: string, exercise: Partial<Exercise>): Promise<Exercise> {
    return this.request(`/exercises/${id}`, {
      method: 'PUT',
      body: JSON.stringify(exercise),
    });
  }

  async deleteExercise(id: string): Promise<void> {
    await this.request(`/exercises/${id}`, {
      method: 'DELETE',
    });
  }

  // Physical Assessments
  async getAssessments(athleteId?: string): Promise<PhysicalAssessment[]> {
    const params = athleteId ? `?athlete_id=${athleteId}` : '';
    return this.request(`/assessments${params}`);
  }

  async createAssessment(assessment: Omit<PhysicalAssessment, 'id' | 'created_at'>): Promise<PhysicalAssessment> {
    return this.request('/assessments', {
      method: 'POST',
      body: JSON.stringify(assessment),
    });
  }

  async updateAssessment(id: string, assessment: Partial<PhysicalAssessment>): Promise<PhysicalAssessment> {
    return this.request(`/assessments/${id}`, {
      method: 'PUT',
      body: JSON.stringify(assessment),
    });
  }

  async deleteAssessment(id: string): Promise<void> {
    await this.request(`/assessments/${id}`, {
      method: 'DELETE',
    });
  }

  // Personal Records
  async getRecords(athleteId?: string): Promise<PersonalRecord[]> {
    const params = athleteId ? `?athlete_id=${athleteId}` : '';
    return this.request(`/records${params}`);
  }

  async createRecord(record: Omit<PersonalRecord, 'id' | 'created_at'>): Promise<PersonalRecord> {
    return this.request('/records', {
      method: 'POST',
      body: JSON.stringify(record),
    });
  }

  async deleteRecord(id: string): Promise<void> {
    await this.request(`/records/${id}`, {
      method: 'DELETE',
    });
  }

  // Session Templates
  async getSessionTemplates(): Promise<SessionTemplate[]> {
    return this.request('/templates/sessions');
  }

  async createSessionTemplate(template: Omit<SessionTemplate, 'id' | 'created_at'>): Promise<SessionTemplate> {
    return this.request('/templates/sessions', {
      method: 'POST',
      body: JSON.stringify(template),
    });
  }

  async deleteSessionTemplate(id: string): Promise<void> {
    await this.request(`/templates/sessions/${id}`, {
      method: 'DELETE',
    });
  }

  // Analytics
  async getAthleteOverview(athleteId: string): Promise<AthleteOverview> {
    return this.request(`/analytics/athlete/${athleteId}/overview`);
  }

  async getAthleteAssessments(athleteId: string): Promise<AssessmentSeries> {
    return this.request(`/analytics/athlete/${athleteId}/assessments`);
  }
}

export const apiService = new ApiService();
export { ApiError };