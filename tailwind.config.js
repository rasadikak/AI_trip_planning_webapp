module.exports = {
  content: [
    "./frontend/**/*.html",
    "./frontend/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        'serendib': {
          'dark'  : '#0D1B0E',
          'green' : '#2E7D32',
          'light' : '#4CAF50',
          'gold'  : '#F59E0B',
          'card'  : '#1A2E1B',
        }
      },
      fontFamily: {
        'heading': ['Playfair Display', 'serif'],
        'body'   : ['Outfit', 'sans-serif'],
      }
    },
  },
  plugins: [],
}