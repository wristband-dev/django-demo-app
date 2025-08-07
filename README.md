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

# Django Demo Application

A clean Django demo application that demonstrates proper project structure and is ready for Wristband authentication integration.

## 🚀 Quick Start

### With Makefile

#### One-time setup
make install

#### Start development server
make dev

#### Run migrations (if needed later)
make migrate

#### See all available commands
make help

#### Clean up
make clean

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

4. **Visit the application:**
   Open http://localhost:6001 in your browser

## 📁 Project Structure

```
wristband_django_demo/
├── manage.py                    # Django management script
├── demo_project/               # Django project (settings, config)
│   ├── __init__.py
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI configuration
├── demo_app/                   # Django app (functionality)
│   ├── __init__.py
│   ├── apps.py                 # App configuration
│   ├── models.py               # Data models (empty for now)
│   ├── views.py                # View logic
│   └── urls.py                 # App URL patterns
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   └── demo_app/               # App-specific templates
│       └── hello_world.html
│       └── home.html
│       └── profile.html
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🎯 Current Features

- ✅ **Standard Django structure** - Project/app separation
- ✅ **Class-based views** - Modern Django view patterns
- ✅ **Template inheritance** - DRY template structure
- ✅ **Bootstrap styling** - Clean, responsive UI
- ✅ **URL namespacing** - Organized URL patterns
- ✅ **Static files ready** - Configured for CSS/JS

## 📄 Available Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Welcome page with feature overview |
| Hello World | `/hello-world/` | Future protected page |
| Profile | `/profile/` | Future user profile page |
| API Example | `/api/hello/` | JSON API endpoint |

## 🔜 Next Steps

This demo is ready for Wristband authentication integration. The next phase will add:

1. **Authentication SDK** - Install and configure Wristband Django SDK
2. **Protected routes** - Add `@login_required` decorators
3. **User context** - Display authenticated user information
4. **Auth UI** - Login/logout buttons and flows
5. **API integration** - Demonstrate access token usage

## 🏗️ Architecture Decisions

### Why Project/App Separation?
- **demo_project/** contains Django configuration (settings, URLs, WSGI)
- **demo_app/** contains application logic (views, models, templates)
- This mirrors how real Django applications are structured
- Makes it easy to add more apps later

### Why Class-Based Views?
- More maintainable than function-based views
- Better code reuse and inheritance
- Easier to add authentication decorators
- Standard in modern Django development

### Why Template Inheritance?
- **base.html** contains common layout (navbar, footer, styles)
- Individual templates extend base and add specific content
- Easy to maintain consistent UI across pages
- Simple to add authentication elements globally

## 🧪 Testing the Demo

1. **Home page** - Overview and navigation
2. **Hello World** - Placeholder for future protected content
3. **Profile** - Placeholder for user information
4. **API endpoint** - JSON response example

## 💡 Learning Django

This demo demonstrates core Django concepts:

- **MVT Pattern** - Models, Views, Templates
- **URL routing** - How URLs map to views
- **Template system** - Django's template language
- **Static files** - CSS, JavaScript, images
- **Apps** - Modular Django components
- **Settings** - Django configuration

Perfect for developers new to Django who want to understand the framework before adding authentication!

<br/>

---

# Wristband Multi-Tenant Demo App for Django (Python)

The Django backend handles all authentication flows, including:
- Storing client ID and secret
- Handling OAuth2 authorization code flow redirections
- Managing session cookies
- Token refresh
- API orchestration

When an unauthenticated user attempts to access the frontend, it will redirect to the Django Login View, which in turn redirects the user to Wristband to authenticate. Wristband then redirects the user back to your application's Callback Endpoint which sets a session cookie before returning the user's browser to the frontend project.

<br>
<hr />
<br>

## Requirements

This demo app requires the following prerequisites:

### Python 3
1. Visit [Python Downloads](https://www.python.org/downloads/)
2. Download and install the latest Python 3 version
3. Verify the installation by opening a terminal or command prompt and running:
```bash
python --version # Should show Python 3.x.x
```

<br>
<hr>
<br>

## Getting Started

You can start up the demo application in a few simple steps.

### 1) Sign up for a Wristband account

First, make sure you sign up for a Wristband account at [https://wristband.dev](https://wristband.dev).

### 2) Provision the Django demo application in the Wristband Dashboard

After your Wristband account is set up, log in to the Wristband dashboard.  Once you land on the home page of the dashboard, click the button labelled "Add Demo App".  Make sure you choose the following options:

- Step 1: Subject to Authenticate - Humans
- Step 2: Application Framework - Django (Python)

You can also follow the [Demo App Guide](https://docs.wristband.dev/docs/setting-up-a-demo-app) for more information.

### 3) Apply your Wristband configuration values

After completing demo app creation, you will be prompted with values that you should use to create environment variables for the Django server. You should see:

- `APPLICATION_VANITY_DOMAIN`
- `CLIENT_ID`
- `CLIENT_SECRET`

Copy those values, then create an environment variable file for the Django server at: `<root_dir>/.env`. Once created, paste the copied values into this file.

### 4) Install dependencies

From the root directory of this project, you can install all required dependencies for both the frontend and backend with a single command:

```bash
npm run setup
```

### 5) Run the application

While still in the root directory, you can start the demo application with:

```bash
npm start
```

<br>
<hr>
<br>

## How to interact with the demo app

The NextJS server starts on port 3001, and the Django server starts on port 6001. NextJS is configured with rewrites to forward all `/api/*` requests to the Django backend at `http://localhost:6001/api/*`. This allows the frontend to make clean API calls using relative URLs like `/api/session` while keeping the backend services separate and maintainable. The Django server includes CORS middleware to allow cross-origin requests from the NextJS frontend.

### Signup Users

You can sign up your first customer on the Signup Page at the following location:

- `https://{application_vanity_domain}/signup`, where `{application_vanity_domain}` should be replaced with the value of the "Application Vanity Domain" value of the application (found in the Wristband Dashboard).

This signup page is hosted by Wristband. Completing the signup form will provision both a new tenant with the specified tenant domain name and a new user that is assigned to that tenant.

### Application-level Login (Tenant Discovery)

Users of this app can access the Application-level Login Page at the following location:

- `https://{application_vanity_domain}/login`, where `{application_vanity_domain}` should be replaced with the value of the "Application Vanity Domain" value of the application.

This login page is hosted by Wristband. Here, the user will be prompted to enter either their email or their tenant's domain name, redirecting them to the Tenant-level Login Page for their specific tenant.

### Tenant-level Login

If users wish to directly access the Tenant-level Login Page without going through the Application-level Login Page, they can do so at:

- `https://localhost:6001/api/auth/login?tenant_domain={tenant_domain}`, where `{tenant_domain}` should be replaced with the desired tenant's domain name.

This login page is hosted by Wristband. Here, the user will be prompted to enter their credentials to login to the application.

### Home Page

The home page of the app can be accessed at `http://localhost:3001`. When the user is not authenticated, they will only see a Login button that will take them to the Application-level Login/Tenant Discovery page.

### Architecture

The application in this repository utilizes the Backend for Frontend (BFF) pattern, where Django is the backend for the NextJS/React frontend. The server is responsible for:

- Storing the client ID and secret.
- Handling the OAuth2 authorization code flow redirections to and from Wristband during user login.
- Creating the application session cookie to be sent back to the browser upon successful login.  The application session cookie contains the access and refresh tokens as well as some basic user info.
- Refreshing the access token if the access token is expired.
- Orchestrating all API calls from the frontend to Wristband.
- Destroying the application session cookie and revoking the refresh token when a user logs out.

API calls made from NextJS/React to Django pass along the application session cookie and a [CSRF token header](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie) (parsed from the CSRF cookie) with every request.  The server has an auth middleware for all protected routes responsbile for:

- Validating the session and refreshing the access token (if necessary)
- Validating the CSRF token

Wristband hosts all onboarding workflow pages (signup, login, etc), and the Django server will redirect to Wristband in order to show users those pages.

<br>
<hr>
<br>

## Wristband Django Auth SDK

This demo app is leveraging the [Wristband django-auth SDK](https://github.com/wristband-dev/django-auth) for all authentication interaction in the Django server. Refer to that GitHub repository for more information.

<br>

## CSRF Protection

Cross Site Request Forgery (CSRF) is a security vulnerability where attackers trick authenticated users into unknowingly submitting malicious requests to your application. This demo app is leveraging a technique called the Syncrhonizer Token Pattern to mitigate CSRF attacks by employing two cookies: a session cookie for user authentication and a CSRF token cookie containing a unique token. With each request, the CSRF token is included both in the cookie and the request payload, enabling server-side validation to prevent CSRF attacks.

Refer to the [OWASP CSRF Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) for more information about this topic.

> [!WARNING]
> Your own application should take effort to mitigate CSRF attacks in addition to any Wristband authentication, and it is highly recommended to take a similar approach as this demo app to protect against thse types of attacks.

Within the demo app code base, you can search in your IDE of choice for the text `CSRF_TOUCHPOINT`.  This will show the various places in both the NextJS/React frontend code and Django backend code where CSRF is involved.

<br/>

## Questions

Reach out to the Wristband team at <support@wristband.dev> for any questions regarding this demo app.

<br/>
