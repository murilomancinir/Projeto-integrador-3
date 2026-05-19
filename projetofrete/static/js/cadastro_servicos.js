// ==========================================
// CADASTRO DE SERVIÇOS / VIAGENS
// ==========================================

document.addEventListener("DOMContentLoaded", function () {
  // ==========================================
  // ELEMENTOS GERAIS
  // ==========================================
  const form = document.getElementById("serviceForm");

  // abas
  const tabLinks = document.querySelectorAll(".tab-link");
  const tabContents = document.querySelectorAll(".tab-content");

  // dados
  const campoOrigem = document.getElementById("origem");
  const campoDestino = document.getElementById("destino");
  const campoDistancia = document.getElementById("distancia");
  const campoDistanciaManual = document.getElementById("distancia_manual");
  const btnCalcularDistancia = document.getElementById("btnCalcularDistancia");
  const boxDistanciaManual = document.getElementById("toggle_distancia_manual");

  // despesas
  const btnAdicionar = document.getElementById("btnAdicionar");
  const campoDespesa = document.getElementById("despesa");
  const campoValor = document.getElementById("valor");
  const listaDespesas = document.getElementById("lista-despesas");
  const hiddenDespesas = document.getElementById("despesas_json");

  // clientes
  const btnSalvaCliente = document.getElementById("btnSalvaCliente");
  const camponome = document.getElementById("nome");
  const campotelefone = document.getElementById("telefone");
  const campoemail = document.getElementById("email");
  const campocidade = document.getElementById("cidade");

  //veiculos 
  const salvaVeiculo = document.getElementById("salvaVeiculo");
  const campoplaca = document.getElementById("placa");
  const campomodelo = document.getElementById("modelo");
  const campomarca = document.getElementById("marca");
  const campoconsumo = document.getElementById("consumo");

  

  // ==========================================
  // TROCA DE ABAS
  // ==========================================
  tabLinks.forEach(link => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      const abaAlvo = this.dataset.tab;

      tabLinks.forEach(item => item.classList.remove("active"));
      tabContents.forEach(item => item.classList.remove("active"));

      this.classList.add("active");

      const conteudoAlvo = document.getElementById(abaAlvo);
      if (conteudoAlvo) {
        conteudoAlvo.classList.add("active");
      }
    });
  });

  // ==========================================
  // FUNÇÕES AUXILIARES
  // ==========================================
  function formatarValor(valor) {
    const numero = Number(valor);
    if (Number.isNaN(numero)) {
      return "0.00";
    }
    return numero.toFixed(2);
  }

  function criarCardDespesa(nome, valor) {
    const item = document.createElement("div");
    item.classList.add("card-despesa");

    item.innerHTML = `
      <div class="card-despesa-conteudo">
        <span class="nome-despesa">${nome}</span>
        <strong class="valor-despesa" data-valor="${formatarValor(valor)}">
          R$ ${formatarValor(valor)}
        </strong>
        <button type="button" class="btn-excluir-despesa" aria-label="Excluir despesa">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
            <path d="M3 6h18"></path>
            <path d="M8 6V4h8v2"></path>
            <path d="M19 6l-1 14H6L5 6"></path>
            <path d="M10 11v6"></path>
            <path d="M14 11v6"></path>
          </svg>
        </button>
      </div>
    `;
    item.querySelector(".btn-excluir-despesa").addEventListener("click", function () {
      item.remove();
      atualizarTotalDespesas();
    });

    return item;
  }

/*   function atualizarTotalDespesas() {
  const valores = document.querySelectorAll(".lista-despesas .valor-despesa");
  let total = 0;

  valores.forEach(valorEl => {
    const valor = parseFloat(valorEl.dataset.valor) || 0;
    total += valor;
  });

  document.getElementById("total-despesas").textContent = `R$ ${formatarValor(total)}`;
  } */

  function atualizarTotalDespesas() {
  const valores = document.querySelectorAll(".valor-despesa");
  let total = 0;

  console.log("quantidade encontrada:", valores.length);

  valores.forEach(valorEl => {
    console.log("data-valor:", valorEl.dataset.valor);
    const valor = parseFloat(valorEl.dataset.valor) || 0;
    total += valor;
  });

  console.log("total calculado:", total);

  document.getElementById("total-despesas").textContent = `R$ ${formatarValor(total)}`;
  }

  function obterDespesasDaTela() {
    const despesas = [];

    const cards = listaDespesas.querySelectorAll(".card-despesa");

    cards.forEach(card => {
      const nomeEl = card.querySelector(".nome-despesa");
      const valorEl = card.querySelector(".valor-despesa");

      const nome = nomeEl ? nomeEl.textContent.trim() : "";
      const valor = valorEl ? valorEl.dataset.valor : "0.00";

      if (nome) {
        despesas.push({
          despesa: nome,
          valor: Number(valor)
        });
      }
    });

    return despesas;
  }

  function atualizarHiddenDespesas() {
    if (!hiddenDespesas) return;

    const despesas = obterDespesasDaTela();
    hiddenDespesas.value = JSON.stringify(despesas);
  }

  function limparCamposDespesa() {
    campoDespesa.value = "";
    campoValor.value = "";
    campoDespesa.focus();
  }
  async function buscarDistanciaAPI() {
  const origem = campoOrigem.value.trim();
  const destino = campoDestino.value.trim();

  if (!origem || !destino) {
    alert("Preencha a origem e o destino.");
    return;
  }

  if (campoDistanciaManual && campoDistanciaManual.value === "1") {
    return;
  }

  try {
    const response = await fetch("/buscar_distancia", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        origem: origem,
        destino: destino
      })
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.erro || "Erro ao buscar distância.");
      return;
    }

    campoDistancia.value = data.distancia_km;
  } catch (error) {
    console.error("Erro ao buscar distância:", error);
    alert("Não foi possível calcular a distância.");
  }
  }

  function alternarDistanciaManual() {
  if (boxDistanciaManual.checked) {
    campoDistancia.readOnly = false;
    campoDistancia.value = "";
    campoDistanciaManual.value = "1";

    btnCalcularDistancia.disabled = true;
    campoDistancia.focus();
  } else {
    campoDistancia.readOnly = true;
    campoDistancia.value = "";
    campoDistanciaManual.value = "0";

    btnCalcularDistancia.disabled = false;
  }
}


  //========================================
  // CHAMADA DA FUNCAO NO CLIQUE PARA CALCULAR DISTANCIA
  //========================================
  if (btnCalcularDistancia) {
    btnCalcularDistancia.addEventListener("click", function () {
      buscarDistanciaAPI();
    });
  }

  //========================================
  // CALCULAR DISTANCIA MANUAL
  //========================================

  if (boxDistanciaManual){
    boxDistanciaManual.addEventListener("change", alternarDistanciaManual);
  }

  // ==========================================
  // ADICIONAR DESPESA
  // ==========================================
  if (btnAdicionar) {
    btnAdicionar.addEventListener("click", function () {
      const despesa = campoDespesa.value.trim();
      const valor = campoValor.value.trim();

      if (!despesa || !valor) {
        alert("Preencha a despesa e o valor.");
        return;
      }

      if (Number(valor) <= 0) {
        alert("Informe um valor maior que zero.");
        return;
      }

      const card = criarCardDespesa(despesa, valor);
      listaDespesas.appendChild(card);

      //const card = criarCardDespesa(despesa, valor);
      //document.querySelector(".lista-despesas").appendChild(card);
      atualizarTotalDespesas();
      atualizarHiddenDespesas();
      limparCamposDespesa();
    });
  }

  // ==========================================
  // ADICIONAR COM ENTER
  // ==========================================
  if (campoValor) {
    campoValor.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        if (btnAdicionar) {
          btnAdicionar.click();
        }
      }
    });
  }

  // ==========================================
  // EXCLUIR DESPESA EM TELA
  // ==========================================
  if (listaDespesas) {
    listaDespesas.addEventListener("click", function (e) {
      if (e.target.closest(".btn-excluir-despesa")) {
        const card = e.target.closest(".card-despesa");
        if (card) {
          card.remove();
          atualizarHiddenDespesas();
        }
      }
    });
  }

  // ==========================================
  // SUBMIT DO FORMULÁRIO
  // ==========================================
  if (form) {
    form.addEventListener("submit", function () {
      atualizarHiddenDespesas();
    });
  }

  // ===========================================
  // SALVAR CLIENTES
  // ===========================================
  const formCliente = document.getElementById("formCliente");
  if (formCliente) {
    const camposObrigatorios = formCliente.querySelectorAll("input");

    formCliente.addEventListener("submit", function (event) {
      let formularioValido = true;

      camposObrigatorios.forEach(function (campo) {
        const grupo = campo.closest(".form-group");
        const mensagemErro = grupo.querySelector(".erro-campo");

        campo.classList.remove("erro");
        mensagemErro.textContent = "";

        if (campo.value.trim() === "") {
          campo.classList.add("erro");
          mensagemErro.textContent = "Este campo é obrigatório.";
          formularioValido = false;
        }
      });

      if (!formularioValido) {
        event.preventDefault();
      }
    });

    camposObrigatorios.forEach(function (campo) {
      campo.addEventListener("input", function () {
        const grupo = campo.closest(".form-group");
        const mensagemErro = grupo.querySelector(".erro-campo");

        if (campo.value.trim() !== "") {
          campo.classList.remove("erro");
          mensagemErro.textContent = "";
        }
      });
    });
  }

  // ===========================================
  // SALVAR MOTORISTA
  // ===========================================

  const formMotorista = document.getElementById("formMotorista");

  if (formMotorista) {
    const camposObrigatorios = formMotorista.querySelectorAll("input");

    formMotorista.addEventListener("submit", function (event) {
      let formularioValido = true;

      camposObrigatorios.forEach(function (campo) {
        const grupo = campo.closest(".form-group");
        const mensagemErro = grupo.querySelector(".erro-campo");

        campo.classList.remove("erro");
        mensagemErro.textContent = "";

        if (campo.value.trim() === "") {
          campo.classList.add("erro");
          mensagemErro.textContent = "Este campo é obrigatório.";
          formularioValido = false;
        }
      });

      if (!formularioValido) {
        event.preventDefault();
      }
    });

    camposObrigatorios.forEach(function (campo) {
      campo.addEventListener("input", function () {
        const grupo = campo.closest(".form-group");
        const mensagemErro = grupo.querySelector(".erro-campo");

        if (campo.value.trim() !== "") {
          campo.classList.remove("erro");
          mensagemErro.textContent = "";
        }
      });
    });
  }

  // ===========================================
  // SALVAR VEICULOS
  // ===========================================

  const formVeiculo = document.getElementById("formVeiculo");

  if (formVeiculo) {
    const camposObrigatorios = formVeiculo.querySelectorAll("input");

    formVeiculo.addEventListener("submit", function (event) {
      let formularioValido = true;

      camposObrigatorios.forEach(function (campo) {
        const grupo = campo.closest(".form-group");
        const mensagemErro = grupo.querySelector(".erro-campo");

        campo.classList.remove("erro");
        mensagemErro.textContent = "";

        if (campo.value.trim() === "") {
          campo.classList.add("erro");
          mensagemErro.textContent = "Este campo é obrigatório.";
          formularioValido = false;
        }
      });

      if (!formularioValido) {
        event.preventDefault();
      }
    });

    camposObrigatorios.forEach(function (campo) {
      campo.addEventListener("input", function () {
        const grupo = campo.closest(".form-group");
        const mensagemErro = grupo.querySelector(".erro-campo");

        if (campo.value.trim() !== "") {
          campo.classList.remove("erro");
          mensagemErro.textContent = "";
        }
      });
    });
  }

  // ===========================================
  // MENSAGEM DE ALERTA
  // ===========================================

  const mensagemAlerta = document.getElementById("mensagemAlerta");
  const fecharMensagem = document.getElementById("fecharMensagem");

  if (mensagemAlerta && fecharMensagem) {
    fecharMensagem.addEventListener("click", function () {
      mensagemAlerta.style.display = "none";
    });

    setTimeout(function () {
      mensagemAlerta.style.display = "none";
    }, 4000);
  }


}); // chaves abertas no inicio do arquivo