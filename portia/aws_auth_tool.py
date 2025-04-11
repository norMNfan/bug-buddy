# # Import these at the top of your Flask app file
# import os
# import secrets
# import boto3
# import json
# import time
# import urllib.parse
# from typing import Dict

# # Add these configurations to your Flask app
# # These could be in a config file or environment variables
# AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
# REDIRECT_URI = os.environ.get("REDIRECT_URI")  # Your backend callback endpoint
# YOUR_APP_DOMAIN = os.environ.get("YOUR_APP_DOMAIN")  # Your application domain
# FRONTEND_SUCCESS_URL = os.environ.get("FRONTEND_SUCCESS_URL")  # Where to redirect after success

# # Store state to prevent CSRF (you might want to use your app's session or database for this)
# active_states = {}

# # Add this function to your existing Flask app
# def get_aws_login_url() -> Dict[str, str]:
#     """
#     Generate a URL for users to sign in with their AWS account.
    
#     Returns:
#         Dict containing the login URL for the frontend to redirect to
#     """
#     # Generate a random state for CSRF protection
#     state = secrets.token_urlsafe(32)
    
#     # Store state with timestamp for cleanup and verification
#     active_states[state] = {
#         "created_at": time.time(),
#         "used": False
#     }
    
#     # Clean up expired states (older than 10 minutes)
#     current_time = time.time()
#     expired_states = [s for s, data in active_states.items() 
#                      if current_time - data["created_at"] > 600]
#     for s in expired_states:
#         active_states.pop(s, None)
    
#     # Create signin URL with state
#     callback_url = f"{REDIRECT_URI}?state={state}"
    
#     # AWS account login URL
#     signin_url = (
#         f"https://signin.aws.amazon.com/oauth?response_type=code"
#         f"&client_id=arn:aws:iam::015428540659:user/homepage"  # AWS console client
#         f"&redirect_uri={urllib.parse.quote_plus(callback_url)}"
#         f"&state={state}"
#     )
    
#     return {"auth_url": signin_url}


# # Add this function to verify the AWS credentials
# def verify_aws_credentials() -> Dict[str, bool]:
#     """
#     Verify the stored AWS credentials are valid.
#     """
#     try:
#         # Create a simple AWS client to test credentials
#         sts_client = boto3.client(
#             'sts',
#             aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
#             aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
#             aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
#             region_name=AWS_REGION
#         )
        
#         # Call GetCallerIdentity to verify credentials
#         response = sts_client.get_caller_identity()
        
#         return {
#             "authenticated": True,
#             "aws_account_id": response.get("Account"),
#             "user_arn": response.get("Arn")
#         }
#     except Exception as e:
#         return {
#             "authenticated": False,
#             "message": str(e)
#         }

# # Optional: Add an endpoint to verify authentication status
# @app.route('/aws/status', methods=['GET'])
# def aws_auth_status():
#     """
#     Check if the user is authenticated with AWS.
#     """
#     status = verify_aws_credentials()
#     return jsonify(status)