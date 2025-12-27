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
        - credential (usn-pwd / session) (implicit)
        - code (auth code) (explicit)
    - Client give the auth grant to auth server
    - Auth server returns an access token
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

