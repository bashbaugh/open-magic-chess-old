<template>
  <div>
  <el-dialog
    class="new-dialog"
    :visible="true"
    title="Create New Game"
    width="50%"
    :before-close="() => $router.push('/')" >
    <div
      v-loading="$store.state.loading"
      element-loading-background="rgba(0, 0, 0, 0.2)"
      :element-loading-text="$store.state.loadingText" >
      <el-select v-model="gameType" placeholder="Select game type">
        <el-option
          key="0"
          label="Player vs board"
          value="0" />
        <el-option
          key="1"
          label="Player vs player"
          value="1"/>
        <el-option
          key="2"
          label="Board vs board"
          value="2" />
      </el-select>
    </div>
    <span slot="footer" class="dialog-footer">
      <el-button @click="$router.push('/')">Cancel</el-button>
      <el-button type="success" @click="startGame" :disabled.sync="$store.state.loading">Start new game</el-button>
    </span>
  </el-dialog>
  </div>
</template>

<script>

export default {
  name: 'NewGame',
  data () {
    return {
      gameType: null,
    }
  },
  methods: {
    startGame () {
      
    }
  },
}
</script>