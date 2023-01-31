from google.auth import jwt


def receive_authorized_get_request(request):
    """
    receive_authorized_get_request takes the "Authorization" header from a
    request, decodes it using the google-auth client library, and returns
    back the email from the header to the caller.
    """
    auth_header = request.headers.get("Authorization")
    # print('auth_header', auth_header)
    if auth_header:

        # split the auth type and value from the header.
        auth_type, creds = auth_header.split(" ", 1)

        if auth_type.lower() == "bearer":
            claims = jwt.decode(creds, verify=False)
            return f"Hello, {claims['email']}!\n"

        else:
            return f"Unhandled header format ({auth_type}).\n"
    return "Hello, anonymous user.\n"
