const explore = document.getElementById("explore-btn");
explore.addEventListener("click", () => {
    const name = document.getElementById("name").value;
    localStorage.setItem("loaded", true);
    localStorage.setItem("name", name);
    document.getElementById("home").click();
});