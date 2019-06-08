<template>
  <el-menu default-active="1" class="el-menu" mode="horizontal">
    <el-menu-item index="1">
      <router-link to='/'><div class="ml">Home</div></router-link>
    </el-menu-item>
    <el-menu-item index="2">
      <router-link to='/new'><div class="ml">New Game</div></router-link>
    </el-menu-item>
    <el-submenu index="3">
      <template slot="title">Games</template>
      <el-menu-item index="3-1">item one</el-menu-item>
      <el-menu-item index="3-2">item two</el-menu-item>
      <el-menu-item index="3-3">item three</el-menu-item>
      <el-submenu index="3-4">
        <template slot="title">item four</template>
        <el-menu-item index="3-4-1">item one</el-menu-item>
        <el-menu-item index="3-4-2">item two</el-menu-item>
        <el-menu-item index="3-4-3">item three</el-menu-item>
      </el-submenu>
    </el-submenu>
    <el-menu-item index="4" class="fright">
      <router-link to='/about'><div class="ml fright">About</div></router-link>
    </el-menu-item>
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