# Documentação da Estrutura de Dados: Sistema de Vendas

Este documento detalha a estrutura de dados escolhida para o projeto do Sistema de Vendas, justificando as escolhas técnicas e explicando o relacionamento entre as entidades, conforme solicitado.

## 1. Estruturas de Dados Utilizadas

Para atender aos requisitos de um sistema simples em Python, sem a complexidade inicial de um banco de dados, optamos por usar uma combinação de **Classes (Programação Orientada a Objetos)** e **Listas**.

### a. Classes (Arquivo `models.py`)

A principal estrutura de dados do nosso projeto são as **Classes**. Elas são a base da Programação Orientada a Objetos (POO) em Python.

**Justificativa da Escolha:**

* **Organização e Clareza:** O professor mencionou a importância de "como os dados aparecem" e "como uma pessoa de fora entenderia o código". As classes são perfeitas para isso. Em vez de usarmos dicionários soltos (`{"nome": "Coca", "preco": 5.0}`) ou listas paralelas (`nomes = ["Coca"], precos = [5.0]`), nós agrupamos todos os dados que pertencem a uma mesma "coisa" (como um `Produto`) em um só lugar.
* **Abstração do Mundo Real:** Classes nos permitem "modelar" o mundo real. Criamos uma classe `Produto`, uma classe `Cliente` e uma classe `Venda`, que representam diretamente as entidades do nosso sistema.
* **Agrupamento de Dados e Comportamento:** Uma classe não guarda só os *dados* (atributos, ex: `produto.nome`), mas também *comportamentos* (métodos/funções, ex: `venda.calcular_total_venda()`). Isso mantém o código organizado.

### b. Listas (`list`)

Dentro das nossas classes, usamos a estrutura de dados nativa do Python `list` (lista).

**Justificativa da Escolha:**

* A **Lista** é usada em um ponto crucial: dentro da classe `Venda`, no atributo `self.itens = []`.
* Isso é necessário para representar o relacionamento de "um para muitos". Uma (1) `Venda` pode conter muitos (N) `ItemVenda`. A lista é a estrutura perfeita para guardar essa coleção de "muitos".

### c. Por que não JSON ou Dicionários puros?

* **Dicionários (`dict`):** Poderíamos usar dicionários (ex: `produto = {"nome": "..."}`), mas isso se torna caótico rapidamente. Não há garantia de quais "chaves" existem, e não podemos anexar "comportamentos" (funções) a um dicionário da mesma forma que fazemos com uma classe.
* **JSON:** JSON é um formato para *armazenar* ou *transportar* dados (ex: salvar em um arquivo ou enviar pela internet). Ele não é uma estrutura de dados para *operar* o sistema em tempo real. Nossas classes Python (definidas em `models.py`) são a estrutura "viva" do sistema; elas *podem* ser convertidas para JSON na hora de salvar, mas o *modelo* principal são as classes.

---

## 2. Entidades e Relações

Baseado no `models.py`, nosso sistema possui 4 entidades principais e suas relações:

### Entidades Definidas:

1.  **`Produto`**: Representa um item que pode ser vendido.
    * *Atributos:* `id_produto`, `nome`, `preco`, `estoque`.
2.  **`Cliente`**: Representa a pessoa que compra.
    * *Atributos:* `id_cliente`, `nome`, `cpf`.
3.  **`Venda`**: Representa a transação/pedido completo.
    * *Atributos:* `id_venda`, `cliente` (relação), `itens` (relação), `total`.
4.  **`ItemVenda`**: Classe especial que "liga" um Produto a uma Venda.
    * *Atributos:* `produto` (relação), `quantidade`.

### Diagrama de Relações (Como elas se conectam)

O professor pediu para explicar "relações entre entidades (por exemplo, um usuário tem várias tarefas)". No nosso caso:

> **Uma `Venda` TEM UM `Cliente`**

* **Como funciona:** A classe `Venda` tem um atributo `self.cliente`. Nós não guardamos apenas o *ID* do cliente (ex: `5`), nós guardamos o **objeto** `Cliente` inteiro.
* **Exemplo em código:** `minha_venda.cliente` (Isso retorna o objeto `Cliente` associado).

> **Uma `Venda` TEM VÁRIOS `ItemVenda`**

* **Como funciona:** Este é o relacionamento "Um-para-Muitos". A classe `Venda` possui um atributo `self.itens` que é uma **Lista** (`list`).
* **Exemplo em código:** `minha_venda.itens` (Isso retorna uma lista, ex: `[<Item 1>, <Item 2>]`).

> **Um `ItemVenda` TEM UM `Produto`**

* **Como funciona:** A classe `ItemVenda` serve como "ponte". Ela guarda o **objeto** `Produto` que foi vendido e a `quantidade` que foi vendida.
* **Exemplo em código:** `meu_item.produto` (Isso retorna o objeto `Produto` associado).

### Exemplo prático da Relação:

Se o **Cliente** "José" compra **2** "Coca-Colas" e **1** "Salgado" em uma única **Venda**:

1.  Teremos 1 objeto `Venda`.
2.  O atributo `Venda.cliente` será o objeto `José`.
3.  O atributo `Venda.itens` será uma **lista** contendo 2 objetos `ItemVenda`:
    * `ItemVenda[0]` -> `produto` = (Objeto `Coca-Cola`), `quantidade` = 2
    * `ItemVenda[1]` -> `produto` = (Objeto `Salgado`), `quantidade` = 1