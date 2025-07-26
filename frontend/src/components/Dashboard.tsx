
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from '@/lib/utils';
import { TrendingUp, Users, Target, Calendar, Activity, Plus, User } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { apiService, Athlete, Goal, Session, PhysicalAssessment } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';
import RadarChart from './RadarChart';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [athletes, setAthletes] = useState<Athlete[]>([]);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [assessments, setAssessments] = useState<PhysicalAssessment[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (isAuthenticated) {
      loadDashboardData();
    }
  }, [isAuthenticated]);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      const [athletesData, goalsData, sessionsData, assessmentsData] = await Promise.all([
        apiService.getAthletes(),
        apiService.getGoals(),
        apiService.getSessions(),
        apiService.getAssessments()
      ]);
      
      setAthletes(athletesData);
      setGoals(goalsData);
      setSessions(sessionsData);
      setAssessments(assessmentsData);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  // Calculate dashboard metrics
  const activeGoals = goals.filter(goal => goal.status === 'active');
  const upcomingSessions = sessions.filter(session => {
    const sessionDate = new Date(session.start);
    const now = new Date();
    return sessionDate > now && session.status === 'scheduled';
  });
  const completedSessions = sessions.filter(session => session.status === 'done');
  const completionRate = sessions.length > 0 ? Math.round((completedSessions.length / sessions.length) * 100) : 0;

  // Get recent sessions for activity feed
  const recentSessions = sessions
    .filter(session => session.status === 'done')
    .sort((a, b) => new Date(b.start).getTime() - new Date(a.start).getTime())
    .slice(0, 5);

  // Get latest assessment for radar chart
  const latestAssessment = assessments.length > 0 
    ? assessments.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())[0]
    : null;

  const summaryMetrics = [
    { 
      label: 'Active Athletes', 
      value: athletes.length, 
      change: 8, 
      isPositive: true,
      icon: Users 
    },
    { 
      label: 'Active Goals', 
      value: activeGoals.length, 
      change: 12, 
      isPositive: true,
      icon: Target 
    },
    { 
      label: 'Completion Rate', 
      value: `${completionRate}%`, 
      change: 5, 
      isPositive: true,
      icon: Activity 
    },
    { 
      label: 'Upcoming Sessions', 
      value: upcomingSessions.length, 
      change: -2, 
      isPositive: false,
      icon: Calendar 
    },
  ];

  if (isLoading) {
    return (
      <div className="space-y-8 fade-in">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <Card key={i}>
              <CardContent className="p-6">
                <div className="animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                  <div className="h-8 bg-gray-200 rounded w-1/3"></div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in">
      {/* Summary metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {summaryMetrics.map((metric, index) => {
          const IconComponent = metric.icon;
          return (
            <Card key={index}>
              <CardContent className="p-6">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <p className="text-sm text-muted-foreground">{metric.label}</p>
                    <h3 className="text-3xl font-bold mt-1">{metric.value}</h3>
                  </div>
                  <div className="flex flex-col items-end space-y-2">
                    <IconComponent className="h-5 w-5 text-muted-foreground" />
                    <div className={cn(
                      "h-fit flex items-center px-2 py-1 rounded-full text-xs",
                      metric.isPositive ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
                    )}>
                      <TrendingUp size={12} className="mr-1" />
                      <span>{Math.abs(metric.change)}%</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Actions bar */}
      <div className="flex justify-between items-center pt-2">
        <h2 className="text-xl font-semibold">Recent Athletes</h2>
        <Button onClick={() => navigate('/athletes')} className="flex items-center">
          <Plus size={16} className="mr-1" />
          View All Athletes
        </Button>
      </div>

      {/* Athletes preview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {athletes.slice(0, 4).map((athlete) => {
          const athleteGoals = activeGoals.filter(goal => goal.athlete_id === athlete.id);
          
          return (
            <Card 
              key={athlete.id} 
              className="hover:shadow-lg transition-shadow cursor-pointer group"
              onClick={() => navigate(`/athletes/${athlete.id}`)}
            >
              <CardHeader className="pb-3">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold">
                    <User size={16} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <CardTitle className="text-lg group-hover:text-blue-600 transition-colors">
                      {athlete.first_name} {athlete.last_name}
                    </CardTitle>
                    <p className="text-sm text-muted-foreground">
                      {athlete.sector || 'General Training'}
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                {athlete.specialties.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {athlete.specialties.slice(0, 2).map((specialty, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {specialty}
                      </Badge>
                    ))}
                    {athlete.specialties.length > 2 && (
                      <Badge variant="outline" className="text-xs">
                        +{athlete.specialties.length - 2}
                      </Badge>
                    )}
                  </div>
                )}
                
                {athleteGoals.length > 0 && (
                  <div>
                    <p className="text-sm font-medium mb-1">Active Goals:</p>
                    <div className="space-y-1">
                      {athleteGoals.slice(0, 2).map((goal) => (
                        <div key={goal.id} className="text-sm text-muted-foreground truncate">
                          • {goal.name}
                        </div>
                      ))}
                      {athleteGoals.length > 2 && (
                        <div className="text-xs text-muted-foreground">
                          +{athleteGoals.length - 2} more goals
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Charts and activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        {/* Physical Assessment Radar Chart */}
        {latestAssessment && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Activity className="mr-2 h-5 w-5" />
                Latest Physical Assessment
              </CardTitle>
              <p className="text-sm text-muted-foreground">
                {new Date(latestAssessment.date).toLocaleDateString()}
              </p>
            </CardHeader>
            <CardContent>
              <RadarChart assessment={latestAssessment} />
            </CardContent>
          </Card>
        )}

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Calendar className="mr-2 h-5 w-5" />
              Recent Training Sessions
            </CardTitle>
          </CardHeader>
          <CardContent>
            {recentSessions.length > 0 ? (
              <div className="space-y-3">
                {recentSessions.map((session) => {
                  const athlete = athletes.find(a => a.id === session.athlete_id);
                  return (
                    <div key={session.id} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                      <div className="flex-1">
                        <p className="font-medium">{session.title}</p>
                        <p className="text-sm text-muted-foreground">
                          {athlete?.first_name} {athlete?.last_name} • {session.type}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-muted-foreground">
                          {new Date(session.start).toLocaleDateString()}
                        </p>
                        {session.rpe && (
                          <Badge variant="outline" className="text-xs">
                            RPE {session.rpe}
                          </Badge>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-8">
                <Calendar className="mx-auto h-12 w-12 text-muted-foreground" />
                <h3 className="mt-2 text-sm font-semibold">No recent sessions</h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  Training sessions will appear here once completed
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="hover:shadow-md transition-shadow cursor-pointer" onClick={() => navigate('/athletes')}>
          <CardContent className="p-6 text-center">
            <Users className="mx-auto h-8 w-8 text-blue-500 mb-2" />
            <h3 className="font-semibold">Manage Athletes</h3>
            <p className="text-sm text-muted-foreground">Add, edit, and track athlete progress</p>
          </CardContent>
        </Card>
        
        <Card className="hover:shadow-md transition-shadow cursor-pointer" onClick={() => navigate('/training-plans')}>
          <CardContent className="p-6 text-center">
            <Target className="mx-auto h-8 w-8 text-green-500 mb-2" />
            <h3 className="font-semibold">Training Plans</h3>
            <p className="text-sm text-muted-foreground">Create and manage training programs</p>
          </CardContent>
        </Card>
        
        <Card className="hover:shadow-md transition-shadow cursor-pointer">
          <CardContent className="p-6 text-center">
            <Activity className="mx-auto h-8 w-8 text-purple-500 mb-2" />
            <h3 className="font-semibold">Assessments</h3>
            <p className="text-sm text-muted-foreground">Track physical performance metrics</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
