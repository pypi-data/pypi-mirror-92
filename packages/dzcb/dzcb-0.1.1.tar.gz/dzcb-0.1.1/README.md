# dzcb

**D**MR **Z**one **C**hannel **B**uilder

## See [Releases](https://github.com/masenf/dzcb/releases) for Default Codeplugs

## Github Actions

This repository uses a Github Actions workflow to build
[codeplugs](./codeplug) automatically in the cloud.

### Customizing Your Own Codeplug

See **[codeplug-example](./codeplug-example/kf7hvm)**

* Fork this repo
* Copy `codeplug-example/kf7hvm` to `codeplug/your-call`
* customize generate.sh and other files
  * `kf7hvm-md-uv380.json`: set your Radio ID and Radio Name
    * Copy templates from [default-tyt-md380](./codeplug/default-tyt-md380) for
      monoband variants.
  * `order.json`: preferred zone order, zone exclusion, preferred talkgroup order
  * `scanlists.json`: additional scanlists
* if using repeaterbook, set secrets in repo settings:
  * REPEATERBOOK_USER
  * REPEATERBOOK_PASSWD
  * `prox.csv`: customize zones
* Github [`default-codeplugs`](.github/workflows/default-codeplugs.yml) workflow
  will automatically build all codeplugs in the [`codeplug`](./codeplug) directory.
* When a Release is published, the generated codeplugs will be hosted publicly 
  with a stable URL.

# Output Formats

## Farnsworth JSON

For import into [editcp](https://www.farnsworth.org/dale/codeplug/editcp/),
with theoretical support for:

* TYT
  * MD-380, MD-390
  * MD-UV380 (tested), MD-UV390
  * MD-2017, 
* Alinco DJ-MD40, 
* Retevis RT3, RT3-G, RT3S, and RT82 radios

Use `--farnsworth-template-json` to specify an exported codeplug to
use as the template for settings and radio capabilities.

`dzcb` includes basic template files for [MD380/390](./codeplug/default-tyt-md380)
and [MD-UV380/390](./src/dzcb/data/farnsworth).

## GB3GF OpenGD77 CSV

For import into [GB3GF CSV tool](http://www.gb3gf.co.uk/downloads.html).
Currently only supporting OpenGD77 target. Tool is "windows-only" but
runs decently under wine.

A subdirectory `gb3gf_opengd77` is created under the output directory
containing the 4 CSV files used by the program:

  * `Channels.csv`
  * `Contacts.csv`
  * `TG_Lists.csv`
  * `Zones.csv`
  
Note: these files are actually semicolon separated.

# Input Format

## K7ABD style

A directory of inter-related CSV files describing the common settings
needed to program all radios. This is a common format used by K7ABD's
original [anytone-config-builder](https://www.k7abd.net/anytone-config-builder/)
and N7EKB's [cps-import-builder](https://github.com/n7ekb/cps-import-builder).

An arbitrary number of files and folders will be combined. At this time duplicate
zone names in different files may be problematic. Keep zone names unique.
Particularly be wary of trucated names.

* `Analog__ZoneName.csv`
  * Zone, Channel Name, Bandwidth, Power, RX Freq, TX Freq, CTCSS Decode, CTCSS Encode, TX Prohibit
* `Talkgroups__ZoneName.csv`
  * **No Header Row** tuples of: talkgroup_name,talkgroup_number
* `Digital-Other__ZoneName.csv` -- only really useful for digital simplex channels or private call
  * Zone, Channel Name, Power, RX Freq, TX Freq, Color Code, Talk Group, TimeSlot, Call Type, TX Permit
* `Digital-Repeaters__ZoneName.csv` -- each line is a digital channel with static talkgroup timeslot assignments
  * Zone Name, Comment, Power, RX Freq, TX Freq, Color Code, talkgroup1, talkgroup2, talkgroup3, ...
  * Typically the Zone Name field is semicolon separated: "Longer Name;LNM"
  * The value for the talkgroup column should be "-", "1", or "2"
  * The talkgroup names must exist in the talkgroups file.
  * Some codeplug targets will create a zone for each frequency with channels for each static talkgroup.
  
## Data Sources

### [PNWdigital.net](http://PNWDigital.net)

**Before using this network, please read the [quick start](http://www.pnwdigital.net/quick-start.html)**

When building a codeplug with the `--pnwdigital` switch, 
data is downloaded from [PNWDigital.net/files/acb](http://www.pnwdigital.net/files/acb/).
The files are updated regularly from the cBridge, so there
could be test data or repeaters that are not yet active.

The data is cached by [`dzcb.pnwdigital`](./src/dzcb/pnwdigital.py)

### [SeattleDMR](https://seattledmr.org/)

**Before using these repeaters, please read the website**

When building a codeplug with the `--seattledmr` switch,
data is downloaded from [seattledmr.org/ConfigBuilder/Digital-Repeaters-Seattle-addon.csv](https://seattledmr.org/ConfigBuilder/Digital-Repeaters-Seattle-addon.csv)
and cleaned up a bit in [`dzcb.seattledmr`](./src/dzcb/seattledmr.py)

### Repeaterbook Proximity

**Repeaterbook account is required to access this endpoint**

Download live analog repeaterbook data within distance of point of
interest.

`--repeaterbook-proximity-csv` references a csv file with the fields:

* Zone Name,Lat,Lon,Distance,Unit(m),Band(14 - 2m, 4 - 70cm)

This corresponds directly to the repeaterbook csv download "prox" http endpoint, which
requires authentication. See [`dzcb.repeaterbook`](./src/dzcb/repeaterbook.py).

When using this option, be sure to set REPEATERBOOK_USER and REPEATERBOOK_PASSWD
in the environment.

#### Example Format

```
Longview WA VHF 35mi,46.13819885,-122.93800354,35,m,14,
Longview WA UHF 35mi,46.13819885,-122.93800354,35,m,4,
```

(it's easy to search on repeaterbook and copy the info from the URL!)

### [Local](./src/dzcb/data/k7abd/Digital-Repeaters__Local.csv)

Information on these Western Washington standalone DMR repeaters was
retrieved from Repeaterbook and respective websites in 2020 October.

### Simplex, GMRS, etc

Some common [Digital](./src/dzcb/data/k7abd/Digital-Others__Simplex.csv)
and [Analog](./src/dzcb/data/k7abd/Analog__Simplex.csv) simplex frequencies,
and [GMRS/FRS and MURS channels](./src/dzcb/data/k7abd/Analog__Unlicensed.csv) are
included if `--default-k7abd` is specified.

# Bonus: Trim the Contact List

Download the usersDB.bin with Farnsworth editcp.

    python -m dzcb.contact_trim \
        < "~/.cache/codeplug/Codeplug Editor/usersDB.bin" \
        > "~/.cache/codeplug/Codeplug Editor/usersDB-trimmed.bin"
        
# Development Usage

## Installation

pip install -e ./dzcb

## Basic Usage

Download live pnwdigital and seattledmr networks and generate a codeplug
in `/tmp/my-codeplug` with local simplex zones included.

```
python -m dzcb \
    --pnwdigital \
    --seattledmr \
    --default-k7abd /tmp/my-codeplug
```

See above and `--help` for more usage details.
