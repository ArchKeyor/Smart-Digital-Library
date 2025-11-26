from rest_framework import serializers
from .models import Emprestimo
from virtuallibrary.models import Book

fields = '__all__'  # Expõe todos os campos do modelo


class LivroSerializer(serializers.ModelSerializer):
    # Dica de ouro: StringRelatedField mostra o nome da categoria em vez do ID (opcional)
    categoria_nome = serializers.ReadOnlyField(source='categoria.nome')

    class Meta:
        model = Book
        fields = ['id', 'titulo', 'autor', 'categoria',
                  'categoria_nome', 'publicado_em', 'capa']


class EmprestimoSerializer(serializers.ModelSerializer):
    livro_titulo = serializers.ReadOnlyField(source='livro.titulo')
    livro_autor = serializers.ReadOnlyField(source='livro.autor')
    livro_capa_url = serializers.ImageField(
        source='livro.capa', read_only=True)

    class Meta:
        model = Emprestimo
        fields = ['id', 'nome_aluno', 'livro', 'livro_titulo', 'livro_autor',
                  'livro_capa_url', 'data_emprestimo', 'data_devolucao', 'devolvido']

    def validate_cpf_aluno(self, value):
        # Validação simples de tamanho (pode implementar algoritmo de CPF real aqui)
        if len(value) < 11:
            raise serializers.ValidationError(
                "CPF inválido. Verifique os dígitos.")
        return value

    def validate(self, data):
        """
        Validações que envolvem múltiplos campos ou lógica de negócio
        """
        # 1. Regra de Estoque (apenas na criação)
        # if not self.instance:  # Se não tem instância, é um CREATE
        #     livro = data.get('livro')
        #     if livro.quantidade <= 0:
        #         raise serializers.ValidationError(
        #             {"livro": "Este livro está esgotado no momento."})

        # 2. Regra de Data
        if data.get('data_devolucao') and data.get('data_emprestimo'):
            if data['data_devolucao'] < data['data_emprestimo']:
                raise serializers.ValidationError(
                    {"data_devolucao": "A devolução não pode ser antes do empréstimo."})

        return data

    # def create(self, validated_data):
    #     # Sobrescreve o create para diminuir o estoque automaticamente
    #     livro = validated_data['livro']
    #     livro.quantidade -= 1
    #     livro.save()
    #     return super().create(validated_data)
