<template>
  <div class="home">
    <el-row
      v-loading="boardLoading"
      element-loading-background="rgba(255, 255, 255, 0.6)"
      :element-loading-text="loadingText" >
      <el-col :sm="12">
        <div id="board" >
          <chessboard
            :free="freeMoves"
            :orientation="boardOrientation"
            :showThreats="showPlays"
            :fen="boardfen"
            @onMove="onMove" />
            <el-radio v-model="boardOrientation" label="white">White at front</el-radio>
            <el-radio v-model="boardOrientation" label="black">Black at front</el-radio>
        </div>
      </el-col>
      <el-col :sm="12">
        <div id="controls">
          
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {chessboard} from 'vue-chessboard'
import 'vue-chessboard/dist/vue-chessboard.css'

export default {
  name: 'home',
  data () {
    return {
      boardOrientation: 'white',
      boardLoading: true,
      loadingText: "",
      freeMoves: false,
      showPlays: false,
      boardfen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    }
  },
  methods: {
    onMove () {
      
    }
  },
  created () {
    
  },
  components: {
    chessboard
  }
}
</script>

<style scoped>
  #board {
    margin: 20px;
  }
  #controls {
    height: 200px;
    background-color: gray;
  }
</style>
