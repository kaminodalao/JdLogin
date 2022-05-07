<template>
  <div>
    <h1>JdLogin</h1>
    <p>STATUS: {{ status }}</p>
    <van-cell-group inset>
      <van-field
        v-model="sendkeys"
        center
        clearable
         readonly
        label="输入"
        placeholder="暂时无法使用,请使用电脑登录"
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
    <div v-if="success">
      <p>登录成功</p>
       <van-button size="small" type="primary" @click="handleDeploy"
            >部署到 qinglong 环境变量</van-button
          >
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Dialog } from "vant";
import { Notify } from "vant";

export default {
  data() {
    return {
      task: null,
      status: null,
      running: null,
      showVnc: false,
      sendkeys: null,
      success: false,
    };
  },
  mounted() {
    this.task = this.$route.params.task;
    const statusCheck = setInterval(() => {
      axios.get("/api/status?task=" + this.task).then((response) => {
        let data = response.data;
        this.status = data.status;
        this.running = data.running;
        if (data.running === 0) {
          clearInterval(statusCheck);
          if (data.status === "LOGIN_FINISHED") {
            this.success = true;
            Dialog.confirm({
              title: "登陆成功",
              message: "是否部署到 qinglong 环境变量",
            })
              .then(() => {
                this.handleDeploy();
              })
              .catch(() => {});
          }
        }
      });
    }, 1000);
  },
  methods: {
    handleDeploy() {
      axios
        .post("/api/deploy", {
          task: this.task,
        })
        .then((r) => {
          Notify({ type: "success", message: "成功" });
        })
        .catch((e) => {
          Notify({ type: "danger", message: "失败" });
        });
    },
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
          console.log(response.data);
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