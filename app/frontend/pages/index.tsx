import Head from 'next/head';
import { useEffect, useState, FC } from 'react';
import { Inter } from 'next/font/google'
import { ResourceTableType } from '@/types/types';
import ResourceTable from '@/components/table';

const inter = Inter({ subsets: ['latin'] })

interface HomeProps {
  data: any;
  title?: string;
}

const Home: FC<HomeProps> = () => {
  const [resourceDatareceived, setResourceDataReceived] = useState<boolean>(false);
  const [resourceData, setResourceData] = useState<ResourceTableType>();

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/handler');
  
    socket.onopen = () => {
      console.log('WebSocket is connected.');
    };
  
    socket.onmessage = (event) => {
      console.log(event)
      const data = JSON.parse(event.data);
      console.log(data)
      if('resource_info' in data){
        setResourceData(data['resource_info']);
        setResourceDataReceived(true);
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
          <div className = 'pb-2'>{'Android Resource Info'}</div>
          {resourceDatareceived ? <ResourceTable data={resourceData!} /> : <div className='text-2xl'>Loading.... </div>}
      </div>
    </main>
  );
};

export default Home;
