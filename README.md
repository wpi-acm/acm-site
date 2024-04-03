# acm-site

Rewrite of the WPI ACM website in Flask

## Development Environment

We provide a Makefile to manage development and production environments. To set
up a new virtual environment, use `make init_env`. Any time project requirements
change, use `make upgrade_env`. When deploying to production, `make
post_upgrade` will be your friend, as it will automatically set up requisite
folders, an environment, and run migrations for you.
