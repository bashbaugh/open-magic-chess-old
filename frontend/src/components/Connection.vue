<template>
  <div>
    
  </div>
</template>

<script>
  export default {
    name: 'Connection',
    mounted () {
      this.$store.commit('setLoading', {loading: true, text: "Connecting to chessboard..."})
      
    }
  }
</script>