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
      <el-select v-model="value" placeholder="Select game type">
        <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value">
        </el-option>
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
      
    }
  },
  methods: {
    startGame () {
      
    }
  },
}
</script>