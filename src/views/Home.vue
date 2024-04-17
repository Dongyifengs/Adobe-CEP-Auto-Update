<template>
  <div class="home">
    <el-descriptions class="margin-top" :column="3" border v-if="showDescriptions">
      <el-descriptions-item>
        <template slot="label">
          <i class="el-icon-user"></i>
          更新主题
        </template>
        {{ cepName }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label">
          <i class="el-icon-document"></i>
          当前版本号
        </template>
        v.{{ version }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label">
          <i class="el-icon-document-add"></i>
          最新版本
        </template>
        v.{{ newVersion }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label">
          <i class="el-icon-cpu"></i>
          更新类型
        </template>
        <el-tag :size="tagType" effect="dark">
          {{ updateTypeText }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label">
          <i class="el-icon-collection"></i>
          更新日志
        </template>
        <div>更新时间:{{ updateTime }}</div>
        {{ updateText }}
      </el-descriptions-item>
    </el-descriptions>
    <!-- 按钮现在受 showUpdateButton 控制是否显示 -->
    <el-button @click="checkUpdateDown" v-if="showUpdateButton">自动更新</el-button>

    <div class="test">
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
      当前显示的是0.3版本的代码页面
    </div>

  </div>
</template>


<script>
// 导入所需的模块和库
import {createReadStream, existsSync, renameSync, rmSync, writeFileSync} from "fs";
import {join} from "path";
import {Extract} from "unzipper";

export default {
  data() {
    return {
      cepName: '',
      version: 0.3,
      newVersion: null,
      updateTypeText: '',
      updateText: '',
      updateUrl: '',
      versionAllNum: null,
      updateTime: '',
      tagType: '',
      tagTypeNum: 1,
      showDescriptions: true,  // 控制描述组件的显示
      showUpdateButton: true,   // 控制更新按钮的显示
    }
  },
  methods: {
    async checkUpdate() {
      try {
        const responseGet = await fetch('http://localhost:3000/updateList');
        const latestUpdateGet = await responseGet.json();
        const versionAllNum = latestUpdateGet.length;
        const response = await fetch(`http://localhost:3000/updateList?id=${versionAllNum}`);
        const latestUpdate = await response.json();
        // 定义一个更新状态信息的函数
        const updateState = (update, isLatestVersion = false, isPreview = false) => {
          const baseState = {
            cepName: update.name,
            newVersion: update.newVersion,
            updateText: update.updateText,
            updateUrl: update.updateUrl,
            updateTime: update.updateTime,
            showUpdateButton: false, // 默认隐藏更新按钮
          };

          if (isLatestVersion) {
            return {...baseState, updateTypeText: '最新版', updateTypeNum: 1};
          } else if (isPreview) {
            return {...baseState, cepName: "开发预览版", updateTypeText: "开发预览版", updateTypeNum: 2};
          } else {
            return {
              ...baseState,
              updateTypeText: update.updateTypeText,
              updateTypeNum: update.updateType,
              showUpdateButton: true
            };
          }
        };

        // 根据版本比较结果更新状态
        if (latestUpdate[0].newVersion === this.version) {
          console.log('当前已是最新版本。');
          Object.assign(this, updateState(latestUpdate[0], true));
          setTimeout(() => this.showDescriptions = false, 5000);  // 5秒后隐藏描述组件
        } else if (latestUpdate[0].newVersion < this.version) {
          Object.assign(this, updateState(latestUpdate[0], false, true));
        } else {
          console.log('有新版本可用！');
          Object.assign(this, updateState(latestUpdate[0]));
          this.updateTagType();
        }

      } catch (error) {
        console.error('更新检查失败：', error);
      }
    },

    // Tag判断颜色
    updateTagType() {
      const tagTypes = {1: '', 2: 'success', 3: 'info', 4: 'danger', 5: 'warning'};
      this.tagType = tagTypes[this.updateTypeNum] || '';
    },

    // 方法：下载并解压更新文件
    async downloadAndExtractUpdate() {
      // 下载更新文件并保存到本地
      const result = (await (await fetch(this.updateUrl)).body.getReader().read()).value;
      const updateZipFilePath = join(__dirname, "update.zip");
      this.removeIfExists(updateZipFilePath);
      // 创建临时目录并解压更新文件
      const updateTmpPath = join(__dirname, "tmp");
      this.removeIfExists(updateTmpPath, {recursive: true, force: true});
      writeFileSync(updateZipFilePath, result);
      createReadStream(updateZipFilePath)
          .pipe(Extract({path: updateTmpPath}))
          .on("close", () => this.replaceFile(updateTmpPath));
    },

    // 方法：点击按钮时检查更新并执行下载更新
    checkUpdateDown() {
      if (this.updateUrl) {
        this.downloadAndExtractUpdate();
      } else {
        console.log('无有效的更新链接。');
      }
    },

    // 方法：如果文件存在则删除
    removeIfExists(path, options = {}) {
      if (existsSync(path)) {
        rmSync(path, options);
      }
    },

    // 方法：替换文件
    replaceFile(updateTmpPath) {
      const replaceFilePath = join(__dirname, "src", "views", "Home.vue");
      this.removeIfExists(replaceFilePath);
      const targetFilePath = join(updateTmpPath, "Home.vue");
      renameSync(targetFilePath, replaceFilePath);
      this.$message('更新完成，请重启扩展');
    }
  },
  // 生命周期函数：组件挂载后执行检查更新方法
  mounted() {
    this.checkUpdate();
  }
}
</script>

<style>
.margin-top {
  margin-top: 20px;
}
</style>
