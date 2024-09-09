<template>
    <div class="container">
        <h1>To-Do List</h1>
        <div>
            <div>
                <TodoNew @new-todo="addNewTodo" />
                <TodoList @toggle-todo="toggleTodo" @delete-todo="deleteTodo" :todos="todos" />
            </div>
        </div>
        <img src="@/assets/logo.svg" class="vue-logo" alt="Vue.js Logo" />
    </div>
</template>
<script lang="ts">
import TodoNew from "@/components/TodoNew.vue";
import TodoList from "@/components/TodoList.vue";
import { addNewTodoItem, deleteTodoItem, getTodoItems, toggleTodoItem, type TodoItem } from "@/utils/api";

export default {
    components: {
        TodoNew,
        TodoList
    },
    methods: {
        addNewTodo: async function (name: string): Promise<void> {
            await addNewTodoItem(name);
            await this.refetchTodos();
        },
        toggleTodo: async function (id: number) {
            await toggleTodoItem(id);
            await this.refetchTodos();
        },
        deleteTodo: async function (id: number) {
            await deleteTodoItem(id);
            await this.refetchTodos();
        },
        refetchTodos: async function () {
            this.todos = (await getTodoItems()).sort((a, b) => a.id - b.id);
        }
    },
    data() {
        return {
            todos: [] as ReadonlyArray<TodoItem>
        };
    },
    beforeMount() {
        this.refetchTodos();
    }
};
</script>

<style scoped>
.container {
    width: 24rem;
    margin: auto;
    background-color: white;
    border-radius: 1rem;
    padding: 1rem;
    box-shadow: 0 0 1rem rgba(0, 0, 0, 0.5);
}

h1 {
    text-align: center;
    margin-top: 0;
}

.vue-logo {
    display: block;
    width: 50px;
    margin: 0 auto;
}
</style>