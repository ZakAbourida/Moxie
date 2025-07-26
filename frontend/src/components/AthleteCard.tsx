
import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { TrendingUp, TrendingDown } from "lucide-react";
import { Athlete } from '@/lib/mockData';
import { cn } from '@/lib/utils';

interface AthleteCardProps {
  athlete: Athlete;
}

const AthleteCard: React.FC<AthleteCardProps> = ({ athlete }) => {
  const { name, sport, level, progress, goals, nextSession, recentPerformance } = athlete;
  const isPerformanceUp = recentPerformance.change > 0;

  return (
    <Card className="card-hover">
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-full bg-athletic-600 flex items-center justify-center text-white font-semibold">
                {name.split(' ').map(n => n[0]).join('')}
              </div>
              <div>
                <h3 className="font-semibold text-lg">{name}</h3>
                <div className="text-sm text-muted-foreground flex items-center">
                  <span className="mr-2">{sport}</span>
                  <span className="w-1 h-1 rounded-full bg-muted-foreground"></span>
                  <span className="ml-2">{level}</span>
                </div>
              </div>
            </div>
          </div>
          <div className="flex items-center">
            <div className={cn(
              "flex items-center px-2 py-1 rounded-full text-xs",
              isPerformanceUp ? "bg-success-100 text-success-700" : "bg-destructive/10 text-destructive"
            )}>
              {isPerformanceUp ? (
                <TrendingUp size={14} className="mr-1" />
              ) : (
                <TrendingDown size={14} className="mr-1" />
              )}
              <span>{Math.abs(recentPerformance.change)}%</span>
            </div>
          </div>
        </div>

        <div className="mt-4">
          <div className="flex justify-between items-center mb-1">
            <span className="text-sm font-medium">Program Progress</span>
            <span className="text-sm font-medium">{progress}%</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {goals.length > 0 && (
          <div className="mt-4">
            <h4 className="text-sm font-medium mb-2">Goals</h4>
            <ul className="space-y-1">
              {goals.slice(0, 2).map((goal, index) => (
                <li key={index} className="text-sm text-muted-foreground">• {goal}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="mt-4 pt-3 border-t border-border">
          <div className="flex justify-between items-center">
            <span className="text-xs font-medium">Next Session</span>
            <span className="text-xs font-semibold text-athletic-600">{nextSession}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AthleteCard;
