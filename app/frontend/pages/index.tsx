import Head from 'next/head';
import { useEffect, useState, FC } from 'react';
import { Inter } from 'next/font/google'
import { TableComponent } from '@/components/table';
import { ProcessTableData } from '@/types/types';

const inter = Inter({ subsets: ['latin'] })

interface HomeProps {
  data: any;
  title?: string;
}

const Home: FC<HomeProps> = () => {
  const [received, setReceived] = useState<boolean>(false);
  const [processData, setProcessData] = useState<ProcessTableData>();
  

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/handler');
  
    socket.onopen = () => {
      console.log('WebSocket is connected.');
    };
  
    socket.onmessage = (event) => {
      console.log(event)
      const data = JSON.parse(event.data);
      setProcessData(data);
      setReceived(true);
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
    <div>
      <main className={`flex min-h-screen flex-col items-center justify-between p-24 ${inter.className}`}>
          <div className = 'flex-col'>
              <div className = 'pb-2'>{'System Process Info'}</div>
              {received ? <TableComponent data={processData!} /> : <div className='text-2xl'>Loading.... </div>}
          </div>
        </main>
    </div>

  );
};

export default Home;
