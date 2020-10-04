# Jeu de données: application des amendements
*Jeu de données afin de faire un logiciel qui applique automatiquement les amendements*

Ce jeu de données contient des articles de loi avant l'application des amendements adoptés sur l'article, les amendements adoptés et l'article ainsi modifié par les amendements.

Prenons l'exemple du dossier `14-transparence_vie_publique_pjl__04_1erelecture_senat_commission__4_bis`:

`article_avant` contient:

>À la fin de l'article 4 de la loi n° 62-1292 du 6 novembre 1962 précitée, la référence : "loi n° 2011-1977 du 28 décembre 2011 de finances pour 2012" est remplacée par la référence : "loi organique n° du relative à la transparence de la vie publique".


`amendement_COM-40` contient:

>Au début de cet article, ajouter un paragraphe ainsi rédigé :
>
>I. – Au troisième alinéa du I de l’article 3 de la loi n° 62-1292 du 6 novembre 1962 précitée, les mots : « à l’article L.O. 135-1 » sont remplacés par les mots : « aux articles L.O. 136-4 et L.O. 136-5 ».


`article_apres` contient:

>I. - Au troisième alinéa du I de l'article 3 de la loi n° 62-1292 du 6 novembre 1962 précitée, les mots : "à l'article L. O. 135-1" sont remplacés par les mots : "aux articles L. O. 136-4 et L. O. 136-5".
>
>II. - À la fin de l'article 4 de la loi n° 62-1292 du 6 novembre 1962, la référence : "loi n° 2011-1977 du 28 décembre 2011 de finances pour 2012" est remplacée par la référence : "loi organique n° du relative à la transparence de la vie publique".

## Benchmark

| Algorithme        | Score   | Precision |
|-------------------|---------|-----------|
| [supprime articles](https://github.com/mdamien/demonstration-benchmark-application-des-amendements/blob/main/benchmark-suppression-simple.py) | 16.95 % | 16.95 % |
| [supprime articles quand amendement de suppression](https://github.com/mdamien/demonstration-benchmark-application-des-amendements/blob/main/benchmark-suppression-et-remplacement-precis.py) | 16.27 % | 71.64 % |

## Source

Les données viennent de https://www.lafabriquedelaloi.fr/, de https://www.nosdeputes.fr/ et de https://www.nossenateurs.fr/, les données sont donc sous [licence ODbL](https://vvlibri.org/fr/licence/odbl-10/legalcode/unofficial).

## Limitations

- La détection des amendements identiques n'est pas parfaite, il peut donc y avoir des amendements identiques
- Si plusieurs comissions ont été saisies, les amendements d'une commission saisie pour avis peuvent se retrouver dans les amendements alors qu'ils n'ont aucun effet
- Les amendements étant à la base du HTML, je les ai transformés en markdown pour les rendre plus lisible mais cette transformation peut ajouter des erreurs comme des "_" intempestifs.

## Projets connexes

- https://git.en-root.org/Seb35/duralex-tests
- https://git.en-root.org/Seb35/duralex-js
- https://github.com/Legilibre/DuraLex
- https://git.en-root.org/Seb35/metslesliens
- https://github.com/mdamien/executeur-de-lois (une petite demo)
