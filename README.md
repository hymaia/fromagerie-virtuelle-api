# fromagerie-virtuelle-inscription

Ce projet utilise [SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) pour être construit et déployé.

## Structure projet
Dans le dossier `fromagerie_virtuelle_register_function` se trouve le code de la lambda register.

Dans `template.yaml` il y a toute l'infra as code en Cloud Formation.

`samconfig.toml` contient la configuration de déploiement pour notre sam app.

## Test

Pour le moment il n'y a pas de tests.

## Deploy

```shell
sam build
sam deploy
```

## CI/CD

À chaque commit github actions déploie automatiquement la sam app sur le compte AWS de Franck Cussac.

## API

### S'enregistrer comme joueur

Pour s'enregistrer, faites un post sur le endpoint `register`. Exemple :

```shell
http POST https://x8jxwlic37.execute-api.eu-west-1.amazonaws.com/Prod/register mail=<mail> pseudo=<pseudo>

{
    "instructions": "Récupérez votre secret_key et gardez la précieusement sans la divulguer.",
    "mail": "mail",
    "pseudo": "pseudo",
    "secret_key": "11b4a846-5ab4-484b-9f05-f9a5c48f713a"
}
```

### Envoyer une réponse

Une réponse est un fichier json multiligne fait pour spark :
```json
{"exemple": "value"}
{"exemple": "value"}
{"exemple": "value"}
```

Le JSON n'est pas valide c'est pourquoi il faut l'envoyer comme texte dans un champs json de notre requête :
```shell
http POST https://x8jxwlic37.execute-api.eu-west-1.amazonaws.com/Prod/answer secret_key=11b4a846-5ab4-484b-9f05-f9a5c48f713a data=@test.json

{
    "data": "{\"test\": \"test\"}\n{\"test\": \"test\"}\n\n",
    "message": "Bien reçu !"
}
```
