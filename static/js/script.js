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

// Read current lang from URL (defaults to 'english')
function getCurrentLang() {
    const params = new URLSearchParams(window.location.search);
    return params.get('lang') || 'english';
}

function addQuote() {
    const quote = document.getElementById("add-quote-input").value;

    fetch("/quotes/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ quote: quote, lang: getCurrentLang() })
    })
    .then(res => res.json())
    .then(() => location.reload());
}

function removeQuote() {
    const index = parseInt(document.getElementById("remove-quote-input").value, 10);

    fetch("/quotes/remove", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index: index, lang: getCurrentLang() })
    })
    .then(res => res.json())
    .then(() => location.reload());
}

function replaceQuote() {
    const index    = parseInt(document.getElementById("replace-index-input").value, 10);
    const newQuote = document.getElementById("replace-text-input").value;

    fetch("/quotes/replace", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index: index, quote: newQuote, lang: getCurrentLang() })
    })
    .then(res => res.json())
    .then(() => location.reload());
}

function regenerate() {
    fetch("/clear-cache", { method: "POST" })
    .then(() => location.reload());
}