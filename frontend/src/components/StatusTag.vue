<template>
  <span class="status-tag" :class="`status-tag--${type}`">
    <slot>{{ text }}</slot>
  </span>
</template>

<script setup>
defineProps({
    type: {
        type: String,
        default: 'default',
        validator: (value) => ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value)
    },
    text: {
        type: String,
        default: ''
    }
})
</script>

<style scoped>
.status-tag {
    display: inline-flex;
    align-items: center;
    padding: 2px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    line-height: 1.8;
    white-space: nowrap;
    transition:
        background-color 0.2s ease,
        color 0.2s ease,
        border-color 0.2s ease;
}

/* ---- default ---- */
.status-tag--default {
    background: var(--tag-bg-default, rgba(128, 128, 128, 0.12));
    color: var(--text-secondary);
}
.status-tag--default:hover {
    background: var(--tag-bg-default-hover, rgba(128, 128, 128, 0.2));
}

/* ---- primary ---- */
.status-tag--primary {
    background: var(--tag-bg-primary, rgba(64, 158, 255, 0.12));
    color: var(--primary-color);
}
.status-tag--primary:hover {
    background: var(--tag-bg-primary-hover, rgba(64, 158, 255, 0.2));
}

/* ---- success ---- */
.status-tag--success {
    background: var(--tag-bg-success, rgba(103, 194, 58, 0.12));
    color: var(--success-color);
}
.status-tag--success:hover {
    background: var(--tag-bg-success-hover, rgba(103, 194, 58, 0.2));
}

/* ---- warning ---- */
.status-tag--warning {
    background: var(--tag-bg-warning, rgba(230, 162, 60, 0.12));
    color: var(--warning-color);
}
.status-tag--warning:hover {
    background: var(--tag-bg-warning-hover, rgba(230, 162, 60, 0.2));
}

/* ---- danger ---- */
.status-tag--danger {
    background: var(--tag-bg-danger, rgba(245, 108, 108, 0.12));
    color: var(--danger-color);
}
.status-tag--danger:hover {
    background: var(--tag-bg-danger-hover, rgba(245, 108, 108, 0.2));
}

/* ---- info ---- */
.status-tag--info {
    background: var(--tag-bg-info, rgba(144, 147, 153, 0.12));
    color: var(--info-color);
}
.status-tag--info:hover {
    background: var(--tag-bg-info-hover, rgba(144, 147, 153, 0.2));
}
</style>
