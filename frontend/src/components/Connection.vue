<template>
  <div>
    
  </div>
</template>

<script>
  export default {
    name: 'Connection',
    mounted: function () {
      this.sockets.subscribe('GAME', (data) => {
        this.$notify({title: "Game channel"})
      })
      this.sockets.subscribe('CHESS', (data) => {
        this.$notify({title: "Chess channel"})
      })
      this.sockets.subscribe('NOTIFICATION', data => {
        this.$notify({title: "Notification", message: data.message});
      })
    }
  }
</script>