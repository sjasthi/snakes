// DataTable Init
$(document).ready(function() {
    if ($('#quotesTable').length) {
        $('#quotesTable').DataTable({
            pageLength: 25,
            order: [[0, 'asc']],
            columnDefs: [
                { width: '5%', targets: 0 },
                { width: '95%', targets: 1 }
            ]
        });
    }
});

// Load quotes function
function addQuote() {
    const quote = document.getElementById("add-quote-input").value;

    fetch("/quotes/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ quote: quote })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        location.reload();
    });
}

function removeQuote() {
    const index = parseInt(document.getElementById("remove-quote-input").value, 10);

    fetch("/quotes/remove", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ index: index })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        location.reload();
    });
}

function replaceQuote() {
    const index = parseInt(document.getElementById("replace-index-input").value, 10);
    const newQuote = document.getElementById("replace-text-input").value;

    fetch("/quotes/replace", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ index: index, quote: newQuote })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        location.reload();
    });
}
