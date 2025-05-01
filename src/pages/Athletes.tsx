
import React, { useState } from 'react';
import Layout from '@/components/Layout';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { athletes } from '@/lib/mockData';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Plus, Search } from 'lucide-react';

const Athletes: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const filteredAthletes = athletes.filter(athlete => 
    athlete.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    athlete.sport.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Layout>
      <div className="space-y-6 fade-in">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">Athletes</h1>
          <Button className="flex items-center">
            <Plus size={16} className="mr-1" />
            Add Athlete
          </Button>
        </div>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-lg">Athlete Roster</CardTitle>
            <div className="relative max-w-sm">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search athletes..."
                className="pl-8"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Sport</TableHead>
                  <TableHead>Level</TableHead>
                  <TableHead>Progress</TableHead>
                  <TableHead>Next Session</TableHead>
                  <TableHead>Recent Performance</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredAthletes.map((athlete) => (
                  <TableRow key={athlete.id}>
                    <TableCell>
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 rounded-full bg-athletic-600 flex items-center justify-center text-white font-semibold">
                          {athlete.name.split(' ').map(n => n[0]).join('')}
                        </div>
                        <div className="font-medium">{athlete.name}</div>
                      </div>
                    </TableCell>
                    <TableCell>{athlete.sport}</TableCell>
                    <TableCell>{athlete.level}</TableCell>
                    <TableCell>
                      <div className="w-full bg-muted rounded-full h-2 mr-2">
                        <div 
                          className="bg-primary h-2 rounded-full" 
                          style={{ width: `${athlete.progress}%` }}
                        />
                      </div>
                      <span className="text-xs text-muted-foreground">{athlete.progress}%</span>
                    </TableCell>
                    <TableCell>{athlete.nextSession}</TableCell>
                    <TableCell>
                      <Badge
                        variant={athlete.recentPerformance.change > 0 ? "success" : "destructive"}
                        className="whitespace-nowrap"
                      >
                        {athlete.recentPerformance.change > 0 ? '+' : ''}
                        {athlete.recentPerformance.change}%
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        variant="ghost"
                        className="h-8 w-8 p-0"
                        onClick={() => {
                          // View athlete detail when implemented
                          console.log(`View athlete ${athlete.id}`);
                        }}
                      >
                        View
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
};

export default Athletes;
