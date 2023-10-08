// TableComponent.tsx
import React from 'react';
import { ResourceTableType } from '@/types/types';

interface ResourceTableProps {
  data: ResourceTableType ;
}

const SystemResourceTable: React.FC<ResourceTableProps> = ({ data }) => {
  const [totalMemory, usedMemory, freeMemory] = data.fullDocument.memory_info.map(num => Math.floor(num * 10) / 10);

  return (
    <div className="p-4">
      <table className="table-auto w-full bg-white shadow-md rounded">
        <tbody className="bg-white">
          <tr className="text-md font-semibold text-left text-gray-900 bg-gray-100 uppercase border-b border-gray-600">
            <td className="px-4 py-3">Time</td>
            <td className="px-4 py-3">CPU Usage</td>
            <td className="px-4 py-3">Battery Level</td>
            <td className="px-4 py-3">Total Memory</td>
            <td className="px-4 py-3">Used Memory</td>
            <td className="px-4 py-3">Free Memory</td>
          </tr>
          <tr className="text-gray-700">
            <td className="px-4 py-3 border">{data.fullDocument.created_at}</td>
            <td className="px-4 py-3 border">{data.fullDocument.cpu_usage}%</td>
            <td className="px-4 py-3 border">{data.fullDocument.battery_level}%</td>
            
            
            <td className="px-4 py-3 border">{totalMemory} GB</td>
            <td className="px-4 py-3 border">{usedMemory} GB</td>
            <td className="px-4 py-3 border">{freeMemory} GB</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default SystemResourceTable;
