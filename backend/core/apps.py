from django.apps import AppConfig
import threading
import requests


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Start the keep-alive function when the server starts
        from django.conf import settings

        def keep_alive():
            try:
                # Replace with your Render app's public URL
                app_url = "https://tesing-backend-deployment.onrender.com/"  # Replace with the actual URL
                requests.get(app_url)
                print(f"Pinged {app_url} successfully.")
            except Exception as e:
                print(f"Error pinging the server: {e}")

            # Schedule the function to run again in 14 minutes (14 * 60 = 840 seconds)
            threading.Timer(840, keep_alive).start()

        # Only run the keep-alive function in production mode
        if not settings.DEBUG:
            keep_alive()
