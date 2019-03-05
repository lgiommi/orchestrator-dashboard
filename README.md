# orchestrator-dashboard
INDIGO PaaS Orchestrator - Simple Graphical UI

Functionalities:
- IAM authentication
- Display user's deployments
- Display deployment details and template
- Delete deployment
- Create new deployment

# How to deploy the dashboard

Register a client in IAM with the following properties:

- redirect uri: http://<DASHBOARD_HOST>:<PORT>/oidc_callback
- scopes: 'openid', 'email', 'profile', 'offline_access'
- introspection endpoint enabled

Create the `client_secrets.json` file (see the [example](app/client_secrets-sample.json)):

````
{
    "web": {
        "issuer": "https://iam.deep-hybrid-datacloud.eu",
        "auth_uri": "https://iam.deep-hybrid-datacloud.eu/authorize",
        "client_id": "*****",
        "client_secret": "*****",
        "redirect_uris": [
            "http://<DASHBOARD_HOST>/*"
        ],
        "userinfo_uri": "https://iam.deep-hybrid-datacloud.eu/userinfo",
        "token_uri": "https://iam.deep-hybrid-datacloud.eu/token",
        "token_introspection_uri": "https://iam.deep-hybrid-datacloud.eu/introspect"
    }
}

````
Clone the tosca-templates repository to get a set of tosca templates that the dashboard will load, e.g.:
````
git clone https://github.com/indigo-dc/tosca-templates -b stable/v3.0
````

Run the docker container:

```
docker run -d -p 80:5001 --name='orchestrator-dashboard' \
           -e ORCHESTRATOR_URL=https://deep-paas.cloud.ba.infn.it/orchestrator \
           -e TOSCA_TEMPLATES_DIR=/tosca -e OIDC_CLIENT_SECRETS=/client_secrets.json \
           -e OIDC_VALID_ISSUERS=https://iam.deep-hybrid-datacloud.eu/ \
           -v $PWD/client_secrets.json:/client_secrets.json \
           -v $PWD/tosca-templates:/tosca \
           marica/orchestrator-dashboard:latest
```

Access the dashboard at http://<DASHBOARD_HOST>/

## Enable HTTPS

You would need to provide
- a pair certificate/key that the container will read from the container paths `/certs/cert.pem` and `/certs/key.pem`;
- the environment variable `ENABLE_HTTPS` set to `True`
- change the redirect_uri in the IAM client replacing http with https (https://<DASHBOARD_HOST>:<PORT>/oidc_callback) 

Run the docker container:
```
docker run -d -p 443:5001 --name='orchestrator-dashboard' \
           -e ORCHESTRATOR_URL=https://deep-paas.cloud.ba.infn.it/orchestrator \
           -e TOSCA_TEMPLATES_DIR=/tosca -e OIDC_CLIENT_SECRETS=/client_secrets.json \
           -e OIDC_VALID_ISSUERS=https://iam.deep-hybrid-datacloud.eu/ \
           -e ENABLE_HTTPS=True \
           -v $PWD/cert.pem:/certs/cert.pem \
           -v $PWD/key.pem:/certs/key.pem \
           -v $PWD/client_secrets.json:/client_secrets.json \
           -v $PWD/tosca-templates:/tosca \
           marica/orchestrator-dashboard:latest
```
Access the dashboard at https://<DASHBOARD_HOST>/


## How to build the docker image

```
git clone https://github.com/maricaantonacci/orchestrator-dashboard.git
cd orchestrator-dashboard
docker build -f docker/Dockerfile -t orchestrator-dashboard .
```




