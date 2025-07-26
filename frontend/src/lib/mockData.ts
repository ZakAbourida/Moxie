
export interface Athlete {
  id: string;
  name: string;
  age: number;
  sport: string;
  level: string;
  image?: string;
  progress: number;
  goals: string[];
  nextSession: string;
  recentPerformance: {
    score: number;
    change: number;
  };
}

export interface TrainingProgram {
  id: string;
  name: string;
  description: string;
  duration: string;
  targetGroup: string;
  athleteCount: number;
  progress: number;
  color: string;
}

export interface WorkoutLog {
  id: string;
  athleteName: string;
  date: string;
  duration: string;
  type: string;
  intensity: 'Low' | 'Medium' | 'High';
  completionRate: number;
  notes: string;
}

export interface ProgressData {
  month: string;
  performance: number;
  average: number;
}

// Athletes mock data
export const athletes: Athlete[] = [
  {
    id: '1',
    name: 'Alex Johnson',
    age: 22,
    sport: 'Track & Field',
    level: 'Advanced',
    progress: 78,
    goals: ['Improve sprint time by 0.5s', 'Increase vertical jump'],
    nextSession: 'Today at 3:00 PM',
    recentPerformance: {
      score: 92,
      change: 4,
    },
  },
  {
    id: '2',
    name: 'Morgan Smith',
    age: 19,
    sport: 'Swimming',
    level: 'Intermediate',
    progress: 65,
    goals: ['Master butterfly technique', 'Build endurance'],
    nextSession: 'Tomorrow at 10:00 AM',
    recentPerformance: {
      score: 78,
      change: 6,
    },
  },
  {
    id: '3',
    name: 'Jamie Williams',
    age: 24,
    sport: 'Basketball',
    level: 'Advanced',
    progress: 88,
    goals: ['Increase free throw accuracy', 'Improve court awareness'],
    nextSession: 'Today at 5:30 PM',
    recentPerformance: {
      score: 89,
      change: -2,
    },
  },
  {
    id: '4',
    name: 'Taylor Reed',
    age: 20,
    sport: 'Soccer',
    level: 'Pro',
    progress: 92,
    goals: ['Enhance defensive positioning', 'Boost stamina'],
    nextSession: 'Tomorrow at 2:00 PM',
    recentPerformance: {
      score: 95,
      change: 3,
    },
  },
];

// Training programs mock data
export const trainingPrograms: TrainingProgram[] = [
  {
    id: '1',
    name: 'Sprint Acceleration',
    description: 'Focus on explosive power and acceleration technique',
    duration: '8 weeks',
    targetGroup: 'Track & Field',
    athleteCount: 12,
    progress: 65,
    color: 'athletic',
  },
  {
    id: '2',
    name: 'Endurance Builder',
    description: 'Progressive cardiovascular and muscular endurance training',
    duration: '12 weeks',
    targetGroup: 'Multiple sports',
    athleteCount: 8,
    progress: 42,
    color: 'success',
  },
  {
    id: '3',
    name: 'Strength Foundation',
    description: 'Core and functional strength development program',
    duration: '10 weeks',
    targetGroup: 'All athletes',
    athleteCount: 15,
    progress: 78,
    color: 'warning',
  },
];

// Recent workout logs
export const workoutLogs: WorkoutLog[] = [
  {
    id: '1',
    athleteName: 'Alex Johnson',
    date: '2025-05-01',
    duration: '45 minutes',
    type: 'Sprint Training',
    intensity: 'High',
    completionRate: 100,
    notes: 'Excellent form and effort, hit all target times',
  },
  {
    id: '2',
    athleteName: 'Morgan Smith',
    date: '2025-04-30',
    duration: '60 minutes',
    type: 'Endurance Training',
    intensity: 'Medium',
    completionRate: 85,
    notes: 'Good session overall, struggled with final set',
  },
  {
    id: '3',
    athleteName: 'Jamie Williams',
    date: '2025-04-30',
    duration: '75 minutes',
    type: 'Skill Development',
    intensity: 'Medium',
    completionRate: 95,
    notes: 'Great improvement on technique drills',
  },
  {
    id: '4',
    athleteName: 'Taylor Reed',
    date: '2025-04-29',
    duration: '90 minutes',
    type: 'Match Simulation',
    intensity: 'High',
    completionRate: 100,
    notes: 'Excellent positioning and decision making',
  },
];

// Progress chart data
export const progressData: ProgressData[] = [
  { month: 'Jan', performance: 65, average: 60 },
  { month: 'Feb', performance: 68, average: 62 },
  { month: 'Mar', performance: 75, average: 65 },
  { month: 'Apr', performance: 73, average: 68 },
  { month: 'May', performance: 80, average: 70 },
  { month: 'Jun', performance: 85, average: 72 },
  { month: 'Jul', performance: 90, average: 75 },
];

// Summary metrics
export const summaryMetrics = [
  { label: 'Active Athletes', value: 42, change: 8, isPositive: true },
  { label: 'Training Programs', value: 12, change: 3, isPositive: true },
  { label: 'Completion Rate', value: '87%', change: 5, isPositive: true },
  { label: 'Upcoming Sessions', value: 18, change: -2, isPositive: false },
];
