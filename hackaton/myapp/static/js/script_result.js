document.getElementById('id_message').addEventListener('input', function() {
  const inputText = document.getElementById('id_message').value;

  // Separare le parole dalla virgola
  const keywords = inputText.split(',').map(keyword => keyword.trim()).filter(keyword => keyword.length > 0);

  // Creare una stringa HTML con le parole evidenziate
  const highlightedKeywords = keywords.map(keyword => `<span class="highlighted">${keyword}</span>`).join(' ');

  // Mostra l'elenco separato da virgola nell'input
  document.getElementById('id_message').value = keywords.join(', ');

  // Aggiornare la visualizzazione nell'anteprima delle parole evidenziate
  document.getElementById('keywordPreview').innerHTML = highlightedKeywords;
});
  
  // Aggiungi un listener per gestire il comportamento della virgola
  document.getElementById('id_message').addEventListener('keyup', function(event) {
    const inputText = document.getElementById('id_message').value;
  
    // Se la virgola viene premuta
    if (event.key === ',') {
      const keywords = inputText.split(',').map(keyword => keyword.trim()).filter(keyword => keyword.length > 0);
  
      // Aggiungi uno spazio dopo la virgola se non è presente
      if (keywords.length > 0) {
        document.getElementById('id_message').value = keywords.join(', ') + ', ';
      }
    }
  });

  document.getElementById('id_message').setAttribute("class","w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500");
  document.getElementById('id_message').setAttribute('placeholder', 'Inserisci parole chiave... (separate da una virgola)');
