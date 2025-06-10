from flask import Flask, jsonify # Keep existing imports
import os
import graphene
from flask_graphql import GraphQLView # New import for the view

app = Flask(__name__)

# --- Sample Data ---
sample_users_data = [
    {
        "id": "1",
        "name": "Alice Wonderland",
        "email": "alice@example.com"
    },
    {
        "id": "2",
        "name": "Bob The Builder",
        "email": "bob@example.com"
    },
    {
        "id": "3",
        "name": "Charlie Brown",
        "email": "charlie@example.com"
    }
]

# --- GraphQL Schema Definition ---
class UserType(graphene.ObjectType):
    id = graphene.String(description="The ID of the user.")
    name = graphene.String(description="The name of the user.")
    email = graphene.String(description="The email address of the user.")

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType, description="Retrieves all users.")
    user = graphene.Field(UserType,
                          id=graphene.String(required=True, description="The ID of the user to retrieve."),
                          description="Retrieves a single user by their ID.")

    def resolve_all_users(root, info):
        # Convert dictionary data to UserType instances
        return [UserType(id=user['id'], name=user['name'], email=user['email']) for user in sample_users_data]

    def resolve_user(root, info, id):
        for user_data in sample_users_data:
            if user_data['id'] == id:
                # Convert dictionary data to UserType instance
                return UserType(id=user_data['id'], name=user_data['name'], email=user_data['email'])
        return None

schema = graphene.Schema(query=Query)

# --- Add GraphQL Route ---
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # Enable GraphiQL interface
    )
)

# --- Existing Flask Routes ---
@app.route('/')
def hello_world():
    return jsonify(message="Hello, World! Visit /graphql for the GraphQL API.") # Updated message

# The __main__ block for running the app should be kept as is.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
