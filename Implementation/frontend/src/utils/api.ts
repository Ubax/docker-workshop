import axios from 'axios'

export interface TodoItem {
  id: number
  name: string
  done: boolean
}

export interface ReportItem {
  name: string
  q1: number
  q2: number
  q3: number
  q4: number
}

const axiosInstance = axios.create({})

export async function addNewTodoItem(name: string): Promise<void> {
  await axiosInstance.post('/api/item', { name }).then((response) => response.data)
}

export function getTodoItems(): Promise<TodoItem[]> {
  return axiosInstance.get('/api/item').then((response) => response.data)
}

export async function toggleTodoItem(id: number) {
  await axiosInstance.post(`/api/item/toggle/${id}`).then((response) => response.data)
}

export async function deleteTodoItem(id: number) {
  await axiosInstance.delete(`/api/item/${id}`).then((response) => response.data)
}

export function getReportItems(): Promise<ReportItem[]> {
  return axiosInstance.get('/api/report').then((response) => response.data)
}