function addTodo() {
    const todoInput = document.getElementById('todo-input');
    const todoText = todoInput.value.trim();
    if (todoText !== '') {
        const todoList = document.getElementById('todo-list');
        const li = document.createElement('li');
        li.appendChild(document.createTextNode(todoText));
        li.onclick = () => li.classList.toggle('completed');
        todoList.appendChild(li);
        todoInput.value = '';
    }
}