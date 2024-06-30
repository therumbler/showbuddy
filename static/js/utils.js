function logToConsole(message, data) {
    const c = document.getElementById('console');
    c.innerHTML += `<p>${message} ${JSON.stringify(data)}</p>`;
    console.log(message, data);
}