import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' // Starting position FEN
  },
  mutations: {
    setFen (state, newFen) {
      state.fen = newFen
    }
  },
  actions: {

  }
})
