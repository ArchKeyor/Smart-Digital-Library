from django.db import models
# Importamos o Livro VERDADEIRO do seu outro app
# (Verifique se o nome da classe no seu models é 'Book' ou 'Livro')
from virtuallibrary.models import Book


class Emprestimo(models.Model):
    # Relacionamento agora aponta para virtuallibrary.Book
    livro = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='emprestimos_api')

    nome_aluno = models.CharField(max_length=100)
    cpf_aluno = models.CharField(max_length=14, default="000.000.000-00")
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateField(null=True, blank=True)
    devolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome_aluno} pegou {self.livro}"
