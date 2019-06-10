import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    boardfen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', // Starting position FEN
    loading: true,
    loadingText: "Connecting to chessboard..."
  },
  mutations: {
    setFen (state, newFen) {
      state.boardfen = newFen
    },
    setLoading (state, newLoading) {
      state.loading = newLoading.loading
      state.loadingText = newLoading.text
    },
    SOCKET_CONNECT(state) {
      state.connected = true
    },
    SOCKET_DISCONNECT(state) {
      state.connected = false;
    },
     SOCKET_ERROR(state, message) {
      state.error = message.error
    },
  },
})
