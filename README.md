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

À faire avec Github Actions
