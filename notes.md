## OAuth2 implementation

### Actors
    - Resource server
    - Resource owner
    - Authorisation server
    - Client
        - confidential
        - public

### Flow
    - Client requests a protected resource
    - Resource server requires authorisation proof
    - Client sends auth request to resource owner
    - Client returns an auth grant
        - credential (usn-pwd / session cookie)
    - Client give the auth grant to auth server
    - Auth server provides
        - either authorization code
            - in this case, client should exchange
            the auth code for a token by authenticating
            itself with the auth server
        - or access token (implicit)
    - Client sends the token to resource server
    - Res server sends the protected resource

We should use the grant type credentials
    (username-password or active session tokens)
Auth code grant type can be an extra, added later

So, the auth server response types can be token / code

### Client
    - id, name, description, redirect_uri

### Authorization
    - client_id, user_id (either)
    - auth_code, access_token, refresh_token, permissions

### Access Token
    - scope, duration, res owner, [RFC6750]
    - identifier for creds or encrypted creds within

### Primary implementation
    - Endpoints: authorization, token
        authorization will return a code using a grant type
        token will return a token using auth code

