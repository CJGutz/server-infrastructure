# Server Infrastructure

**Setup for services on personal server**

Services currently running:
- Website at [gutzkow.com](https://www.gutzkow.com). Image from [unchained](https://github.com/CJGutz/unchained)
- Vaultwarden passwordmanager
- Backups of vaultwarden to google drive
- Nginx and certbot for reverse proxy and letsencrypt certificates

## Installation and Setup

```sh
git clone git@github.com:CJGutz/server-infrastructure.git
cd server-infrastructure
```

_Create environment variables. Replace the ones found in the example environment file._
```sh
cp .env.example .env
```

_To enable the admin panel for vaultwarden, you need to generate an admin token and add the token to the ADMIN_TOKEN environment variable. To generate from a password, run:_
```sh
docker exec -it vaultwarden /vaultwarden hash --preset owaspdocker \
exec -it vaultwarden /vaultwarden hash --preset owasp
```
_This assumes the container running vaultwarden is named `vaultwarden` as the `docker-compose.yml` file defines._

**To start services, run:**
```sh
sh setup.sh
```
