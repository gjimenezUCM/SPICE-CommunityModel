# Demos

It contains data and scripts to run demos for each case study.

## Quick start

1. Run `sh init.sh <museumName>` to configure and launch a Community Model server for a museum (available demos are GAM, HECHT and DMH).
2. Run `python postUser.py <museumName>` to load user data to the Community Model server.
3. Run `python postContribution.py <museumName>` to load user contributions to the Community Model server.
4. Run `python postPerspective.py <museumName>` to load  a default perspective to the Community Model server.

## Developing

### Structure

- `init.sh`: Shell script to configure and launch a community model
- `data`: contains sample data for each case study. Additionally, there is a `<museum>_template.env` that can
be used to deploy the Community model
- `config.py`: Dictionaries employed to send POST requests. They are configured according to the template.env
described above.
- `postUser.py`, `postPerspective.py` and `postContribution.py` are scripts to launch POST requests in order to
inject data to the Community model simulating the work of the User Model.

## License

The content of this repository is distributed under [Apache 2.0 License](LICENSE).
