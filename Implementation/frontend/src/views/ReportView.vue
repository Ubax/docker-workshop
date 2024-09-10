<template>
    <div class="container">
        <h1>Report</h1>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Q1</th>
                    <th>Q2</th>
                    <th>Q3</th>
                    <th>Q4</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="row in rows" :key="row.name">
                    <td>{{ row.name }}</td>
                    <td>{{ row.q1 }}</td>
                    <td>{{ row.q2 }}</td>
                    <td>{{ row.q3 }}</td>
                    <td>{{ row.q4 }}</td>
                </tr>
            </tbody>
        </table>
        <img src="@/assets/logo.svg" class="vue-logo" alt="Vue.js Logo" />
    </div>
</template>
<script lang="ts">
import { getReportItems, type ReportItem } from "@/utils/api";

export default {
    data() {
        return {
            rows: [] as ReportItem[]
        };
    },
    methods: {
        async refetchReport() {
            this.rows = await getReportItems();
        }
    },
    beforeMount() {
        this.refetchReport()
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

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

thead th {
    background-color: #f4f4f4;
    padding: 0.75rem;
    text-align: left;
    border-bottom: 2px solid #ddd;
    color: #333;
    font-weight: bold;
}

tbody tr:nth-child(even) {
    background-color: #f9f9f9;
}

tbody tr:hover {
    background-color: #f1f1f1;
}

td {
    padding: 0.75rem;
    border-bottom: 1px solid #ddd;
    text-align: left;
    color: #555;
}
</style>