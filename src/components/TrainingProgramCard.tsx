
import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Users } from "lucide-react";
import { TrainingProgram } from '@/lib/mockData';
import { cn } from '@/lib/utils';

interface TrainingProgramCardProps {
  program: TrainingProgram;
}

const TrainingProgramCard: React.FC<TrainingProgramCardProps> = ({ program }) => {
  const { name, description, duration, targetGroup, athleteCount, progress, color } = program;

  const getGradientClass = () => {
    switch (color) {
      case 'athletic':
        return 'athletic-bg-gradient';
      case 'success':
        return 'success-bg-gradient';
      case 'warning':
        return 'bg-gradient-to-br from-warning-500 to-warning-700';
      default:
        return 'bg-gradient-to-br from-athletic-700 to-athletic-900';
    }
  };

  return (
    <Card className="card-hover overflow-hidden">
      <div className={cn("h-2", getGradientClass())}></div>
      <CardContent className="p-4">
        <h3 className="font-semibold text-lg">{name}</h3>
        <p className="text-sm text-muted-foreground line-clamp-2 mt-1">{description}</p>
        
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div>
            <span className="text-xs text-muted-foreground">Duration</span>
            <p className="text-sm font-medium">{duration}</p>
          </div>
          <div>
            <span className="text-xs text-muted-foreground">Target</span>
            <p className="text-sm font-medium">{targetGroup}</p>
          </div>
        </div>
        
        <div className="mt-4">
          <div className="flex justify-between items-center mb-1">
            <span className="text-sm font-medium">Progress</span>
            <span className="text-sm font-medium">{progress}%</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>
        
        <div className="mt-4 flex items-center text-sm text-muted-foreground">
          <Users size={16} className="mr-1" />
          <span>{athleteCount} athletes</span>
        </div>
      </CardContent>
    </Card>
  );
};

export default TrainingProgramCard;
