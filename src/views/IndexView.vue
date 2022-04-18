<template>
  <div>
    <van-button @click="createJdLoginTask">开始</van-button>
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