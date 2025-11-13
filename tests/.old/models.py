# models.py
# Este arquivo define as CLASSES do nosso sistema.
# É o nosso "molde" para criar os dados.

class Produto:
    #Molde para representar um produto da loja.
    def __init__(self, id_produto, nome, preco, estoque):
        self.id_produto = id_produto  # int (identificador único)
        self.nome = nome            # str (ex: "Coca-Cola 2L")
        self.preco = preco          # float (ex: 9.50)
        self.estoque = estoque      # int (ex: 50)

    def __repr__(self):
        # Isso ajuda a "printar" o objeto de um jeito bonito
        return f"<Produto: {self.nome} (R$ {self.preco})>"

class Cliente:
    #Molde para representar um cliente que faz compras.
    def __init__(self, id_cliente, nome, cpf):
        self.id_cliente = id_cliente # int
        self.nome = nome           # str
        self.cpf = cpf             # str (ex: "123.456.789-00")

    def __repr__(self):
        return f"<Cliente: {self.nome}>"

class ItemVenda:
    #Molde para representar UM item DENTRO de uma venda.
    #Isso é crucial para o relacionamento!
    def __init__(self, produto, quantidade):
        # --- Relacionamento: Um ItemVenda TEM UM Produto ---
        self.produto = produto      # Objeto da classe Produto
        self.quantidade = quantidade  # int

    def calcular_subtotal(self):
        """Calcula o subtotal (preço do produto * quantidade)"""
        return self.produto.preco * self.quantidade

    def __repr__(self):
        return f"<{self.quantidade}x {self.produto.nome}>"

class Venda:
    #Molde para representar a transação de venda completa.
    def __init__(self, id_venda, cliente):
        self.id_venda = id_venda    # int

        # --- Relacionamento: Uma Venda TEM UM Cliente ---
        self.cliente = cliente      # Objeto da classe Cliente
        
        # --- Relacionamento: Uma Venda TEM VÁRIOS ItensVenda ---
        self.itens = []             # Esta será uma LISTA de objetos ItemVenda
        self.total = 0.0            # float

    def adicionar_item(self, produto, quantidade):
        #Adiciona um produto e sua quantidade na venda.
        #(Isso aqui já é uma "regra de negócio"!)
        # 1. Verifica se temos estoque
        if produto.estoque >= quantidade:
            # 2. Cria o objeto ItemVenda
            novo_item = ItemVenda(produto, quantidade)
            
            # 3. Adiciona o item na LISTA de itens da venda
            self.itens.append(novo_item)
            
            # 4. Abate do estoque (importante!)
            produto.estoque -= quantidade
            
            # 5. Recalcula o total da venda
            self.calcular_total_venda()
            print(f"Item adicionado: {novo_item}")
            return True
        else:
            print(f"Erro: Estoque insuficiente para {produto.nome}. (Disponível: {produto.estoque})")
            return False

    def calcular_total_venda(self):
        #Calcula o valor total da venda somando os subtotais dos itens.
        self.total = 0.0
        for item in self.itens:
            self.total += item.calcular_subtotal()

    def __repr__(self):
        return f"<Venda {self.id_venda} | Cliente: {self.cliente.nome} | Total: R$ {self.total}>"