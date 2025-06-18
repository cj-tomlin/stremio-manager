import sys
import os

print("Current Working Directory:", os.getcwd())
print("\n sys.path:")
for p in sys.path:
    print(p)

try:
    print("\nAttempting to import httpx_oauth...")
    import httpx_oauth
    print("Successfully imported httpx_oauth")
    print(f"httpx_oauth location: {httpx_oauth.__file__}")
    
    print("\nAttempting to import httpx_oauth.clients...")
    import httpx_oauth.clients
    print("Successfully imported httpx_oauth.clients")
    print(f"httpx_oauth.clients location: {httpx_oauth.clients.__file__}")

    print("\nAttempting to import httpx_oauth.clients.trakt...")
    from httpx_oauth.clients.trakt import TraktOAuth2
    print("Successfully imported TraktOAuth2 from httpx_oauth.clients.trakt")
    print(f"TraktOAuth2 object: {TraktOAuth2}")

except ImportError as e:
    print(f"\nImportError: {e}")
except Exception as e:
    print(f"\nAn unexpected error occurred during import test: {e}")
