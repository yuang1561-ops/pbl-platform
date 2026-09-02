<template>
  <el-container class="layout">
    <!-- 移动端顶栏 -->
    <div class="mobile-topbar">
      <div class="m-logo">
        <div class="logo-icon-sm">PBL</div>
        <span class="m-title">PBL 导师工作台</span>
      </div>
      <el-button class="m-menu-btn" text @click="drawerOpen = true">
        <el-icon size="22"><Menu /></el-icon>
      </el-button>
    </div>

    <!-- 桌面侧边栏 -->
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <div class="logo-icon">PBL</div>
        <div class="logo-text">
          <div class="logo-title">导师工作台</div>
          <div class="logo-sub">浸思研学</div>
        </div>
      </div>
      <el-menu :default-active="$route.path" router class="menu">
        <el-menu-item index="/"><el-icon><HomeFilled /></el-icon>首页</el-menu-item>
        <el-menu-item index="/academy"><el-icon><Reading /></el-icon>培训学院</el-menu-item>
        <el-menu-item index="/knowledge"><el-icon><Search /></el-icon>知识库</el-menu-item>
        <el-menu-item index="/workshop"><el-icon><Tools /></el-icon>项目工坊</el-menu-item>
        <el-menu-item index="/templates"><el-icon><FolderOpened /></el-icon>项目库</el-menu-item>
      </el-menu>
      <div class="sidebar-footer">学习进度存于本机浏览器</div>
    </el-aside>

    <!-- 移动端抽屉菜单 -->
    <el-drawer v-model="drawerOpen" direction="ltr" size="240px" :with-header="false">
      <el-menu :default-active="$route.path" router @select="drawerOpen = false">
        <el-menu-item index="/"><el-icon><HomeFilled /></el-icon>首页</el-menu-item>
        <el-menu-item index="/academy"><el-icon><Reading /></el-icon>培训学院</el-menu-item>
        <el-menu-item index="/knowledge"><el-icon><Search /></el-icon>知识库</el-menu-item>
        <el-menu-item index="/workshop"><el-icon><Tools /></el-icon>项目工坊</el-menu-item>
        <el-menu-item index="/templates"><el-icon><FolderOpened /></el-icon>项目库</el-menu-item>
      </el-menu>
    </el-drawer>

    <el-main class="main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { HomeFilled, Reading, Search, Tools, FolderOpened, Menu } from '@element-plus/icons-vue'
const drawerOpen = ref(false)
</script>

<style>
body { margin: 0; background: #f5f7fa; font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; }
.layout { min-height: 100vh; }
.sidebar { background: #fff; border-right: 1px solid #e4e7ed; display: flex; flex-direction: column; position: fixed; top: 0; bottom: 0; left: 0; z-index: 10; }
.logo { display: flex; align-items: center; gap: 10px; padding: 20px 16px; border-bottom: 1px solid #f0f0f0; }
.logo-icon { width: 44px; height: 44px; border-radius: 10px; background: linear-gradient(135deg, #409eff, #7c5cff); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 15px; letter-spacing: 1px; }
.logo-title { font-weight: 700; font-size: 15px; }
.logo-sub { font-size: 12px; color: #909399; }
.menu { border-right: none; flex: 1; }
.sidebar-footer { padding: 14px 16px; font-size: 11px; color: #c0c4cc; border-top: 1px solid #f0f0f0; }
.main { margin-left: 220px; padding: 24px; }

/* 移动端顶栏默认隐藏 */
.mobile-topbar { display: none; }

/* 响应式：<768px 隐藏侧边栏，显示顶栏 */
@media (max-width: 768px) {
  .sidebar { display: none; }
  .main { margin-left: 0; padding: 10px 8px; }
  .mobile-topbar { display: flex; align-items: center; justify-content: space-between; background: #fff; padding: 10px 14px; border-bottom: 1px solid #e4e7ed; position: sticky; top: 0; z-index: 20; }
  .m-logo { display: flex; align-items: center; gap: 8px; }
  .logo-icon-sm { width: 30px; height: 30px; border-radius: 8px; background: linear-gradient(135deg, #409eff, #7c5cff); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; }
  .m-title { font-weight: 600; font-size: 15px; }
  .doc { padding: 20px 16px !important; }
}
</style>
