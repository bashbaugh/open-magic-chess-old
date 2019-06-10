<template>
  <div
    v-loading="$store.state.loading"
    element-loading-background="rgba(255, 255, 255, 0.6)"
    :element-loading-text="$store.state.loadingText" >
    <h2>Games</h2>
  </div>
</template>

<script>

export default {
  name: 'Games',
  data () {
    return {
      
    }
  },
}
</script>