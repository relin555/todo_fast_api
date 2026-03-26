const API = "http://127.0.0.1:8000";
let tasksData = [];
if (window.location.pathname.includes("tasks.html")) {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "auth.html";
    }
}

function renderTasks(tasks) {
    const list = document.getElementById("tasks");
    list.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");

        const doneButton =
            task.status === "в ожидании" || task.status === "в работе"
                ? `<button class="done-btn" onclick="markTaskDone(${task.id})">Выполнено</button>`
                : "";

        li.innerHTML = `
            <div class="task-title">${task.title}</div>
            <div class="task-desc">${task.description}</div>
            <div class="task-meta">
                Статус: ${task.status} | Приоритет: ${task.priority}
            </div>
            <div class="task-actions">
                ${doneButton}
                <button class="delete-btn" onclick="deleteTask(${task.id})">Удалить</button>
            </div>
        `;

        list.appendChild(li);
    });
}

function sortTasks() {
    const sortType = document.getElementById("sortSelect").value;

    let sorted = [...tasksData];

    if (sortType === "priority_asc") {
        sorted.sort((a, b) => a.priority - b.priority);
    }

    if (sortType === "priority_desc") {
        sorted.sort((a, b) => b.priority - a.priority);
    }

    if (sortType === "status") {
        sorted.sort((a, b) => a.status.localeCompare(b.status));
    }

    renderTasks(sorted);
}

function logout() {
    localStorage.clear();
    window.location.href = "auth.html";
}
function setStatus(message) {
    const statusEl = document.getElementById("statusMessage");
    if (statusEl) {
        statusEl.innerText = message;
    }
}

async function register() {
    try {
        const email = document.getElementById("reg_email").value;
        const password = document.getElementById("reg_password").value;

        const res = await fetch(`${API}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            setStatus("Ошибка регистрации: " + JSON.stringify(data));
            return;
        }

        setStatus("Регистрация прошла успешно. Теперь войди.");
    } catch (error) {
        console.error(error);
        setStatus("Ошибка запроса регистрации");
    }
}

async function login() {
    try {
        const email = document.getElementById("login_email").value;
        const password = document.getElementById("login_password").value;

        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        const res = await fetch(`${API}/auth/jwt/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        const text = await res.text();

        if (!res.ok) {
            setStatus("Ошибка входа: " + text);
            return;
        }

        const data = JSON.parse(text);

        localStorage.setItem("token", data.access_token);
        window.location.href = "tasks.html";
    } catch (error) {
        console.error(error);
        setStatus("Ошибка запроса входа");
    }
}

async function createTask() {
    try {
        const token = localStorage.getItem("token");

        if (!token) {
            setStatus("Сначала войди в аккаунт");
            return;
        }

        const task = {
            title: document.getElementById("title").value,
            description: document.getElementById("description").value,
            status: document.getElementById("status").value,
            priority: Number(document.getElementById("priority").value)
        };

        const res = await fetch(`${API}/tasks/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(task)
        });

        const data = await res.json();

        if (!res.ok) {
            setStatus("Ошибка создания задачи: " + JSON.stringify(data));
            return;
        }

        setStatus("Задача успешно создана");

        document.getElementById("title").value = "";
        document.getElementById("description").value = "";
        document.getElementById("priority").value = "";

        getTasks();
    } catch (error) {
        console.error(error);
        setStatus("Ошибка запроса создания задачи");
    }
}

async function getTasks() {
    try {
        const token = localStorage.getItem("token");

        if (!token) {
            setStatus("Сначала войди в аккаунт");
            return;
        }

        const res = await fetch(`${API}/tasks/`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();

        if (!res.ok) {
            setStatus("Ошибка загрузки задач: " + JSON.stringify(data));
            return;
        }

        const list = document.getElementById("tasks");
        if (!list) return;

        list.innerHTML = "";

        tasksData = data;
        renderTasks(tasksData);

        setStatus("Задачи загружены");
    } catch (error) {
        console.error(error);
        setStatus("Ошибка запроса списка задач");
    }
}

async function deleteTask(id) {
    try {
        const token = localStorage.getItem("token");

        if (!token) {
            setStatus("Сначала войди в аккаунт");
            return;
        }

        const res = await fetch(`${API}/tasks/${id}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!res.ok) {
            const data = await res.json();
            setStatus("Ошибка удаления: " + JSON.stringify(data));
            return;
        }

        setStatus("Задача удалена");
        getTasks();
    } catch (error) {
        console.error(error);
        setStatus("Ошибка удаления задачи");
    }
}

async function markTaskDone(id) {
    try {
        const token = localStorage.getItem("token");

        if (!token) {
            setStatus("Сначала войди в аккаунт");
            return;
        }

        const res = await fetch(`${API}/tasks/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ status: "завершено" })
        });

        const data = await res.json();

        if (!res.ok) {
            setStatus("Ошибка обновления задачи: " + JSON.stringify(data));
            return;
        }

        setStatus("Задача отмечена как завершённая");
        getTasks();
    } catch (error) {
        console.error(error);
        setStatus("Ошибка обновления задачи");
    }
}