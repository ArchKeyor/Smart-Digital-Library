document.addEventListener('DOMContentLoaded', async function() {
    const container = document.getElementById('container-emprestimos');
    const API_URL = '/api/emprestimos';

    try {
        const response = await fetch(API_URL);
        
        if (!response.ok) throw new Error('Erro ao buscar dados');
        
        const emprestimos = await response.json();

        // Limpa o texto "Carregando..."
        container.innerHTML = '';

        if (emprestimos.length === 0) {
            container.innerHTML = `
                <div class="book-card">
                    <h3>Nenhum livro emprestado</h3>
                    <p>Você ainda não possui livros emprestados.</p>
                </div>`;
            return;
        }

        // Itera sobre os dados da API e cria o HTML
        emprestimos.forEach(emprestimo => {
            // Formata datas (a API manda em formato ISO)
            const dataEmp = new Date(emprestimo.data_emprestimo).toLocaleDateString('pt-BR');
            const dataDev = emprestimo.data_devolucao ? new Date(emprestimo.data_devolucao).toLocaleDateString('pt-BR') : 'Pendente';

            // Lógica para capa (placeholder se não tiver imagem)
            let imagemHtml = `
                <div class="book-cover-placeholder">
                    Sem capa
                </div>`;
            
            if (emprestimo.livro_capa_url) {
                imagemHtml = `<img src="${emprestimo.livro_capa_url}" alt="${emprestimo.livro_titulo}" class="book-cover">`;
            }

            // Montando o Card (Copiando a estrutura do seu HTML original)
            const cardHtml = `
                <div class="book-card">
                    ${imagemHtml}
                    
                    <div class="book-info">
                        <h3>
                            <a href="/livros/${emprestimo.livro}/"> 
                                ${emprestimo.livro_titulo}
                            </a>
                        </h3>
                        <p class="book-author">${emprestimo.livro_autor || 'Autor desconhecido'}</p>
                        <p class="loan-date">Emprestado: ${dataEmp}</p>
                        <p class="return-date">Devolução: ${dataDev}</p>
                        
                        <button onclick="devolverLivro(${emprestimo.id})" class="return-btn">
                             📤 Devolver Livro
                        </button>
                    </div>
                </div>
            `;
            
            // Adiciona o card ao container
            container.innerHTML += cardHtml;
        });

    } catch (error) {
        console.error('Erro:', error);
        container.innerHTML = '<p>Erro ao carregar os empréstimos. Tente recarregar a página.</p>';
    }
});

// Função extra para o botão de devolver
async function devolverLivro(id) {
    if(confirm("Deseja realmente devolver este livro?")) {
        // Exemplo de como seria um DELETE ou PATCH na API
        // await fetch(`/api/emprestimos/${id}/`, { method: 'DELETE' });
        alert(`Lógica de devolução para o ID ${id} acionada via API!`);
        location.reload(); // Recarrega para atualizar a lista
    }
}

// Função para carregar livros no Select
async function carregarSelectLivros() {
    const res = await fetch('http://127.0.0.1:8000/api/livros/');
    const livros = await res.json();
    const select = document.getElementById('livroSelect');
    select.innerHTML = '';
    livros.forEach(livro => {
        // Só mostra se tem estoque
        if(livro.quantidade > 0) {
            select.innerHTML += `<option value="${livro.id}">${livro.titulo} (Qtd: ${livro.quantidade})</option>`;
        }
    });
}

function abrirModal() {
    document.getElementById('modalEmprestimo').style.display = 'block';
    carregarSelectLivros();
}

// Enviar o formulário (CREATE)
document.getElementById('formEmprestimo').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dados = {
        livro: document.getElementById('livroSelect').value,
        nome_aluno: "Usuário Teste", // Pegar do user logado se possível
        cpf_aluno: document.getElementById('cpfInput').value
    };

    try {
        const res = await fetch('http://127.0.0.1:8000/api/emprestimos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Se usar autenticação, precisa do Token aqui
                'X-CSRFToken': getCookie('csrftoken') // Django precisa disso pra POSTs
            },
            body: JSON.stringify(dados)
        });

        if(!res.ok) {
            const erro = await res.json();
            alert("Erro: " + JSON.stringify(erro)); // Mostra erro de validação (ex: estoque)
            return;
        }

        alert("Empréstimo realizado!");
        location.reload();

    } catch (err) {
        console.error(err);
    }
});

// Helper para pegar o cookie CSRF do Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}