/*!
* Start Bootstrap - Simple Sidebar v6.0.6 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/

document.addEventListener('DOMContentLoaded', inicializarToggleTipoEntrada);
document.addEventListener('DOMContentLoaded', inicializarMenuOpcoes);


// =======================================================
// Sidebar - Start Bootstrap Simple Sidebar
// =======================================================
window.addEventListener('DOMContentLoaded', event => {
  const sidebarToggle = document.body.querySelector('#sidebarToggle');
  if (sidebarToggle) {
    // Uncomment Below to persist sidebar toggle between refreshes
    // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
    //     document.body.classList.toggle('sb-sidenav-toggled');
    // }
    sidebarToggle.addEventListener('click', event => {
      event.preventDefault();
      document.body.classList.toggle('sb-sidenav-toggled');
      localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
    });
  }
});


// Formulário de Seção - Toggle URL / Arquivo
function inicializarToggleTipoEntrada() {
  const tipoEntradaSelect = document.getElementById("id_tipo_entrada");
  const campoUrl = document.getElementById("campo-url");
  const campoArquivo = document.getElementById("campo-arquivo");
  const inputUrl = document.getElementById("id_url");
  const inputArquivo = document.getElementById("id_arquivo");

  if (!tipoEntradaSelect || !campoUrl || !campoArquivo) return;

  function atualizarCampos() {
    const tipo = tipoEntradaSelect.value;
    campoUrl.style.display = (tipo === "url") ? "block" : "none";
    campoArquivo.style.display = (tipo === "arquivo") ? "block" : "none";
    // Alterna o required conforme o campo visível
    inputUrl.required = isUrl;
    inputArquivo.required = !isUrl;

    if (isUrl) {
      inputArquivo.value = "";   // Se o campo visível é URL, limpa o de arquivo
    } else {
      inputUrl.value = "";       // Se o campo visível é Arquivo, limpa o de URL
    }

  }

  tipoEntradaSelect.addEventListener("change", atualizarCampos);
  atualizarCampos();
}


// Menu de Opções (dropdown por item da lista)
function inicializarMenuOpcoes() {
  document.addEventListener("click", function (e) {
    const isMenuButton = e.target.closest(".toggle-menu");
    const isInsideMenu = e.target.closest(".menu-opcoes");

    if (isMenuButton) {
      fecharTodosMenus();

      const container = isMenuButton.closest(".list-group-item");
      const menu = container.querySelector(".menu-opcoes");
      menu.classList.toggle("d-none");

      e.stopPropagation();
      return;
    }

    if (!isInsideMenu) {
      fecharTodosMenus();
    }
  });
}

function fecharTodosMenus() {
  document.querySelectorAll(".menu-opcoes").forEach(menu => {
    menu.classList.add("d-none");
  });
}