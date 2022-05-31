<script setup lang="ts">
import SearchBar from '@/components/SearchBar.vue';
import WaveLayout from '../components/WaveLayout.vue';
</script>

<template>
  <WaveLayout>
    <div class="content flex align-items-center justify-content-center">
      <div class="panel flex flex-column align-items-center">
        <div class="logo flex align-items-center">
          <img class="image" src="@/assets/justice.png" />
          <div class="text">Case Lookup</div>
        </div>
        <SearchBar :with-button="true" />
      </div>
    </div>

    <template v-slot:footer>
      <div class="foot">
        搜索引擎技术基础 &nbsp;&nbsp; | &nbsp;&nbsp; 周天泽&nbsp; 王通泽
      </div>
    </template>
  </WaveLayout>
</template>

<style scoped lang="scss">
.content {
  min-height: 80vh;
}
.panel {
  margin: auto;
  padding: 2rem;
  padding-bottom: 2.5rem;
  width: fit-content;
  background-color: rgba(255, 255, 255, 0.5);
  // backdrop-filter: blur(2px);
  border-radius: 1.5rem;
  // box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}

.logo {
  margin-bottom: 2.5rem;
  .image {
    width: 10vw;
    margin-right: 1rem;
  }
  .text {
    font-size: 3rem;
    font-weight: bold;
    font-family: Verdana;
    color: #494a4c;
  }
}

:deep(.searchbar) {
  width: 65vh;
}

.foot {
  width: fit-content;
  margin: auto;
  margin-top: 1rem;
  text-align: center;
  color: #aeb1b6;
}
</style>
