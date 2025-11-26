from rest_framework import viewsets
from virtuallibrary.models import Book
from .models import Emprestimo
from .serializers import LivroSerializer, EmprestimoSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes


# Muda o nome da categoria no Swagger
@extend_schema(tags=['Gestão de Livros'])
class LivroViewSet(viewsets.ModelViewSet):
    """
    API completa para gerenciamento do acervo da biblioteca.
    Permite listar, cadastrar, atualizar e remover livros.
    """
    queryset = Book.objects.all()
    serializer_class = LivroSerializer

    @extend_schema(
        summary="Listar todos os livros",
        description="Retorna uma lista paginada de livros. Use o filtro 'search' para buscar por autor.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Cadastrar novo livro",
        description="Adiciona um livro ao acervo. A capa é opcional.",
        # Documenta os erros
        responses={201: LivroSerializer, 400: "Erro de validação"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@extend_schema(tags=['Gestão de Empréstimos'])
class EmprestimoViewSet(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer

    @extend_schema(
        summary="Registrar um novo empréstimo",
        description="""
        Cria um registro de empréstimo e **baixa automaticamente o estoque** do livro.
        
        **Regras de Negócio:**
        * **Estoque:** Retorna erro `400` se a quantidade do livro for 0.
        * **Datas:** A data de devolução não pode ser anterior à data de empréstimo.
        * **CPF:** Validação básica de formato.
        """,
        # Documentando os possíveis erros para o Front-end saber tratar
        responses={
            201: EmprestimoSerializer,
            400: OpenApiTypes.OBJECT,
        },
        # Exemplo prático que aparecerá pronto para copiar no Swagger
        examples=[
            OpenApiExample(
                'Exemplo Válido',
                summary='Empréstimo padrão',
                description='Um empréstimo com datas corretas e livro com estoque.',
                value={
                    "livro": 1,
                    "nome_aluno": "Engenheiro de Software",
                    "cpf_aluno": "123.456.789-00",
                    "data_devolucao": "2024-12-30"
                }
            ),
            OpenApiExample(
                'Erro de Estoque',
                summary='Livro Esgotado',
                description='Exemplo de resposta quando o livro não tem quantidade disponível.',
                value={
                    "livro": ["Este livro está esgotado no momento."]
                },
                status_codes=['400']
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        # Mantemos o comportamento padrão, pois a lógica está toda no Serializer
        return super().create(request, *args, **kwargs)
