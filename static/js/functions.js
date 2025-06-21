
function carregarDetalhe(pk) {
  fetch(`/${pk}/`, {
    headers: {'X-Requested-With': 'XMLHttpRequest'}
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('main-content').innerHTML = data.html;
  });
}

function carregar_secoes() {
  fetch('/listar_secoes/', {
    headers: {'X-Requested-With': 'XMLHttpRequest'}
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('nav-lateral').innerHTML = data.html;
  });
}

function carregarFormulario() {
  fetch(`/add/`, {
    headers: {'X-Requested-With': 'XMLHttpRequest'}
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('main-content').innerHTML = data.html;
    ativarListenersFormulario();  // carrega o detalhe da seção criada
  });
}

function ativarListenersFormulario() {
  const tipoEntradaSelect = document.getElementById("id_tipo_entrada");
  const campoUrl = document.getElementById("campo-url");
  const campoArquivo = document.getElementById("campo-arquivo");

  function atualizarCampos() {
    const tipo = tipoEntradaSelect.value;
    campoUrl.style.display = (tipo === "url") ? "block" : "none";
    campoArquivo.style.display = (tipo === "file") ? "block" : "none";
  }

  tipoEntradaSelect.addEventListener("change", atualizarCampos);
  atualizarCampos();
}

document.addEventListener("DOMContentLoaded", function () {
  ativarListenersFormulario();
});



document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.link-secao').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      const pk = event.currentTarget.dataset.pk;
      carregarDetalhe(pk);
    });
  });
});
