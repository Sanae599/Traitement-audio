# Traitement-audio

## **1. Contexte du projet**

Ce projet a été réalisé dans le cadre d’un brief ayant pour objectif  de **c****onstruire un système de traitement de données audio reproductible et traçable** ,comme on le ferait pour de la donnée texte ou tabulaire.

L’entreprise souhaite exploiter ses archives audio afin de développer une  **solution conversationnelle interne** .

Pour cela, elle a besoin d’un pipeline capable de :

* nettoyer,
* transformer,
* enrichir,
* augmenter les fichiers audio existants.

Ce projet montre comment construire un  **pipeline audio modulaire** , configurable via un fichier YAML, et capable d’appliquer différents effets audio.

## **2. Description du cas étudié**

Pour le pipeline, nous utilisons un fichier audio réel :

**Éléonore présente sa journée type** (voix propre, sans bruit de fond).

Nous avons ensuite ajouté un second fichier :

**Un bruit de train** , pour simuler une présentation faite dans des conditions réelles particulières (déplacement professionnel en train).

Le pipeline permet :

1. de **combiner** la voix propre avec un bruit de fond,
2. d’**appliquer des effets audio** pour générer un  **audio augmenté** .

Ces transformations permettent d’illustrer comment l’entreprise pourrait améliorer ses enregistrements archivés et les rendre exploitables.
