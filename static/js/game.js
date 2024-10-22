let correctOperations = [];

function startGame() {
    const level = document.getElementById('level').value;

    fetch('/get_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ level: level })
    })
    .then(response => response.json())
    .then(data => {
        // Tampilkan gambar sebelum dan sesudah
        document.getElementById('before-image').src = 'data:image/jpeg;base64,' + data.before;
        document.getElementById('after-image').src = 'data:image/jpeg;base64,' + data.after;

        // Simpan operasi yang benar untuk validasi nanti
        correctOperations = data.operations;

        // Hapus hasil sebelumnya
        document.getElementById('result').textContent = '';
    });
}

function submitGuess() {
    const guess = document.getElementById('guess').value.toLowerCase();
    const guessArray = guess.split(',').map(g => g.trim());

    if (JSON.stringify(guessArray) === JSON.stringify(correctOperations)) {
        document.getElementById('result').textContent = 'Correct! You guessed the operations!';
    } else {
        document.getElementById('result').textContent = 'Incorrect! Try again.';
    }
}
