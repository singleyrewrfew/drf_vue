<template>
  <div class="auth-page">
    <div class="bg-animation">
      <div class="bg-gradient"></div>
      <div class="bg-shapes">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>

    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <div class="auth-logo">
            <span class="logo-icon">C</span>
          </div>
          <h2>{{ title }}</h2>
          <p>{{ subtitle }}</p>
        </div>

        <slot name="form"></slot>

        <div class="auth-divider">
          <span>或</span>
        </div>

        <SocialLogin />

        <div class="auth-footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import SocialLogin from './SocialLogin.vue'

defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: var(--bg-color);
  padding: 20px;
}

.bg-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}

.bg-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #0078d4 0%, #106ebe 50%, #005a9e 100%);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.bg-shapes {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.bg-shapes span {
  position: absolute;
  display: block;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite;
}

.bg-shapes span:nth-child(1) {
  width: 80px;
  height: 80px;
  left: 10%;
  top: 20%;
  animation-delay: 0s;
}

.bg-shapes span:nth-child(2) {
  width: 120px;
  height: 120px;
  left: 20%;
  bottom: 20%;
  animation-delay: 2s;
}

.bg-shapes span:nth-child(3) {
  width: 60px;
  height: 60px;
  left: 60%;
  top: 40%;
  animation-delay: 4s;
}

.bg-shapes span:nth-child(4) {
  width: 100px;
  height: 100px;
  right: 10%;
  top: 10%;
  animation-delay: 1s;
}

.bg-shapes span:nth-child(5) {
  width: 150px;
  height: 150px;
  right: 20%;
  bottom: 10%;
  animation-delay: 3s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) rotate(0deg);
    opacity: 0.5;
  }
  50% {
    transform: translateY(-40px) rotate(180deg);
    opacity: 1;
  }
}

.auth-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 360px;
  margin: 0 auto;
}

.auth-card {
  background: var(--card-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: var(--radius-md);
  padding: 24px 20px;
  border: 1px solid var(--border-color);
  box-shadow:
    0 20px 40px -12px rgba(0, 0, 0, 0.15),
    0 8px 16px -8px rgba(0, 0, 0, 0.08);
  animation: fadeInUp 0.2s ease-out;
  max-height: calc(100vh - 32px);
  max-height: calc(100dvh - 32px);
  overflow-y: auto;
  overscroll-behavior: contain;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.auth-card::-webkit-scrollbar {
  display: none;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.auth-header {
  text-align: center;
  margin-bottom: 20px;
}

.auth-logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
}

.logo-icon {
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark, #1e40af));
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 22px;
  font-weight: bold;
  box-shadow: 0 3px 10px rgba(var(--primary-rgb), 0.25);
}

.auth-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 5px;
  letter-spacing: -0.01em;
}

.auth-header p {
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.4;
}

.auth-form {
  margin-bottom: 16px;
}

.auth-form :deep(.el-form-item) {
  margin-bottom: 14px;
}

.auth-form :deep(.el-form-item:last-of-type) {
  margin-bottom: 12px;
}

.auth-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-primary);
  padding-bottom: 5px;
  font-size: 12px;
}

.auth-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-sm);
  padding: 2px 9px;
  box-shadow: none;
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
  background: var(--bg-primary);
}

.auth-form :deep(.el-input__wrapper:hover) {
  border-color: var(--border-dark);
  background: var(--bg-secondary);
}

.auth-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(var(--primary-rgb), 0.15);
  background: var(--card-bg);
}

.auth-form :deep(.el-input__inner) {
  height: 32px;
  line-height: 32px;
  font-size: 13px;
}

.auth-form :deep(.el-input__icon) {
  width: 15px;
  height: 15px;
  font-size: 15px;
}

.auth-divider {
  display: flex;
  align-items: center;
  margin: 16px 0;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-light);
}

.auth-divider span {
  padding: 0 12px;
  color: var(--text-tertiary);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.auth-footer {
  text-align: center;
  color: var(--text-secondary);
  font-size: 12px;
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
  line-height: 1.4;
}

.auth-footer .el-button {
  font-weight: 600;
  margin-left: 3px;
  font-size: 12px;
}

.submit-btn {
  width: 100%;
  height: 38px;
  font-size: 13px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  letter-spacing: 0.8px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(var(--primary-rgb), 0.3);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0) scale(0.98);
}

@media (max-width: 480px) {
  .auth-page {
    padding: 14px;
  }

  .auth-container {
    max-width: 100%;
  }

  .auth-card {
    padding: 20px 18px;
    border-radius: var(--radius-md);
  }

  .auth-header h2 {
    font-size: 19px;
  }

  .auth-header p {
    font-size: 11px;
  }

  .logo-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }

  .submit-btn {
    height: 36px;
    font-size: 13px;
  }

  .auth-form :deep(.el-form-item) {
    margin-bottom: 14px;
  }
}

@media (max-width: 375px) {
  .auth-page {
    padding: 10px;
  }

  .auth-card {
    padding: 18px 16px;
  }

  .auth-header {
    margin-bottom: 18px;
  }

  .auth-header h2 {
    font-size: 18px;
  }

  .logo-icon {
    width: 38px;
    height: 38px;
    font-size: 19px;
  }

  .submit-btn {
    height: 36px;
    font-size: 12px;
    letter-spacing: 0.5px;
  }

  .auth-form :deep(.el-input__inner) {
    font-size: 12px;
    height: 32px;
    line-height: 32px;
  }
}
</style>
