import java.util.LinkedList;
import java.util.Queue;

class Produto {
    String nome;
    float preco;

    Produto(String nome, float preco) {
        this.nome = nome;
        this.preco = preco;
    }
}

public class teste {
    public static void main(String[] args) {
        Queue<Produto> fila = new LinkedList<>();

        fila.offer(new Produto("Melancia", 10.50f));
        fila.offer(new Produto("Arroz", 8f));
        fila.offer(new Produto("Laranja", 5.75f));
        fila.offer(new Produto("Feijão", 12f));

        float soma = 0f;

        for (Produto p : fila) {
            soma += p.preco;
        }

        while (!fila.isEmpty()) {
            Produto p = fila.poll();
            System.out.println("* o produto*: " + p.nome + ", preço: " + p.preco);
        }

        System.out.println("O valor total é de: " + soma);
    }
}