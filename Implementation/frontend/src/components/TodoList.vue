<template>
    <ul class="tasks">
        <li v-for="todo in todos" :key="todo.id" :class="{ completed: todo.done }" class="task"
            @click="toggleTodo(todo.id)">
            {{ todo.name }}
            <span class="delete" @click="deleteTodo(todo.id)">ⓧ</span>
        </li>
    </ul>
</template>

<script lang="ts">
import type { TodoItem } from '@/utils/api';
import type { PropType } from 'vue';

export default {
    props: {
        todos: Array as PropType<ReadonlyArray<TodoItem>>,
    },
    methods: {
        toggleTodo: function (id: number) {
            this.$emit('toggle-todo', id);
        },
        deleteTodo: function (id: number) {
            this.$emit('delete-todo', id);
        }
    },
    emits: ['toggle-todo', 'delete-todo']
};
</script>

<style>
.tasks {
    padding: 0;
    list-style-type: none;
}

.task {
    padding: 10px;
    margin-bottom: 0.5rem;
    border: 0.5px solid #999;
    border-radius: 5px;
    color: #34495e;
    font-weight: bold;
}

.task:before {
    content: "\2002";
}

.task:hover {
    cursor: pointer;
}

.completed {
    text-decoration: line-through;
    color: #41b883;
}

.completed:before {
    content: "\2714";
}

.delete {
    display: block;
    float: right;
    color: #d22;
    width: 1.25rem;
    height: 1.25rem;
    text-align: center;
}
</style>