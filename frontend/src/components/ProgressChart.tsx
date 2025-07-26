
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { progressData } from '@/lib/mockData';

const ProgressChart: React.FC = () => {
  return (
    <Card className="col-span-2">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">Athlete Performance Trends</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={progressData}
              margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis 
                dataKey="month" 
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12 }}
              />
              <Tooltip />
              <Line
                type="monotone"
                name="Performance"
                dataKey="performance"
                stroke="#3B82F6"
                strokeWidth={3}
                dot={{ r: 4, strokeWidth: 2 }}
                activeDot={{ r: 6 }}
              />
              <Line 
                type="monotone"
                name="Group Average" 
                dataKey="average" 
                stroke="#9CA3AF" 
                strokeDasharray="5 5" 
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default ProgressChart;
