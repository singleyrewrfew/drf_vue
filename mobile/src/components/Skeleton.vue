<template>
    <div class="skeleton-wrapper">
        <div v-if="type === 'card'" class="skeleton-card">
            <div class="skeleton skeleton-title"></div>
            <div class="skeleton skeleton-text"></div>
            <div class="skeleton skeleton-text" style="width: 85%;"></div>
            <div class="skeleton skeleton-meta"></div>
        </div>

        <div v-else-if="type === 'card-image'" class="skeleton-card">
            <div class="skeleton skeleton-title"></div>
            <div class="skeleton skeleton-text"></div>
            <div class="skeleton skeleton-image"></div>
            <div class="skeleton skeleton-meta"></div>
        </div>

        <div v-else-if="type === 'avatar'" class="skeleton-avatar-row">
            <div class="skeleton skeleton-avatar"></div>
            <div class="skeleton-avatar-info">
                <div class="skeleton skeleton-name"></div>
                <div class="skeleton skeleton-desc"></div>
            </div>
        </div>

        <div v-else-if="type === 'article'" class="skeleton-article">
            <div class="skeleton skeleton-article-title"></div>
            <div class="skeleton-article-meta">
                <div class="skeleton skeleton-avatar-sm"></div>
                <div class="skeleton skeleton-author"></div>
            </div>
            <div class="skeleton skeleton-image-lg"></div>
            <div class="skeleton skeleton-text"></div>
            <div class="skeleton skeleton-text" style="width: 90%;"></div>
            <div class="skeleton skeleton-text" style="width: 75%;"></div>
        </div>

        <div v-else-if="type === 'list'" class="skeleton-list-item">
            <div class="skeleton skeleton-list-icon"></div>
            <div class="skeleton-list-content">
                <div class="skeleton skeleton-list-title"></div>
                <div class="skeleton skeleton-list-desc"></div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    type: {
        type: String,
        default: 'card',
        validator: (v) => ['card', 'card-image', 'avatar', 'article', 'list'].includes(v)
    }
})
</script>

<style scoped>
.skeleton-wrapper {
    width: 100%;
}

.skeleton {
    background: linear-gradient(
        90deg,
        #f0f0f0 25%,
        #e0e0e0 37%,
        #f0f0f0 63%
    );
    background-size: 400% 100%;
    animation: skeleton-loading 1.4s ease infinite;
    border-radius: var(--radius-sm);
}

:global(.dark) .skeleton,
:global([data-theme="dark"]) .skeleton {
    background: linear-gradient(
        90deg,
        #2a2a2a 25%,
        #3a3a3a 37%,
        #2a2a2a 63%
    );
    background-size: 400% 100%;
}

@keyframes skeleton-loading {
    0% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0 50%;
    }
}

.skeleton-card {
    padding: 16px;
    background: var(--card-bg);
}

.skeleton-title {
    height: 20px;
    width: 75%;
    margin-bottom: 12px;
}

.skeleton-text {
    height: 14px;
    margin-bottom: 8px;
}

.skeleton-meta {
    height: 12px;
    width: 50%;
    margin-top: 12px;
}

.skeleton-image {
    height: 120px;
    width: 100%;
    margin: 12px 0;
    border-radius: var(--radius-md);
}

.skeleton-avatar-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    background: var(--card-bg);
}

.skeleton-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    flex-shrink: 0;
}

.skeleton-avatar-info {
    flex: 1;
}

.skeleton-name {
    height: 16px;
    width: 100px;
    margin-bottom: 8px;
}

.skeleton-desc {
    height: 12px;
    width: 160px;
}

.skeleton-article {
    padding: 16px;
    background: var(--card-bg);
}

.skeleton-article-title {
    height: 24px;
    width: 85%;
    margin-bottom: 16px;
}

.skeleton-article-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
}

.skeleton-avatar-sm {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}

.skeleton-author {
    height: 14px;
    width: 80px;
}

.skeleton-image-lg {
    height: 180px;
    width: 100%;
    margin-bottom: 16px;
    border-radius: var(--radius-md);
}

.skeleton-list-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    background: var(--card-bg);
}

.skeleton-list-icon {
    width: 40px;
    height: 40px;
    border-radius: var(--radius-md);
    flex-shrink: 0;
}

.skeleton-list-content {
    flex: 1;
}

.skeleton-list-title {
    height: 16px;
    width: 70%;
    margin-bottom: 8px;
}

.skeleton-list-desc {
    height: 12px;
    width: 50%;
}
</style>
