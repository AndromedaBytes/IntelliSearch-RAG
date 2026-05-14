/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './app/**/*.{ts,tsx,js,jsx}',
    './components/**/*.{ts,tsx,js,jsx}',
    './hooks/**/*.{ts,tsx}',
    './lib/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Sora', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['DM Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
      colors: {
        gold: {
          DEFAULT: '#C9A84C',
          light: '#E8C87A',
          soft: '#F5E0A0',
        },
        accent: {
          DEFAULT: '#6366F1',
          glow: 'rgba(99,102,241,0.20)',
          soft: 'rgba(99,102,241,0.10)',
        },
        surface: {
          base: '#0a0d14',
          DEFAULT: '#0f1117',
          raised: '#151821',
          elevated: '#1c1f2e',
        },
        ink: {
          1: '#f0f1f8',
          2: '#8890aa',
          3: '#4e5468',
          4: '#2c2f42',
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
      animation: {
        'pulse-dot': 'pulse-dot 1.2s ease infinite',
        'spin-slow': 'spin 0.7s linear infinite',
        'bounce-dot': 'tdot 1.3s ease infinite',
        'slide-up': 'slideUp 0.25s ease both',
        'fade-in': 'fadeIn 0.2s ease both',
        'scale-in': 'scaleIn 0.25s ease both',
      },
      keyframes: {
        'pulse-dot': {
          '0%,100%': { opacity: '1' },
          '50%': { opacity: '0.35' },
        },
        tdot: {
          '0%,80%,100%': { transform: 'translateY(0)', opacity: '0.5' },
          '40%': { transform: 'translateY(-5px)', opacity: '1' },
        },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(10px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        scaleIn: {
          from: { opacity: '0', transform: 'scale(0.96)' },
          to: { opacity: '1', transform: 'scale(1)' },
        },
      },
      boxShadow: {
        'glow-accent': '0 0 20px rgba(99,102,241,0.20)',
        'glow-gold': '0 0 20px rgba(201,168,76,0.20)',
        card: '0 4px 24px rgba(0,0,0,0.4)',
      },
      borderColor: {
        DEFAULT: 'rgba(255,255,255,0.07)',
      },
    },
  },
  plugins: [],
}
