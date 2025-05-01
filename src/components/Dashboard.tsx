
import React from 'react';
import AthleteCard from './AthleteCard';
import TrainingProgramCard from './TrainingProgramCard';
import ProgressChart from './ProgressChart';
import WorkoutLog from './WorkoutLog';
import { Card, CardContent } from "@/components/ui/card";
import { athletes, trainingPrograms, workoutLogs, summaryMetrics } from '@/lib/mockData';
import { TrendingUp, TrendingDown, Plus } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { cn } from '@/lib/utils';

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-8 fade-in">
      {/* Summary metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {summaryMetrics.map((metric, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">{metric.label}</p>
                  <h3 className="text-3xl font-bold mt-1">{metric.value}</h3>
                </div>
                <div className={cn(
                  "h-fit flex items-center px-2 py-1 rounded-full text-xs",
                  metric.isPositive ? "bg-success-100 text-success-700" : "bg-destructive/10 text-destructive"
                )}>
                  {metric.isPositive ? (
                    <TrendingUp size={14} className="mr-1" />
                  ) : (
                    <TrendingDown size={14} className="mr-1" />
                  )}
                  <span>{Math.abs(metric.change)}%</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Actions bar */}
      <div className="flex justify-between items-center pt-2">
        <h2 className="text-xl font-semibold">Athletes</h2>
        <Button className="flex items-center">
          <Plus size={16} className="mr-1" />
          Add Athlete
        </Button>
      </div>

      {/* Athletes grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {athletes.map((athlete) => (
          <AthleteCard key={athlete.id} athlete={athlete} />
        ))}
      </div>

      {/* Charts and logs */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
        <ProgressChart />
        <WorkoutLog logs={workoutLogs} />
      </div>

      {/* Training programs section */}
      <div>
        <div className="flex justify-between items-center mb-4 pt-2">
          <h2 className="text-xl font-semibold">Training Programs</h2>
          <Button className="flex items-center">
            <Plus size={16} className="mr-1" />
            Create Program
          </Button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {trainingPrograms.map((program) => (
            <TrainingProgramCard key={program.id} program={program} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
