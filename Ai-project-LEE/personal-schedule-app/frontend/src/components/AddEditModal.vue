<template>
  <div class="modal-overlay" v-if="isVisible">
    <div class="modal-content card">
      <h2>{{ currentTask && currentTask.id ? '編輯行程' : '新增行程' }}</h2>
      <form @submit.prevent="saveTask">
        <div class="form-group">
          <label for="content">內容:</label>
          <input type="text" id="content" v-model="taskForm.content" required />
        </div>
        <div class="form-group">
          <label for="date">日期:</label>
          <input type="date" id="date" v-model="taskForm.date" required />
        </div>
        <div class="form-group">
          <label for="time">時間 (可選):</label>
          <input type="time" id="time" v-model="taskForm.time" />
        </div>
        <div class="form-group">
          <label for="priority">緊急程度:</label>
          <select id="priority" v-model.number="taskForm.priority">
            <option :value="1">高</option>
            <option :value="2">中</option>
            <option :value="3">低</option>
          </select>
        </div>
        <div class="form-actions">
          <button type="submit" class="save-button">儲存</button>
          <button type="button" @click="cancel" class="cancel-button">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddEditModal',
  props: {
    isVisible: Boolean,
    task: Object, // The task object to be edited (optional)
  },
  data() {
    return {
      taskForm: {
        id: null,
        content: '',
        date: '',
        time: '',
        priority: 2, // Default to medium priority
      },
    };
  },
  watch: {
    task: {
      immediate: true,
      handler(newTask) {
        if (newTask) {
          this.taskForm = {
            id: newTask.id || null,
            content: newTask.content || '',
            // Ensure date is in 'YYYY-MM-DD' format for input type="date"
            date: newTask.date instanceof Date ? newTask.date.toISOString().split('T')[0] : newTask.date || '',
            // Ensure time is in 'HH:MM' format for input type="time"
            time: newTask.time ? newTask.time.substring(0, 5) : '',
            priority: newTask.priority || 2,
          };
        } else {
          this.resetForm();
        }
      },
    },
    isVisible(newVal) {
      if (!newVal) {
        this.resetForm();
      }
    }
  },
  methods: {
    saveTask() {
      // Emit the taskForm data to the parent component
      this.$emit('save', this.taskForm);
      this.resetForm();
    },
    cancel() {
      this.$emit('close');
      this.resetForm();
    },
    resetForm() {
      this.taskForm = {
        id: null,
        content: '',
        date: '',
        time: '',
        priority: 2,
      };
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8); /* Darker overlay for tech theme */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--background-light); /* Use theme background */
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); /* Darker shadow */
  width: 100%;
  max-width: 500px;
  border: 1px solid var(--border-color); /* Add border */
}

h2 {
  text-align: center;
  color: var(--primary-color); /* Use primary color for heading */
  margin-bottom: 25px;
  font-size: 1.8em;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: var(--text-light); /* Light text for labels */
}

input[type="text"],
input[type="date"],
input[type="time"],
select {
  width: calc(100% - 22px);
  padding: 12px 10px;
  border: 1px solid var(--border-color);
  border-radius: 5px;
  font-size: 1em;
  box-sizing: border-box;
  background-color: var(--background-dark); /* Darker input background */
  color: var(--text-light); /* Light text for inputs */
  font-family: 'Roboto Mono', monospace; /* Consistent font */
}

input[type="text"]:focus,
input[type="date"]:focus,
input[type="time"]:focus,
select:focus {
  border-color: var(--accent-color); /* Accent color on focus */
  outline: none;
  box-shadow: 0 0 5px rgba(var(--accent-color-rgb), 0.5);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
}

.save-button, .cancel-button {
  padding: 12px 25px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease, transform 0.2s ease;
  font-family: 'Roboto Mono', monospace;
  font-weight: bold;
}

.save-button {
  background-color: var(--primary-color);
  color: var(--secondary-color); /* Dark text on primary button */
}

.save-button:hover {
  background-color: var(--accent-color);
  transform: translateY(-2px);
}

.cancel-button {
  background-color: var(--border-color); /* Muted color for cancel */
  color: var(--text-light);
}

.cancel-button:hover {
  background-color: var(--text-muted);
  transform: translateY(-2px);
}
</style>
