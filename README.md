# clenv - Clearml environment profile manager



## Pre-requisites

- `clearml` installed, please refer to [ClearML installation guide](https://clear.ml/docs/latest/docs/getting_started/ds/ds_first_steps) for more details.
- Run `clearml-init` and initialize your first ever config file.



## Installation

```bash
pip install clenv
```



## Usage

### Subcommand `config`
Note: All config files must be in the format of `clearml-<profile_name>.conf`

#### List all config profiles
```bash
clenv config list
```

#### Create a new config profile
```bash
clenv config create <profile_name>
```

#### Delete a config profile
```bash
clenv config del <profile_name>
```

#### Switch to a config profile
```bash
clenv config checkout <profile_name>
```

#### Reinitialize the `api` section of a config
```bash
clenv config reinit <profile_name>
# Please paste your multi-line configuration and press Enter:
```
Then paste your multi-line configuration generated through clearML server.

### Subcommand `user`

#### Generate user/password hocon config
```bash
clenv user genpass <user_name>
```



## Examples

### Create a new clearml config profile for privately hosted clearml server 

#### Initialize profiles

```bash
$ ./clearenvoy.bin config list
# Input a name for your current profile
```

#### Create a new profile

```bash
$ ./clearenvoy.bin config create brainco
```

#### Reinit the profile credentials

```bash
$ ./clearenvoy.bin config reinit brainco
```

#### Checkout the new profile

```bash
$ ./clearenvoy.bin config checkout brainco
```

## Roadmap
- [x] Config profile management
- [x] BCrypt password generation
- [ ] Support custom config file path
- [ ] Server side utils and config management
- [ ] ClearML Agent side utils and config management

## Disclaimer & License
This project is not affiliated with Allegro AI, Inc. in any way. It is an independent and unofficial software. It's licensed under the MIT license.