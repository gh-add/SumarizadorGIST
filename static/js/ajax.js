document.addEventListener('DOMContentLoaded', carregarSecaoList);

function carregarSecaoList() {
  const container = document.getElementById('secao_list');
  const url = container.dataset.url;
  fetch(url)
    .then(response => response.text())
    .then(html => {
      container.innerHTML = html;
    })
    .catch(error => console.error("Erro ao carregar o conteúdo:", error));
}

document.addEventListener('submit', function (e) {
  const form = e.target.closest('.form-excluir');
  if (!form) return;

  e.preventDefault(); // impede o envio tradicional do form

  const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

  fetch(form.action, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
    },
  })
    .then(response => {
      if (response.ok) {
        carregarSecaoList(); // só recarrega DEPOIS que o delete confirmou no servidor
      } else {
        console.error('Erro ao excluir a seção.');
      }
    })
    .catch(error => console.error("Erro ao excluir:", error));
});