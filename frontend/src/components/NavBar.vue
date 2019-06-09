<template>
  <el-menu default-active="1" class="el-menu" mode="horizontal">
    <el-menu-item index="1">
      <router-link to='/'><div class="ml">Home</div></router-link>
    </el-menu-item>
    <el-submenu index="2">
      <template slot="title">Games</template>
      <el-menu-item index="2-1">
        <router-link to='/new'>
          <div class="ml">New Game</div>
        </router-link>
      </el-menu-item>
      <el-menu-item index="2-2">
        <router-link to='/current-games'>
          <div class="ml">In progress games</div>
        </router-link>
      </el-menu-item>
      <el-menu-item index="2-3">
        <router-link to='/finished-games'>
          <div class="ml">Finished games</div>
        </router-link>
      </el-menu-item>
    </el-submenu>
    <el-submenu index="3">
      <template slot="title">More</template>
      <el-menu-item index="3-1">
        <router-link to='/settings'>
          <div class="ml">Settings</div>
        </router-link>
      </el-menu-item>
      <el-menu-item index="3-2">
        <a href='https://github.com/scitronboy/open-magic-chess/issues/new' target="_blank">
          <div class="ml">Report an issue</div>
        </a>
      </el-menu-item>
      <el-menu-item index="3-3">
        <router-link to='/about'>
          <div class="ml">About</div>
        </router-link>
      </el-menu-item>
    </el-submenu>
  </el-menu>
</template>

<style scoped>
  .ml {
    height: 100%;
    width: 100%;
  }
  .fright {
    float: right;
  }
</style>