<div align="center">
  <a href="https://wristband.dev">
    <picture>
      <img src="https://assets.wristband.dev/images/email_branding_logo_v1.png" alt="Github" width="297" height="64">
    </picture>
  </a>
  <p align="center">
    Enterprise-ready auth that is secure by default, truly multi-tenant, and ungated for small businesses.
  </p>
  <p align="center">
    <b>
      <a href="https://wristband.dev">Website</a> •
      <a href="https://docs.wristband.dev">Documentation</a>
    </b>
  </p>
</div>

<br/>

---

<br/>

# Wristband Multi-Tenant Demo App for Django (Python)

The Django backend handles all authentication flows, including:
- Storing client ID and secret
- Handling OAuth2 authorization code flow redirections
- Managing session cookies
- Cross-site Request Forgery (CSRF Protection)
- Token refresh

When an unauthenticated user attempts to access the a protected page or API, it will redirect to the Django Login View, which in turn redirects the user to Wristband to authenticate. Wristband then redirects the user back to your application's Callback View which sets a session cookie before returning the user to the browser.

<br>

---

<br>

## Requirements

This demo app requires the following prerequisites:

### Python 3.10 or higher

1. Visit [Python Downloads](https://www.python.org/downloads/)
2. Download and install the latest Python 3 version
3. Verify the installation by opening a terminal or command prompt and running:

```bash
# On macOS/Linux (should show Python 3.x.x)
python3 --version

# On Windows (should show Python 3.x.x)
py -3 --version
```

<br>

---

<br>

## Getting Started

You can start up the demo application in a few simple steps.

### 1) Sign up for a Wristband account

First, make sure you sign up for a Wristband account at [https://wristband.dev](https://wristband.dev).

### 2) Provision the Django demo application in the Wristband Dashboard

After your Wristband account is set up, log in to the Wristband dashboard.  Once you land on the home page of the dashboard, click the "Add Application" button.  Make sure you choose the following options:

- Step 1: Try a Demo
- Step 2: Subject to Authenticate - Humans
- Step 3: Application Framework - Django Backend with Server-Side Templates

You can also follow the [Demo App Guide](https://docs.wristband.dev/docs/setting-up-a-demo-app) for more information.

### 3) Apply your Wristband configuration values

After completing demo app creation, you will be prompted with values that you should use to create environment variables for the Django server. You should see:

- `APPLICATION_VANITY_DOMAIN`
- `CLIENT_ID`
- `CLIENT_SECRET`

Copy those values, then create an environment variable file for the Django server at: `<root_dir>/.env`. Once created, paste the copied values into this file.

### 4) Install dependencies

From the root directory of this project, you can install all required dependencies by running the following command:

```bash
make install
```

### 5) Run the application

While still in the root directory, you can start the demo application with:

```bash
make run
```

### 6) Cleaning up

Whe you are done testing the demo app, you can clean up your Python virtual environment with:

```bash
make clean
```

<br>

---

<br>

## How to interact with the demo app

The Django server starts on port 6001.

### Home Page

The home page of the app can be accessed at `http://localhost:6001`. When the user is not authenticated, they will see a Login button that will take them to the Application-level Login/Tenant Discovery page.

### Signup Users

You can sign up your first customer on the Signup Page at the following location:

- `https://{application_vanity_domain}/signup`, where `{application_vanity_domain}` should be replaced with the value of the "Application Vanity Domain" value of the application (found in the Wristband Dashboard).

This signup page is hosted by Wristband. Completing the signup form will provision both a new tenant with the specified tenant name and a new user that is assigned to that tenant.

### Application-level Login (Tenant Discovery)

Users of this app can access the Application-level Login Page at the following location:

- `https://{application_vanity_domain}/login`, where `{application_vanity_domain}` should be replaced with the value of the "Application Vanity Domain" value of the application.

This login page is hosted by Wristband. Here, the user will be prompted to enter either their email or their tenant's name, redirecting them to the Tenant-level Login Page for their specific tenant.

### Tenant-level Login

If users wish to directly access the Tenant-level Login Page without going through the Application-level Login Page, they can do so at:

- `https://localhost:6001/api/auth/login?tenant_name={tenant_name}`, where `{tenant_name}` should be replaced with the desired tenant's name.

This login page is hosted by Wristband. Here, the user will be prompted to enter their credentials to login to the application.

### Architecture

The application in this repository utilizes the Backend Server Integration Pattern, where Django is the backend and serves up server-side templates on the frontend. The server is responsible for:

- Storing the client ID and secret.
- Handling the OAuth2 authorization code flow redirections to and from Wristband during user login.
- Creating the application session cookie to be sent back to the browser upon successful login.  The application session cookie contains the access and refresh tokens as well as some basic user info.
- Refreshing the access token if the access token is expired.
- Orchestrating all API calls from the frontend to Wristband.
- Destroying the application session cookie and revoking the refresh token when a user logs out.

Page and API calls made from the browser to the server pass along the application session cookie and a [CSRF token header](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie) (parsed from the CSRF cookie) with every request.  The server has an auth middleware for all protected routes responsbile for validating the session and refreshing the access token (if necessary).

Wristband hosts all onboarding workflow pages (signup, login, etc), and the Django server will redirect to Wristband in order to show users those pages.

Within the demo app code base, you can search in your IDE of choice for the text `__WRISTBAND__`.  This will show the various places in the code where either auth, sessions, or CSRF is involved.

<br>
<hr>
<br>

## Wristband Django Auth SDK

This demo app is leveraging the [Wristband django-auth SDK](https://github.com/wristband-dev/django-auth) for all authentication interaction in the Django server. Refer to that GitHub repository for more information.

<br/>

## Questions

Reach out to the Wristband team at <support@wristband.dev> for any questions regarding this demo app.

<br/>
