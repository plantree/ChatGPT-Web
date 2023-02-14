/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/*.{js,ts,jsx,tsx,vue}",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
  ],
  theme: {
    extend: {
      colors: {
        'main': '#646cff'
      },
      maxWidth: {
        '1/2': '50%',
        '3/4': '75%'
      }
    },
  },
  plugins: [],
}