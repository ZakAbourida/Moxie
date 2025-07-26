import React from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';
import { PhysicalAssessment } from '@/lib/api';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

interface RadarChartProps {
  assessment: PhysicalAssessment;
  className?: string;
}

const RadarChart: React.FC<RadarChartProps> = ({ assessment, className = '' }) => {
  const labels = [
    'Max Strength',
    'Endurance Strength',
    'Explosive Strength',
    'Linear Speed',
    'Agility',
    'Power',
    'Mobility',
    'Aerobic Endurance',
    'Lactate Endurance',
    'ICM'
  ];

  const dataValues = [
    assessment.strength_max || 0,
    assessment.strength_endurance || 0,
    assessment.strength_explosive || 0,
    assessment.speed_linear || 0,
    assessment.agility || 0,
    assessment.power || 0,
    assessment.mobility || 0,
    assessment.endurance_aerobic || 0,
    assessment.endurance_lactate || 0,
    assessment.icm || 0
  ];

  const data = {
    labels,
    datasets: [
      {
        label: 'Assessment Score',
        data: dataValues,
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(59, 130, 246, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(59, 130, 246, 1)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            return `${context.label}: ${context.parsed.r}/10`;
          }
        }
      }
    },
    scales: {
      r: {
        angleLines: {
          display: true,
        },
        suggestedMin: 0,
        suggestedMax: 10,
        ticks: {
          stepSize: 2,
          callback: function(value: any) {
            return value.toString();
          }
        },
        pointLabels: {
          font: {
            size: 12,
          }
        }
      },
    },
    maintainAspectRatio: false,
  };

  return (
    <div className={`${className}`} style={{ height: '400px' }}>
      <Radar data={data} options={options} />
    </div>
  );
};

export default RadarChart;