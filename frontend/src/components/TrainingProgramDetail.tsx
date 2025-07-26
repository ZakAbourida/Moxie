
import React from 'react';
import { TrainingProgram } from '@/lib/mockData';
import { Progress } from "@/components/ui/progress";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Users, Calendar, CheckCircle } from 'lucide-react';

interface TrainingProgramDetailProps {
  program: TrainingProgram;
}

const TrainingProgramDetail: React.FC<TrainingProgramDetailProps> = ({ program }) => {
  const { name, description, duration, targetGroup, athleteCount, progress } = program;

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row gap-6">
        <div className="space-y-4 flex-1">
          <div>
            <h2 className="text-2xl font-bold">{name}</h2>
            <p className="text-muted-foreground mt-1">{description}</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center gap-2">
              <Calendar size={16} className="text-muted-foreground" />
              <span className="text-sm">Duration: {duration}</span>
            </div>
            <div className="flex items-center gap-2">
              <Users size={16} className="text-muted-foreground" />
              <span className="text-sm">Athletes: {athleteCount}</span>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline">{targetGroup}</Badge>
            </div>
          </div>
          
          <div>
            <div className="flex justify-between items-center mb-1">
              <span className="text-sm font-medium">Overall Progress</span>
              <span className="text-sm font-medium">{progress}%</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>
        </div>
      </div>

      <Tabs defaultValue="overview" className="w-full">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="schedule">Schedule</TabsTrigger>
          <TabsTrigger value="progress">Progress</TabsTrigger>
          <TabsTrigger value="assignments">Assignments</TabsTrigger>
        </TabsList>
        <TabsContent value="overview">
          <Card>
            <CardContent className="pt-6">
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold">Objectives</h3>
                  <ul className="mt-2 space-y-2">
                    <li className="flex items-start">
                      <CheckCircle size={16} className="mr-2 text-success-700 mt-0.5" />
                      <span>Improve overall athletic performance</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle size={16} className="mr-2 text-success-700 mt-0.5" />
                      <span>Develop sport-specific skills and techniques</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle size={16} className="mr-2 text-success-700 mt-0.5" />
                      <span>Build endurance and stamina for competition</span>
                    </li>
                  </ul>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold">Key Metrics</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2">
                    <div className="bg-muted p-3 rounded-md">
                      <div className="text-sm text-muted-foreground">Sessions</div>
                      <div className="text-2xl font-bold">24</div>
                    </div>
                    <div className="bg-muted p-3 rounded-md">
                      <div className="text-sm text-muted-foreground">Hours</div>
                      <div className="text-2xl font-bold">36</div>
                    </div>
                    <div className="bg-muted p-3 rounded-md">
                      <div className="text-sm text-muted-foreground">Completion</div>
                      <div className="text-2xl font-bold">{progress}%</div>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold">Required Equipment</h3>
                  <p className="mt-2 text-muted-foreground">
                    Standard fitness equipment (weights, resistance bands), timing device, 
                    and sport-specific equipment depending on the focus area.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="schedule">
          <Card>
            <CardContent className="pt-6">
              <p className="text-muted-foreground">Schedule information will be displayed here.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="progress">
          <Card>
            <CardContent className="pt-6">
              <p className="text-muted-foreground">Detailed progress tracking will be displayed here.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="assignments">
          <Card>
            <CardContent className="pt-6">
              <p className="text-muted-foreground">Training assignments and tasks will be displayed here.</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default TrainingProgramDetail;
