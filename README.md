
# GraphQL Backend Skeleton

This repository contains an **async**, **Relay-compatible** GraphQL API built with Django and Strawberry. It provides a base skeleton for a cloud solution where users can create and manage apps.

## Features

- **Async Django models** (`User`, `DeployedApp`)
- **Relay-compatible Node interface** for global object identification
- **GraphQL DataLoader** batching for efficient nested lookups (`User.apps`)
- **Mutations** to `upgradeAccount` and `downgradeAccount`
- **Custom GraphQL view & context** for per-request DataLoader instances
- **Fixtures** for sample Hobby/Pro users and apps
- **Clean error handling** with GraphQLError

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- (Optional) Virtual environment tool (`venv`, `virtualenv`, `conda`)

### Installation

1. **Create & activate a virtual environment**  
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations & load fixtures**  
   ```bash
   python manage.py migrate
   python manage.py loaddata core/fixtures/initial_data.json
   ```

### Project Structure

```
.
├── core
│   ├── fixtures
│   │   └── initial_data.json
│   ├── loaders.py
│   ├── models.py
│   ├── schema.py
│   ├── views.py
│   └── context.py
├── wasmer_graphql_backend_challenge
│   ├── asgi.py
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Usage

1. **Start the development server**  
   ```bash
   python manage.py runserver
   ```

2. **Open GraphQL Playground**  
   Navigate to [http://localhost:8000/graphql](http://localhost:8000/graphql) to explore the schema and run queries/mutations.

### Example Queries

```graphql
# Fetch a user by raw ID (no Base64)
query {
  node(id: "u_123") {
    ... on User {
      id
      username
      plan
      apps {
        id
        active
      }
    }
  }
}
```

```graphql
# Upgrade a user plan
mutation {
  upgradeAccount(userId: "u_123") {
    id
    username
    plan
  }
}
```

## Testing & Debugging

- **SQL Logging**: Enable in `settings.py` to verify batching behavior.
- **Invalid ID Handling**: Node resolver raises `GraphQLError` for bad IDs.
- **Mutations**: Confirm upgrade/downgrade persist and re-query.

## Next Steps (Optional)

- Add Relay **connections** for paginated lists.
- Introduce **filtering** and **sorting** arguments.
- Write **unit tests** with `pytest-django`.
- Integrate **error logging** and monitoring for production.

---
