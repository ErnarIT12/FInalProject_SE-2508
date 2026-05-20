document.addEventListener("DOMContentLoaded", () => {
    const attachDeleteConfirmations = () => {
        document.querySelectorAll(".delete-form").forEach((form) => {
            if (form.dataset.confirmAttached === "true") {
                return;
            }
            form.dataset.confirmAttached = "true";
            form.addEventListener("submit", (event) => {
                if (!confirm("Delete this user and all related records?")) {
                    event.preventDefault();
                }
            });
        });
    };

    document.querySelectorAll(".validate-auth-form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const username = form.querySelector("input[name='username']");
            const password = form.querySelector("input[name='password']");

            if (username && username.value.trim().length < 3) {
                event.preventDefault();
                alert("Username must be at least 3 characters.");
                username.focus();
                return;
            }

            if (password && password.value.length < 6) {
                event.preventDefault();
                alert("Password must be at least 6 characters.");
                password.focus();
            }
        });
    });

    attachDeleteConfirmations();

    const searchInput = document.querySelector("#userSearch");
    const usersTableBody = document.querySelector("#usersTableBody");

    if (searchInput && usersTableBody) {
        let searchTimer = null;

        const renderUsers = (users) => {
            if (users.length === 0) {
                usersTableBody.innerHTML = "<tr><td colspan=\"5\" class=\"table-state\">No users found.</td></tr>";
                return;
            }
            usersTableBody.innerHTML = users.map((user) => `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.role}</td>
                    <td>${user.created_at}</td>
                    <td>
                        <form action="/admin/users/delete/${user.id}" method="post" class="inline-form delete-form">
                            <button type="submit" class="button danger">Delete</button>
                        </form>
                    </td>
                </tr>
            `).join("");
            attachDeleteConfirmations();
        };

        searchInput.addEventListener("input", () => {
            clearTimeout(searchTimer);
            searchTimer = setTimeout(async () => {
            const query = encodeURIComponent(searchInput.value.trim());
                usersTableBody.innerHTML = "<tr><td colspan=\"5\" class=\"table-state\">Searching...</td></tr>";

                try {
                    const response = await fetch(`/api/admin/users?q=${query}`);
                    if (!response.ok) {
                        throw new Error("Search request failed.");
                    }
                    renderUsers(await response.json());
                } catch (error) {
                    usersTableBody.innerHTML = "<tr><td colspan=\"5\" class=\"table-state\">Search failed. Try again.</td></tr>";
                }
            }, 250);
        });
    }
});
