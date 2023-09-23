import Head from 'next/head';
import { useEffect, useState, FC } from 'react';

interface HomeProps {
  data: any;
  title?: string;
}

export async function getServerSideProps() {
  try {
    const response = await fetch('http://localhost:8000/handler-initial-data');
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    const initialData = await response.json();
    console.log(initialData)
    return { props: { data: initialData } };
  } catch (error) {
    console.error('Fetch error:', error);
    return { props: { data: null } };
  }
}

const Home: FC<HomeProps> = ({ data, title = 'Untitled Document' }) => {
  const [stateData, setData] = useState(data);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/handler');
  
    socket.onopen = () => {
      console.log('WebSocket is connected.');
    };
  
    socket.onmessage = (event) => {
      console.log(event)
      const data = JSON.parse(event.data);
      setData(data);
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
      <Head>
        <title>OSS Docs</title>
        <meta name="description" content="Fast like SSR, Powerful like WebSockets" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1>{title}</h1>
        <div>Data is: {JSON.stringify(stateData)}</div>
      </main>
    </div>
  );
};

export default Home;
