import networkx as nx
import matplotlib.pyplot as plt
def ler_atividades():
    atividades = {}
    while True:
        try:
            n = int(input("Digite o número de atividades: "))
            if n <= 0:
                print("O número de atividades deve ser positivo.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro.")

    for _ in range(n):
        while True:
            try:
                atividade = int(input("Atividade (número inteiro): "))
                duracao = int(input("Duração (dias, número inteiro): "))
                if duracao <= 0:
                    print("A duração deve ser um número positivo.")
                    continue
                precedentes = input("Precedentes/Anterior (separados por vírgula, deixe em branco se não houver): ")
                if precedentes:
                    precedentes = [int(x) for x in precedentes.split(',')]
                else:
                    precedentes = []
                atividades[atividade] = {'duracao': duracao, 'precedente': precedentes}
                break
            except ValueError:
                print("Entrada inválida. Por favor, insira números inteiros.")
    return atividades


def construir_grafo(atividades):
    G = nx.DiGraph()
    for atividade, dados in atividades.items():
        G.add_node(atividade, duracao=dados['duracao'])
        for precedente in dados['precedente']:
            G.add_edge(precedente, atividade)
    return G


def calcular_tempos(grafo):
    # Calcula os tempos de início mais cedo e término mais cedo
    for node in nx.topological_sort(grafo):
        es = max([grafo.nodes[p]['ef'] for p in grafo.predecessors(node)], default=0)
        ef = es + grafo.nodes[node]['duracao']
        grafo.nodes[node]['es'] = es
        grafo.nodes[node]['ef'] = ef

    # Calculo do tempo total
    tempo_total = max([data['ef'] for node, data in grafo.nodes(data=True)])

    # Calcula os tempos de inicio e fim
    for node in reversed(list(nx.topological_sort(grafo))):
        lf = min([grafo.nodes[s]['ls'] for s in grafo.successors(node)], default=tempo_total)
        ls = lf - grafo.nodes[node]['duracao']
        grafo.nodes[node]['ls'] = ls
        grafo.nodes[node]['lf'] = lf

    # Calcula folgas
    for node in grafo.nodes:
        grafo.nodes[node]['folga'] = grafo.nodes[node]['ls'] - grafo.nodes[node]['es']

    return tempo_total


def identificar_caminho_critico(grafo):
    caminho_critico = [node for node, data in grafo.nodes(data=True) if data['es'] == data['ls']]
    return caminho_critico


def imprimir_resultados(grafo, caminho_critico, tempo_total):
    print(f"Duração Total do Projeto: {tempo_total} dias")
    print(f"Caminho Crítico: {caminho_critico}")
    for atividade in grafo.nodes:
        print(f"Atividade {atividade}: ES = {grafo.nodes[atividade]['es']}, EF = {grafo.nodes[atividade]['ef']}, "
              f"LS = {grafo.nodes[atividade]['ls']}, LF = {grafo.nodes[atividade]['lf']}, "
              f"Folga = {grafo.nodes[atividade]['folga']}")


def visualizar_grafo(grafo, caminho_critico):
    # Adiciona o nó "fim"
    grafo.add_node('fim', duracao=0, es=0, ef=0, ls=0, lf=0, folga=0)
    for node in grafo.nodes:
        if grafo.out_degree(node) == 0 and node != 'fim':
            grafo.add_edge(node, 'fim')

    pos = nx.planar_layout(grafo)
    node_colors = ['red' if node in caminho_critico or node == 'fim' else 'lightblue' for node in grafo.nodes()]

    plt.figure(figsize=(12, 8))
    nx.draw(grafo, pos, with_labels=True, node_size=3000, node_color=node_colors, font_size=10, font_weight='bold')

    edge_labels = {(u, v): grafo.nodes[v]['duracao'] for u, v in grafo.edges()}
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)

    # Adiciona labels para os nós com os tempos calculados
    node_labels = {
        node: f"ES: {data['es']}\nEF: {data['ef']}\nLS: {data['ls']}\nLF: {data['lf']}\nFolga: {data['folga']}"
        for node, data in grafo.nodes(data=True)
    }
    nx.draw_networkx_labels(grafo, pos, labels=node_labels, font_size=8, font_color='black', verticalalignment='bottom')

    plt.show()
def main():
    atividades = ler_atividades()
    grafo = construir_grafo(atividades)
    tempo_total = calcular_tempos(grafo)
    caminho_critico = identificar_caminho_critico(grafo)
    imprimir_resultados(grafo, caminho_critico, tempo_total)
    visualizar_grafo(grafo, caminho_critico)

if __name__ == "__main__":
    main()
