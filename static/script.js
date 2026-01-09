
document.addEventListener("DOMContentLoaded", () => {
    const gameSelect = document.getElementById("game-select");
    const customField = document.getElementById("custom-game-field");

    if (!gameSelect) return;

    gameSelect.addEventListener("change", () => {
        if (gameSelect.value === "OTHER") {
            customField.style.display = "block";
        } else {
            customField.style.display = "none";
        }
    });
});
