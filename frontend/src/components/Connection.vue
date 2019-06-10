<script>
  export default {
    name: 'Connection',
    data () {
      return {

      }
    },
    sockets: {
      connect () {
        this.$notify({title: "Connection established", duration: 8000,})
        this.$store.commit('setLoading', {loading: false, text: ""})
      },
      disconnect () {
        this.$notify({title: "Connection lost",})
        this.$store.commit('setLoading', {loading: true, text: "Connection lost. Reconnecting..."})
      },
      error (message) {
        this.$notify({title: "Connection error", message: message.error}) // I can't figure out how to get the error message.
      },
      // THE GAMEUPDATE channel is used for updates about the current game, e.g. moves
      GAMEUPDATE (message) {
        console.log(message)
      },
      // The DATA channel is used to transfer other data, such as previous games
      DATA (message) {
        console.log(message)
      },
      // The NOTIFICATIONS channel is used by the board to send notifications to the app user
      NOTIFICATION (message) {
        this.$notify({title: "Notification", duration: 0, message})
      }
    },
    mounted () {

    }
  }
</script>