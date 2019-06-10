import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    loading: true,
    loadingText: "Connecting to chessboard...",
  },
  mutations: {
    setFen (state, newFen) {
      state.boardfen = newFen
    },
    setLoading (state, newLoading) {
      state.loading = newLoading.loading
      state.loadingText = newLoading.text
    },
  },
})
