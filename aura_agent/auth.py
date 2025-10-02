import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes required for the application.
# For now, we'll request read-only access to Gmail.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_google_credentials():
    """
    Handles Google authentication and returns valid credentials.
    - Checks for existing `token.json`.
    - If not found or invalid, runs the OAuth 2.0 flow.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # The credentials.json file must be downloaded from the Google Cloud Console
            # and placed in the same directory as this script.
            if not os.path.exists("credentials.json"):
                print("Error: `credentials.json` not found.")
                print("Please download your OAuth 2.0 Client ID from the Google Cloud Console and place it here.")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def get_gmail_service():
    """
    Authenticates and returns a Gmail API service object.
    """
    creds = get_google_credentials()
    if creds:
        try:
            service = build("gmail", "v1", credentials=creds)
            return service
        except Exception as e:
            print(f"An error occurred while building the Gmail service: {e}")
            return None
    return None

if __name__ == "__main__":
    # This is for testing the authentication flow directly.
    print("Attempting to authenticate with Google...")
    service = get_gmail_service()
    if service:
        print("Successfully authenticated and created Gmail service client.")
        # You can test the service by getting the user's profile
        profile = service.users().getProfile(userId="me").execute()
        print(f"Authenticated as: {profile['emailAddress']}")
    else:
        print("Authentication failed. Please check the console for errors.")