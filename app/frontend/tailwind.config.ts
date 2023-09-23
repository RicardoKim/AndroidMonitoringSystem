import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
        fontFamily: { // 폰트패밀리
          roboto: ["var(--roboto)"], // 다음과 같이 배열 안에 string으로 작성합니다.
        },
    },
  },
  plugins: [],
}
export default config
