<template>
  <div class="home">
    <!-- 使用 Element UI 的描述组件 -->
    <el-descriptions class="margin-top" :column="3" border>
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
    <el-button @click="checkUpdateDown"></el-button>
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
      // 数据属性：更新扩展主题
      cepName: '',
      // 数据属性：当前扩展版本号
      version: 0.1,
      // 数据属性：最新扩展版本号
      newVersion: null,
      // 数据属性：扩展更新类型
      updateTypeText: '',
      // 数据属性：扩展更新日志
      updateText: '',
      // 数据属性：扩展更新链接
      updateUrl: '',
      // 所有版本数
      versionAllNum: null,
      // 更新时间
      updateTime: '',
      // tagType默认颜色
      tagType: '',
      tagTypeNum: 1
    }
  },
  methods: {
    // 方法：检查更新 - 启动检查
    async checkUpdate() {
      try {
        // 发起 HTTP 请求获取最新更新所有信息
        const responseGet = await fetch('http://localhost:3000/updateList');
        // 解析 JSON 格式的响应
        const latestUpdateGet = await responseGet.json();
        const versionAllNum = latestUpdateGet.length;
        // 发起 HTTP 请求获取最新更新信息
        const response = await fetch(`http://localhost:3000/updateList?id=${versionAllNum}`);
        const latestUpdate = await response.json();
        // 检查是否有新版本可用
        if (latestUpdate[0].newVersion <= this.version) {
          console.log('当前已是最新版本。');
          return;
        }
        // 更新数据属性为最新的更新信息
        Object.assign(this, {
          cepName: latestUpdate[0].name,
          newVersion: latestUpdate[0].newVersion,
          updateTypeText: latestUpdate[0].updateTypeText,
          updateText: latestUpdate[0].updateText,
          updateUrl: latestUpdate[0].updateUrl,
          updateTime: latestUpdate[0].updateTime,
          updateTypeNum: latestUpdate[0].updateType
        });
        this.updateTagType()
        console.log('有新版本可用！');
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
