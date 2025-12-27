## Get the api up and running (14-08-25)
- Setup database
- Setup dev env for Django
- Run the base api
- Test base api with dummy data from db
Done: 15-08-25

## Add authenticate wrapper to blog api (15-08-25)
- Add a dummy authenticate endpoint
- Let the endpoint accept username and pwd
- Validate the credentials
Done: 16-09-25

## Support multiple authenticators (16-09-25)
- Plan to support diff types of authenticators
- Initially add OAuth2 support
- Add support to sign in with google
Abandoned: 08-12-25
We should be the auth server, not google

## Research on OAuth2 (28-11-25)
- Create a table to store auth codes and tokens
    - user_id(fk), auth_code(varchar), 
    - access_token(varchar), refresh_token(varchar)
    - permissions(varchar)(comma-separated list)
- Define user attributes and permissions
- Define data structure for external clients
    - client id, redirect_uri (unique)
- Define and manage permissions for oauth tokens

