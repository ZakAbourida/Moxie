
import React, { useState } from 'react';
import Layout from '@/components/Layout';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Plus, Search, Filter } from 'lucide-react';
import { trainingPrograms } from '@/lib/mockData';
import TrainingProgramCard from '@/components/TrainingProgramCard';
import { TrainingProgram } from '@/lib/mockData';
import TrainingProgramDetail from '@/components/TrainingProgramDetail';

const TrainingPlans: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProgram, setSelectedProgram] = useState<TrainingProgram | null>(null);
  
  const filteredPrograms = trainingPrograms.filter(program => 
    program.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    program.targetGroup.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSelectProgram = (program: TrainingProgram) => {
    setSelectedProgram(program);
  };

  const closeTrainingProgramDetail = () => {
    setSelectedProgram(null);
  };

  return (
    <Layout>
      <div className="space-y-6 fade-in">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">Training Plans</h1>
          <Button className="flex items-center">
            <Plus size={16} className="mr-1" />
            Add Training Plan
          </Button>
        </div>

        {/* Search and filter section */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-grow max-w-md">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search training plans..."
              className="pl-8"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <Button variant="outline" className="flex items-center">
            <Filter size={16} className="mr-1" />
            Filters
          </Button>
        </div>

        {/* Training plans grid */}
        {filteredPrograms.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredPrograms.map((program) => (
              <div 
                key={program.id} 
                onClick={() => handleSelectProgram(program)}
                className="cursor-pointer"
              >
                <TrainingProgramCard program={program} />
              </div>
            ))}
          </div>
        ) : (
          <Card className="text-center py-8">
            <CardContent>
              <p className="text-muted-foreground">No training plans found. Try adjusting your search.</p>
            </CardContent>
          </Card>
        )}

        {/* Training plan detail section - shown below the grid when a plan is selected */}
        {selectedProgram && (
          <Card className="mt-6">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-xl">Training Plan Details</CardTitle>
              <Button variant="ghost" size="icon" onClick={closeTrainingProgramDetail} className="h-8 w-8">
                <span className="sr-only">Close</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="h-4 w-4"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              </Button>
            </CardHeader>
            <CardContent>
              <TrainingProgramDetail program={selectedProgram} />
            </CardContent>
          </Card>
        )}
      </div>
    </Layout>
  );
};

export default TrainingPlans;
