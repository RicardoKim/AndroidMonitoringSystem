// TableComponent.tsx
import React from 'react';
import { ProcessDataType, MemoryDataType } from '@/types/types';

interface ProcessTableProps {
  data: ProcessDataType ;
}

interface MemoryTableProps {
  data: MemoryDataType ;
}

export const ProcessTableComponent: React.FC<ProcessTableProps> = ({ data }) => {
  return (
    (data != null &&
      <div className="min-w-full overflow-hidden overflow-x-auto border-2 border-neutral-800">
        <table className="min-w-full bg-white">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b border-gray-200 text-left">Running</th>
              <th className="py-2 px-4 border-b border-gray-200 text-left">Sleeping</th>
              <th className="py-2 px-4 border-b border-gray-200 text-left">Stopped</th>
              <th className="py-2 px-4 border-b border-gray-200 text-left">Task</th>
              <th className="py-2 px-4 border-b border-gray-200 text-left">Zombie</th>
            </tr>
          </thead>
          <tbody>
              <tr>
                <td className="py-2 px-4 border-b border-gray-200">{data.fullDocument.Running}</td>
                <td className="py-2 px-4 border-b border-gray-200">{data.fullDocument.Sleeping}</td>
                <td className="py-2 px-4 border-b border-gray-200">{data.fullDocument.Stopped}</td>
                <td className="py-2 px-4 border-b border-gray-200">{data.fullDocument.Task}</td>
                <td className="py-2 px-4 border-b border-gray-200">{data.fullDocument.Zombie}</td>
              </tr>
          </tbody>
        </table>
      </div>  
    )
    
  );
};

export const MemoryTableComponent: React.FC<MemoryTableProps> = ({ data }) => {
  return (
    (data != null &&
      <div className="min-w-full overflow-hidden overflow-x-auto border-2 border-neutral-800">
        <table className="min-w-full bg-white">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b border-gray-200 text-left">Total</th>
              <th className="py-2 px-4 border-b border-gray-200 text-left">Used</th>
              <th className="py-2 px-4 border-b border-gray-200 text-left">Free</th>
            </tr>
          </thead>
          <tbody>
              <tr>
                <td className="py-2 px-4 border-b border-gray-200">{Math.round(data.fullDocument.Total * 10) / 10 + 'GB'}</td>
                <td className="py-2 px-4 border-b border-gray-200">{Math.round(data.fullDocument.Used * 10) / 10  + 'GB'}</td>
                <td className="py-2 px-4 border-b border-gray-200">{Math.round(data.fullDocument.Free * 10) / 10  + 'GB'}</td>
              </tr>
          </tbody>
        </table>
      </div>  
    )
    
  );
};