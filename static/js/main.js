document.addEventListener("DOMContentLoaded", () => {
    const modal = document.querySelector("#confirmModal");
    const modalTitle = document.querySelector("#confirmTitle");
    const modalMessage = document.querySelector("#confirmMessage");
    const modalCancel = document.querySelector("#confirmCancel");
    const modalAccept = document.querySelector("#confirmAccept");
    let pendingDeleteForm = null;

    const openConfirmModal = (form) => {
        pendingDeleteForm = form;
        modalTitle.textContent = form.dataset.confirmTitle || "Confirm delete?";
        modalMessage.textContent = form.dataset.confirmMessage || "This action cannot be undone.";
        modal.classList.add("open");
        modal.setAttribute("aria-hidden", "false");
    };

    const closeConfirmModal = () => {
        modal.classList.remove("open");
        modal.setAttribute("aria-hidden", "true");
        pendingDeleteForm = null;
    };

    const attachDeleteConfirmations = () => {
        document.querySelectorAll(".delete-form").forEach((form) => {
            if (form.dataset.confirmAttached === "true") {
                return;
            }
            form.dataset.confirmAttached = "true";
            form.addEventListener("submit", (event) => {
                event.preventDefault();
                openConfirmModal(form);
            });
        });
    };

    if (modalCancel && modalAccept) {
        modalCancel.addEventListener("click", closeConfirmModal);
        modal.addEventListener("click", (event) => {
            if (event.target === modal) {
                closeConfirmModal();
            }
        });
        modalAccept.addEventListener("click", () => {
            if (pendingDeleteForm) {
                pendingDeleteForm.submit();
            }
        });
    }

    document.querySelectorAll(".flash-stack .alert").forEach((alert) => {
        setTimeout(() => {
            alert.classList.add("hide");
            setTimeout(() => alert.remove(), 300);
        }, 4000);
    });

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
                usersTableBody.innerHTML = "<tr><td colspan=\"5\"><div class=\"empty-state\"><strong>No users found.</strong><span>Try a different search query.</span></div></td></tr>";
                return;
            }
            usersTableBody.innerHTML = users.map((user) => `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td><span class="badge ${user.role}">${user.role}</span></td>
                    <td>${user.created_at}</td>
                    <td>
                        <form action="/admin/users/delete/${user.id}" method="post" class="inline-form delete-form" data-confirm-title="Delete user?" data-confirm-message="This will also delete all records owned by this user.">
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
