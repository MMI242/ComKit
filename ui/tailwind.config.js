/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
    "./assets/styles/**/*.{css,scss}"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#DAD7CD',
          100: '#A3B18A',
          200: '#588157',
          300: '#3A5A40',
          400: '#344E41',
          500: '#2D3748',
          600: '#1A1E29',
          700: '#0F172A',
        },
        sage: {
          50: '#DAD7CD',
          100: '#A3B18A',
          200: '#588157',
          300: '#3A5A40',
          400: '#344E41',
          500: '#2D3748',
          600: '#1A1E29',
          700: '#0F172A',
        }
      }
    },
  },
  plugins: [],
}

