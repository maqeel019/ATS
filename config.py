# config.py
import os
# Debug settings
DEBUG_TEXT_OUTPUT = True

# Recruiter-defined parameters
MIN_EXPERIENCE        = 3.0    # minimum experience in years
MIN_SCORE             = 70     # minimum score threshold
REQUIRED_SKILLS = {
    "react",
    "javascript",
    "html",
    "API's Integration",
    "Material UI",
    "react.js",
    "css",
    "tailwind css",
    "typescript",
    "redux",
    "react router",
    "rest api",
    "git"
}

MIN_EDUCATION         = {"bachelor", "master", "phd"}

# I/O Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_DIR = os.path.join(OUTPUT_DIR, "logs")

PDF_FOLDER = os.path.join(BASE_DIR, "candidates")
OUTPUT_ALL_EXCEL = os.path.join(OUTPUT_DIR, "all_candidates_ranked.xlsx")
OUTPUT_FILTERED_EXCEL = os.path.join(OUTPUT_DIR, "filtered_candidates.xlsx")

# Scoring weights
RANKING_WEIGHTS       = {
    "experience": 30,
    "skills": 40,
    "education": 20,
    "profiles": 10
}

# Month map for date parsing
_MONTH_MAP = {
    "january": 1, "jan": 1, "jan.": 1,
    "february": 2, "feb": 2, "feb.": 2,
    "march": 3, "mar": 3, "mar.": 3,
    "april": 4, "apr": 4, "apr.": 4,
    "may": 5,
    "june": 6, "jun": 6, "jun.": 6,
    "july": 7, "jul": 7, "jul.": 7,
    "august": 8, "aug": 8, "aug.": 8,
    "september": 9, "sep": 9, "sept": 9, "sep.": 9, "sept.": 9,
    "october": 10, "oct": 10, "oct.": 10,
    "november": 11, "nov": 11, "nov.": 11,
    "december": 12, "dec": 12, "dec.": 12,
}



# Degree ranking
_DEGREE_KEYWORDS = {
    "phd": 4,
    "doctor": 4,
    "master": 3,
    "m.sc": 3,
    "msc": 3,
    "mba": 3,
    "mca": 3,
    "m.s.": 3,
    "m.s.c": 3,
    "m.tech": 3,
    "m.e.": 3,
    "bachelor's": 2,
    "bachelor of science": 2,
    "bachelor of arts": 2,
    "bachelor of engineering": 2,
    "bachelor of technology": 2,
    "bachelor of computer applications": 2,
    "bachelor of computer science": 2,
    "bachelor of business administration": 2,
    "bachelor of commerce": 2,
    "bachelor of science in computer science": 2,
    "bachelor of science in information technology": 2,
    "bachelor of science in information systems": 2,
    "bachelor of science in software engineering": 2,
    "bachelor of science in data science": 2,
    "bachelor of science in artificial intelligence": 2,
    "bachelor of science in machine learning": 2,
    "bachelor of science in cybersecurity": 2,
    "bachelor of science in cloud computing": 2,
    "bachelor": 2,
    "b.sc": 2,
    "bsc": 2,
    "bs": 2,
    "bca": 2,
    "b.tech": 2,
    "ba": 2,
    "be": 2,
    "b.e.": 2,
    "b.e": 2,
    "diploma": 1,
    "polytechnic": 1,
    "high school": 0,
    "Higher school": 0,
    "hsc": 0,
    "ssc": 0,
    "intermediate": 0,
    "12th": 0,
    "10th": 0,
}


# Default skill set (optional; can be used for broad extraction)
DEFAULT_SKILL_SET = {
    # Core Web Technologies
    "html",
    "css",
    "javascript",
    "typescript",
      "react",
    "javascript",
    "html",
    "API's Integration",
    "Material UI",
    "react.js",
    "css",
    "tailwind css",
    "typescript",
    "redux",
    "react router",
    "rest api",
    "git",
    # React Ecosystem
    "react",
    "react.js",
    "react hooks",
    "react router",
    "next.js",
    "redux",
    "redux toolkit",
    "zustand",
    "context api",
    "recoil",

    # Styling in React
    "tailwind css",
    "styled components",
    "sass",
    "css modules",
    "emotion",
    "material ui",
    "chakra ui",
    "bootstrap",

    # Component Design & Architecture
    "component based architecture",
    "atomic design",
    "design systems",
    "storybook",

    # API Integration
    "rest api",
    "graphql",
    "axios",
    "react query",
    "fetch api",
    "swr",

    # Routing & State
    "react router dom",
    "client side routing",
    "server side rendering",
    "hydration",
    "state management",

    # Build Tools & Dev Experience
    "vite",
    "webpack",
    "babel",
    "eslint",
    "prettier",

    # Testing Tools
    "jest",
    "react testing library",
    "cypress",
    "vitest",
    "enzyme",

    # DevOps & Version Control
    "git",
    "github",
    "bitbucket",
    "github actions",
    "vercel",
    "netlify",
    "firebase hosting",

    # Browser & Performance
    "chrome devtools",
    "lighthouse",
    "core web vitals",
    "code splitting",
    "lazy loading",

    # Accessibility & SEO
    "semantic html",
    "aria",
    "a11y",
    "seo optimization",
    "structured data",

    # Package Managers
    "npm",
    "yarn",
    "pnpm",

    # Design & Collaboration Tools
    "figma",
    "adobe xd",
    "sketch",

    # Concepts
    "responsive design",
    "mobile first design",
    "cross browser compatibility",
    "progressive web apps",
    "single page applications",
    "component reusability",
    "clean code practices"
     # Core Web Technologies
    "html",
    "css",
    "javascript",
    "typescript",

    # Frontend Frameworks & Libraries
    "react",
    "react.js",
    "next.js",
    "vue.js",
    "angular",
    "svelte",
    "jquery",

    # Styling & UI Frameworks
    "tailwind css",
    "bootstrap",
    "material ui",
    "chakra ui",
    "styled components",
    "sass",
    "less",

    # State Management
    "redux",
    "zustand",
    "mobx",
    "context api",
    "recoil",

    # API Integration & Communication
    "rest api",
    "graphql",
    "axios",
    "fetch api",
    "websockets",

    # Build Tools & Compilers
    "webpack",
    "vite",
    "babel",
    "eslint",
    "prettier",
    "postcss",

    # Testing Tools
    "jest",
    "react testing library",
    "cypress",
    "playwright",
    "vitest",

    # Version Control & CI/CD
    "git",
    "github",
    "gitlab",
    "bitbucket",
    "jenkins",
    "github actions",

    # Deployment & Hosting
    "vercel",
    "netlify",
    "firebase hosting",
    "aws amplify",
    "cloudflare pages",

    # Accessibility & SEO
    "a11y",
    "aria",
    "semantic html",
    "lighthouse",
    "core web vitals",

    # Design & Prototyping Tools
    "figma",
    "adobe xd",
    "sketch",

    # Package Managers
    "npm",
    "yarn",
    "pnpm",

    # Browser Dev Tools & Debugging
    "chrome devtools",
    "lighthouse",
    "source maps",
    "performance profiling",
     # Miscellaneous
    "responsive design",
    "cross browser compatibility",
    "mobile first design",
    "progressive web apps",
    "web performance optimization"
}
