<template>
  <router-view />

  <!-- 通用悬浮按钮组 -->
  <FloatingActions>
    <!-- 额外按钮插槽（由子页面填充） -->
    <template #extra>
      <slot name="floating-actions"></slot>
    </template>
  </FloatingActions>
</template>

<script setup>
import FloatingActions from '@/components/common/FloatingActions.vue'
</script>
