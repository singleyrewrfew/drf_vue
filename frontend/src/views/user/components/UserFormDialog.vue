<template>
    <FormDialog
        v-model="form"
        :show="dialogVisible"
        @update:show="(val) => emit('update:dialogVisible', val)"
        :is-edit="isEdit"
        create-title="新建用户"
        edit-title="编辑用户"
        width="600px"
        label-width="100px"
        :rules="rules"
        :loading="submitLoading"
        @submit="handleSubmit"
    >
        <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="请输入用户名" :disabled="isEdit" maxlength="150"/>
        </el-form-item>
        <el-form-item v-if="!isEdit" label="密码" prop="password">
            <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password maxlength="128"/>
        </el-form-item>
        <el-form-item v-if="!isEdit" label="确认密码" prop="password_confirm">
            <el-input v-model="form.password_confirm" type="password" placeholder="请确认密码" show-password maxlength="128"/>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
            <el-input v-model="form.email" placeholder="请输入邮箱"/>
        </el-form-item>
        <el-form-item label="角色" prop="role">
            <el-select v-model="form.role" placeholder="请选择角色" :disabled="isEditingSelf" style="width: 100%">
                <el-option v-for="role in roles" :key="role.id" :label="role.name" :value="role.id"/>
            </el-select>
            <div v-if="isEditingSelf" class="form-tip">不能修改自己的角色</div>
        </el-form-item>
        <el-form-item label="后台权限">
            <el-switch v-model="form.is_staff" active-text="允许" inactive-text="禁止"/>
            <div class="form-tip">允许访问后台管理系统</div>
        </el-form-item>
        <el-form-item label="状态">
            <el-switch v-model="form.is_active" active-text="启用" inactive-text="禁用" :disabled="isEditingSelf"/>
            <div v-if="isEditingSelf" class="form-tip">不能禁用自己的账号</div>
        </el-form-item>
    </FormDialog>
</template>

<script setup>
import {reactive, computed} from 'vue'
import {useUserStore} from '@/stores/user'
import FormDialog from '@/components/FormDialog.vue'

const props = defineProps({
    dialogVisible: {
        type: Boolean,
        required: true
    },
    submitLoading: {
        type: Boolean,
        default: false
    },
    isEdit: {
        type: Boolean,
        default: false
    },
    editingId: {
        type: [Number, String, null],
        default: null
    },
    roles: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits(['update:dialogVisible', 'submit', 'update:form'])

let form = reactive({
    username: '',
    password: '',
    password_confirm: '',
    email: '',
    role: null,
    is_staff: false,
    is_active: true,
})

const validatePassword = (rule, value, callback) => {
    if (!props.isEdit && !value) {
        callback(new Error('请输入密码'))
    } else if (value && value.length < 6) {
        callback(new Error('密码长度不能少于6位'))
    } else {
        callback()
    }
}

const validatePasswordConfirm = (rule, value, callback) => {
    if (!props.isEdit && !value) {
        callback(new Error('请确认密码'))
    } else if (value !== form.password) {
        callback(new Error('两次输入的密码不一致'))
    } else {
        callback()
    }
}

const rules = {
    username: [
        {required: true, message: '请输入用户名', trigger: 'blur'},
        {min: 3, max: 150, message: '用户名长度在 3 到 150 个字符', trigger: 'blur'},
    ],
    password: [{validator: validatePassword, trigger: 'blur'}],
    password_confirm: [{validator: validatePasswordConfirm, trigger: 'blur'}],
    email: [
        {type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur'},
    ],
    role: [{required: true, message: '请选择角色', trigger: 'change'}],
}

const userStore = useUserStore()
const isEditingSelf = computed(() => props.editingId === userStore?.user?.id)

const handleSubmit = () => {
    emit('submit', form)
}

const resetForm = () => {
    Object.assign(form, {
        username: '', password: '', password_confirm: '',
        email: '', role: null, is_staff: false, is_active: true,
    })
}

const fillForm = (row) => {
    Object.assign(form, {
        username: row.username,
        password: '',
        password_confirm: '',
        email: row.email,
        role: row.role,
        is_staff: row.is_staff,
        is_active: row.is_active,
    })
}

defineExpose({resetForm, fillForm, form})
</script>

<style scoped>
.form-tip {
    font-size: 12px;
    color: var(--text-tertiary);
    margin-top: 4px;
    line-height: 1.5;
    padding-left: 4px;
    display: flex;
    align-items: center;
}
</style>
