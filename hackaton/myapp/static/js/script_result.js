document.getElementById('searchButton').addEventListener('click', function() {
    const keywords = document.getElementById('keywordInput').value.split(',').map(keyword => keyword.trim());
    fetch('/search_keywords/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
      },
      body: JSON.stringify({ keywords: keywords })
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('summaryText').textContent = data.summary || 'Nessun risultato trovato.';
    })
    .catch(error => console.error('Errore:', error));
  });