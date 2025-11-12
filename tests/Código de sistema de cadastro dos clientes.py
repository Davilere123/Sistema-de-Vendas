class Cliente:
    def __init__(self, id, nome, email, telefone, endereco):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

class SistemaCadastro:
    def __init__(self):
        self.clientes = {}
        self.proximo_id = 1

    def adicionar_cliente(self, nome, email, telefone, endereco):
        """Adiciona um novo cliente ao sistema."""
        cliente = Cliente(self.proximo_id, nome, email, telefone, endereco)
        self.clientes[self.proximo_id] = cliente
        self.proximo_id += 1
        print(f"Cliente {nome} cadastrado com sucesso! ID: {cliente.id}")
        return cliente.id

    def buscar_cliente(self, id):
        """Busca um cliente pelo ID."""
        if id in self.clientes:
            cliente = self.clientes[id]
            return cliente
        return None

    def listar_clientes(self):
        """Lista todos os clientes cadastrados."""
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
            return
        
        print("\n=== Lista de Clientes ===")
        for id, cliente in self.clientes.items():
            print(f"\nID: {cliente.id}")
            print(f"Nome: {cliente.nome}")
            print(f"Email: {cliente.email}")
            print(f"Telefone: {cliente.telefone}")
            print(f"Endereço: {cliente.endereco}")
            print("=" * 25)

    def atualizar_cliente(self, id, nome=None, email=None, telefone=None, endereco=None):
        """Atualiza os dados de um cliente."""
        cliente = self.buscar_cliente(id)
        if cliente:
            if nome:
                cliente.nome = nome
            if email:
                cliente.email = email
            if telefone:
                cliente.telefone = telefone
            if endereco:
                cliente.endereco = endereco
            print(f"Dados do cliente ID {id} atualizados com sucesso!")
            return True
        print("Cliente não encontrado.")
        return False

    def remover_cliente(self, id):
        """Remove um cliente do sistema."""
        if id in self.clientes:
            nome = self.clientes[id].nome
            del self.clientes[id]
            print(f"Cliente {nome} (ID: {id}) removido com sucesso!")
            return True
        print("Cliente não encontrado.")
        return False

def main():
    sistema = SistemaCadastro()
    
    while True:
        print("\n=== Sistema de Cadastro de Clientes ===")
        print("1. Adicionar Cliente")
        print("2. Buscar Cliente")
        print("3. Listar Clientes")
        print("4. Atualizar Cliente")
        print("5. Remover Cliente")
        print("6. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            sistema.adicionar_cliente(nome, email, telefone, endereco)

        elif opcao == "2":
            id = int(input("Digite o ID do cliente: "))
            cliente = sistema.buscar_cliente(id)
            if cliente:
                print("\n=== Dados do Cliente ===")
                print(f"Nome: {cliente.nome}")
                print(f"Email: {cliente.email}")
                print(f"Telefone: {cliente.telefone}")
                print(f"Endereço: {cliente.endereco}")
            else:
                print("Cliente não encontrado.")

        elif opcao == "3":
            sistema.listar_clientes()

        elif opcao == "4":
            id = int(input("Digite o ID do cliente: "))
            print("Digite os novos dados (ou deixe em branco para manter o atual):")
            nome = input("Novo nome: ")
            email = input("Novo email: ")
            telefone = input("Novo telefone: ")
            endereco = input("Novo endereço: ")
            sistema.atualizar_cliente(id, nome, email, telefone, endereco)

        elif opcao == "5":
            id = int(input("Digite o ID do cliente a ser removido: "))
            sistema.remover_cliente(id)

        elif opcao == "6":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()