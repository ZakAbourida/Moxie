
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { WorkoutLog as WorkoutLogType } from '@/lib/mockData';
import { cn } from '@/lib/utils';
import { Calendar } from 'lucide-react';

interface WorkoutLogProps {
  logs: WorkoutLogType[];
}

const WorkoutLog: React.FC<WorkoutLogProps> = ({ logs }) => {
  const getIntensityClass = (intensity: string) => {
    switch (intensity) {
      case 'Low':
        return 'bg-green-100 text-green-800';
      case 'Medium':
        return 'bg-amber-100 text-amber-800';
      case 'High':
        return 'bg-rose-100 text-rose-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  return (
    <Card className="col-span-1">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">Recent Workout Logs</CardTitle>
      </CardHeader>
      <CardContent className="px-2">
        <div className="space-y-3">
          {logs.map((log) => (
            <div key={log.id} className="p-3 rounded-lg bg-background hover:bg-secondary/40 transition-colors">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-medium">{log.athleteName}</h4>
                  <p className="text-sm text-muted-foreground">{log.type}</p>
                </div>
                <div className={cn(
                  "px-2 py-1 rounded-full text-xs font-medium",
                  getIntensityClass(log.intensity)
                )}>
                  {log.intensity}
                </div>
              </div>
              <div className="mt-2 text-sm text-muted-foreground flex items-center">
                <Calendar size={14} className="mr-1" />
                <span>{formatDate(log.date)} • {log.duration}</span>
              </div>
              <div className="mt-2 flex items-center">
                <div className="flex-1">
                  <div className="h-1.5 w-full bg-gray-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary rounded-full"
                      style={{ width: `${log.completionRate}%` }}
                    ></div>
                  </div>
                </div>
                <div className="ml-2 text-xs font-medium">{log.completionRate}%</div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default WorkoutLog;
