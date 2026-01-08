<template>
  <div class="home-view-container">
    <div class="header-section">
      <h1>行程總覽</h1>
      <button @click="openAddModal" class="add-task-button">
        <i class="fas fa-plus-circle"></i> 新增行程
      </button>
    </div>

    <div class="content-grid">
      <div class="main-calendar-area card">
        <VCalendar
          class="integrated-calendar"
          :attributes="calendarAttributes"
          @update:from-page="fetchTasksForMonth"
          @dayclick="onDayClick"
          is-expanded
          locale="zh-TW"
        />
        <div class="selected-date-display" v-if="selectedDate">
          <h3>
            <i class="fas fa-calendar-alt"></i> {{ selectedDate.toLocaleDateString('zh-TW', { year: 'numeric', month: 'numeric', day: 'numeric', weekday: 'long' }) }}
          </h3>
        </div>
      </div>

      <div class="task-list-area">
        <div class="upcoming-tasks-card card">
          <h2><i class="fas fa-stream"></i> 今日與本週重要任務</h2>
          <ul v-if="sortedImportantTasks.length" class="task-list">
            <li v-for="task in sortedImportantTasks" :key="task.id"
                :class="['task-item', getPriorityClass(task.priority), { 'task-completed': task.completed }]">
              <div class="task-info">
                <span class="task-time">{{ formatTime(task.time) }}</span>
                <span class="task-date">{{ formatDate(task.date) }}</span>
                <span class="task-content">{{ task.content }}</span>
                <span class="task-priority">({{ getPriorityText(task.priority) }})</span>
              </div>
              <div class="task-actions">
                <button @click="editTask(task)" class="edit-button icon-button" title="編輯">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click="deleteTask(task.id)" class="delete-button icon-button" title="刪除">
                  <i class="fas fa-trash-alt"></i>
                </button>
                <button v-if="!task.completed" @click="toggleComplete(task)" class="complete-button icon-button" title="標記完成">
                  <i class="fas fa-check-circle"></i>
                </button>
                <button v-else @click="toggleComplete(task)" class="incomplete-button icon-button" title="取消完成">
                  <i class="fas fa-times-circle"></i>
                </button>
              </div>
            </li>
          </ul>
          <p v-else class="no-tasks-message">
            今日與本週沒有重要任務。
          </p>
        </div>

        <div class="selected-day-tasks-card card" v-if="selectedDayTasks.length > 0 && selectedDate">
          <h2><i class="fas fa-list-alt"></i> {{ selectedDate.toLocaleDateString('zh-TW', { month: 'numeric', day: 'numeric' }) }} 的詳細行程</h2>
          <ul class="task-list">
            <li v-for="task in selectedDayTasks" :key="task.id"
                :class="['task-item', getPriorityClass(task.priority), { 'task-completed': task.completed }]">
              <div class="task-info">
                <span class="task-time">{{ formatTime(task.time) }}</span>
                <span class="task-content">{{ task.content }}</span>
                <span class="task-priority">({{ getPriorityText(task.priority) }})</span>
              </div>
              <div class="task-actions">
                <button @click="editTask(task)" class="edit-button icon-button" title="編輯">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click="deleteTask(task.id)" class="delete-button icon-button" title="刪除">
                  <i class="fas fa-trash-alt"></i>
                </button>
                <button v-if="!task.completed" @click="toggleComplete(task)" class="complete-button icon-button" title="標記完成">
                  <i class="fas fa-check-circle"></i>
                </button>
                <button v-else @click="toggleComplete(task)" class="incomplete-button icon-button" title="取消完成">
                  <i class="fas fa-times-circle"></i>
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <AddEditModal
      :isVisible="showModal"
      :task="currentTask"
      @close="closeModal"
      @save="handleSaveTask"
    />
  </div>
</template>

<script>
import axios from 'axios';
import { Calendar } from 'v-calendar';
import 'v-calendar/dist/style.css';
import AddEditModal from '@/components/AddEditModal.vue';

export default {
  name: 'HomeView',
  components: {
    VCalendar: Calendar,
    AddEditModal,
  },
  data() {
    return {
      allTasks: [],
      todayTasks: [],
      weekTasks: [],
      selectedDate: new Date(),
      selectedDayTasks: [],
      showModal: false,
      currentTask: null,
    };
  },
  computed: {
    calendarAttributes() {
      return this.allTasks.map(task => ({
        key: task.id,
        dot: {
          color: this.getPriorityColor(task.priority),
          class: task.completed ? 'opacity-50' : '', // Dim completed tasks
        },
        popover: {
          label: `${this.formatTime(task.time)} ${this.getPriorityText(task.priority)} ${task.content}`,
        },
        dates: new Date(task.date),
      }));
    },
    sortedImportantTasks() {
      const importantTasks = [...this.todayTasks, ...this.weekTasks].filter((task, index, self) =>
        index === self.findIndex((t) => (
          t.id === task.id // Filter out duplicates if a task is both today and this week
        ))
      );

      // Sort by priority (1=High, 2=Medium, 3=Low), then by time, then by date
      return importantTasks.sort((a, b) => {
        if (a.priority !== b.priority) {
          return a.priority - b.priority;
        }
        if (a.time && b.time) {
          return a.time.localeCompare(b.time);
        }
        if (a.date && b.date) {
            return a.date.localeCompare(b.date);
        }
        return 0;
      });
    },
  },
  created() {
    this.fetchInitialTasks();
  },
  watch: {
    selectedDate: {
      handler(newDate) {
        this.filterTasksForSelectedDay(newDate);
      },
      immediate: true,
    },
    allTasks: {
      handler() {
        this.filterTasksForSelectedDay(this.selectedDate);
      },
      deep: true,
    }
  },
  methods: {
    async fetchInitialTasks() {
      await this.fetchTodayTasks();
      await this.fetchWeekTasks();
      // Fetch all tasks for the current month for calendar display
      this.fetchTasksForMonth({ month: new Date().getMonth() + 1, year: new Date().getFullYear() });
    },
    async fetchTasksForMonth(page) {
      const year = page.year;
      const month = String(page.month).padStart(2, '0');
      const startDate = `${year}-${month}-01`;
      const endDate = `${year}-${month}-${new Date(year, month, 0).getDate()}`;

      try {
        const response = await axios.get(`http://localhost:5000/todos?start_date=${startDate}&end_date=${endDate}`);
        this.allTasks = response.data;
      } catch (error) {
        console.error('Error fetching tasks for month:', error);
      }
    },
    async fetchTodayTasks() {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      const formattedDate = `${year}-${month}-${day}`;

      try {
        const response = await axios.get(`http://localhost:5000/todos?start_date=${formattedDate}&end_date=${formattedDate}`);
        this.todayTasks = response.data;
      } catch (error) {
        console.error('Error fetching today\'s tasks:', error);
      }
    },
    async fetchWeekTasks() {
      const today = new Date();
      const startOfWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - today.getDay());
      const endOfWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - today.getDay() + 6);

      const format = (date) => {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
      };

      const formattedStartOfWeek = format(startOfWeek);
      const formattedEndOfWeek = format(endOfWeek);

      try {
        const response = await axios.get(`http://localhost:5000/todos?start_date=${formattedStartOfWeek}&end_date=${formattedEndOfWeek}`);
        this.weekTasks = response.data;
      } catch (error) {
        console.error('Error fetching week\'s tasks:', error);
      }
    },
    onDayClick(day) {
      this.selectedDate = day.date;
    },
    filterTasksForSelectedDay(date) {
      if (!date) {
        this.selectedDayTasks = [];
        return;
      }
      const selectedDateISO = date.toISOString().split('T')[0];
      this.selectedDayTasks = this.allTasks.filter(
        task => task.date === selectedDateISO
      ).sort((a, b) => {
        if (!a.time && !b.time) return 0;
        if (!a.time) return 1;
        if (!b.time) return -1;
        return a.time.localeCompare(b.time);
      });
    },
    openAddModal() {
      this.currentTask = {
        date: this.selectedDate ? this.selectedDate.toISOString().split('T')[0] : new Date().toISOString().split('T')[0]
      };
      this.showModal = true;
    },
    editTask(task) {
      this.currentTask = { ...task, date: new Date(task.date), time: task.time ? task.time.substring(0, 5) : '' };
      this.showModal = true;
    },
    async handleSaveTask(task) {
      try {
        if (task.id) {
          const response = await axios.put(`http://localhost:5000/todos/${task.id}`, task);
          this.allTasks = this.allTasks.map(t => (t.id === task.id ? response.data : t));
        } else {
          const response = await axios.post('http://localhost:5000/todos', task);
          this.allTasks.push(response.data);
        }
        this.closeModal();
        this.fetchInitialTasks(); // Refresh all task lists
      } catch (error) {
        console.error('Error saving task:', error);
      }
    },
    async deleteTask(id) {
      if (confirm('確定要刪除此行程嗎？')) {
        try {
          await axios.delete(`http://localhost:5000/todos/${id}`);
          this.allTasks = this.allTasks.filter(task => task.id !== id);
          this.fetchInitialTasks(); // Refresh all task lists
        } catch (error) {
          console.error('Error deleting task:', error);
        }
      }
    },
    async toggleComplete(task) {
      try {
        const updatedTask = { ...task, completed: !task.completed };
        const response = await axios.put(`http://localhost:5000/todos/${task.id}`, updatedTask);
        this.allTasks = this.allTasks.map(t => (t.id === task.id ? response.data : t));
        this.fetchInitialTasks(); // Refresh all task lists
      } catch (error) {
        console.error('Error toggling task completion:', error);
      }
    },
    closeModal() {
      this.showModal = false;
      this.currentTask = null;
    },
    formatTime(time) {
      if (!time) return '全天';
      const [hour, minute] = time.split(':');
      return `${hour}:${minute}`;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-TW', { month: 'numeric', day: 'numeric' });
    },
    getPriorityText(priority) {
      switch (priority) {
        case 1: return '高';
        case 2: return '中';
        case 3: return '低';
        default: return '未知';
      }
    },
    getPriorityClass(priority) {
      switch (priority) {
        case 1: return 'priority-high';
        case 2: return 'priority-medium';
        case 3: return 'priority-low';
        default: return '';
      }
    },
    getPriorityColor(priority) {
      switch (priority) {
        case 1: return 'red';
        case 2: return 'orange';
        case 3: return 'green';
        default: return 'gray';
      }
    },
  },
};
</script>

<style scoped>
.home-view-container {
  padding: 20px;
  max-width: 1000px; /* Adjusted max-width */
  margin: 0 auto; /* Center the container */
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 20px;
}

.header-section h1 {
  margin: 0;
  font-size: 2.5em;
  color: var(--primary-color);
}

.add-task-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: var(--primary-color);
  color: var(--secondary-color);
  padding: 12px 20px;
  font-size: 1.1em;
}

.add-task-button:hover {
  background-color: var(--accent-color);
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}

@media (min-width: 992px) {
  .content-grid {
    grid-template-columns: 3fr 2fr; /* Calendar takes larger portion, tasks smaller */
  }
}

.main-calendar-area {
  min-height: 600px; /* Ensure calendar is large */
  display: flex;
  flex-direction: column;
}

.integrated-calendar {
  flex-grow: 1;
  /* V-Calendar specific overrides for tech theme */
  --vc-header-background: var(--background-light);
  --vc-nav-item-hover-bg: var(--background-dark);
  --vc-font-family: 'Roboto Mono', monospace;
  --vc-text-color: var(--text-light);
  --vc-border-color: var(--border-color);
  --vc-focus-ring: 0 0 0 3px rgba(var(--primary-color-rgb), 0.5);

  border-radius: 8px !important;
  font-family: 'Roboto Mono', monospace !important;
  color: var(--text-light) !important;
}

/* V-Calendar specific overrides for better styling */
.vc-container {
  border: none !important; /* Remove default border */
  background-color: var(--background-light) !important;
  color: var(--text-light) !important;
}

.vc-header {
  background-color: var(--background-light) !important;
  border-bottom: 1px solid var(--border-color) !important;
}

.vc-title {
  color: var(--primary-color) !important;
  font-weight: bold !important;
}

.vc-arrow {
  color: var(--accent-color) !important;
}

.vc-weeks {
  padding: 10px 0 !important;
}

.vc-day {
  border-radius: 5px !important;
}

.vc-day-content {
  font-weight: normal !important;
  color: var(--text-light) !important;
}

.vc-day.is-today .vc-day-content {
  color: var(--secondary-color) !important;
  background-color: var(--primary-color) !important;
  border-radius: 50%;
  font-weight: bold !important;
}

.vc-day.is-not-in-month .vc-day-content {
  color: var(--text-muted) !important;
}

/* Style for dots on calendar */
.vc-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin: 0 1px;
}

.selected-date-display {
  text-align: center;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px dashed var(--border-color);
  color: var(--primary-color);
}
.selected-date-display h3 {
  font-size: 1.3em;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 0;
}
.selected-date-display i {
  color: var(--accent-color);
}


.task-list-area {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.upcoming-tasks-card, .selected-day-tasks-card {
  /* Inherits from .card */
  padding: 25px;
}

.upcoming-tasks-card h2, .selected-day-tasks-card h2 {
  font-size: 1.8em;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 15px;
  margin-bottom: 20px;
  color: var(--primary-color);
}
.upcoming-tasks-card h2 i, .selected-day-tasks-card h2 i {
  color: var(--accent-color);
}

.task-list {
  list-style: none;
  padding: 0;
}

.task-item {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px dashed var(--border-color);
  font-size: 1em;
  color: var(--text-light);
  transition: background-color 0.2s ease;
}

.task-item:last-child {
  border-bottom: none;
}

.task-item:hover {
  background-color: rgba(var(--primary-color-rgb), 0.05); /* Slight highlight on hover */
}

.task-info {
  display: flex;
  flex-grow: 1;
  align-items: center;
  flex-wrap: wrap;
}

.task-time {
  font-weight: bold;
  color: var(--accent-color);
  margin-right: 15px;
  min-width: 60px;
}

.task-date {
  font-size: 0.9em;
  color: var(--text-muted);
  margin-right: 15px;
}

.task-content {
  flex-grow: 1;
  color: var(--text-light);
}

.task-priority {
  margin-left: 10px;
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 0.85em;
  color: var(--secondary-color); /* Text color for priority tags */
  min-width: 40px;
  text-align: center;
  font-weight: bold;
}

/* Priority specific styles */
.priority-high .task-priority {
  background-color: #f44336; /* Red */
}
.priority-medium .task-priority {
  background-color: #ffc107; /* Amber */
}
.priority-low .task-priority {
  background-color: #4caf50; /* Green */
}

.task-completed .task-content, .task-completed .task-time, .task-completed .task-date {
  text-decoration: line-through;
  color: var(--text-muted);
}

.task-actions {
  margin-left: 20px;
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.task-actions .icon-button {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 8px;
  font-size: 1.2em;
  transition: color 0.3s ease;
  border-radius: 50%; /* Make them round */
}

.task-actions .icon-button:hover {
  color: var(--primary-color);
  background-color: rgba(var(--primary-color-rgb), 0.1);
}

.edit-button { color: var(--primary-color); }
.delete-button { color: #f44336; } /* Red for delete */
.complete-button { color: #4caf50; } /* Green for complete */
.incomplete-button { color: var(--text-muted); } /* Muted for incomplete */

.no-tasks-message {
  text-align: center;
  color: var(--text-muted);
  font-style: italic;
  padding: 20px;
  border: 1px dashed var(--border-color);
  border-radius: 5px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  .add-task-button {
    width: 100%;
    justify-content: center;
  }
  .task-item {
    flex-direction: column;
    align-items: flex-start;
  }
  .task-info {
    width: 100%;
    margin-bottom: 10px;
  }
  .task-actions {
    margin-left: 0;
    width: 100%;
    justify-content: flex-end;
  }
}

</style>
