# Flask API with Heroku Deployment

This is a sample Flask API that can be automatically deployed to Heroku using GitHub Actions.

## Deployment

To deploy this application to Heroku, you need to set the following secrets in your GitHub repository settings:

1.  `HEROKU_API_KEY`: Your Heroku API key. You can find this in your Heroku account settings.
2.  `HEROKU_APP_NAME`: The name of your Heroku application. This application must be created in Heroku beforehand.

Once these secrets are set, any push to the `main` branch will trigger the deployment workflow.

## API Endpoint

-   `GET /`: Returns a simple JSON message: `{"message": "Hello, World!"}`
