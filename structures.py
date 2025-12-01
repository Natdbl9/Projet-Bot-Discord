class Node:
    """Nœud de base pour la liste chaînée."""
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def peek(self):
        return self.top.data if self.top else None

    def to_list(self):
        elements = []
        current = self.top
        while current:
            elements.append(current.data)
            current = current.next
        return elements[::-1]

class ArbreNode:
    """Nœud de l'arbre de discussion (pour le questionnaire)."""
    def __init__(self, question, conclusion=None):
        self.question = question
        self.conclusion = conclusion
        self.yes = None
        self.no = None

C_C = ArbreNode("Fin : Vous êtes un programmeur de bas niveau ! Choisissez le **Langage C**.", conclusion="C")
C_PYTHON = ArbreNode("Fin : Vous aimez la lisibilité et la rapidité de développement ! Choisissez **Python**.", conclusion="Python")
C_JAVA = ArbreNode("Fin : Vous visez la portabilité et le monde de l'entreprise ! Choisissez **Java**.", conclusion="Java")
C_JS = ArbreNode("Fin : Le web est votre terrain de jeu ! Choisissez **JavaScript**.", conclusion="JavaScript")

Q_OOP = ArbreNode("Le concept de Programmation Orientée Objet (POO) est-il essentiel pour vous ?")
Q_OOP.yes = C_JAVA; Q_OOP.no = C_C

Q_WEB = ArbreNode("La création d'applications web interactives est-elle votre priorité ?")
Q_WEB.yes = C_JS; Q_WEB.no = C_PYTHON

Q_ROOT = ArbreNode("Avez-vous besoin d'une exécution rapide et d'un accès bas niveau à la mémoire ?")
Q_ROOT.yes = Q_OOP
Q_ROOT.no = Q_WEB

def get_root():
    """Retourne la racine de l'arbre."""
    return Q_ROOT

def traverse_tree(node, target_subject):
    """Vérifie si le sujet existe dans les conclusions de l'arbre."""
    if node is None: return False
    if node.conclusion and target_subject.lower() in node.conclusion.lower(): 
        return True
    return traverse_tree(node.yes, target_subject) or traverse_tree(node.no, target_subject)
