const name = document.getElementById("name");
name.textContent = "Welcome, " + localStorage.getItem("name");

document.getElementById("annotate").addEventListener("click", () => {
    // alert("Closing");
    window.close();
})