<template>
  <div>
    <p>{{ status }}</p>
    <p>{{ running }}</p>
    <div>
      <iframe class="vncbox"
        :src="`/vnc/vnc_lite.html?scaleViewport=1&path=websockify/?token=${this.task}&password=${this.task}`"
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
    };
  },
  mounted() {
    this.task = this.$route.params.task;
    setInterval(() => {
      axios
        .get("/api/status?task=" + this.task)
        .then((response) => {
          let data = response.data;
          this.status = data.status;
          this.running = data.running;
        });
    }, 1000);
  },
};
</script>

<style>
.vncbox{
    width: 100%;
    height: 660px;
}
</style>