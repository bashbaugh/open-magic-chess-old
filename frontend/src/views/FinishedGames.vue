<template>
  <div
    v-loading="$store.state.loading"
    element-loading-background="rgba(255, 255, 255, 0.6)"
    :element-loading-text="$store.state.loadingText" >
    <h2>Finished Games</h2>
  </div>
</template>

<script>

  export default {
    name: 'FinishedGames',
    data () {
      return {

      }
    },
  }
</script>