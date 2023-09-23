import '@/styles/globals.css'
import Header from '@/components/layout/header'
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div className='flex'>
      <Header/>
      <Component {...pageProps} />
    </div>
  )
}
