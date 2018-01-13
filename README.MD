Compilateur C--
=============

Réalisé dans le cadre du cours de compilation (APP4 Info - Polytech Paris-Sud) par :
* Léo MULLOT
 * Mathieu HIREL

Cours réalisé par [M. Lavergne](https://www.limsi.fr/fr/infos?login=lavergne)

## Prérequis

* Python 2.7

## Compilation

`python main.py <fichier cmm> `

Le fichier à compiler peut être passé par l'entrée standard

 Le compilateur sort sur la *sortie standard* le code compilé
 exemple d'utilisation
 `cat test.cmm |python main.py |MSM/msm`

## Execution

Pour éxecuter le code compiler il faut utiliser le compilateur [**MSM**](https://perso.limsi.fr/lavergne/msm.tgz)

## Tests unitaires

Un ensemble de tests unitaires sont disponibles.
Certains proviennent des [fichiers de tests](https://perso.limsi.fr/lavergne/tests.tgz) fournis dans le cadre du cours.

Pour les lancer:
`python -m unittest discover`



