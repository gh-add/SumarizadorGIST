const secaoConteudo = document.getElementById('secao-conteudo');
const statusUrl = secaoConteudo.dataset.url;
const parcialUrl = secaoConteudo.dataset.parcialUrl;
const eventSource = new EventSource(statusUrl);

eventSource.onmessage = function (event) {
  const data = JSON.parse(event.data);

  if (data.status === 'concluido' || data.status === 'erro') {
    eventSource.close();
    recarregarConteudo();
  }
};

eventSource.onerror = function () {
  console.error('Conexão SSE perdida.');
  eventSource.close();
};

async function recarregarConteudo() {
  try {
    const res = await fetch(parcialUrl);
    const html = await res.text();
    secaoConteudo.innerHTML = html; 
  } catch (e) {
    console.error('Erro ao recarregar conteúdo:', e);
  }
}