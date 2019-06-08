<template>
  <el-menu :default-active="activeIndex" class="el-menu" mode="horizontal">
    <el-menu-item index="1">
      <router-link to='/'>Home</router-link>
    </el-menu-item>
    <el-menu-item index="2">
      <router-link to='/new'>New Game</router-link>
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
      <router-link to='/about'>About</router-link>
    </el-menu-item>
  </el-menu>
</template>

<style scoped>
  a {
    height: 100%;
    width: 100%;
  }
</style>