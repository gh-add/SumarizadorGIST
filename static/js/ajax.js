document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('secao_list');
  const url = container.dataset.url;
  fetch(url)
  .then(response => response.text())
  .then(html =>{
    container.innerHTML = html;
  })
  .catch(error => console.error("Erro ao carregar o conteúdo:", error));
});



