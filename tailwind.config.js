/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./template/**/*.html", // template at the project level
    "./**/template/**/*.html" // template inside the app
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

