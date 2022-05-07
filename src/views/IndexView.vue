<template>
  <div>
    <h1>JdLogin</h1>
    <p>使用VNC登录jd，部署cookie到qinglong。</p>
    <p>登录成功后并不会展示cookie。</p>
    <p>自用系统，运行在腾讯云江苏轻量。</p>
    <van-button type="primary" @click="createJdLoginTask">开始登录</van-button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  methods: {
    createJdLoginTask() {
      axios.post("/api/create").then((response) => {
        this.$router.push({ path: "/login/" + response.data.task });
      });
    },
  },
};
</script>

<style>
</style>