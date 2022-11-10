<template>
  <v-app>
    <notifications :max="3" :width="300" position="top center" />
    <MenuBar>
      <!-- -->
    </MenuBar>
    <v-main>
      <router-view class="content">
        <!-- -->
      </router-view>
    </v-main>
  </v-app>
</template>

<script>
import MenuBar from "./components/MenuBar";

export default {
  name: "App",
  components: { MenuBar },
};
</script>
