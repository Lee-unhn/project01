<template>
  <div id="app" class="tech-theme">
    <header class="app-header">
      <nav class="main-nav">
        <router-link to="/" class="nav-item">儀表板 & 日曆</router-link>
        <!-- Removed separate calendar link as they are integrated -->
      </nav>
    </header>
    <main class="app-main">
      <router-view/>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
/* Global Tech-Style Dark Theme */
:root {
  --primary-color: #00bcd4; /* Cyan */
  --secondary-color: #212121; /* Dark Grey */
  --background-dark: #121212; /* Very Dark Grey */
  --background-light: #1e1e1e; /* Slightly Lighter Dark Grey */
  --text-light: #e0e0e0; /* Light Grey for text */
  --text-muted: #9e9e9e; /* Muted grey for secondary text */
  --accent-color: #ff4081; /* Pink accent */
  --border-color: #424242; /* Medium Dark Grey for borders */
  --shadow-sm: rgba(0, 188, 212, 0.1) 0px 1px 3px 0px, rgba(0, 188, 212, 0.06) 0px 1px 2px 0px;
  --shadow-md: rgba(0, 188, 212, 0.2) 0px 4px 6px -1px, rgba(0, 188, 212, 0.1) 0px 2px 4px -1px;
}

body {
  margin: 0;
  font-family: 'Roboto Mono', monospace; /* Techy font */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--background-dark);
  color: var(--text-light);
  line-height: 1.6;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: var(--secondary-color);
  padding: 15px 20px;
  box-shadow: var(--shadow-md);
  border-bottom: 2px solid var(--primary-color);
}

.main-nav {
  display: flex;
  justify-content: center;
  gap: 30px;
}

.nav-item {
  color: var(--text-light);
  text-decoration: none;
  font-weight: bold;
  font-size: 1.1em;
  padding: 8px 15px;
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
  border: 1px solid transparent;
}

.nav-item:hover,
.nav-item.router-link-exact-active {
  background-color: var(--primary-color);
  color: var(--secondary-color);
  border-color: var(--primary-color);
}

.app-main {
  flex-grow: 1;
  padding: 20px;
  max-width: 1000px; /* Adjusted max-width */
  margin: 0 auto;
  width: 100%;
}

/* Base styles for containers/cards */
.card {
  background-color: var(--background-light);
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid var(--border-color);
}

h1, h2, h3, h4, h5, h6 {
  color: var(--primary-color); /* Headings use primary color */
  margin-top: 0;
  margin-bottom: 15px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

button {
  background-color: var(--primary-color);
  color: var(--secondary-color);
  border: none;
  padding: 10px 18px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease, transform 0.2s ease;
  font-family: 'Roboto Mono', monospace;
  font-weight: bold;
}

button:hover {
  background-color: var(--accent-color); /* Accent color on hover */
  transform: translateY(-2px);
}
</style>
