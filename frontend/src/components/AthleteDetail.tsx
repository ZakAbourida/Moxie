
import React from 'react';
import { Athlete } from '@/lib/mockData';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent } from '@/components/ui/card';
import { TrendingUp, TrendingDown, Calendar, Dumbbell, Clipboard, LineChart } from 'lucide-react';

interface AthleteDetailProps {
  athlete: Athlete;
}

const AthleteDetail: React.FC<AthleteDetailProps> = ({ athlete }) => {
  const isPerformanceUp = athlete.recentPerformance.change > 0;

  // Sample data for demonstration - would normally come from backend
  const weightData = [
    { date: '2025-01-01', value: 180 },
    { date: '2025-02-01', value: 178 },
    { date: '2025-03-01', value: 176 },
    { date: '2025-04-01', value: 175 },
    { date: '2025-05-01', value: 173 },
  ];

  const performanceData = [
    { metric: 'Speed', current: 85, previous: 80 },
    { metric: 'Strength', current: 78, previous: 75 },
    { metric: 'Endurance', current: 92, previous: 85 },
    { metric: 'Technique', current: 88, previous: 90 },
    { metric: 'Agility', current: 76, previous: 74 },
  ];

  return (
    <div className="space-y-6">
      {/* Athlete header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 rounded-full bg-athletic-600 flex items-center justify-center text-white text-xl font-bold">
            {athlete.name.split(' ').map(n => n[0]).join('')}
          </div>
          <div>
            <h2 className="text-2xl font-bold">{athlete.name}</h2>
            <div className="flex items-center space-x-2 text-muted-foreground">
              <span>{athlete.sport}</span>
              <span>•</span>
              <span>{athlete.level}</span>
            </div>
          </div>
        </div>
        <div className="flex flex-col items-end">
          <div className={`flex items-center px-3 py-1 rounded-full text-sm ${
            isPerformanceUp ? "bg-success-100 text-success-700" : "bg-destructive/10 text-destructive"
          }`}>
            {isPerformanceUp ? (
              <TrendingUp size={18} className="mr-1" />
            ) : (
              <TrendingDown size={18} className="mr-1" />
            )}
            <span>{isPerformanceUp ? '+' : ''}{athlete.recentPerformance.change}%</span>
          </div>
          <span className="text-sm text-muted-foreground mt-1">Recent Performance</span>
        </div>
      </div>

      {/* Progress section */}
      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <h3 className="font-medium">Program Progress</h3>
          <span className="font-medium">{athlete.progress}%</span>
        </div>
        <Progress value={athlete.progress} className="h-2" />
      </div>

      <Separator />

      {/* Tabs section */}
      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid grid-cols-4 mb-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="training">Training</TabsTrigger>
          <TabsTrigger value="metrics">Metrics</TabsTrigger>
          <TabsTrigger value="notes">Notes</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Next session */}
            <Card>
              <CardContent className="p-4">
                <div className="flex items-start space-x-3">
                  <div className="bg-primary/10 p-2 rounded-full">
                    <Calendar className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h4 className="text-sm font-medium">Next Session</h4>
                    <p className="text-lg font-semibold">{athlete.nextSession}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Current focus */}
            <Card>
              <CardContent className="p-4">
                <div className="flex items-start space-x-3">
                  <div className="bg-primary/10 p-2 rounded-full">
                    <Dumbbell className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h4 className="text-sm font-medium">Current Focus</h4>
                    <p className="text-lg font-semibold">{athlete.goals[0] || 'No focus set'}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Goals section */}
          <div>
            <h3 className="text-lg font-medium mb-3">Goals</h3>
            <ul className="space-y-2">
              {athlete.goals.map((goal, index) => (
                <li key={index} className="flex items-center space-x-2 bg-muted/50 rounded-md p-3">
                  <div className="bg-primary/10 p-1.5 rounded-full">
                    <Clipboard className="h-4 w-4 text-primary" />
                  </div>
                  <span>{goal}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Recent performance */}
          <div>
            <h3 className="text-lg font-medium mb-3">Recent Performance</h3>
            <div className="space-y-3">
              {performanceData.map((item, index) => (
                <div key={index}>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm font-medium">{item.metric}</span>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-muted-foreground">{item.previous}</span>
                      <span className="text-sm">→</span>
                      <span className="text-sm font-medium">{item.current}</span>
                    </div>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${item.current > item.previous ? 'bg-success-500' : 'bg-primary'}`} 
                      style={{ width: `${item.current}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="training">
          <div className="p-4 text-center border border-dashed rounded-md">
            <h3 className="text-lg font-medium mb-2">Training History</h3>
            <p className="text-muted-foreground">Training history will be displayed here.</p>
          </div>
        </TabsContent>

        <TabsContent value="metrics">
          <div className="p-4 text-center border border-dashed rounded-md">
            <h3 className="text-lg font-medium mb-2">Athlete Metrics</h3>
            <p className="text-muted-foreground">Detailed metrics will be displayed here.</p>
          </div>
        </TabsContent>

        <TabsContent value="notes">
          <div className="p-4 text-center border border-dashed rounded-md">
            <h3 className="text-lg font-medium mb-2">Coach Notes</h3>
            <p className="text-muted-foreground">Notes and feedback will be displayed here.</p>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AthleteDetail;
