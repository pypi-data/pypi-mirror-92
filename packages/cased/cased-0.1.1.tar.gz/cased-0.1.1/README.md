`cased`: Cased Guard on the Command Line
==========================================

**Guard your team's critical command line infrastructure with Cased Guard**

Overview
-----------

`cased` is the command-line tool for configuring and running [Cased Guard](https://cased.com/guard).
It works via simple _shims_ that wrap your other command-line programs.
It handles the hard parts of configuring these shims, and keeps itself up-to-date
with changes and additions to your remote Cased Guard configuration.


Requirements & Setup
-----------------------

The only requirement to run `cased` is Python 3.5 or better. Additionally, if you
use our automated `install.sh` script, you will need `git`.

First, install `cased` itself. We provide a script for this—
it takes care of adding `cased` to your `PATH` so it can be easily invoked. Run
it directly:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/cased/guard-install/main/install.sh)"
```

Or clone this repo and run:

```
./install
```

Now _initialize_ the tool. You need to make sure `cased-init` (a single-purpose `init` script)
runs every time a shell starts. To do that, just add this to your `~/.bashrc` or `~/.zshrc`:

```
eval "$(cased-init -)"
```

Next configure Cased Guard via your unique user token. This will also sync your local client
with your Cased Guard remote settings.

```
cased configure <your-user-token>
```

And lastly, start a new shell.

You can confirm the entire installation with:

```
cased verify
```

Usage
------

After you've installed `cased` and configured it, you're all set.
Just run your programs as usual, and any that have been configured by
your Cased Guard server will run under `cased`.

We recommend you periodically (and automatically)
run `cased sync` to keep your local guarded programs up-to-date
with your remote configuration. After you run `cased sync`, you
must start a new shell.

The Cased Guard remote server defaults to `api.cased.com`. To change that
url, just set with:

```
cased url <your-remote-server>
```

You can also reset the URL to use the default:

```
cased url --reset
```


Internal commands
------------------

Although not needed for regular use, `cased` does expose some low-level plumbing commands:


**List available local shims**

To see all currently installed shims:

```
cased local-shims
```

**List available remote shims**

To see all remote  shims:

```
cased remote-shims
```

Uninstalling
---------------------

Since the Cased Guard client is so lightweight, you can simply remove the ` eval "$(cased-init -)"` from your shell startup script, and open a new shell. Programs will no longer be guarded.

To _completely_ remove a Cased Guard install, you can `rm` the `~/.cguard/` directory, where the client stores data, although this isn't strictly necessary. You can also remove the `cased` and `cased-init` programs, which are likely in `/usr/local/bin/` or a similar location (try `which cased` and `which cased-init` to find their location.)
