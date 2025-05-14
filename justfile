# Run program
run:
    uv run python main.py -e

# Sync uv
[macos]
sync:
    uv sync --no-group prod
[linux]
sync:
    uv sync --no-dev --group prod

# Deploy
deploy: && sync
    git pull
