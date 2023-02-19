let id, summ;

function getSelectedText() {
    return getSelection().toString();
}

window.addEventListener("click", () => {
    if(!getSelectedText()) {
        earlier_buttons = document.getElementsByClassName("summarize-btn");
        for(let i of earlier_buttons)
            i.remove();
    }
})

function getSummary(event) {
    let summary;
    // alert("Hello");
    fetch("http://127.0.0.1:8000/api/extract", {
        method: "POST",
        body: JSON.stringify({
            "text": getSelectedText()
        }),
    }).then(data => data.json()).then(res => changeBGC(res.data));
}

window.addEventListener("mouseup", () => {
    text = getSelectedText();
    if(text) {
        // alert(text);
        flag = false;
        var ele = document.createElement("button");
        ele.classList.add("summarize-btn");
        ele.style.position = "absolute";
        ele.innerHTML = `Summarize`;
        ele.style.cursor = "pointer";
        ele.style.zIndex = 1000;
        ele.style.border = "none"
        ele.style.backgroundColor = "#ffbd59";
        ele.style.borderRadius = "50px";
        ele.style.padding = "8px 16px";
        earlier_buttons = document.getElementsByClassName("summarize-btn");
        for(let i of earlier_buttons)
            i.remove();
        document.body.appendChild(ele);
        ele.addEventListener("mousedown", (e) => getSummary(e));
        var r = window.getSelection().getRangeAt(0).getBoundingClientRect();
        var relative = document.body.parentNode.getBoundingClientRect();
        ele.style.top = (r.bottom -relative.top) + 'px';
        ele.style.right =- (r.right-relative.right) + 'px';
    }
})

function changeBGC(summary) {
    let doc = summary;
    sentences = doc.split(". ")
    text = document.body.innerHTML;
    for(let sent of sentences) {
        text = text.replace(sent, "<mark class='extractor'>" + sent + "</mark>");
    }
    document.body.innerHTML = text;
}

// changeBGC();