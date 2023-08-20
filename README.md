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

```shell
http POST https://pdpaci2ge1.execute-api.eu-west-1.amazonaws.com/Prod/signup username=<username> email=<email>
```

### S'authentifier pour jouer

```shell
http POST https://pdpaci2ge1.execute-api.eu-west-1.amazonaws.com/Prod/signin username=<username> password=<password>
```

Une fois son premier token obtenu, on peut utiliser le refresh token pour se réauthentifier à l'expiration du premier :
```shell
http POST https://pdpaci2ge1.execute-api.eu-west-1.amazonaws.com/Prod/signin/refresh refresh_token=<token>
```

### Envoyer une réponse

Exemple de JSON :

```json
{
  "predictions": {
    "roquefort": {"quantity_ordered":11888117},
    "raclette": {"quantity_ordered":21436453},
    "camembert": {"quantity_ordered":7144144},
    "emmental": {"quantity_ordered":7140079},
    "brie": {"quantity_ordered":19030271},
    "parmesan": {"quantity_ordered":11903091},
    "comté": {"quantity_ordered":11897341},
    "mimolette": {"quantity_ordered":11902662},
    "gouda": {"quantity_ordered":9512205},
    "fourme de Montbrison": {"quantity_ordered":2381163}
  },
  "month":"1"
}
```

```shell
http -A bearer -a <token> POST https://pdpaci2ge1.execute-api.eu-west-1.amazonaws.com/Prod/result @<file>
```
