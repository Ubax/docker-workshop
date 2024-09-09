<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Todos</RouterLink>
      <RouterLink to="/report">Reports</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  height: 50px;
  width: 100%;
  background-color: #fff;
  position: fixed;
  top:0;
  left: 0;
  box-shadow: 0 0 1rem rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

nav {
  display: flex;
  gap: 1rem;
}
</style>