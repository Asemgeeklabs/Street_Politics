import subprocess

def clear_celery_logs(container_name='street_celery'):
    try:
        # Get the container ID of the celery worker
        container_id = subprocess.check_output(
            ['docker', 'ps', '-qf', f'name={container_name}']
        ).decode().strip()

        if not container_id:
            print("No running Celery container found.")
            return

        # Get the log file path of the container
        log_path = subprocess.check_output(
            ['docker', 'inspect', '--format={{.LogPath}}', container_id]
        ).decode().strip()

        # Truncate the log file
        subprocess.run(['truncate', '-s', '0', log_path], check=True)
        print(f"Cleared logs for container {container_id} at {log_path}")

    except subprocess.CalledProcessError as e:
        print("Error while trying to clear logs:", e)
