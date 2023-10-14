import os
import click

def create_flask_app(app_name):
    app_folder = os.path.join('app', app_name)
    os.makedirs(app_folder, exist_ok=True)

    # Create __init__.py
    with open(os.path.join(app_folder, '__init__.py'), 'w') as f:
        pass

    # Create forms.py
    with open(os.path.join(app_folder, 'forms.py'), 'w') as f:
        pass

    # Create routes.py
    with open(os.path.join(app_folder, 'routes.py'), 'w') as f:
        pass

    # Create models.py
    with open(os.path.join(app_folder, 'models.py'), 'w') as f:
        pass

    # Create handlers.py
    with open(os.path.join(app_folder, 'handlers.py'), 'w') as f:
        pass

@click.command()
@click.argument('app_name')
def main(app_name):
    create_flask_app(app_name)
    print(f'Flask app "{app_name}" created successfully.')

if __name__ == '__main__':
    main()
