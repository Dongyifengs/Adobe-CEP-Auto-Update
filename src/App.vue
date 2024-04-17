<template>
  <div id="app">
    <Panel>
      <router-view/>
    </Panel>
    <Menus refresh debug/>
  </div>
</template>

<script>
import {Menus, Panel} from "lokney";

export default {
  name: "App",
  components: {
    Menus,
    Panel,
  },
  async mounted() {
  },
  methods: {
    getCSS(prop) {
      return window
          .getComputedStyle(document.documentElement)
          .getPropertyValue(`${/^\-\-/.test(prop) ? prop : "--" + prop}`);
    },
    setCSS(prop, data) {
      document.documentElement.style.setProperty(
          `${/^\-\-/.test(prop) ? prop : "--" + prop}`,
          data
      );
    },
  },
};
</script>

<style>
#nav {
  padding: 10px;
  display: flex;
  justify-content: center;
  color: var(--color-default);
}

#nav a {
  padding: 0px 5px;
  font-weight: bold;
  color: var(--color-default);
}

#nav a.router-link-exact-active {
  color: var(--color-selection);
}
</style>
