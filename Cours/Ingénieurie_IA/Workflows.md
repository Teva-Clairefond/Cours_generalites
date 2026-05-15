# Comprendre les différents workflows :

https://www.anthropic.com/engineering/building-effective-agents

## Agent ou Workflow ?

https://www.anthropic.com/engineering/building-effective-agents

"Workflows are systems where LLMs and tools are orchestrated through predefined code paths.
Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."

"When more complexity is warranted, workflows offer predictability and consistency for well-defined tasks, whereas agents are the better option when flexibility and model-driven decision-making are needed at scale."


## Les frameworks :

A check :

"There are many frameworks that make agentic systems easier to implement, including:

    The Claude Agent SDK;
    Strands Agents SDK by AWS;
    Rivet, a drag and drop GUI LLM workflow builder; and
    Vellum, another GUI tool for building and testing complex workflows."

"We suggest that developers start by using LLM APIs directly: many patterns can be implemented in a few lines of code. If you do use a framework, ensure you understand the underlying code."




## Agent observability tool :

- Self-hosting
- Open Source 
- Besoin de "Governance (AI Gateway)” ? “Cet outil peut servir de point de contrôle central pour les appels IA, pas seulement de tableau de bord de monitoring.”


## Le LLM augmenté :

**Les augmentations majeures :**

"The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. Our current models can actively use these capabilities—generating their own search queries, selecting appropriate tools, and determining what information to retain."


Cache = optimisation technique pour ne pas envoyer plusieurs fois la même requête.

Memory = connaissance persistante ou semi-persistante utile à l’agent. Celui-ci place les informations qu'il trouve pertinentes dans sa mémoire. Ces informations peuvent être stockées sous différents formats, mais seront finalement convertis en tokens et ajoutés au contexte lors d'une commande/prompt.

Retrival = capacité du LLM à aller récupérer des informations hors de son corpus d'entrainement, dans l'ensemble des ressources auxquelles le LLM a accès.


**Amélioration des augmentations :**

"We recommend focusing on two key aspects of the implementation: tailoring these capabilities to your specific use case and ensuring they provide an easy, well-documented interface for your LLM."


## Les différents workflow :

### Prompt Chaining :

Décomposition des taches pas à pas : Le LLM effectue la 1ere tâche, analyse la sortie de la 1ere tâche, la prend en compte pour effectuer la 2eme tâche.

**Avantages et inconvients :**

perte de vitesse mais gain de précisions (ps: c'est ce que j'ai tendance à utilisé lors de mon vibecoding de projet lourds)

### Routing :

D'abords l'agent va classer la demande dans différentes catégories, puis :
1. Option - Un sous-agent spécialisé a traité la demande
2. Option - L'agent principal change de contexte pour traiter la demande

Avantages : Evite un contexte trop vaste pour le LLM, permet des réponses plus précises. Fonctionne bien quand il y a des catégories distinctes.

### Parallelisation : 

L'idée est de faire travailler plusieurs sous-agents en parallèle pour ensuite fusionner leur résultat.

Les deux idées :

- Sectionning : Une tâche est divisées en plusieurs sous-tâches différentes.
- Voting : La même tâche est effectuées plusieurs fois pour voir les différences de résultats.

Avantages :
- Sectionning : Gain de temps
- Voting : Obtenir des résultats dans lesquels il y a une plus grande confiance.

### Orchestrator - workers :

L'orchestrateur analyse l'entrée, définit les sous-tâches et les attribue aux sous-agents (les workers). Par la suite, c'est aussi lui qui joue le rôle d'aggregateur pour produire l'output final.

Ce workflow ressemble beaucoup à celui de la parallèlisation. La principale différence étant que c'est un LLM (orchestrateur) qui crée les sous-tâches, qui ne sont pas prédéfinies. L'entrée nécessitant une analyse.


### Evaluator-optimizer :

Un LLM générateur de contenu produit du code/texte jusqu'à ce qu'un LLM d'évalutation valide le l'output.

![alt text](image.png)

"When to use this workflow: This workflow is particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value."


