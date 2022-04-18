<template>
  <div>
    <h1>JdLogin</h1>
    <p>STATUS: {{ status }}</p>
    <van-cell-group inset>
      <van-field
        v-model="sendkeys"
        center
        clearable
        label="输入"
        placeholder="向服务器输入文本"
      >
        <template #button>
          <van-button size="small" type="primary" @click="handleSendKey"
            >提交</van-button
          >
        </template>
      </van-field>
    </van-cell-group>
    <div v-if="running">
      <iframe
        class="vncbox"
        :src="`/vnc/?scale=1&path=websockify/?token=${this.task}&password=${this.task}`"
        frameborder="0"
      ></iframe>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      task: null,
      status: null,
      running: null,
      showVnc: false,
      sendkeys: null,
    };
  },
  mounted() {
    this.task = this.$route.params.task;
    setInterval(() => {
      axios.get("/api/status?task=" + this.task).then((response) => {
        let data = response.data;
        this.status = data.status;
        this.running = data.running;
      });
    }, 1000);
  },
  methods: {
    handleSendKey() {
      if (this.sendkeys === null) {
        return;
      }
      axios
        .post("/api/sendkeys", {
          task: this.task,
          keys: this.sendkeys,
        })
        .then((response) => {
            console.log(response.data)
          this.sendkeys = null;
        });
    },
  },
};
</script>

<style>
.vncbox {
  width: 400px;
  height: 400px;
  margin: 0 auto;
}
</style>