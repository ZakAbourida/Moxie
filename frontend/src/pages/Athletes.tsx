
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '@/components/Layout';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Loader2, Plus, Search, User, MapPin, Calendar, Target } from 'lucide-react';
import { apiService, Athlete, Goal, PersonalRecord } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';

const Athletes: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [athletes, setAthletes] = useState<Athlete[]>([]);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [records, setRecords] = useState<PersonalRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSector, setSelectedSector] = useState('');

  useEffect(() => {
    if (isAuthenticated) {
      loadData();
    }
  }, [isAuthenticated]);

  const loadData = async () => {
    try {
      setIsLoading(true);
      const [athletesData, goalsData, recordsData] = await Promise.all([
        apiService.getAthletes(),
        apiService.getGoals(),
        apiService.getRecords()
      ]);
      
      setAthletes(athletesData);
      setGoals(goalsData);
      setRecords(recordsData);
    } catch (error) {
      console.error('Error loading data:', error);
      toast.error('Failed to load athletes data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAthleteClick = (athleteId: string) => {
    navigate(`/athletes/${athleteId}`);
  };

  const getAthleteGoals = (athleteId: string) => {
    return goals.filter(goal => goal.athlete_id === athleteId && goal.status === 'active');
  };

  const getAthleteRecords = (athleteId: string) => {
    return records.filter(record => record.athlete_id === athleteId);
  };

  const filteredAthletes = athletes.filter(athlete => {
    const matchesSearch = searchTerm === '' || 
      athlete.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      athlete.last_name.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesSector = selectedSector === '' || athlete.sector === selectedSector;
    
    return matchesSearch && matchesSector;
  });

  const uniqueSectors = [...new Set(athletes.map(athlete => athlete.sector).filter(Boolean))];

  const getAgeFromBirthDate = (birthDate?: string) => {
    if (!birthDate) return null;
    const today = new Date();
    const birth = new Date(birthDate);
    const age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      return age - 1;
    }
    return age;
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <Layout>
      <div className="space-y-8 fade-in">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Athletes</h1>
            <p className="text-muted-foreground">Manage your athletes and track their progress</p>
          </div>
          <Button onClick={() => navigate('/athletes/new')} className="flex items-center">
            <Plus size={16} className="mr-2" />
            Add Athlete
          </Button>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" size={16} />
            <Input
              placeholder="Search athletes by name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <select
            value={selectedSector}
            onChange={(e) => setSelectedSector(e.target.value)}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 sm:w-48"
          >
            <option value="">All Sectors</option>
            {uniqueSectors.map(sector => (
              <option key={sector} value={sector}>{sector}</option>
            ))}
          </select>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex justify-center items-center py-12">
            <Loader2 className="h-6 w-6 animate-spin" />
            <span className="ml-2">Loading athletes...</span>
          </div>
        )}

        {/* Athletes Grid */}
        {!isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredAthletes.map((athlete) => {
              const athleteGoals = getAthleteGoals(athlete.id);
              const athleteRecords = getAthleteRecords(athlete.id);
              const age = getAgeFromBirthDate(athlete.birth_date);

              return (
                <Card 
                  key={athlete.id} 
                  className="hover:shadow-lg transition-shadow cursor-pointer group"
                  onClick={() => handleAthleteClick(athlete.id)}
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
                        <div className="flex items-center text-sm text-muted-foreground">
                          {age && (
                            <>
                              <Calendar size={12} className="mr-1" />
                              <span>{age} years old</span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* Basic Info */}
                    <div className="space-y-2">
                      {athlete.sector && (
                        <div className="flex items-center text-sm">
                          <MapPin size={12} className="mr-2 text-muted-foreground" />
                          <span>{athlete.sector}</span>
                        </div>
                      )}
                      {athlete.specialties.length > 0 && (
                        <div className="flex flex-wrap gap-1">
                          {athlete.specialties.slice(0, 2).map((specialty, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {specialty}
                            </Badge>
                          ))}
                          {athlete.specialties.length > 2 && (
                            <Badge variant="outline" className="text-xs">
                              +{athlete.specialties.length - 2} more
                            </Badge>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Goals */}
                    {athleteGoals.length > 0 && (
                      <div>
                        <div className="flex items-center text-sm font-medium mb-2">
                          <Target size={12} className="mr-2 text-blue-500" />
                          Active Goals ({athleteGoals.length})
                        </div>
                        <div className="space-y-1">
                          {athleteGoals.slice(0, 2).map((goal) => (
                            <div key={goal.id} className="text-sm text-muted-foreground truncate">
                              • {goal.name}
                            </div>
                          ))}
                          {athleteGoals.length > 2 && (
                            <div className="text-xs text-muted-foreground">
                              ... and {athleteGoals.length - 2} more
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Personal Records */}
                    {athleteRecords.length > 0 && (
                      <div>
                        <div className="text-sm font-medium mb-1">
                          Recent PB: {athleteRecords[0]?.discipline}
                        </div>
                        <div className="text-lg font-bold text-blue-600">
                          {athleteRecords[0]?.value}
                        </div>
                      </div>
                    )}

                    {/* Health Status */}
                    {athlete.health_status && (
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">Health:</span>
                        <Badge 
                          variant={athlete.health_status === 'Excellent' ? 'default' : 'secondary'}
                          className="text-xs"
                        >
                          {athlete.health_status}
                        </Badge>
                      </div>
                    )}
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}

        {/* Empty State */}
        {!isLoading && filteredAthletes.length === 0 && (
          <div className="text-center py-12">
            <User className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-2 text-sm font-semibold">No athletes found</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              {searchTerm || selectedSector 
                ? 'Try adjusting your search filters'
                : 'Get started by adding your first athlete'
              }
            </p>
            {!searchTerm && !selectedSector && (
              <div className="mt-6">
                <Button onClick={() => navigate('/athletes/new')}>
                  <Plus className="mr-2 h-4 w-4" />
                  Add Athlete
                </Button>
              </div>
            )}
          </div>
        )}

        {/* Stats Summary */}
        {!isLoading && athletes.length > 0 && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold">{athletes.length}</div>
                <div className="text-sm text-muted-foreground">Total Athletes</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold">{goals.filter(g => g.status === 'active').length}</div>
                <div className="text-sm text-muted-foreground">Active Goals</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold">{uniqueSectors.length}</div>
                <div className="text-sm text-muted-foreground">Sectors</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold">{records.length}</div>
                <div className="text-sm text-muted-foreground">Personal Records</div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Athletes;
