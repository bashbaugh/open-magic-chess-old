<template>
  <div id="app">
    <NavBar />
    <Connection />
    <keep-alive include="home">
      <router-view/>
    </keep-alive>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import Connection from '@/components/Connection.vue'

export default {
  name: 'app',
  components: {
    NavBar,
    Connection
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
