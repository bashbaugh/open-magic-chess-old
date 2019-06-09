<template>
  <div
    v-loading="$store.state.loading"
    element-loading-background="rgba(0, 0, 0, 0.5)"
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