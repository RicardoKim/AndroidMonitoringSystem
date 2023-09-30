import Head from 'next/head';
import { useEffect, useState, FC } from 'react';
import { Inter } from 'next/font/google'
import { ProcessTableComponent, MemoryTableComponent } from '@/components/table';
import { ProcessDataType, MemoryDataType } from '@/types/types';

const inter = Inter({ subsets: ['latin'] })

interface HomeProps {
  data: any;
  title?: string;
}

const Home: FC<HomeProps> = () => {
  const [processDatareceived, setProcessDataReceived] = useState<boolean>(false);
  const [memoryDatareceived, setMemoryDataReceived] = useState<boolean>(false);
  const [processData, setProcessData] = useState<ProcessDataType>();
  const [memoryData, setMemoryData] = useState<MemoryDataType>()

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/handler');
  
    socket.onopen = () => {
      console.log('WebSocket is connected.');
    };
  
    socket.onmessage = (event) => {
      console.log(event)
      const data = JSON.parse(event.data);
      // console.log(data)
      if('process_info' in data){
        setProcessData(data['process_info']);
        setProcessDataReceived(true);
      }else if('memory_info' in data){
        setMemoryData(data['memory_info']);
        setMemoryDataReceived(true)
      }
    };
  
    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  
    socket.onclose = () => {
      console.log('WebSocket is closed.');
    };
  
    return () => {
      socket.close();
    };
  }, []);
  

  return (
    <main className={`flex-col space-y-4 min-h-screen flex-col items-center justify-between p-24 ${inter.className}`}>
      <div className = 'flex-col'>
          <div className = 'pb-2'>{'System Process Info'}</div>
          {processDatareceived ? <ProcessTableComponent data={processData!} /> : <div className='text-2xl'>Loading.... </div>}
      </div>
      <div className = 'flex-col'>
          <div className = 'pb-2'>{'System Memory Info'}</div>
          {processDatareceived ? <MemoryTableComponent data={memoryData!} /> : <div className='text-2xl'>Loading.... </div>}
      </div>
    </main>
  );
};

export default Home;
