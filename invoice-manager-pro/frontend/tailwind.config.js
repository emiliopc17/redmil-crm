/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                spotify: {
                    green: "#1DB954",
                    black: "#121212",
                    gray: {
                        DEFAULT: "#181818",
                        light: "#282828",
                        text: "#b3b3b3"
                    }
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
