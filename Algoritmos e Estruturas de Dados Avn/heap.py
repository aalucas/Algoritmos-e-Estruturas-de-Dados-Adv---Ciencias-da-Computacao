import heapq
import itertools

class PriorityQueue:
    REMOVED = "<removed-task>"

    def __init__(self):
        self.heap = []  # lista de entradas: [priority, count, task]
        self.entry_finder = {}  # task -> entry
        self.counter = itertools.count()  # quebra empates

    def add_task(self, task, priority=0):
        """Adiciona uma tarefa ou atualiza a prioridade se já existir."""
        if task in self.entry_finder:
            # marca a entrada antiga como removida
            old_entry = self.entry_finder.pop(task)
            old_entry[2] = self.REMOVED
        entry = [priority, next(self.counter), task]
        self.entry_finder[task] = entry
        heapq.heappush(self.heap, entry)

    def pop_task(self):
        """Remove e retorna a tarefa com menor prioridade. Levanta KeyError se vazio."""
        while self.heap:
            priority, _, task = heapq.heappop(self.heap)
            if task is not self.REMOVED and task != self.REMOVED:
                # entrada válida
                self.entry_finder.pop(task, None)
                return task, priority
            # caso seja removida/obsoleta, ignora e continua
        raise KeyError("pop from an empty priority queue")

    def change_priority(self, task, new_priority):
        """Altera a prioridade de uma tarefa existente (ou adiciona se não existir)."""
        self.add_task(task, new_priority)

    def __len__(self):
        return len(self.entry_finder)

    def __repr__(self):
        items = [(entry[0], entry[2]) for entry in self.entry_finder.values()]
        items_sorted = sorted(items, key=lambda x: x[0])
        return f"PriorityQueue({items_sorted})"

def test_priority_queue():
    pq = PriorityQueue()
    # Exemplo com Linguagens de Programação -> Definição a Priorização de Estudos destas Linguagens
    print("Inicializando fila de prioridade e adicionando Linguagens de Programação...")
    pq.add_task("JavaScript", 5)
    pq.add_task("React", 1)
    pq.add_task("Java", 3)
    print(pq)

    print("\nInserindo nova tarefa Python (prioridade 2)...")
    pq.add_task("Python", 2)
    print(pq)

    print("\nAlterando prioridade de JavaScript para 0 (mais urgente)...")
    pq.change_priority("JavaScript", 0)
    print(pq)

    print("\nRemovendo Linguagens de Programação na ordem de prioridade:")
    popped = []
    try:
        while True:
            task, prio = pq.pop_task()
            print(f"  Removido: {task} (prioridade {prio})")
            popped.append((task, prio))
    except KeyError:
        print("  Fila vazia.")

    expected_order = [("JavaScript", 0), ("React", 1), ("Python", 2), ("Java", 3)]
    # Verifica apenas a ordem dos nomes e prioridades conhecidas (algumas prioridades podem variar se alteradas)
    assert [t for t, _ in popped] == [t for t, _ in expected_order], "Ordem de remoção incorreta"
    print("\nTeste concluído com sucesso.")

if __name__ == "__main__":
    test_priority_queue()